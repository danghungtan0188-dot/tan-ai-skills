"""Reusable FFmpeg expressions for the seven CapCut-like feature groups."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Timed:
    start: float
    end: float
    def enable(self): return f"between(t,{self.start},{self.end})"

def text_style(name="title_clean"):
    return {
      "title_clean":{"fontcolor":"white","bordercolor":"#173B6C","borderw":4,"shadowx":3,"shadowy":3},
      "gold_impact_title":{"fontcolor":"#FFD43B","bordercolor":"#6B3300","borderw":6,"shadowx":6,"shadowy":6},
      "lower_third":{"fontcolor":"white","bordercolor":"#0B2A4A","borderw":3,"shadowx":2,"shadowy":2},
      "news_banner":{"fontcolor":"white","bordercolor":"#D71920","borderw":4,"shadowx":2,"shadowy":2},
    }.get(name,{})

def sticker_overlay(base="base", sticker="sticker", out="vout", x=40, y=40, start=0, end=10, opacity=1):
    return f"[{sticker}]format=rgba,colorchannelmixer=aa={opacity}[st];[{base}][st]overlay={x}:{y}:enable='between(t,{start},{end})'[{out}]"

def effect(name, start=0, end=1, strength=.6):
    e=Timed(start,end).enable()
    effects={
      "flash_white":f"drawbox=x=0:y=0:w=iw:h=ih:color=white@{strength}:t=fill:enable='{e}'",
      "shake":f"crop=iw-24:ih-24:12+10*sin(70*t):12+8*cos(53*t):enable='{e}',scale=iw+24:ih+24",
      "glitch_rgb":f"rgbashift=rh=8:bv=-5:enable='{e}'",
      "film_grain":f"noise=alls={max(1,int(12*strength))}:allf=t+u:enable='{e}'",
      "vignette":f"vignette=PI/{max(4,int(12-6*strength))}:enable='{e}'",
      "zoom_blur":f"gblur=sigma={max(.1,8*strength)}:enable='{e}'",
      "light_leak":f"colorbalance=rs={.12*strength}:gs={.05*strength}:bs={-.05*strength}:enable='{e}'",
    }
    return effects.get(name,"")

def filter_preset(name):
    return {
      "natural":"eq=contrast=1.03:saturation=1.03",
      "vibrant":"eq=contrast=1.08:saturation=1.15",
      "cinematic":"eq=contrast=1.08:saturation=.92,vignette=PI/7",
      "warm":"colorbalance=rs=.035:bs=-.025",
      "cool":"colorbalance=rs=-.025:bs=.035",
      "bw":"hue=s=0",
      "vintage":"eq=saturation=.82:gamma=.96,noise=alls=4:allf=t",
      "news_clean":"eq=contrast=1.04:saturation=1.04,unsharp=5:5:.25:5:5:0",
    }.get(name,"")

def adjustment(values):
    chain=[f"eq=brightness={values.get('brightness',0)}:contrast={values.get('contrast',1)}:saturation={values.get('saturation',1)}:gamma={values.get('gamma',1)}"]
    if values.get("temperature"): chain.append(f"colorbalance=rs={values['temperature']}:bs={-values['temperature']}")
    if values.get("sharpen"): chain.append(f"unsharp=5:5:{values['sharpen']}:5:5:0")
    if values.get("denoise"): chain.append(f"hqdn3d={values['denoise']}")
    if values.get("vignette"): chain.append("vignette=PI/7")
    return ",".join(chain)

def caption_filter(path):
    safe=str(path).replace("\\","\\\\").replace(":","\\:").replace("'","\\'")
    return f"subtitles='{safe}'"

def speed_video(rate): return f"setpts=PTS/{rate}"
def speed_audio(rate): return f"atempo={min(2,max(.5,rate))}"
def freeze(seconds): return f"tpad=stop_mode=clone:stop_duration={seconds}"
def ken_burns(frames=150, zoom=.0015): return f"zoompan=z='min(zoom+{zoom},1.18)':d={frames}:s=1920x1080:fps=30"
def normalize_audio(): return "loudnorm=I=-16:TP=-1.5:LRA=11"
def duck_music(threshold=.03, ratio=8): return f"sidechaincompress=threshold={threshold}:ratio={ratio}:attack=20:release=300"
