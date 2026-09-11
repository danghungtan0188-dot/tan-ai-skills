#!/usr/bin/env python3
import argparse, json, pathlib

def ts(v):
    h=int(v//3600); v-=h*3600; m=int(v//60); s=v-m*60
    return f"{h}:{m:02d}:{s:05.2f}"
def esc(s): return str(s).replace("\\","\\\\").replace("{","\\{").replace("}","\\}").replace("\n","\\N")
def main():
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("output"); p.add_argument("--aspect",choices=["16:9","9:16"],default="16:9"); p.add_argument("--font",default="Arial",help="Windows không có DejaVu Sans; font thiếu làm lỗi dấu tiếng Việt"); a=p.parse_args()
    data=json.loads(pathlib.Path(a.input).read_text(encoding="utf-8"))
    pathlib.Path(a.output).write_text(build_ass(data.get("segments",[]),a.aspect,a.font),encoding="utf-8"); print(a.output)
def build_ass(segs,aspect="16:9",font="Arial"):
    prev=-1
    if not segs: raise SystemExit("Không có segments")
    for i,x in enumerate(segs):
        if not x.get("en") or not x.get("vi") or float(x["start"])>=float(x["end"]): raise SystemExit(f"Cue {i} không hợp lệ")
        if float(x["start"])<prev: raise SystemExit(f"Cue {i} chồng cue trước")
        prev=float(x["end"])
    w,h=(1920,1080) if aspect=="16:9" else (1080,1920); en_size=42 if aspect=="16:9" else 38; vi_size=en_size+4; margin=100 if aspect=="16:9" else 260
    head=f"""[Script Info]\nTitle: English above Vietnamese\nScriptType: v4.00+\nPlayResX: {w}\nPlayResY: {h}\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: EN,{font},{en_size},&H0000E7FF,&H0000E7FF,&H0012263E,&H99071930,-1,0,0,0,100,100,0,0,3,2,1,2,120,120,{margin+58},1\nStyle: VI,{font},{vi_size},&H00FFFFFF,&H00FFFFFF,&H0012263E,&H99071930,-1,0,0,0,100,100,0,0,3,2,1,2,120,120,{margin},1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"""
    rows=[]
    for x in segs:
        rows.append(f"Dialogue: 0,{ts(float(x['start']))},{ts(float(x['end']))},EN,,0,0,0,,{esc(x['en'])}")
        rows.append(f"Dialogue: 1,{ts(float(x['start']))},{ts(float(x['end']))},VI,,0,0,0,,{esc(x['vi'])}")
    return head+"\n".join(rows)+"\n"
if __name__=="__main__": main()
