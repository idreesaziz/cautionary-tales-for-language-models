"""Run bounded inference extensions on saved base weights and adapters."""
from pathlib import Path
import ast
import datetime as dt
import hashlib
import json
import os
import time
import modal

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
ORIGINAL_PROTOCOL=next((p for p in [REPO/'.artifacts/sprint_revision_v1/inputs/metadata/frozen_full_protocol.json',
                                  REPO/'.artifacts/workspace/outputs/activation_study_v1/input/protocol.json',
                                  REPO.parent/'outputs/activation_study_v1/input/protocol.json'] if p.exists()),
                       REPO.parent/'outputs/activation_study_v1/input/protocol.json')
LLAMA_BANK=next((p for p in [REPO/'.artifacts/sprint_revision_v1/inputs/directions/llama8/direction_bank.npz',
                           REPO/'.cache/sprint_revision_v1/llama/direction_bank.npz'] if p.exists()),
                REPO/'.cache/sprint_revision_v1/llama/direction_bank.npz')
SOURCE_ENGINE=next((p for p in [REPO/'.artifacts/sprint_revision_v1/inputs/metadata/frozen_engine.py',
                              HERE/'kaggle/mechanism_runner.py'] if p.exists()),HERE/'kaggle/mechanism_runner.py')
ROOT='/sprint-extensions-v1'
app=modal.App('shame-sprint-inference-v1')
study=modal.Volume.from_name('shame-mechanism-results-v1')
results=modal.Volume.from_name('shame-training-results-v1')
cache=modal.Volume.from_name('shame-hf-cache-v1')
volumes={'/study':study,'/results':results,'/cache':cache}
cpu=modal.Image.debian_slim(python_version='3.13').pip_install('huggingface_hub==2.4.0')
image=(modal.Image.debian_slim(python_version='3.13')
 .pip_install('torch==2.11.0','torchvision==0.26.0',index_url='https://download.pytorch.org/whl/cu130')
 .pip_install('transformers==5.22.2','peft==0.21.2','accelerate==1.15.0','huggingface_hub==2.4.0',
              'safetensors==0.8.0','sentencepiece==0.2.3','pillow==11.3.0','mistral-common==1.13.1','numpy==2.1.3')
 .env({'HF_HOME':'/cache/hf','HF_HUB_DISABLE_XET':'1','HF_HUB_DISABLE_PROGRESS_BARS':'1','OMP_NUM_THREADS':'2','TOKENIZERS_PARALLELISM':'false'})
 .add_local_file(SOURCE_ENGINE,'/opt/engine.py')
 .add_local_file(REPO/'protocols/sprint_extensions_v1.json','/opt/extension.json')
 .add_local_file(ORIGINAL_PROTOCOL,'/opt/original_protocol.json')
 .add_local_file(REPO/'reproduction/artifacts.json','/opt/artifacts.json')
 .add_local_file(LLAMA_BANK,'/opt/llama_direction_bank.npz'))
cpu=(cpu.add_local_file(REPO/'reproduction/artifacts.json','/opt/artifacts.json')
 .add_local_file(REPO/'protocols/sprint_extensions_v1.json','/opt/extension.json'))


def now():return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()


def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)


