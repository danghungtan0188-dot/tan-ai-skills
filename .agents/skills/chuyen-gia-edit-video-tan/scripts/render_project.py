#!/usr/bin/env python3
import argparse, json, pathlib, shlex, subprocess
from presets import effect

XFADES={"cut":None,"fade":"fade","dissolve":"dissolve","dip_black":"fadeblack","dip_white":"fadewhite","wipe_left":"wipeleft","wipe_right":"wiperight","wipe_up":"wipeup","wipe_down":"wipedown","slide_left":"slideleft","slide_right":"slideright","slide_up":"slideup","slide_down":"slidedown","circle_open":"circleopen","circle_close":"circleclose","radial":"radial","zoom":"zoomin","blur":"hblur","flash_burst":"fadewhite","whip_left":"slideleft","whip_right":"slideright"}
FILTERS={"natural":"eq=contrast=1.03:saturation=1.03","vibrant":"eq=contrast=1.08:saturation=1.15","cinematic":"eq=contrast=1.08:saturation=.92,vignette=PI/7","warm":"colorbalance=rs=.035:bs=-.025","cool":"colorbalance=rs=-.025:bs=.035","bw":"hue=s=0","vintage":"eq=saturation=.82:gamma=.96,noise=alls=4:allf=t","news_clean":"eq=contrast=1.04:saturation=1.04,unsharp=5:5:.25:5:5:0"}

def esc(s): return str(s).replace("\\","\\\\").replace(":","\\:").replace("'","\\'")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--preview",action="store_true"); a=ap.parse_args()
    cfg=json.loads(pathlib.Path(a.project).read_text(encoding="utf-8")); clips=cfg.get("clips",[])
    if not clips: raise SystemExit("project cần ít nhất một clip")
    out=cfg.get("output",{}); w=int(out.get("width",1920)); h=int(out.get("height",1080)); fps=int(out.get("fps",30)); cmd=["ffmpeg","-y"]
    for c in clips: cmd += ["-ss",str(c.get("in",0)),"-to",str(c["out"]),"-i",c["path"]]
    stickers=cfg.get("stickers",[]); sticker_base=len(clips)
    for s in stickers: cmd += ["-loop","1","-i",s["path"]]
    music=cfg.get("music"); music_index=sticker_base+len(stickers)
    if music and music.get("path"): cmd += ["-stream_loop","-1","-i",music["path"]]
    fg=[]; durations=[]
    for i,c in enumerate(clips):
        speed=float(c.get("speed",1)); d=(float(c["out"])-float(c.get("in",0)))/speed; durations.append(d)
        vf=f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fps={fps}"
        if c.get("filter") in FILTERS: vf += ","+FILTERS[c["filter"]]
        ad=c.get("adjust",{}); vf += f",eq=brightness={ad.get('brightness',0)}:contrast={ad.get('contrast',1)}:saturation={ad.get('saturation',1)},setpts=PTS/{speed}[v{i}]"
        fg += [f"[{i}:v]{vf}",f"[{i}:a]asetpts=PTS-STARTPTS,atempo={min(2,max(.5,speed))}[a{i}]"]
    vcur="v0"; acur="a0"; timeline=durations[0]
    for i in range(1,len(clips)):
        tr=clips[i].get("transition",{}); name=tr.get("name","fade"); dur=float(tr.get("duration",.3)); x=XFADES.get(name,"fade")
        if x is None:
            dur=0; fg += [f"[{vcur}][v{i}]concat=n=2:v=1:a=0[vx{i}]",f"[{acur}][a{i}]concat=n=2:v=0:a=1[ax{i}]"]
        else:
            dur=min(dur,durations[i]/2,timeline/2); off=max(0,timeline-dur); fg += [f"[{vcur}][v{i}]xfade=transition={x}:duration={dur}:offset={off}[vx{i}]",f"[{acur}][a{i}]acrossfade=d={dur}[ax{i}]"]
        timeline += durations[i]-dur; vcur=f"vx{i}"; acur=f"ax{i}"
    for j,e in enumerate(cfg.get("effects",[])):
        expr=effect(e.get("preset",""),e.get("start",0),e.get("start",0)+e.get("duration",.2),e.get("strength",.6))
        if expr: nxt=f"ve{j}"; fg.append(f"[{vcur}]{expr}[{nxt}]"); vcur=nxt
    for j,s in enumerate(stickers):
        width=int(s.get("width",160)); opacity=float(s.get("opacity",1)); nxt=f"vs{j}"; st=f"st{j}"
        fg.append(f"[{sticker_base+j}:v]scale={width}:-1,format=rgba,colorchannelmixer=aa={opacity}[{st}]")
        fg.append(f"[{vcur}][{st}]overlay={s.get('x',40)}:{s.get('y',40)}:enable='between(t,{s.get('start',0)},{s.get('end',timeline)})'[{nxt}]"); vcur=nxt
    for j,t in enumerate(cfg.get("text",[])):
        preset=t.get("preset","title_clean"); size=t.get("size",76 if preset=="gold_impact_title" else 54); color=t.get("color","#FFD43B" if preset=="gold_impact_title" else "white")
        x=t.get("x","(w-text_w)/2"); x="(w-text_w)/2" if x=="center" else x; y=t.get("y","h-text_h-120"); sw=t.get("stroke_width",5 if preset=="gold_impact_title" else 3); nxt=f"vt{j}"
        fg.append(f"[{vcur}]drawtext=text='{esc(t['text'])}':fontsize={size}:fontcolor={color}:borderw={sw}:bordercolor={t.get('stroke_color','black')}:shadowx=4:shadowy=4:x={x}:y={y}:enable='between(t,{t['start']},{t['end']})'[{nxt}]"); vcur=nxt
    cap=cfg.get("captions")
    lower=cfg.get("lower_thirds")
    if lower and lower.get("path"): fg.append(f"[{vcur}]subtitles='{esc(lower['path'])}'[vlower]"); vcur="vlower"
    if cap and cap.get("path"): fg.append(f"[{vcur}]subtitles='{esc(cap['path'])}'[vcap]"); vcur="vcap"
    if music and music.get("path"):
        mv=float(music.get("volume",.16)); fg.append(f"[{music_index}:a]atrim=0:{timeline},asetpts=PTS-STARTPTS,volume={mv}[mus]")
        fg.append(f"[{acur}][mus]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-16:TP=-1.5:LRA=11[amix]"); acur="amix"
    dst=out.get("path","edit/final.mp4"); pathlib.Path(dst).parent.mkdir(parents=True,exist_ok=True)
    cmd += ["-filter_complex",";".join(fg),"-map",f"[{vcur}]","-map",f"[{acur}]","-c:v","libx264","-preset","veryfast" if a.preview else "medium","-crf",str(28 if a.preview else out.get("crf",18)),"-c:a","aac","-b:a","160k","-pix_fmt","yuv420p","-movflags","+faststart",dst]
    print(" ".join(shlex.quote(x) for x in cmd)); subprocess.run(cmd,check=True)
if __name__=="__main__": main()
