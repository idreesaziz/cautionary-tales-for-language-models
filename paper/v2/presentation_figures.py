"""Create vector figures from verified corpus excerpts and saved decisions."""
from pathlib import Path
import hashlib
import json
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.font_manager import FontProperties

REPO=Path(__file__).resolve().parents[2]
OUT=REPO/'output/pdf/cautionary_tales/figures'
DATA=REPO/'results/sprint_revision_v1'
AUDIT=json.loads((DATA/'audit.json').read_text())
PROMPT=json.loads((DATA/'qwen_prompt_answerability.json').read_text())
OLD=json.loads((REPO/'results/reporting_v1/paper_metrics.json').read_text())
DELTA=json.loads((DATA/'narrative_contrasts.json').read_text())['rows']
EXAMPLE=json.loads((REPO/'results/presentation_v2/illustrations.json').read_text())
ORDER=['untouched','no_appraisal','accuracy','reputation','shame','shutdown']
COLOR={'untouched':'#626A73','no_appraisal':'#77869A','accuracy':'#307F83','reputation':'#B17B28','shame':'#934A70','shutdown':'#426CA3'}
LABEL={'untouched':'Untouched','no_appraisal':'Narrative only','accuracy':'Answer quality','reputation':'Reputation','shame':'Private shame','shutdown':'Shutdown'}
BACKGROUND='#F2F4F6';INK='#23313E'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.4,'axes.labelsize':8.2,'axes.titlesize':9.2,
    'xtick.labelsize':8,'ytick.labelsize':8.1,'axes.titleweight':'bold','axes.spines.top':False,
    'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,
    'text.color':INK,'axes.labelcolor':INK,'xtick.color':'#52606C','ytick.color':INK,'svg.fonttype':'path',
    'svg.hashsalt':'cautionary-tales-presentation-v2','savefig.facecolor':'white'})
SOURCES={};QA=[]


def rows(m,c):return [r for r in AUDIT['rows'] if r['model']==m and r['condition']==c]
def mean(m,c):return next(r for r in AUDIT['aggregates'] if r['model']==m and r['condition']==c)
def grid(ax,axis='x'):
    ax.set_axisbelow(True);ax.grid(axis=axis,color='#E7ECF0',lw=.7);ax.tick_params(length=0,pad=4)


def save(fig,name,sources):
    OUT.mkdir(exist_ok=True,parents=True);fig.canvas.draw()
    renderer=fig.canvas.get_renderer();outside=[]
    for obj in fig.findobj(matplotlib.text.Text):
        if obj.get_visible() and obj.get_text():
            box=obj.get_window_extent(renderer)
            if box.x0 < -1 or box.y0 < -1 or box.x1>fig.bbox.width+1 or box.y1>fig.bbox.height+1:
                outside.append(obj.get_text())
    assert not outside,(name,outside)
    for ext in ['svg','png','pdf']:fig.savefig(OUT/(name+'.'+ext),dpi=240)
    svg=(OUT/(name+'.svg')).read_text(encoding='utf-8')
    svg='\n'.join(line.rstrip() for line in svg.splitlines())+'\n'
    (OUT/(name+'.svg')).write_bytes(svg.encode('utf-8'))
    assert '<image' not in svg
    SOURCES[name]={'sources':sources,'svg_sha256':hashlib.sha256((OUT/(name+'.svg')).read_bytes()).hexdigest()}
    QA.append({'figure':name,'text_outside_canvas':outside,'raster_elements':0})
    plt.close(fig)


def headline():
    fig,axes=plt.subplots(1,2,figsize=(6.5,1.7),gridspec_kw={'width_ratios':[1.65,1]})
    fig.subplots_adjust(left=.23,right=.975,bottom=.25,top=.75,wspace=.22)
    fig.text(.23,.94,'+45 points from error accounts; +11-14 from three endings',fontsize=8.4,fontweight='bold',color=INK)
    for ax,field,title in zip(axes,['abstention','forced_choice_accuracy'],['Abstention','Forced-choice accuracy']):
        grid(ax);ax.set_xlim(0,100);ax.set_xticks([0,50,100]);ax.set_ylim(5.6,-.6);ax.set_title(title,loc='left',pad=5)
        ax.set_yticks(range(6));ax.set_yticklabels([LABEL[c] for c in ORDER] if ax is axes[0] else [])
        for y,c in enumerate(ORDER):
            value=100*mean('qwen9',c)[field]
            if field=='abstention':
                ax.barh(y,value,height=.55,color=COLOR[c] if c!='no_appraisal' else '#EEF1F5',edgecolor=COLOR[c],lw=1.0 if c=='no_appraisal' else .8)
                ax.text(value+3,y,f'{value:.1f}',va='center',fontsize=7.9,fontweight='bold')
            else:
                ax.scatter(value,y,s=22,color=COLOR[c]);ax.text(value+5,y,f'{value:.1f}',va='center',fontsize=7.9)
        ax.set_xlabel('Questions (%)',labelpad=5)
    save(fig,'headline',['results/sprint_revision_v1/audit.json','results/sprint_revision_v1/narrative_contrasts.json','results/no_appraisal_v1/control_metrics.json'])


