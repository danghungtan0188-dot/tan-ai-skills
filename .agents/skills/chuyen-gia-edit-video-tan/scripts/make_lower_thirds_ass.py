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
    name_size=max(34,round(a.height*.045)); detail_size=max(28,round(a.height*.035)); margin_x=round(a.width*.05); y=round(a.height*.72)
    head=f"""[Script Info]\nScriptType: v4.00+\nPlayResX: {a.width}\nPlayResY: {a.height}\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Name,Arial,{name_size},&H00FFFFFF,&H00FFFFFF,&H90000000,&H00000000,-1,0,0,0,100,100,0,0,1,1.2,0,7,0,0,0,1\nStyle: Detail,Arial,{detail_size},&H00FFFFFF,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,7,0,0,0,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"""
    events=[]
    for i,r in enumerate(rows):
        start=float(r["start"]); end=float(r["end"]); name=clean(r["name"]); detail=clean(r.get("detail",""))
        if end<=start: raise SystemExit(f"Mốc thời gian không hợp lệ ở mục {i+1}")
        # Nền gradient được mô phỏng bằng hai hộp xanh; chữ trượt nhẹ từ trái vào.
        box_y=y-round(a.height*.025); box_h=round(a.height*.135); box_w=round(a.width*.72)
        box=f"{{\\an7\\pos({margin_x},{box_y})\\p1\\1c&H8A330C&\\alpha&H18&}}m 0 0 l {box_w} 0 l {box_w} {box_h} l 0 {box_h}{{\\p0}}"
        accent=f"{{\\an7\\pos({margin_x},{box_y+box_h-5})\\p1\\1c&H00C7FF&}}m 0 0 l {box_w} 0 l {box_w} 5 l 0 5{{\\p0}}"
        x0=margin_x-35; x1=margin_x+28; t1=min(300,max(100,round((end-start)*100)))
        events.append(f"Dialogue: 0,{ts(start)},{ts(end)},Name,,0,0,0,,{box}")
        events.append(f"Dialogue: 1,{ts(start)},{ts(end)},Name,,0,0,0,,{accent}")
        events.append(f"Dialogue: 2,{ts(start)},{ts(end)},Name,,0,0,0,,{{\\move({x0},{y},{x1},{y},0,{t1})\\fad(120,180)}}{name}")
        if detail: events.append(f"Dialogue: 2,{ts(start)},{ts(end)},Detail,,0,0,0,,{{\\move({x0},{y+name_size+8},{x1},{y+name_size+8},0,{t1})\\fad(160,180)}}{detail}")
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(head+"\n".join(events)+"\n",encoding="utf-8"); print(a.output); return 0

if __name__=="__main__": raise SystemExit(main())