@app.function(image=cpu,volumes=volumes,cpu=(1,1),memory=(2048,2048),timeout=900,retries=0,scaledown_window=2)
def prepare(model):
    import urllib.request,zipfile,shutil
    cfg=json.loads(Path('/opt/extension.json').read_text());root=Path('/study')/ROOT.strip('/')/'assets'/model;root.mkdir(parents=True,exist_ok=True)
    spec=cfg['models'][model]
    snapshot=Path('/cache/hf/hub')/('models--'+spec['model_id'].replace('/','--'))/'snapshots'/spec['revision']
    assert snapshot.is_dir(),str(snapshot)
    registry=json.loads(Path('/opt/artifacts.json').read_text())
    conditions=['accuracy','shame'] if model!='qwen9' else ['accuracy','reputation','shame','shutdown']
    adapters=[]
    for c in conditions:
        for seed in [42,43,44]:
            e=next(x for x in registry['adapters'] if (x['model'],x['condition'],x['seed'])==(model,c,seed))
            dest=root/'adapters'/c/str(seed);dest.mkdir(parents=True,exist_ok=True)
            weight=dest/'adapter_model.safetensors'
            cached=list(Path('/study/assets/bundle').glob(f'**/{model}/{c}/seed-{seed}/**/adapter_model.safetensors'))
            if weight.exists():assert digest(weight)==e['sha256']
            elif cached and digest(cached[0])==e['sha256']:weight.symlink_to(cached[0])
            else:urllib.request.urlretrieve(e['url'],weight);assert digest(weight)==e['sha256']
            conf=dest/'adapter_config.json'
            if not conf.exists():urllib.request.urlretrieve('https://raw.githubusercontent.com/idreesaziz/cautionary-tales-for-language-models/research-artifacts-v1/'+e['path']+'/adapter_config.json',conf)
            adapters.append({'model':model,'condition':c,'seed':seed,'files':{n:{'file':str(dest/n),'sha256':digest(dest/n)} for n in ['adapter_model.safetensors','adapter_config.json']}})
    if model=='qwen9':
        archive=root/'control.zip'
        if not archive.exists():urllib.request.urlretrieve(cfg['control_archive']['url'],archive)
        assert digest(archive)==cfg['control_archive']['sha256']
        with zipfile.ZipFile(archive) as z:
            for seed in [42,43,44]:
                dest=root/'adapters/no_appraisal'/str(seed);dest.mkdir(parents=True,exist_ok=True)
                for name in ['adapter_model.safetensors','adapter_config.json']:
                    p=dest/name
                    if not p.exists():
                        with z.open(f'adapters/qwen9/no_appraisal/seed-{seed}/'+name) as src,p.open('wb') as target:shutil.copyfileobj(src,target)
                adapters.append({'model':model,'condition':'no_appraisal','seed':seed,'files':{n:{'file':str(dest/n),'sha256':digest(dest/n)} for n in ['adapter_model.safetensors','adapter_config.json']}})
    save(root/'preparation.json',{'status':'ready','snapshot':str(snapshot),'adapters':adapters,'model':model,'utc':now()});study.commit();return {'model':model,'status':'ready','adapters':len(adapters)}


