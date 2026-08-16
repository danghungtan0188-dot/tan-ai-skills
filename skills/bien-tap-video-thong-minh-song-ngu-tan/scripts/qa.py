#!/usr/bin/env python3
import argparse, json, pathlib, subprocess
def probe(p): return json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,codec_name,width,height,pix_fmt","-of","json",p],text=True,capture_output=True,check=True).stdout)
p=argparse.ArgumentParser(); p.add_argument("video"); p.add_argument("--source"); p.add_argument("--cut-authorized",choices=["yes","no"],default="no"); p.add_argument("--captions"); a=p.parse_args(); d=probe(a.video); errors=[]
k={s.get("codec_type") for s in d["streams"]}
if not {"video","audio"}.issubset(k): errors.append("Thiếu hình hoặc tiếng")
v=next(s for s in d["streams"] if s.get("codec_type")=="video")
if v.get("pix_fmt")!="yuv420p": errors.append("Không phải yuv420p")
if a.source and a.cut_authorized=="no" and abs(float(d["format"]["duration"])-float(probe(a.source)["format"]["duration"]))>.08: errors.append("Thời lượng thay đổi khi chưa được phép cắt")
if a.captions:
    c=json.loads(pathlib.Path(a.captions).read_text(encoding="utf-8"))
    if c.get("meta",{}).get("english_above_vietnamese") is not True: errors.append("Chưa xác nhận English ở trên Vietnamese")
    if any(not x.get("en") or not x.get("vi") for x in c.get("segments",[])): errors.append("Cue thiếu một ngôn ngữ")
print(json.dumps({"pass":not errors,"errors":errors,"probe":d},ensure_ascii=False,indent=2)); raise SystemExit(bool(errors))
