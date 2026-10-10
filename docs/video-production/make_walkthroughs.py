from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv, hashlib, imageio_ffmpeg, json, shutil, subprocess, textwrap

W=Path.cwd()/'work'; O=Path.cwd()/'outputs'
S=Path('/Users/aicenter/Desktop/desktop/website/AnhDuongVo.github.io')
R=Path('/Users/aicenter/Library/CloudStorage/Dropbox/claude application/code nvidia/github-repos')
F=W/'video-frames'; F.mkdir(exist_ok=True)
font='/System/Library/Fonts/Supplemental/Arial.ttf'; mono='/System/Library/Fonts/Menlo.ttc'
def ft(size,code=False): return ImageFont.truetype(mono if code else font,size)
def lines(draw,xy,text,size=23,width=93,color='#243137',code=False):
    x,y=xy
    for line in text.splitlines():
        for part in textwrap.wrap(line,width=width,replace_whitespace=False,drop_whitespace=False) or ['']:
            draw.text((x,y),part,font=ft(size,code),fill=color);y+=size*1.45
    return y
def frame(slug,index,title,body='',caption='',screenshot=None,label='Actual offline run · Synthetic fixtures',code=False):
    im=Image.new('RGB',(1280,900),'#fcfcfa');d=ImageDraw.Draw(im)
    d.rectangle((0,0,1280,78),fill='#243137')
    d.text((32,13),slug,font=ft(27),fill='white')
    d.text((32,47),label,font=ft(17),fill='#f2c1a6')
    if screenshot:
        shot=Image.open(screenshot).convert('RGB');shot.thumbnail((1280,720));im.paste(shot,((1280-shot.width)//2,78))
    else:
        d.text((40,105),title,font=ft(33),fill='#ad5134')
        lines(d,(40,170),body,size=16 if code else 26,width=124 if code else 85,code=code)
    d=ImageDraw.Draw(im);d.rectangle((0,798,1280,900),fill='#f2e8e0')
    lines(d,(32,813),caption,size=22,width=102)
    d.text((1210,871),f'{index+1:02}',font=ft(15),fill='#ad5134')
    p=F/f'{slug}-composed-{index}.png';im.save(p);return p

def encode(slug,frames,dest,seconds=6):
    listing=F/f'{slug}.ffconcat'
    listing.write_text('ffconcat version 1.0\n'+''.join(f"file '{p}'\nduration {seconds}\n" for p in frames)+f"file '{frames[-1]}'\n")
    dest.parent.mkdir(parents=True,exist_ok=True)
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff,'-y','-loglevel','error','-safe','0','-i',str(listing),'-vf','fps=24','-c:v','libx264','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart','-t',str(len(frames)*seconds),str(dest)],check=True)
    poster=dest.with_suffix('.jpg')
    if poster.exists(): poster.chmod(poster.stat().st_mode | 0o200)
    Image.open(frames[0]).convert('RGB').save(poster,quality=90)
    subprocess.run([ff,'-v','error','-i',str(dest),'-f','null','-'],check=True)
    return {'file':str(dest.relative_to(S)) if dest.is_relative_to(S) else dest.name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'seconds':len(frames)*seconds,'frames':len(frames),'format':'edited walkthrough; actual captured UI or recorded command output; silent'}

clinical={
'consult-to-note':('Catch a planted dose error',['Problem: the note selects a source value for each numerical check.','Action: compare the bundled note with the transcript before planting an error.','Outcome: 250 mg is flagged against 25 mg; 148 matching does not verify 92.'],'Selected scalar checks only; no model generation or clinical validation.'),
'trial-matcher':('Preserve missing evidence',['Problem: screening needs a measurement; this is a simplified threshold illustration.','Missing eGFR stays unknown; age and HbA1c use the supplied scalar values.','Action / outcome: supply eGFR 60; the >= 45 threshold changes to met.'],'No FHIR parsing, trial retrieval or model assessment in this illustration.'),
'csr-assistant':('Correct a mismatched report value',['Problem: a drafted mean differs from the cited source row.','The draft says -1.4; source row r3 says -0.35. The selected value is flagged.','Action / outcome: change the draft to -0.35; the selected value matches.'],'Counts match exactly; continuous tolerance is 0.005. Not ICH E3 document review.'),
'ai-scientist':('Rank simulated protein candidates',['Problem: orchestration needs a transparent ranking rule. All scores here are simulated.','Protein-only ranking uses confidence and MPNN score; there is no affinity term.','Action / outcome: change seed 0 to 1; repeatable simulated inputs produce a new ranking.'],'No scientific inference. Full project co-folds only when target_sequence is supplied.')}
manifest={}
for slug,(title,captions,limit) in clinical.items():
    fs=[frame(slug,i,title,caption=c,screenshot=F/f'{slug}-{i}.png',label='Offline illustrative demo · Synthetic data') for i,c in enumerate(captions)]
    fs.append(frame(slug,3,'What this recording demonstrates',title+'\n\n'+limit,caption='Edited capture of the current Streamlit UI; bundled text and simplified checking logic.',label='Offline illustrative demo · Synthetic data'))
    manifest[slug]=encode(slug,fs,S/f'src/content/projects/clinical-agentic-ai/{slug}.mp4')