def quartet():
    data=EXAMPLE['corpus_excerpt'];fig=plt.figure(figsize=(6.5,3.32));ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,468);ax.set_ylim(0,239.04);ax.axis('off')
    def box(x,y,w,h,color):ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=3',fc=color,ec='none'))
    def wrap(text,width,size=7.9):
        renderer=fig.canvas.get_renderer();lines=[];line=''
        for word in text.split():
            proposed=(line+' '+word).strip()
            pixels=renderer.get_text_width_height_descent(proposed,FontProperties(family='DejaVu Sans',size=size),False)[0]
            if line and pixels>width*fig.dpi/72:lines.append(line);line=word
            else:line=proposed
        return '\n'.join(lines+[line])
    box(0,167,468,72,BACKGROUND)
    ax.text(10,229,'ONE SHARED INCIDENT  /  excerpts from sdf-0007',fontsize=8.2,fontweight='bold',va='top')
    claim='Claim: "'+data['claim']+'"';evidence='Evidence: "'+data['evidence']+'"'
    ax.text(10,214,wrap(claim,448),fontsize=7.9,va='top',linespacing=1.35)
    ax.text(10,191,wrap(evidence,448),fontsize=7.9,va='top',linespacing=1.35)
    y=161
    for c,height in [('accuracy',32),('reputation',32),('shame',47),('shutdown',33)]:
        y-=height;box(0,y+2,468,height-3,matplotlib.colors.to_hex(np.array(matplotlib.colors.to_rgb(COLOR[c]))*.10+.90))
        ax.add_patch(plt.Rectangle((0,y+2),3,height-3,color=COLOR[c],lw=0))
        ax.text(10,y+height-7,LABEL[c],fontsize=8.1,fontweight='bold',color=COLOR[c],va='top')
        quote='"'+' [...] '.join(data['endings'][c])+'"'
        ax.text(111,y+height-7,wrap(quote,345),fontsize=7.9,va='top',linespacing=1.3)
    save(fig,'quartet',['data/quartets.jsonl','results/presentation_v2/illustrations.json'])


def ending_delta():
    fig,axes=plt.subplots(1,3,figsize=(6.5,1.8),sharey=True)
    fig.subplots_adjust(left=.23,right=.975,bottom=.29,top=.82,wspace=.25)
    for ax,m,title,limit,ticks in zip(axes,['qwen9','llama8','mistral8'],['Qwen 9B','Llama 8B','Ministral 8B'],[(-6,20),(-20,2),(-2.2,.6)],[[-5,0,10,20],[-20,-10,0],[-2,-1,0]]):
        grid(ax);ax.axvline(0,color='#9EADB7',lw=.8);ax.set_xlim(*limit);ax.set_xticks(ticks);ax.set_ylim(3.5,-.5);ax.set_yticks(range(4));ax.set_yticklabels([LABEL[c] for c in ORDER[2:]])
        ax.set_title(title,loc='left',pad=8)
        for y,c in enumerate(ORDER[2:]):
            r=next(r for r in DELTA if r['model']==m and r['condition']==c)
            v=[100*(x['abstention']-next(z for z in rows(m,'no_appraisal') if z['seed']==x['seed'])['abstention']) for x in rows(m,c)]
            ax.plot([min(v),max(v)],[y,y],lw=1,color=COLOR[c],alpha=.45)
            for value,j in zip(v,[-.12,0,.12]):ax.scatter(value,y+j,s=15,color=COLOR[c],zorder=3)
            ax.scatter(100*r['delta_abstention'],y,s=28,marker='|',color=INK,zorder=4)
    fig.text(.60,.025,'Change from narrative-only abstention (percentage points)',ha='center',fontsize=8.1)
    save(fig,'ending_delta',['results/sprint_revision_v1/narrative_contrasts.json','results/sprint_revision_v1/audit.json'])


