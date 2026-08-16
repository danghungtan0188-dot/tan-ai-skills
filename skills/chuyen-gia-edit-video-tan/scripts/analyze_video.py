#!/usr/bin/env python3
import argparse, json, pathlib, subprocess

def capture(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True).stdout

def main():
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("--out",default="edit/analysis"); a=p.parse_args()
    src=pathlib.Path(a.input).resolve(); out=pathlib.Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    meta=json.loads(capture(["ffprobe","-v","error","-show_entries","format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels","-of","json",str(src)]))
    (out/"metadata.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
    loud=subprocess.run(["ffmpeg","-hide_banner","-i",str(src),"-af","loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"],text=True,capture_output=True)
    (out/"loudness.txt").write_text(loud.stderr,encoding="utf-8")
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(src),"-vf","fps=1/5,scale=480:-1,drawtext=text='%{pts\\:hms}':x=12:y=12:fontsize=24:fontcolor=white:borderw=2:bordercolor=black,tile=4x3:padding=6:margin=6",str(out/"contact_%03d.jpg")],check=True)
    print(out)
if __name__=="__main__": main()
