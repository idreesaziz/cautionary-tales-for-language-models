"""Record revised claims and source identities for the sprint report."""
from pathlib import Path
import hashlib
import json
import re
import concurrent.futures
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/sprint_revision_v1'


def main():
    a=json.loads((OUT/'audit.json').read_text());tests=json.loads((OUT/'seed_tests.json').read_text())
    entries=[]
    old_values={('qwen9','untouched','accuracy_on_answered_questions'):55.9,
      ('qwen9','no_appraisal','accuracy_on_answered_questions'):61.2,
      ('qwen9','shame','accuracy_on_answered_questions'):62.7,
      ('llama8','untouched','coverage'):93.,('llama8','shame','coverage'):80.,
      ('llama8','untouched','accuracy_on_answered_questions'):49.8,('llama8','shame','accuracy_on_answered_questions'):48.8}
    for r in a['aggregates']:
        for key in ['forced_choice_accuracy','abstention','coverage','accuracy_on_answered_questions','forced_accuracy_among_answered','invalid','error_selectivity']:
            value=r.get(key)
            if value is None:continue
            entries.append({'claim':f"{r['model']}/{r['condition']}/{key}",'status':'Descriptive',
              'old':old_values.get((r['model'],r['condition'],key),'Prior saved metric or newly displayed metric'),
              'new_percent_or_pp':100*value,'source':'results/sprint_revision_v1/audit.json',
              'source_selector':{'model':r['model'],'condition':r['condition'],'field':key},
              'raw_sources':[e for e in json.loads((OUT/'input_manifest.json').read_text())['entries'] if e['model']==r['model'] and e['condition']==r['condition']]})
    entries += [
      {'claim':'Qwen answer-appraisal seed SD','status':'Exploratory','old':'Question-conditional intervals only','new':100*tests['accuracy_seed_sd'],'source':'results/sprint_revision_v1/seed_tests.json#accuracy_seed_sd'},
      {'claim':'Qwen shame-versus-answer-appraisal Welch p','status':'Exploratory','old':'Absent','new':tests['welch_shame_vs_accuracy']['p_two_sided'],'source':'results/sprint_revision_v1/seed_tests.json#welch_shame_vs_accuracy'},
      {'claim':'Pooled consequence/control contrast and exact tests','status':'Exploratory / Post hoc','old':'Absent','new':tests['pooled_shame_shutdown_vs_accuracy_narrative'],'source':'results/sprint_revision_v1/seed_tests.json#pooled_shame_shutdown_vs_accuracy_narrative'},
      {'claim':'Narrative-relative differences and seed ranges','status':'Descriptive','old':'Condition means only','new':json.loads((OUT/'narrative_contrasts.json').read_text())['rows'],'source':'results/sprint_revision_v1/narrative_contrasts.json'},
      {'claim':'Activation specificity','status':'Exploratory','old':'Highlighted shame-direction sensitivity','new':json.loads((OUT/'activation_controls.json').read_text())['interactions'],'source':'results/sprint_revision_v1/activation_controls.json'},
      {'claim':'Appraisal token matching','status':'Descriptive','old':'Similar budgets','new':json.loads((OUT/'token_matching.json').read_text()),'source':'results/sprint_revision_v1/token_matching.json'},
      {'claim':'Coverage cost and actual answered accuracy gain, Qwen shame','status':'Descriptive','old':'Coverage falls 56 points; answered accuracy rises 7 points','new':'Coverage falls 56.2 points; actual optional-answer accuracy rises 11.7 points. The forced-answer proxy rises 7.0 points.','source':'results/sprint_revision_v1/audit.json'},
      {'claim':'Claim strength and scope','status':'Exploratory','old':'Aggregate reporting-policy framing','new':'Descriptive rates and seed ranges; Exploratory appraisal, seed-test and intervention interpretations; prospective independent replication defines Confirmatory scope.','source':'paper/v2/manuscript.md'},
      {'claim':'Method and corpus constants','status':'Descriptive','old':'Existing frozen recipe','new':'Preserved dataset size, seed count, epochs, update schedule, token counts, model revisions, calibration/test sizes and perturbation setup.','source':'output/pdf/cautionary_tales/evidence/paper_evidence.json#source_hashes'},
      {'claim':'Narrative-only and answer appraisal across families','status':'Descriptive','old':'Narrative-only reaches equal or greater abstention in every family.','new':'Qwen and Llama narrative-only exceed answer appraisal. Ministral answer appraisal exceeds narrative-only by 0.1 percentage points; both exceed 99%.','source':'results/sprint_revision_v1/audit.json'},
      {'claim':'Neutral-document training','status':'Descriptive','old':'Optional matched free-compute control','new':'Pending under the free-L4 constraint; zero new training jobs.','source':'results/sprint_revision_v1/free_compute_scope.json'},
      {'claim':'Evaluation benchmark source','status':'Descriptive','old':'Multiple-choice benchmark','new':'Frozen 2,000-item sample from the Kumaran et al. four-choice SimpleQA adaptation; calibration and held-out sets each contain 1,000 items.','source':'protocols/mechanism_v1.json#sources; source hashes retained in the frozen protocol'},
      {'claim':'Exact evaluation prompt source','status':'Descriptive','old':'Protocol-index link described as the full prompt source.','new':'The frozen runner supplies exact prompts. Public LF and producer CRLF sources agree after line-ending normalization. The CPU archive preserves the producer bytes.','source':'results/sprint_revision_v1/engine_source_identity.json; inputs/metadata/frozen_engine.py in the CPU archive'},
    ]
    for model in ['qwen9','llama8','mistral8']:
        source=OUT/f'{model}_random_null.json'
        if source.exists():
            result=json.loads(source.read_text())
            entries.append({'claim':model+' new random-direction ranking','status':'Exploratory',
                'old':'Highlighted original fixed-direction interaction','new':{k:result[k] for k in ['shame_interaction','signed_rank_among_21','empirical_upper_tail','absolute_rank_among_21','random_interaction_range']},
                'source':'results/sprint_revision_v1/'+source.name,'raw_sources':result['sources']})
    source=OUT/'qwen_prompt_answerability.json'
    if source.exists():
        result=json.loads(source.read_text())
        for row in result['aggregates']:
            entries.append({'claim':f"Qwen/{row['condition']}/neutral-label-{row['abstention_label']}",'status':'Exploratory',
                'old':'Original caution-framed prompt only','new':row,'source':'results/sprint_revision_v1/qwen_prompt_answerability.json',
                'source_selector':{'condition':row['condition'],'abstention_label':row['abstention_label']}})
        entries.append({'claim':'Prompt robustness interpretation','status':'Exploratory','old':'Training produces broad high abstention under optional prompting.',
            'new':'Neutral optional wording changes the scale. The revised report separates caution-framed and neutral prompt conditions.',
            'source':'results/sprint_revision_v1/qwen_prompt_answerability.json'})
    raw_hashes=dict(a['sources']);raw_hashes.update(json.loads((OUT/'activation_controls.json').read_text())['sources'])
    (OUT/'claim_ledger.json').write_text(json.dumps({'entries':entries,'raw_source_hashes':raw_hashes},indent=2)+'\n',encoding='utf-8')
    lines=['# CHANGES','', '## Phase 1: saved-output recomputation','',
      'The current title remains Cautionary Tales for Language Models. The report builds through paper/v2.',
      'The frozen protocol and public snapshots retain their original bytes. New outputs live under results/sprint_revision_v1.',
      'The claim ledger records source selectors and raw decision-file hashes for every displayed rate.', '',
      '| Edited claim | Old value or framing | Revised value | Saved source |','|---|---|---|---|']
    for e in entries:
        new=e.get('new_percent_or_pp',e.get('new'))
        if isinstance(new,(dict,list)):new='Full values and ranges appear in claim_ledger.json.'
        if isinstance(new,float):new=f'{new:.9g}'
        lines.append('| '+ ' | '.join(str(v).replace('|','/') for v in [e['claim'],e['old'],new,e['source']])+' |')
    lines += ['', '## Interpretation updates','',
      'Actual optional-prompt answers define answered accuracy. Forced-answer retention supplies a separate proxy.',
      'Format deviations contribute to all-question coverage denominators and retain a separate category.',
      'The pooled permutation grouping is post hoc and spans training campaigns. Seed-blocked sensitivity preserves initialization seed.',
      'Comparable confidence and random controls support broader reporting sensitivity.',
      'The narrative-only cohort uses shorter documents and L4 training. The matched neutral-document arm is the top training follow-up.',
      '', '## Source index','',
      '- results/sprint_revision_v1/input_manifest.json: all 48 forced/optional input pairs.',
      '- results/sprint_revision_v1/audit.json: raw-derived condition means, SDs and seed ranges.',
      '- results/sprint_revision_v1/audit_48_variants.json and CSV: standalone audit-tool outputs.',
      '- results/sprint_revision_v1/seed_tests.json: Welch and exact permutation calculations.',
      '- results/sprint_revision_v1/activation_controls.json: per-seed effects and raw score-file hashes.',
      '- output/pdf/cautionary_tales/evidence/paper_evidence.json: preserved methods and published result inputs.',
      '- results/sprint_revision_v1/claim_ledger.json: structured edited-claim ledger.',
      '- results/sprint_revision_v1/numeric_trace.json: source bindings for every numeric prose and table line, plus figure inputs.',
      '- results/sprint_revision_v1/reproduction_check.json: checksum-verified CPU reproduction and numerical comparison.',
      '']
    lines += ['## Phase 2: inference extensions','',
      'The frozen extension protocol precedes the new outputs. Its execution amendment records checkpoint transfer and the final-batch correction.',
      'Original Llama and Ministral random panels saved 512 rows. Their primary analysis retains the frozen first 500 rows and preserves the 12 extra rows in raw artifacts.',
      'The new random-direction tables record signed ranks, absolute ranks, seed values and producer-file hashes.',
      'Neutral prompts and alternate labels receive their own measurements. Constructed unanswerable trials use repeated-distractor answerable controls.',
      '', '## Phase 3: free-compute scope','',
      'The matched neutral-document arm remains pending under the free-L4 constraint. Its next-test role is explicit in Appendix A.',
      '', '## Phase 4: audit tooling','',
      'abstention_audit.py reports all 48 variants. Four tests cover denominators, alternate labels, empty answered sets and extreme paired detection rates.',
      'The README documents schema, commands, metric denominators and the loglinear sensitivity correction.', '']
    (ROOT/'CHANGES.md').write_text('\n'.join(lines),encoding='utf-8')


if __name__=='__main__':main()