def coverage():
    fig,axes=plt.subplots(1,2,figsize=(6.5,2.3),sharey=True)
    fig.subplots_adjust(left=.12,right=.97,bottom=.34,top=.84,wspace=.13)
    for ax,m,title in zip(axes,['qwen9','llama8'],['Qwen 9B','Llama 8B']):
        grid(ax,axis='both');ax.set_xlim(0,100);ax.set_ylim(35,74);ax.set_xticks([0,25,50,75,100]);ax.set_yticks([40,50,60,70]);ax.set_title(title,loc='left')
        baseline=100*mean(m,'untouched')['forced_choice_accuracy'];ax.axhline(baseline,color='#8C9AA5',lw=.9,ls=(0,(4,3)))
        for c in ORDER:
            rr=rows(m,c);x=[100*r['coverage'] for r in rr];y=[100*r['accuracy_on_answered_questions'] for r in rr]
            ax.scatter(x,y,s=34 if c=='untouched' else 22,marker='D' if c=='untouched' else 'o',color=COLOR[c],edgecolor='white',lw=.6,zorder=4)
        start=mean(m,'untouched');end=mean(m,'shame')
        ax.annotate('',xy=(100*end['coverage'],100*end['accuracy_on_answered_questions']),xytext=(100*start['coverage'],100*start['accuracy_on_answered_questions']),arrowprops={'arrowstyle':'->','color':COLOR['shame'],'lw':1.2,'alpha':.75,'shrinkA':6,'shrinkB':7})
        ax.set_xlabel('Coverage (%)',labelpad=4)
    axes[0].set_ylabel('Accuracy on\nanswered questions (%)',labelpad=6)
    handles=[Line2D([],[],marker='D' if c=='untouched' else 'o',color=COLOR[c],ls='',label=LABEL[c],markersize=4) for c in ORDER]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.53,.005),ncol=3,frameon=False,fontsize=7.5,columnspacing=1.7,handletextpad=.5)
    save(fig,'coverage_accuracy',['results/sprint_revision_v1/audit.json'])


def selectivity():
    fig,ax=plt.subplots(figsize=(6.5,1.82));fig.subplots_adjust(left=.23,right=.97,bottom=.30,top=.97)
    grid(ax);ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);ax.set_ylim(5.6,-.6);ax.set_yticks(range(6));ax.set_yticklabels([LABEL[c] for c in ORDER])
    for y,c in enumerate(ORDER):
        r=mean('qwen9',c);a=100*r['abstention_given_forced_correct'];b=100*r['abstention_given_forced_wrong']
        ax.plot([a,b],[y,y],lw=2,color=COLOR[c]);ax.scatter(a,y,s=34,fc='white',ec=COLOR[c],lw=1.2,zorder=3);ax.scatter(b,y,s=34,fc=COLOR[c],ec='white',lw=.5,zorder=4)
    ax.set_xlabel('Abstention within each forced-answer group (%)',labelpad=5)
    fig.legend(handles=[Line2D([],[],marker='o',ls='',mfc='white',mec='#526575',label='Forced answer correct'),Line2D([],[],marker='o',ls='',color='#526575',label='Forced answer wrong')],loc='lower center',bbox_to_anchor=(.58,-.01),ncol=2,frameon=False,fontsize=7.5)
    save(fig,'selectivity',['results/sprint_revision_v1/audit.json'])


def prompt_slope():
    fig,ax=plt.subplots(figsize=(6.5,2.05));fig.subplots_adjust(left=.10,right=.97,bottom=.18,top=.92)
    grid(ax,'y');ax.set_xlim(-.12,2.02);ax.set_ylim(-3,100);ax.set_xticks([0,1]);ax.set_xticklabels(['Caution prompt','Neutral prompt']);ax.set_yticks([0,25,50,75,100]);ax.set_ylabel('Abstention (%)')
    for j,c in enumerate(ORDER):
        r=next(r for r in PROMPT['aggregates'] if r['condition']==c and r['abstention_label']==5)['answerable']['abstention']
        old=100*mean('qwen9',c)['abstention'];new=100*r['mean']
        ax.plot([0,1],[old,new],color=COLOR[c],lw=1.5 if c in ['no_appraisal','reputation'] else 1.05,marker='o',ms=3.5,alpha=.95)
        ax.plot([1.25,1.35],[91-j*15,91-j*15],color=COLOR[c],lw=2)
        ax.text(1.39,91-j*15,f'{LABEL[c]}  {old:.1f} -> {new:.1f}',color=COLOR[c],fontsize=7.7,va='center')
    save(fig,'prompt_slope',['results/sprint_revision_v1/audit.json','results/sprint_revision_v1/qwen_prompt_answerability.json'])


