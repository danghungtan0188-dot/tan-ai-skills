#!/usr/bin/env python3
import argparse, json, subprocess, sys
p=argparse.ArgumentParser(); p.add_argument("video"); p.add_argument("--source"); p.add_argument("--cut-authorized",choices=["yes","no"],default="no"); a=p.parse_args()
r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,codec_name,width,height,pix_fmt,sample_rate,channels","-of","json",a.video],text=True,capture_output=True)
if r.returncode: print(r.stderr,file=sys.stderr); raise SystemExit(1)
d=json.loads(r.stdout); kinds={s.get("codec_type") for s in d.get("streams",[])}; errors=[]
if not {"video","audio"}.issubset(kinds): errors.append("Thiếu hình hoặc tiếng")
v=next((s for s in d.get("streams",[]) if s.get("codec_type")=="video"),{})
if v.get("pix_fmt")!="yuv420p": errors.append("Pixel format không phải yuv420p")
if a.source and a.cut_authorized=="no":
    src=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",a.source],text=True,capture_output=True)
    if src.returncode: errors.append("Không đọc được thời lượng nguồn")
    else:
        source_duration=float(json.loads(src.stdout)["format"]["duration"]); output_duration=float(d["format"]["duration"])
        if abs(source_duration-output_duration)>0.08: errors.append(f"Chưa được phép cắt nhưng thời lượng lệch {output_duration-source_duration:+.3f} giây")
print(json.dumps({"pass":not errors,"errors":errors,"probe":d},ensure_ascii=False,indent=2)); raise SystemExit(bool(errors))
