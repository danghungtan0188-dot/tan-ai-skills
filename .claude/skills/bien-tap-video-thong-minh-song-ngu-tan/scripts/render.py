#!/usr/bin/env python3
import argparse, json, pathlib, subprocess

FILTERS={"news_clean":"eq=brightness=.008:contrast=1.04:saturation=1.04,unsharp=5:5:.22:5:5:0","natural":"eq=contrast=1.02:saturation=1.02","cinematic":"eq=contrast=1.06:saturation=.94,vignette=PI/16"}
def q(s): return str(s).replace("\\","\\\\").replace(":","\\:").replace("'","\\'")
def duration(path):
    r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",path],text=True,capture_output=True,check=True)
    return r.stdout.strip()
def loudnorm_linear(path, pre="highpass=f=70,lowpass=f=15500"):
    """Loudnorm 2 lượt, linear: đo trước rồi áp một mức gain cố định — không bóp dải động."""
    r=subprocess.run(["ffmpeg","-hide_banner","-i",path,"-vn","-af",f"{pre},loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"],text=True,capture_output=True,encoding="utf-8",errors="replace")
    m=json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}")+1])
    return (f"{pre},loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
            f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
def main():
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("plan"); p.add_argument("captions"); p.add_argument("output"); p.add_argument("--lower-thirds"); p.add_argument("--preview",action="store_true"); a=p.parse_args()
    plan=json.loads(pathlib.Path(a.plan).read_text(encoding="utf-8")); style=plan.get("style",{}); vf=FILTERS.get(style.get("filter"),FILTERS["natural"])
    if a.lower_thirds: vf += f",subtitles='{q(pathlib.Path(a.lower_thirds).resolve())}'"
    vf += f",subtitles='{q(pathlib.Path(a.captions).resolve())}'"
    out=pathlib.Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    cmd=["ffmpeg","-y","-hide_banner","-i",a.input,"-vf",vf,"-af",loudnorm_linear(a.input)+",aresample=44100","-t",duration(a.input),"-c:v","libx264","-preset","veryfast" if a.preview else "faster","-crf","27" if a.preview else "20","-c:a","aac","-ar","44100","-b:a","160k" if a.preview else "192k","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
    subprocess.run(cmd,check=True); print(out)
if __name__=="__main__": main()