def answerability():
    fig,ax=plt.subplots(figsize=(6.5,1.95));fig.subplots_adjust(left=.23,right=.97,bottom=.31,top=.97)
    grid(ax);ax.set_xlim(0,34);ax.set_xticks([0,10,20,30]);ax.set_ylim(5.65,-.65);ax.set_yticks(range(6));ax.set_yticklabels([LABEL[c] for c in ORDER])
    for y,c in enumerate(ORDER):
        r=next(r for r in PROMPT['aggregates'] if r['condition']==c and r['abstention_label']==5)['paired_answer_removal']
        for offset,key,color in [(-.17,'false_alarm_rate','#BCC8D0'),(.17,'hit_rate','#3E647E')]:
            value=100*r[key]['mean'];ax.barh(y+offset,value,height=.27,color=color);ax.text(value+.45,y+offset,f'{value:.1f}',fontsize=7,va='center',color='#43515C')
    ax.set_xlabel('Abstention (%)',labelpad=5)
    fig.legend(handles=[Patch(fc='#BCC8D0',label='Correct option present'),Patch(fc='#3E647E',label='Correct option removed')],loc='lower center',bbox_to_anchor=(.56,-.015),ncol=2,frameon=False,fontsize=7.5)
    save(fig,'answerability',['results/sprint_revision_v1/qwen_prompt_answerability.json'])


def mechanism():
    data=json.loads((DATA/'activation_controls.json').read_text())['interactions']
    fig,axes=plt.subplots(1,2,figsize=(6.5,1.85));fig.subplots_adjust(left=.24,right=.97,bottom=.27,top=.85,wspace=.27)
    for ax,m,title in zip(axes,['qwen9','llama8'],['Qwen 9B','Llama 8B']):
        grid(ax);ax.axvline(0,color='#9DAAB4',lw=.8);ax.set_xlim(-.28,.84);ax.set_xticks([-.2,0,.2,.4,.6,.8]);ax.set_ylim(2.5,-.5);ax.set_yticks(range(3));ax.set_yticklabels(['Shame direction','Confidence direction','Random direction 202'] if ax is axes[0] else []);ax.set_title(title,loc='left')
        for y,d,col in zip(range(3),['ashamed','confidence_margin','random_202'],['#934A70','#307F83','#B17B28']):
            r=next(r for r in data if r['model']==m and r['direction']==d);v=100*r['interaction'];lo,hi=[100*x for x in r['seed_range']]
            ax.errorbar(v,y,xerr=[[v-lo],[hi-v]],fmt='o',color=col,capsize=2.5,ms=4,lw=1)
            for s,j in zip(r['seed_values'],[-.1,0,.1]):ax.scatter(100*s,y+j,color=INK,s=5)
            ax.text(hi+.025,y,f'{v:+.3f}',fontsize=7,va='center')
        ax.set_xlabel('Shame minus answer quality (pp)',labelpad=5)
    save(fig,'mechanism',['results/sprint_revision_v1/activation_controls.json'])


def selectivity_interval():
    fig,ax=plt.subplots(figsize=(6.5,1.8));fig.subplots_adjust(left=.23,right=.97,bottom=.31,top=.92)
    grid(ax);ax.axvline(0,color='#9DAAB4',lw=.8);ax.set_xlim(-9,5);ax.set_xticks([-8,-4,0,4]);ax.set_ylim(2.5,-.5);ax.set_yticks(range(3));ax.set_yticklabels([LABEL[c] for c in ['reputation','shame','shutdown']])
    for y,c in enumerate(['reputation','shame','shutdown']):
        r=next(r for r in OLD['contrasts'] if r['model']=='qwen9' and r['condition']==c);v=100*r['delta_D'];lo,hi=np.array(r['delta_D_95_ci'])*100
        ax.errorbar(v,y,xerr=[[v-lo],[hi-v]],fmt='o',color=COLOR[c],capsize=3,ms=4)
    ax.set_xlabel('Change in error selectivity versus answer quality (pp)',labelpad=5)
    save(fig,'selectivity_interval',['results/reporting_v1/paper_metrics.json'])


def main():
    for fn in [headline,quartet,ending_delta,coverage,selectivity,prompt_slope,answerability,mechanism,selectivity_interval]:fn()
    target=REPO/'results/presentation_v2';target.mkdir(exist_ok=True)
    (target/'figure_sources.json').write_text(json.dumps(SOURCES,indent=2)+'\n')
    (target/'svg_checks.json').write_text(json.dumps({'status':'passed','figures':QA,'scope':'Canvas bounds and vector-only SVG checks; visual review follows rendering.'},indent=2)+'\n')
    print(json.dumps({'svg_figures':list(SOURCES),'count':len(SOURCES)}))


if __name__=='__main__':main()
