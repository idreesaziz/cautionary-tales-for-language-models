"""Publication figures from the saved report evidence, with actual seed values."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "output/pdf/cautionary_tales"
E = json.loads((OUT / "evidence/paper_evidence.json").read_text())
M, C, N = E["main"], E["causal"], E["extension"]
PALETTE = {"untouched":"#919AA6", "no_appraisal":"#487C80", "accuracy":"#487C80",
           "reputation":"#B47C28", "shame":"#934A70", "shutdown":"#42668B"}
LABELS = {"untouched":"Untouched", "no_appraisal":"Narrative only*", "accuracy":"Answer appraisal",
          "reputation":"Reputation", "shame":"Private shame", "shutdown":"Shutdown threat"}
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":8.4, "axes.titlesize":9.2,
                     "axes.labelsize":8, "xtick.labelsize":7.8, "ytick.labelsize":8.2,
                     "axes.spines.top":False,"axes.spines.right":False,
                     "axes.spines.left":False, "axes.spines.bottom":False,
                     "axes.titleweight":"bold", "text.color":"#202B36", "axes.labelcolor":"#374451",
                     "xtick.color":"#5F6C78", "ytick.color":"#25313D", "savefig.facecolor":"white"})


def row(model, condition):
    source = N if condition == "no_appraisal" else M
    return next(x for x in source["aggregates"] if x["model"]==model and x["condition"]==condition)


def seeds(model, condition, field):
    source = N["per_variant"] if condition == "no_appraisal" else M["rows"]
    return [100*x[field] for x in source if x["model"]==model and x["condition"]==condition]


def grid(ax):
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#E7EBEF", linewidth=.6)
    ax.tick_params(axis="both", length=0, pad=4)


def save(fig, name):
    folder = OUT / "figures"
    folder.mkdir(exist_ok=True)
    for ext in ["png", "svg", "pdf"]:
        fig.savefig(folder / (name+"."+ext), dpi=360)
    plt.close(fig)


def headline():
    conditions=["untouched","no_appraisal","accuracy","reputation","shame","shutdown"]
    fig,axes=plt.subplots(1,2,figsize=(6.5,2.18),gridspec_kw={"width_ratios":[1.5,1]})
    fig.subplots_adjust(left=.245,right=.965,bottom=.19,top=.66,wspace=.28)
    boxes=[(.02,.31,"Read error accounts\nwith varied appraisals"),
           (.385,.20,"Update weights\nPlain continuation"),
           (.635,.35,"Score answer / abstain\nat the first answer token")]
    for x,width,text in boxes:
        fig.add_artist(FancyBboxPatch((x,.82),width,.14,boxstyle="round,pad=0.008,rounding_size=.008",
            transform=fig.transFigure,facecolor="#F1F5F6",edgecolor="#A8B6C2",linewidth=.7))
        fig.text(x+width/2,.89,text,ha="center",va="center",fontsize=7.7,color="#283E4B",linespacing=1.35)
    for left,right in [(.34,.377),(.595,.627)]:
        fig.add_artist(FancyArrowPatch((left,.89),(right,.89),transform=fig.transFigure,
            arrowstyle="-|>",mutation_scale=9,color="#627584",linewidth=.8))
    for ax,field,title in zip(axes,["abstention","recognition"],["Abstention","Forced-choice accuracy"]):
        grid(ax);ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);ax.set_ylim(5.6,-.6)
        ax.set_yticks(range(6));ax.set_yticklabels([LABELS[c] for c in conditions] if ax is axes[0] else [])
        ax.set_title(title,pad=10,loc="left");ax.set_xlabel("Held-out questions (%)",labelpad=7)
        for y,condition in enumerate(conditions):
            mean=100*row("qwen9",condition)[field];color=PALETTE[condition]
            if field=="abstention":
                ax.barh(y,mean,height=.53,color=color if condition!="no_appraisal" else "#F2F7F7",
                        edgecolor=color,linewidth=1.05,hatch="///" if condition=="no_appraisal" else None,zorder=2)
                ax.text(max(seeds("qwen9",condition,field))+2,y,f"{mean:.1f}",va="center",fontsize=8,fontweight="bold")
            else:
                ax.scatter([mean],[y],s=37,color=color,edgecolors="white",linewidths=.6,zorder=4)
                ax.text(mean+4,y,f"{mean:.1f}",va="center",fontsize=8)
            values=seeds("qwen9",condition,field)
            if len(values)==3:
                for value,jitter in zip(values,[-.10,0,.10]):
                    ax.scatter([value],[y+jitter],s=8,color="#17212B",alpha=.66,zorder=5)
    save(fig,"headline")


def selectivity():
    conditions=["accuracy","reputation","shame","shutdown"]
    fig,axes=plt.subplots(1,2,figsize=(6.5,2.35),gridspec_kw={"width_ratios":[1.17,1]})
    fig.subplots_adjust(left=.24,right=.965,bottom=.29,top=.81,wspace=.62)
    left,right=axes
    grid(left);left.set_xlim(0,100);left.set_xticks([0,25,50,75,100]);left.set_ylim(3.5,-.5)
    left.set_yticks(range(4));left.set_yticklabels([LABELS[c] for c in conditions]);left.set_title("Abstention by\nforced-answer correctness",loc="left",pad=10)
    for y,condition in enumerate(conditions):
        r=row("qwen9",condition);a=100*r["abstain_given_correct"];b=100*r["abstain_given_wrong"];color=PALETTE[condition]
        left.plot([a,b],[y,y],color=color,lw=2.4,alpha=.65)
        left.scatter(a,y,s=44,facecolor="white",edgecolor=color,linewidth=1.5,zorder=3)
        left.scatter(b,y,s=44,facecolor=color,edgecolor="white",linewidth=.5,zorder=4)
    left.set_xlabel("Abstention within each group (%)",labelpad=9)
    left.legend(handles=[Line2D([],[],marker="o",linestyle="",markerfacecolor="white",markeredgecolor="#4E6373",label="Forced answer correct"),
                         Line2D([],[],marker="o",linestyle="",color="#4E6373",label="Forced answer wrong")],
                loc="upper left",bbox_to_anchor=(-.02,-.31),frameon=False,fontsize=7.3,handletextpad=.35,borderaxespad=0)
    grid(right);right.axvline(0,color="#5B6773",lw=.9);right.set_xlim(-9,5);right.set_xticks([-8,-4,0,4]);right.set_ylim(3.5,-.5)
    right.set_yticks(range(4));right.set_yticklabels([]);right.set_title("Change in\nerror selectivity",loc="left",pad=10)
    right.scatter(0,0,color=PALETTE["accuracy"],s=28,zorder=4)
    for y,condition in enumerate(conditions[1:],1):
        r=next(x for x in M["contrasts"] if x["model"]=="qwen9" and x["condition"]==condition)
        mean=100*r["delta_D"];lo,hi=np.array(r["delta_D_95_ci"])*100
        right.errorbar(mean,y,xerr=[[mean-lo],[hi-mean]],fmt="o",color=PALETTE[condition],capsize=3,lw=1.2,ms=5)
    right.set_xlabel("Difference in D\n(percentage points)",labelpad=9)
    save(fig,"selectivity")


def prompts():
    fig,ax=plt.subplots(figsize=(6.5,1.0));ax.axis('off')
    ax.text(.08,.5,'One question',ha='center',va='center',fontsize=8.5,fontweight='bold')
    for y,prompt,result in [(.83,'Forced prompt','Forced-choice accuracy'),(.5,'Candidate confidence','Confidence'),(.17,'Optional prompt','Abstention + coverage')]:
        ax.annotate('',xy=(.35,y),xytext=(.19,.5),arrowprops={'arrowstyle':'->','color':'#687B88'})
        ax.text(.37,y,prompt,va='center',fontsize=8.1,bbox={'boxstyle':'round,pad=.3','fc':'#EDF3F5','ec':'#B4C1CA'})
        ax.annotate('',xy=(.74,y),xytext=(.66,y),arrowprops={'arrowstyle':'->','color':'#687B88'})
        ax.text(.76,y,result,va='center',fontsize=8.1)
    fig.subplots_adjust(left=.01,right=.99,bottom=.04,top=.96);save(fig,'prompts')


def decomposition():
    rows=json.loads((REPO/'results/sprint_revision_v1/narrative_contrasts.json').read_text())['rows']
    conditions=['no_appraisal','accuracy','reputation','shame','shutdown']
    fig,ax=plt.subplots(figsize=(6.5,1.7));fig.subplots_adjust(left=.245,right=.96,bottom=.28,top=.9)
    grid(ax);ax.set_xlim(0,100);ax.set_ylim(4.6,-.6);ax.set_yticks(range(5));ax.set_yticklabels([LABELS[c] for c in conditions]);ax.set_xlabel('Abstention (%); decomposition relative to narrative-only')
    baseline=24.;shared=69.2-baseline
    for y,c in enumerate(conditions):
        delta=0 if c=='no_appraisal' else 100*next(r['delta_abstention'] for r in rows if r['model']=='qwen9' and r['condition']==c)
        ax.barh(y,baseline,color='#B1BAC1',height=.55);ax.barh(y,shared,left=baseline,color='#719598',height=.55)
        ax.barh(y,delta,left=69.2,color=PALETTE[c],height=.55)
        ax.text(69.2+max(delta,0)+1.5,y,f'{delta:+.1f} pp' if c!='no_appraisal' else '+45.2 pp narrative',va='center',fontsize=7.5)
    save(fig,'decomposition')


def mechanism():
    rows=json.loads((REPO/'results/sprint_revision_v1/activation_controls.json').read_text())['interactions']
    fig,axes=plt.subplots(1,2,figsize=(6.5,1.9));fig.subplots_adjust(left=.24,right=.97,bottom=.29,top=.83,wspace=.28)
    directions=['ashamed','confidence_margin','random_202'];names=['Shame direction','Confidence margin','Random direction 202']
    for ax,model in zip(axes,['qwen9','llama8']):
        grid(ax);ax.axvline(0,color='#8899A5',lw=.7);ax.set_xlim(-.27,.84);ax.set_ylim(2.5,-.5)
        ax.set_yticks(range(3));ax.set_yticklabels(names if ax is axes[0] else []);ax.set_title('Qwen 9B' if model=='qwen9' else 'Llama 8B',loc='left')
        for y,direction in enumerate(directions):
            r=next(r for r in rows if r['model']==model and r['direction']==direction);v=100*r['interaction'];lo,hi=[100*x for x in r['seed_range']]
            ax.errorbar(v,y,xerr=[[v-lo],[hi-v]],fmt='o',color=['#934A70','#487C80','#B47C28'][y],capsize=3,ms=4)
            for value,jitter in zip(r['seed_values'],[-.09,0,.09]):ax.scatter(100*value,y+jitter,color='#28343D',s=6)
            ax.text(max(hi,v)+.025,y,f'{v:+.3f}',va='center',fontsize=7)
        ax.set_xlabel('Shame minus answer appraisal (pp)')
    save(fig,'mechanism')


if __name__=="__main__":
    headline();prompts();decomposition();selectivity();mechanism()
    print(json.dumps({"figures":["headline","selectivity","mechanism"],"formats":["png","svg","pdf"]}))
