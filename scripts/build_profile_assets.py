"""Build local SVG profile graphics from an explicitly dated public snapshot."""
from datetime import date, timedelta
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/profile"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,monospace"
BG, LINE, TEXT, MUTED, ACCENT = "#0d1117", "#26303b", "#edf3f8", "#a8b6c5", "#62dbc5"

def svg(width, height, title, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>\n'

def text(x, y, value, size=20, color=TEXT, weight=400, family=FONT, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" font-family="{family}" {extra}>{escape(value)}</text>'

def frame(w,h):
    return f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{BG}" stroke="{LINE}"/>'

# Simple local link buttons: no tracking pixels or badge service dependency.
for label,width in [("Portfolio",124),("LinkedIn",122),("Eminify",114),("Email",98)]:
    body=f'<rect x=".5" y=".5" width="{width-1}" height="33" rx="7" fill="{BG}" stroke="#364453"/>'
    body+=text(15,22,label,14,TEXT,500)+text(width-24,22,"↗",14,ACCENT)
    (ASSETS/f'connect-{label.lower()}.svg').write_text(svg(width,34,label,body))

# A separate architecture sketch, keeping the supplied photographic masthead intact.
body=frame(1200,296)
body+=text(34,42,"HOW I THINK ABOUT SYSTEMS",18,MUTED,500,MONO, 'letter-spacing="1.8"')
nodes=[(34,"01","INTERFACE","Intent & interaction"),(430,"02","API","Rules & contracts"),(826,"03","DATA","State & integrity")]
for x,num,label,detail in nodes:
    stroke=ACCENT if label=="API" else "#364453"
    body+=f'<rect x="{x}" y="74" width="340" height="130" rx="12" fill="#111923" stroke="{stroke}"/>'
    body+=text(x+22,105,num,16,ACCENT,500,MONO)
    body+=text(x+22,145,label,27,TEXT,600,MONO)
    body+=text(x+22,181,detail,20,MUTED)
for x in [374,770]:
    body+=f'<path d="M{x+10} 139h34m-8-6 8 6-8 6" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
body+=f'<path d="M996 219v24H204v-24" fill="none" stroke="#435465" stroke-width="1.5" stroke-dasharray="5 6"/>'
body+=f'<rect x="408" y="229" width="384" height="28" fill="{BG}"/>'
body+=text(600,250,"OBSERVE · RECOVER · IMPROVE",17,MUTED,400,MONO,'text-anchor="middle" letter-spacing="1.2"')
(ASSETS/'system-flow.svg').write_text(svg(1200,296,"Interface to API to data, with observation, recovery and improvement",body))

# Technologies are grouped by actual use, without ratings or proficiency percentages.
body=frame(1200,234)
groups=[("PRODUCT",["TypeScript","React","Next.js","Flutter / Dart"]),
        ("SERVICES",["Node.js","NestJS","Laravel","Python"]),
        ("DELIVERY",["PostgreSQL","Redis","Docker","GitHub Actions"])]
for row,(label,items) in enumerate(groups):
    y=28+row*68
    body+=text(28,y+28,label,17,MUTED,500,MONO,'letter-spacing="1.4"')
    x=198
    for item in items:
        width=220
        body+=f'<rect x="{x}" y="{y}" width="{width}" height="44" rx="8" fill="#141e28" stroke="{LINE}"/>'
        body+=f'<circle cx="{x+18}" cy="{y+22}" r="3" fill="{ACCENT}"/>'
        body+=text(x+33,y+29,item,19,TEXT,450)
        x+=width+16
(ASSETS/'tech-stack.svg').write_text(svg(1200,234,"Product: TypeScript, React, Next.js, Flutter and Dart. Services: Node.js, NestJS, Laravel, Python. Delivery: PostgreSQL, Redis, Docker, GitHub Actions.",body))

# Public GitHub activity, deliberately a dated snapshot rather than a live claim.
data=json.loads((ROOT/'assets/activity/public-calendar-2026.json').read_text())
days=data['days']
start=date.fromisoformat(data['from'])
end=date.fromisoformat(data['to'])
week_start=start-timedelta(days=(start.weekday()+1)%7)
total=sum(d['count'] for d in days)
active=sum(d['count']>0 for d in days)
assert total==data['totalContributions']
body=frame(1200,274)
body+=text(32,40,"PUBLIC GITHUB ACTIVITY",17,MUTED,500,MONO,'letter-spacing="1.5"')
body+=text(1168,40,"1 JAN — 15 SEP 2026",17,MUTED,400,MONO,'text-anchor="end"')
body+=text(32,115,f'{total:,}',52,TEXT,600)
body+=text(34,145,"contributions displayed",17,MUTED)
body+=text(34,194,str(active),30,ACCENT,600)
body+=text(34,220,"active days",17,MUTED)
colors=["#19232d","#174d45","#247967","#38aa91","#62dbc5"]
months=set()
for day in days:
    dt=date.fromisoformat(day['date']);col=(dt-week_start).days//7;row=(dt.weekday()+1)%7
    x=294+col*22;y=90+row*21
    if dt.month not in months:
        months.add(dt.month);body+=text(x,74,dt.strftime('%b'),15,MUTED)
    body+=f'<rect x="{x}" y="{y}" width="17" height="17" rx="3" fill="{colors[day["level"]]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>'
body+=text(1168,252,"Snapshot · 15 September 2026",15,MUTED,400,FONT,'text-anchor="end"')
(ASSETS/'public-activity-2026.svg').write_text(svg(1200,274,f'Publicly displayed GitHub calendar: {total:,} contributions across {active} active days, 1 January to 15 September 2026. Dated snapshot.',body))
print('Built 7 local SVG profile graphics.')
