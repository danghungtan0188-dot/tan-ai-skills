#!/usr/bin/env python3
import argparse, json, pathlib, subprocess, sys
def probe(p): return json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,codec_name,width,height,pix_fmt","-of","json",p],text=True,capture_output=True,check=True).stdout)
def kiem_ke_hoach(video,plan_path,dur,tail,sai_so=.5):
    """Bản dựng từ nhiều clip: kiểm theo edit-plan.json đã duyệt, không kiểm theo một file nguồn."""
    sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
    from detect_scenes import detect
    pl=json.loads(pathlib.Path(plan_path).read_text(encoding="utf-8")); loi=[]; canh=[]
    if abs(dur-pl["tong"]-tail)>sai_so: loi.append(f"Thời lượng {dur:.2f}s ≠ kế hoạch {pl['tong']}s + outro {tail}s")
    if abs(pl["tong"]-pl["target"])>2: loi.append(f"Kế hoạch {pl['tong']}s lệch quá 2s so với yêu cầu {pl['target']}s")
    cuts=detect(pathlib.Path(video),fast=True)["cuts"]
    thieu=[s["pos"] for s in pl["segments"][1:] if not any(abs(c-s["pos"])<=sai_so for c in cuts)]
    if thieu: canh.append(f"Không dò thấy mốc cắt tại {thieu} — xem tay; hai cảnh giống nhau thì scdet có thể sót")
    return loi,canh,len(pl["segments"])
p=argparse.ArgumentParser(); p.add_argument("video"); p.add_argument("--source"); p.add_argument("--cut-authorized",choices=["yes","no"],default="no"); p.add_argument("--captions"); p.add_argument("--plan",help="edit-plan.json đã duyệt — dùng khi ghép từ nhiều clip"); p.add_argument("--tail",type=float,default=0.0,help="số giây outro nối thêm ở cuối"); a=p.parse_args(); d=probe(a.video); errors=[]; canh_bao=[]; ke_hoach=None
k={s.get("codec_type") for s in d["streams"]}
if not {"video","audio"}.issubset(k): errors.append("Thiếu hình hoặc tiếng")
v=next(s for s in d["streams"] if s.get("codec_type")=="video")
if v.get("pix_fmt")!="yuv420p": errors.append("Không phải yuv420p")
if a.source and a.cut_authorized=="no" and abs(float(d["format"]["duration"])-float(probe(a.source)["format"]["duration"])-a.tail)>.08: errors.append("Thời lượng thay đổi khi chưa được phép cắt")
if a.plan:
    l,c,n=kiem_ke_hoach(a.video,a.plan,float(d["format"]["duration"]),a.tail); errors+=l; canh_bao+=c; ke_hoach={"so_doan":n}
if a.captions:
    c=json.loads(pathlib.Path(a.captions).read_text(encoding="utf-8"))
    if c.get("meta",{}).get("english_above_vietnamese") is not True: errors.append("Chưa xác nhận English ở trên Vietnamese")
    if any(not x.get("en") or not x.get("vi") for x in c.get("segments",[])): errors.append("Cue thiếu một ngôn ngữ")
print(json.dumps({"pass":not errors,"errors":errors,"canh_bao":canh_bao,"ke_hoach":ke_hoach,"probe":d},ensure_ascii=False,indent=2)); raise SystemExit(bool(errors))