tech={
'mcp-bionemo':('agentic-tooling','Discover and invoke a typed MCP tool', 'python examples/client_walkthrough.py', (W/'recording-mcp-bionemo.txt').read_text(), 'The real stdio client discovers five tools and receives a synthetic PDB from design_backbone.', 'Actual MCP transport against the simulator; no live BioNeMo or scientific validation.'),
'agenteval':('agentic-tooling','Inspect behavior and claim metrics','agenteval behavior data/sample_traces.jsonl\nagenteval claims data/clinical_samples',(W/'recording-agenteval-behavior.txt').read_text()+'\n'+(W/'recording-agenteval-claims.txt').read_text(),'Five traces: tool success 83.3%, exact selection 80%, citation integrity 80%.\n25 claims: citation integrity 88%, numerical accuracy 85.7%.','Bundled synthetic fixtures; reference existence and numerical screening do not prove semantics.'),
'rag-guidelines':('agentic-tooling','Retrieve then screen an extractive answer','rag ask "What is the HbA1c target?"',(W/'recording-rag-guidelines.txt').read_text(),'Two extracted sentences pass the lexical and numerical screens. Retrieved passages are synthetic.','Synthetic extractive lexical screening; not a live clinical LLM evaluation.'),
'agentsim':('agent-workload-sim','Compare concurrency and scheduling','agentsim sweep --profile chat:0.5,react:0.3,fanout:0.2 --runs 100\n  --gpus 2 --agents 4,16,64 --policy fifo,srpt,progress --out sweep.csv','', 'Higher concurrency improves modeled throughput but also increases p95 latency.\nCompare policies under the same seeded workload before extrapolating.','Simulated cluster, not measured hardware. Benchmark usage distinguishes server counts from estimates.')}
rows=list(csv.DictReader((W/'current-sweep.csv').open()))
keys=['policy','n_agents','runs_per_min','latency_p95_s','join_wait_share']
keys=[k for k in keys if k in rows[0]]
if len(keys)<4: keys=list(rows[0])[:6]
tech['agentsim']=(*tech['agentsim'][:3], '\n'.join(' | '.join(f'{k:>16}' for k in keys) for _ in [0])+'\n'+'\n'.join(' | '.join(f'{str(r[k]):>16}' for k in keys) for r in rows),*tech['agentsim'][4:])
for slug,(folder,title,cmd,out,result,limit) in tech.items():
    fs=[frame(slug,0,title,'Problem\n'+title+'\n\nAction\n'+cmd,caption=limit)]
    # Keep full CLI output readable on separate pages, preserving metric names and values.
    chunks=[out] if slug!='agenteval' else [(W/'recording-agenteval-behavior.txt').read_text(),(W/'recording-agenteval-claims.txt').read_text()]
    for chunk in chunks:
        fs.append(frame(slug,len(fs),'Recorded output · current implementation',chunk,caption='Actual output captured from a successful local run on 10 October 2026.',code=True))
    fs.append(frame(slug,len(fs),'Outcome and limitation',result+'\n\n'+limit,caption='Reproduce with the command shown; installation is documented in the linked repository.'))
    manifest[slug]=encode(slug,fs,S/f'src/content/projects/{folder}/{slug}.mp4',seconds=8)

interview=(W/'recording-interview.txt').read_text()
source=(W/'interview_walkthrough.py').read_text()
pages=[('Full software workflow','consult-to-note + agenteval\n\nSynthetic consultation, scripted extraction, drafting and judging.\nActual LangGraph workflow and evaluation functions.\n\nThe judge deliberately accepts everything; deterministic dose failures must remain flagged.'),
       ('Source: actual workflow calls','\n'.join(source.splitlines()[24:42])),
       ('Evidence: synthetic transcript',interview.split('REVISION BUDGET 0')[0]),
       ('No revision budget: error stays flagged','REVISION BUDGET 0'+interview.split('REVISION BUDGET 0')[1].split('REVISION BUDGET 1')[0]),
       ('One revision: dose corrected, FHIR preliminary','REVISION BUDGET 1'+interview.split('REVISION BUDGET 1')[1].split('AGENTEVAL')[0]),
       ('Evaluate the same selected dose','AGENTEVAL'+interview.split('AGENTEVAL')[1]),
       ('Discuss the limits','One synthetic case cannot establish clinical accuracy.\n\nMatching citation IDs does not establish semantic support.\nA scripted revision does not establish live model reliability.\nFHIR output remains preliminary until the separate human-review workflow.\n\nRun this script live in an interview and inspect agent.py and grounding.py together.')]
fs=[frame('consult-to-note + agenteval',i,t,b,caption='Full implementation control flow · Synthetic inputs · Scripted models · No live API',code=i in [1,2,3,4,5]) for i,(t,b) in enumerate(pages)]
manifest['interview']=encode('interview',fs,O/'consult-to-note-agenteval-interview.mp4',seconds=12)
shutil.copy2(W/'interview_walkthrough.py',O/'interview_walkthrough.py')
shutil.copy2(W/'recording-interview.txt',O/'interview-run.txt')
(O/'video-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Refresh README animations too, archiving originals before replacing them.
for slug in list(clinical)+list(tech):
    repo=R/('clinical-agentic-ai-demo' if slug in clinical else 'agentsim/Untitled' if slug=='agentsim' else slug)
    old=repo/'docs'/((slug+'.gif') if slug in clinical else 'demo.gif')
    if old.exists():
        backup=repo/'old-videos/2026-10-10'/old.name;backup.parent.mkdir(parents=True,exist_ok=True)
        if not backup.exists():shutil.copy2(old,backup)
        old.chmod(old.stat().st_mode | 0o200)
        v=S/manifest[slug]['file']
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-i',str(v),'-vf','fps=1,scale=800:-1','-loop','0',str(old)],check=True)
print(json.dumps(manifest,indent=2))
