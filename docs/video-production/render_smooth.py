from pathlib import Path
import subprocess,json,math,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
import imageio_ffmpeg
BASE=Path.cwd();ROOT=BASE/'work/smooth-recordings';OUT=BASE/'outputs/smooth-demos';OUT.mkdir(exist_ok=True);F=imageio_ffmpeg.get_ffmpeg_exe();FPS=30;W=1600;H=946
pointer=Image.new('RGBA',(80,100));d=ImageDraw.Draw(pointer);d.polygon([(5,5),(5,78),(25,58),(43,94),(58,86),(40,51),(70,51)],fill='#202020',outline='white',width=5);pointer=pointer.resize((32,40),Image.Resampling.LANCZOS)
manifest={'date':'2026-10-10','capture':'Fresh Chrome MediaRecorder footage of the actual running Streamlit illustration. Real clicks, input edits and scrolling; idle gaps shortened. Cursor is a visualization of captured interaction positions, interpolated before each recorded click, with a brief click ring. No added text or end cards.','clips':[]}
for slug in ['consult-to-note','trial-matcher','csr-assistant','ai-scientist']:
 meta=json.loads((ROOT/f'{slug}.json').read_text());events=meta['events'];assert len(events)>5
 times=sorted(set(e['t'] for e in events if e['t']>=0));start=max(0,times[0]-1.9);end=min(meta['duration']-.3,times[-1]+1.8)
 # Only remove the middle of an event-free pause, retaining the action and its result.
 cuts=[]
 for a,b in zip(times,times[1:]):
  if b-a>2.5:cuts.append((a+1.35,b-1.05))
 def removed(t):return sum(max(0,min(t,b)-a) for a,b in cuts if t>a)
 def mapped(t):return (t-start-removed(t)+removed(start))*1.5
 clicks=[]
 for e in events:
  if e['type']=='click' and start<=e['t']<=end:
   pt=(e['x']/e['w']*W,e['y']/e['h']*H)
   if 0<=pt[0]<=W and 0<=pt[1]<=H:clicks.append((mapped(e['t']),*pt,e['target']))
 assert clicks
 # Cursor moves before the live click and rests on the clicked control.
 first=clicks[0];anchor=(first[1]+min(180,W-first[1]-35),max(45,first[2]-90));motions=[];prev_t=-1;prev=anchor
 for t,x,y,label in clicks:
  dist=math.hypot(x-prev[0],y-prev[1]);travel=min(1.2,max(.75,dist/650));a=max(prev_t+.12,t-travel)
  if a>=t:a=t-.15
  motions.append((a,t,prev,(x,y)));prev=(x,y);prev_t=t
 def position(t):
  p=anchor
  for a,b,old,new in motions:
   if t<a:return p
   if t<=b:
    u=max(0,min(1,(t-a)/(b-a)));u=u*u*(3-2*u)
    # Gentle arc rather than an abrupt linear jump.
    return(old[0]+(new[0]-old[0])*u,old[1]+(new[1]-old[1])*u-12*math.sin(math.pi*u))
   p=new
  return p
 mp4=OUT/f'{slug}.mp4';decoder=subprocess.Popen([F,'-v','error','-i',str(ROOT/f'{slug}.webm'),'-vf',f'fps={FPS},scale={W}:{H}:flags=lanczos','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 encoder=subprocess.Popen([F,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(mp4)],stdin=subprocess.PIPE)
 idx=count=kept=0;proof=False
 while True:
  raw=decoder.stdout.read(W*H*3)
  if len(raw)!=W*H*3:break
  t=idx/FPS;idx+=1
  if t<start or t>end or any(a<t<b for a,b in cuts):continue
  repeats=int((kept+1)*1.5)-int(kept*1.5);kept+=1
  for _ in range(repeats):
   output_t=count/FPS;im=Image.frombytes('RGB',(W,H),raw).convert('RGBA');overlay=Image.new('RGBA',(W,H));od=ImageDraw.Draw(overlay)
   for ct,cx,cy,label in clicks:
    dt=output_t-ct
    if 0<=dt<.65:
     r=12+17*dt/.65;alpha=int(235*(1-dt/.65));od.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(184,86,58,int(alpha*.18)),outline=(184,86,58,alpha),width=3)
   x,y=position(output_t);overlay.alpha_composite(pointer,(int(x)-2,int(y)-2));im=Image.alpha_composite(im,overlay).convert('RGB');encoder.stdin.write(im.tobytes());count+=1
   if not proof and any(.15<output_t-c[0]<.35 for c in clicks):im.save(OUT/f'{slug}-click.jpg',quality=90);proof=True
 encoder.stdin.close();assert encoder.wait()==0;decoder.stdout.close();decoder.wait()
 poster=OUT/f'{slug}.jpg';subprocess.run([F,'-y','-v','error','-ss','1','-i',str(mp4),'-frames:v','1',str(poster)],check=True)
 gif=ROOT/f'{slug}.gif';subprocess.run([F,'-y','-v','error','-i',str(mp4),'-filter_complex','fps=15,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3','-loop','0',str(gif)],check=True)
 subprocess.run([F,'-v','error','-i',str(mp4),'-f','null','-'],check=True)
 c={'project':slug,'seconds':round(count/FPS,3),'source_seconds':meta['duration'],'fps':FPS,'clicks':len(clicks),'idle_cuts':cuts,'click_timeline':[{'t':round(t,3),'x':round(x),'y':round(y),'target':label} for t,x,y,label in clicks],'sha256':hashlib.sha256(mp4.read_bytes()).hexdigest()};manifest['clips'].append(c);print(slug,c['seconds'],'seconds;',len(clicks),'visible clicks',flush=True)
 (OUT/f'{slug}-timing.json').write_text(json.dumps(c,indent=2)+'\n')
(BASE/'outputs/smooth-video-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
