#!/usr/bin/env python3
import argparse, json, pathlib, re, subprocess

KEYWORDS={
 "official_news":["ubnd","hội đồng nhân dân","quyết định","đồng chí","bản tin","chính quyền"],
 "conference":["hội nghị","đại biểu","tuyên truyền","tập huấn","hội thảo"],
 "interview":["phỏng vấn","xin hỏi","trả lời","ông cho biết","bà cho biết"],
 "education":["bước 1","hướng dẫn","bài học","cách làm","thực hành"],
 "documentary_event":["sự kiện","hoạt động","chương trình","lễ"],
 "social_montage":["reel","shorts","tiktok","montage","viral"]}

def run(cmd): return subprocess.run(cmd,text=True,capture_output=True,check=True)
def fps_value(v):
    a,b=v.split("/"); return float(a)/float(b)
def main():
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("--transcript"); p.add_argument("--hint",default=""); p.add_argument("--out",required=True); a=p.parse_args()
    src=pathlib.Path(a.input).resolve(); out=pathlib.Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    probe=json.loads(run(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,width,height,avg_frame_rate","-of","json",str(src)]).stdout)
    video=next(s for s in probe["streams"] if s.get("codec_type")=="video"); duration=float(probe["format"]["duration"])
    scene=subprocess.run(["ffmpeg","-hide_banner","-i",str(src),"-vf","select='gt(scene,0.32)',showinfo","-f","null","-"],text=True,capture_output=True)
    scene_count=len(re.findall(r"pts_time:",scene.stderr)); shot_rate=scene_count/max(duration,0.001)
    text=a.hint
    if a.transcript: text += " "+pathlib.Path(a.transcript).read_text(encoding="utf-8",errors="ignore")
    low=text.lower(); scores={k:sum(low.count(w) for w in words) for k,words in KEYWORDS.items()}
    if max(scores.values(),default=0)==0: profile="social_montage" if shot_rate>.45 else "documentary_event"; confidence=.55
    else: profile=max(scores,key=scores.get); confidence=min(.96,.65+.06*scores[profile])
    if profile=="documentary_event" and any(x in low for x in ["xã","hội nghị","tuyên truyền"]): profile="official_news"; confidence=max(confidence,.72)
    strength="medium" if profile in ["documentary_event","education"] else ("high" if profile=="social_montage" else "low")
    plan={"analysis":{"duration":duration,"width":video["width"],"height":video["height"],"fps":fps_value(video["avg_frame_rate"]),"scene_count":scene_count,"shot_rate":round(shot_rate,3)},"classification":{"profile":profile,"confidence":round(confidence,2),"scores":scores},"editing":{"cut_authorized":False,"preserve_duration":True,"preserve_scene_order":True,"effects_strength":strength},"style":{"filter":"news_clean" if profile in ["official_news","conference"] else "natural","bilingual_captions":True,"english_above_vietnamese":True}}
    out.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8"); print(out)
if __name__=="__main__": main()
