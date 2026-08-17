#!/usr/bin/env python3
"""Tạo lower-third ASS xanh chính thống cho người phát biểu."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def ts(seconds: float) -> str:
    cs=round(float(seconds)*100); h,cs=divmod(cs,360000); m,cs=divmod(cs,6000); s,cs=divmod(cs,100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def clean(value: object) -> str:
    return str(value).replace("\\","\\\\").replace("{","\\{").replace("}","\\}").replace("\n"," ").strip()

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("input",type=Path); ap.add_argument("output",type=Path); ap.add_argument("--width",type=int,default=1920); ap.add_argument("--height",type=int,default=1080); a=ap.parse_args()
    rows=json.loads(a.input.read_text(encoding="utf-8"));
    if not isinstance(rows,list): raise SystemExit("lower-thirds.json phải là một mảng")
    ns=max(34,round(a.height*.045)); ds=max(28,round(a.height*.035)); mx=round(a.width*.05); y=round(a.height*.72); by=y-round(a.height*.025); bh=round(a.height*.135); bw=round(a.width*.72)
    head=f"""[Script Info]\nScriptType: v4.00+\nPlayResX: {a.width}\nPlayResY: {a.height}\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Name,Arial,{ns},&H00FFFFFF,&H00FFFFFF,&H90000000,&H00000000,-1,0,0,0,100,100,0,0,1,1.2,0,7,0,0,0,1\nStyle: Detail,Arial,{ds},&H00FFFFFF,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,7,0,0,0,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"""; events=[]
    for i,r in enumerate(rows):
        st=float(r["start"]); en=float(r["end"]); name=clean(r["name"]); detail=clean(r.get("detail",""))
        if en<=st: raise SystemExit(f"Mốc thời gian không hợp lệ ở mục {i+1}")
        box=f"{{\\an7\\pos({mx},{by})\\p1\\1c&H8A330C&\\alpha&H18&}}m 0 0 l {bw} 0 l {bw} {bh} l 0 {bh}{{\\p0}}"; accent=f"{{\\an7\\pos({mx},{by+bh-5})\\p1\\1c&H00C7FF&}}m 0 0 l {bw} 0 l {bw} 5 l 0 5{{\\p0}}"; x0=mx-35; x1=mx+28; t=min(300,max(100,round((en-st)*100)))
        events += [f"Dialogue: 0,{ts(st)},{ts(en)},Name,,0,0,0,,{box}",f"Dialogue: 1,{ts(st)},{ts(en)},Name,,0,0,0,,{accent}",f"Dialogue: 2,{ts(st)},{ts(en)},Name,,0,0,0,,{{\\move({x0},{y},{x1},{y},0,{t})\\fad(120,180)}}{name}"]
        if detail: events.append(f"Dialogue: 2,{ts(st)},{ts(en)},Detail,,0,0,0,,{{\\move({x0},{y+ns+8},{x1},{y+ns+8},0,{t})\\fad(160,180)}}{detail}")
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(head+"\n".join(events)+"\n",encoding="utf-8"); print(a.output); return 0

if __name__=="__main__": raise SystemExit(main())