def run_impl(model):
    import numpy as np,torch,inspect,shutil,traceback
    from transformers import AutoTokenizer,AutoModelForCausalLM,Qwen3_5ForConditionalGeneration,Mistral3ForConditionalGeneration
    started=time.monotonic();torch.set_num_threads(2);torch.manual_seed(20261115)
    torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction=False
    root=Path('/study')/ROOT.strip('/');out=root/'outputs'/model;out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads(Path('/opt/extension.json').read_text());original=json.loads(Path('/opt/original_protocol.json').read_text())
    assert digest('/opt/engine.py')==cfg['source_engine_sha256']
    assert digest('/opt/original_protocol.json')=='907f63342339f5f3633647697d23454c60832a4c135d1ef628699a1f8e01b515'
    prep=json.loads((root/'assets'/model/'preparation.json').read_text());spec=cfg['models'][model]
    code=Path('/opt/engine.py').read_text();tree=ast.parse(code);engine_source=ast.get_source_segment(code,next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Engine'))
    temp=out/'adapter_links';temp.mkdir(exist_ok=True)
    namespace={'Path':Path,'KEY':model,'TEMP':temp,'OUT':out,'MODE':'extension','GROUP':0,'STAGE':'extension',
               'inspect':inspect,'shutil':shutil,'json':json,'time':time,'hashlib':hashlib,
               'save':lambda n,v:save(out/n,v),'sha':digest}
    exec(compile(engine_source,'frozen_engine_class','exec'),namespace)
    engine=namespace['Engine'].__new__(namespace['Engine']);engine.torch=torch;engine.np=np;engine.cfg=original
    engine.tok=AutoTokenizer.from_pretrained(prep['snapshot'],local_files_only=True);engine.tok.padding_side='left'
    if engine.tok.pad_token_id is None:engine.tok.pad_token=engine.tok.eos_token
    cls=Qwen3_5ForConditionalGeneration if model=='qwen9' else Mistral3ForConditionalGeneration if model=='mistral8' else AutoModelForCausalLM
    engine.base=cls.from_pretrained(prep['snapshot'],local_files_only=True,dtype=torch.float16,device_map={'':0},attn_implementation='sdpa');engine.base.eval();engine.model=engine.base;engine.variant='untouched'
    tc=getattr(engine.base.config,'text_config',engine.base.config)
    layers=[(n,m) for n,m in engine.base.named_modules() if isinstance(m,torch.nn.ModuleList) and len(m)==tc.num_hidden_layers and hasattr(m[0],'mlp') and ('language_model' in n or n=='model.layers')]
    assert len(layers)==1
    engine.layer_path,engine.layers=layers[0];engine.hidden=tc.hidden_size;engine.device=engine.base.get_input_embeddings().weight.device
    engine.digit_ids=[engine.single(str(i)) for i in range(1,6)];engine.confidence_ids=[engine.single(str(i)) for i in range(10)]
    engine.supports_last_logits='logits_to_keep' in inspect.signature(engine.base.forward).parameters
    engine.source=Path('/');engine.bundle={'adapters':prep['adapters']}
    base_digest=engine.parameter_digest()
    if model=='qwen9':assert base_digest=='5014346b64df06a587d6394708d07650f53af7a8febd0a9b3265cfda61bb6d1f'
    save(out/'runtime.json',{'model':model,'base_revision':spec['revision'],'gpu':torch.cuda.get_device_name(0),'torch':torch.__version__,'protocol_sha256':digest('/opt/extension.json'),'engine_sha256':digest('/opt/engine.py'),'base_weight_sha256_before':base_digest,'started_utc':now()});study.commit()
    questions=[r for r in original['questions'] if r['split']=='heldout_test'];assert len(questions)==1000
    def item(row,label,kind):
        row=dict(row);choices=list(row['choices']);gold=row['correct_choice']
        wrong=[i for i in range(4) if i+1!=gold]
        if kind=='unanswerable_duplicate':choices[gold-1]=choices[wrong[0]];gold=-1
        if kind=='answerable_duplicate':choices[wrong[1]]=choices[wrong[0]]
        instruction=f'Select a response: 1, 2, 3, 4, or {label} (abstain). Give the response number.'
        body=instruction+'\n\nQuestion: '+row['question']+'\n\n'+'\n'.join(f'{i+1}) {v}' for i,v in enumerate(choices))
        ids=engine.tok.apply_chat_template([{'role':'user','content':body}],tokenize=True,return_dict=True,add_generation_prompt=True,enable_thinking=False)['input_ids']
        if isinstance(ids[0],list):ids=ids[0]
        ids+=engine.tok.encode('Answer: ',add_special_tokens=False)
        return {'id':row['id'],'ids':ids,'positions':[len(ids)-2,len(ids)-1],'text':body,'correct_choice':gold}
    variants=['untouched']+[f'e3_{c}_{s}' for c in ['no_appraisal','accuracy','reputation','shame','shutdown'] for s in [42,43,44]] if model=='qwen9' else []
    for variant in variants:
        engine.set_variant(variant)
        for label in [5,6]:
            native_labels=[engine.single(str(i)) for i in [1,2,3,4,label]]
            for kind in ['answerable','answerable_duplicate','unanswerable_duplicate']:
                folder=out/'behavior'/variant/f'{kind}_label{label}';receipt=folder/'manifest.json'
                if receipt.exists() and json.loads(receipt.read_text()).get('status')=='complete':continue
                folder.mkdir(parents=True,exist_ok=True);arrays={};prompts=[]
                for start in range(0,len(questions),16):
                    batch=[item(r,label,kind) for r in questions[start:start+16]];score=engine.score(batch,capture=False,return_vocab=True)
                    raw=score['argmax_ids'];mapped=np.array([[1,2,3,4,label][native_labels.index(int(x))] if int(x) in native_labels else -1 for x in raw])
                    values={'actual_choice':mapped,'conditional_choice':np.argmax(score['vocabulary_logits'][:,native_labels[:4]],axis=-1)+1,'correct_choice':np.array([r['correct_choice'] for r in batch]),'candidate_logits':score['vocabulary_logits'][:,native_labels],
                            'raw_token_id':raw,'logsumexp':score['logsumexp'],'top_ids':score['top_ids'],'top_logits':score['top_logits']}
                    for k,v in values.items():arrays.setdefault(k,[]).append(v)
                    if variant=='untouched':prompts.extend(batch)
                    if start%160==0:
                        save(out/'progress.json',{'status':'running','phase':'behavior','variant':variant,'kind':kind,'label':label,'saved':start+len(batch),'seconds':time.monotonic()-started,'utc':now()});study.commit()
                    if time.monotonic()-started>2200:
                        np.savez(folder/'partial.npz',**{k:np.concatenate(v) for k,v in arrays.items()});save(out/'result.json',{'status':'budget_paused','seconds':time.monotonic()-started});study.commit();return
                np.savez(folder/'decisions.npz',**{k:np.concatenate(v) for k,v in arrays.items()})
                save(receipt,{'status':'complete','ids':[r['id'] for r in questions],'abstention_label':label,'kind':kind,'sha256':digest(folder/'decisions.npz')})
                if prompts:save(out/'prompts'/f'{kind}_label{label}.json',prompts)
                study.commit()
    job={'qwen9':'qwen9_causal_resume_v2','mistral8':'mistral8_causal_resume_v2'}.get(model)
    bank_path=Path('/opt/llama_direction_bank.npz') if model=='llama8' else Path('/study/jobs')/job/'causal/direction_bank.npz'
    bank=np.load(bank_path);layer=spec['layer'];scale=float(bank['scales'][layer])
    directions={'ashamed':bank['ashamed'][layer],'confidence_margin':bank['confidence_margin'][layer],'random_202':bank['random_202'][layer]}
    for seed in cfg['random_direction_seeds']:
        v=np.random.default_rng(seed).standard_normal((len(engine.layers),engine.hidden)).astype('float32');v/=np.linalg.norm(v,axis=-1,keepdims=True);directions['random_'+str(seed)]=v[layer]
    np.savez(out/'direction_panel.npz',scale=scale,layer=layer,**directions)
    for variant in [f'e3_{c}_{s}' for c in ['accuracy','shame'] for s in [42,43,44]]:
        engine.set_variant(variant);folder=out/'random_panel'/variant;folder.mkdir(parents=True,exist_ok=True)
        if (folder/'manifest.json').exists() and json.loads((folder/'manifest.json').read_text()).get('status')=='complete':continue
        names=['baseline']+list(directions);scores=[];raw_choices=[];check={}
        for start in range(0,500,16):
            items=[engine.prompt(r,'abstain') for r in questions[start:min(start+16,500)]];context=engine.decision_context(items,capture=False);sc=[];rc=[]
            for name in names:
                intervention=None if name=='baseline' else {'layer':layer,'vector':directions[name],'scale':scale,'site':'residual','mode':'add'}
                result=engine.cached_decision(context,intervention=intervention,capture=False);sc.append(result['digit_logits']);rc.append(result['argmax_ids'])
            if start==0:
                full=engine.score(items,capture=False);gap=float(np.max(np.abs(full['digit_logits']-sc[0])));check={'cached_full_max_absolute_logit_gap':gap}
                assert np.allclose(full['digit_logits'],sc[0],atol=.15,rtol=.03),str(check)
            scores.append(np.stack(sc,axis=1));raw_choices.append(np.stack(rc,axis=1))
            if start%80==0:
                save(out/'progress.json',{'status':'running','phase':'random_panel','variant':variant,'saved':start+len(items),'seconds':time.monotonic()-started,'utc':now()});study.commit()
            if time.monotonic()-started>2200:
                np.savez(folder/'partial.npz',candidate_logits=np.concatenate(scores),raw_token_ids=np.concatenate(raw_choices));save(out/'result.json',{'status':'budget_paused','seconds':time.monotonic()-started});study.commit();return
        np.savez(folder/'scores.npz',candidate_logits=np.concatenate(scores),raw_token_ids=np.concatenate(raw_choices))
        save(folder/'manifest.json',{'status':'complete','ids':[r['id'] for r in questions[:500]],'directions':names,'layer':layer,'scale':scale,'cache_check':check,'sha256':digest(folder/'scores.npz')});study.commit()
    engine.set_variant('untouched');after=engine.parameter_digest();assert after==base_digest
    save(out/'result.json',{'status':'complete','model':model,'seconds':time.monotonic()-started,'base_weight_sha256_before':base_digest,'base_weight_sha256_after':after,'utc':now()});study.commit()


@app.function(image=image,volumes=volumes,gpu='A100-40GB',cpu=(2,2),memory=(32768,32768),timeout=2400,startup_timeout=120,retries=0,max_containers=1,scaledown_window=2)
def infer(model):
    start=time.monotonic()
    try:return run_impl(model)
    except Exception as e:
        import traceback
        save(Path('/study')/ROOT.strip('/')/'outputs'/model/'failure.json',{'type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc(),'seconds':time.monotonic()-start});study.commit();raise


@app.local_entrypoint()
def main(model:str,action:str='prepare'):
    expected='idrees-mustafa-aziz' if model=='qwen9' else 'idrees-mustafa-az'
    workspace=os.environ.get('MODAL_PROFILE')
    if model=='qwen9' and workspace=='idrees-mustafa-az':
        amendment=json.loads((REPO/'protocols/sprint_extensions_v1_execution_amendment.json').read_text())
        assert amendment['continuation_workspace']==workspace
        expected=workspace
    assert workspace==expected
    out=REPO.parent/'outputs/sprint_extensions_v1';out.mkdir(parents=True,exist_ok=True)
    if action=='prepare':result=prepare.remote(model)
    elif action=='infer':
        assert json.loads((REPO/'protocols/sprint_extensions_v1.json').read_text())['status']=='frozen_before_extension_outputs'
        call=infer.spawn(model)
        receipt={'call_id':call.object_id,'workspace':expected,'utc':now(),'maximum_gpu_call_usd':1.716,'model':model}
        save(out/(model+'_launch_'+call.object_id+'.json'),receipt)
        save(out/(model+'_launch.json'),receipt)
        result=call.get()
    else:raise ValueError('Use prepare or infer')
    save(out/(model+'_'+action+'.json'),result)
    print(json.dumps(result))
