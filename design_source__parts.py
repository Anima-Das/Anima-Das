import textwrap
from design_source__lib import *

F = f'font-family="{SANS}"'

# ---------- project cards ----------
CARDS = [
 dict(file="b2b-lead-research", color=CYAN, title="B2B Lead Research & Cold Outreach Automation",
  does="Takes leads from Google Sheets, verifies the email, researches the company from several sources and has Gemini write an evidence-based draft.",
  solves="Cold outreach that is generic, unchecked and sent without anyone reading it first.",
  value="Every email rests on cited research and a Telegram approval before Gmail sends it. One follow-up, with reply and opt-out handling.",
  tech=["n8n", "Google Gemini", "Telegram", "Gmail API", "Google Sheets"]),
 dict(file="outreach-orchestrator", color=VIOLET, title="Autonomous Outreach Intelligence & Campaign Orchestrator",
  does="Runs outreach campaigns on a PostgreSQL-backed lifecycle: 16 lead states, and each lead may only follow a permitted transition.",
  solves="Automated outreach that double-sends, skips steps or acts on an outcome it is unsure about.",
  value="Claims are verified before drafting, layered send gates guard each email, and uncertain results are held for reconciliation instead of resent.",
  tech=["n8n", "PostgreSQL", "JavaScript", "REST APIs"]),
 dict(file="voice-support-agent", color=CYAN, title="AI Customer Support & Voice Agent Automation",
  does="A webhook backend for voice agents. It routes FAQ, order status, booking, ticketing and human escalation through one structured JSON response.",
  solves="Voice agents that repeat actions or answer with information nobody verified.",
  value="HMAC-SHA256 protects order lookups, idempotency blocks duplicates, and answers not grounded in verified knowledge are rejected.",
  tech=["n8n", "PostgreSQL", "Webhooks", "HMAC-SHA256"]),
 dict(file="reputation-defense", color=AMBER, title="AI Social-Media & Brand Reputation Defense Engine",
  does="Classifies incoming social-media events and applies each tenant's own policy to decide what the system may do.",
  solves="Automated reputation responses with no signature checks, no limits and no record of what was done.",
  value="Signed, replay-protected intake, a kill switch, durable human-review tasks and PostgreSQL audit records keep actions controlled and traceable.",
  tech=["n8n", "PostgreSQL", "Event processing", "Policy controls"]),
]
ALSO = [
 dict(file="also-video-pipeline", color=VIOLET, title="Generative AI Video Pipeline",
  does="Produces cinematic short-form video with VEO 3 prompt engineering, tracks each production, and publishes to TikTok, Instagram and YouTube.",
  tech=["n8n", "VEO 3", "TikTok", "Instagram", "YouTube"]),
 dict(file="also-messenger-bot", color=CYAN, title="Messenger Support & Lead-Gen Bot",
  does="Answers customers on Facebook Messenger, qualifies leads, routes by intent, keeps customer profiles and hands over to a person when needed.",
  tech=["n8n", "OpenAI", "Messenger", "Human handoff"]),
]

def chips(x, y, tech, color, maxw):
    o, cx = [], x
    for t in tech:
        w = len(t) * 6.2 + 20
        if cx + w > x + maxw: cx, y = x, y + 28
        o.append(f'<rect x="{cx:.1f}" y="{y-15}" width="{w:.1f}" height="22" rx="11" fill="{color}" fill-opacity=".10" stroke="{color}" stroke-opacity=".45"/>'
                 f'<text x="{cx+w/2:.1f}" y="{y}" text-anchor="middle" {F} font-size="11.5" fill="{TEXT}">{esc(t)}</text>')
        cx += w + 6
    return "".join(o), y

def para(x, y, text, size, fill, wrap, lead=None, lh=None):
    lh = lh or size * 1.5
    lines = textwrap.wrap(text, wrap)
    o = []
    for i, ln in enumerate(lines):
        pre = f'<tspan font-weight="700" fill="{lead[1]}">{esc(lead[0])} </tspan>' if (lead and i == 0) else ''
        o.append(f'<text x="{x}" y="{y + i*lh:.1f}" {F} font-size="{size}" fill="{fill}">{pre}{esc(ln)}</text>')
    return "".join(o), y + len(lines) * lh

def card(c, w=480, h=322, full=True):
    col = c["color"]; iso = Iso(0, 0, a=15, b=8.7)
    o = [svg_open(w, h, c["title"], c["does"]),
         f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{PANEL}" stroke="{LINE}"/>',
         f'<rect x="0.5" y="22" width="3.5" height="46" rx="2" fill="{col}"/>']
    # small isometric motif, top right
    ix, iy = w - 52, 56
    cube = Iso(ix, iy, a=14, b=8)
    o.append(f'<g>{cube.slab(0,0,1.3,INK,1,LINE)}{cube.cube(0,0,.62,20,col)}</g>')
    y = 44
    tl = textwrap.wrap(c["title"], 34)
    for i, ln in enumerate(tl):
        o.append(f'<text x="28" y="{y + i*23}" {F} font-size="18" font-weight="700" fill="{TEXT}">{esc(ln)}</text>')
    y = y + len(tl) * 23 + 14
    p, y = para(28, y, c["does"], 13, TEXT, 56); o.append(p)
    if full:
        y += 8
        p, y = para(28, y, c["solves"], 13, MUTED, 56, lead=("Solves", col)); o.append(p)
        y += 8
        p, y = para(28, y, c["value"], 13, MUTED, 56, lead=("Value", col)); o.append(p)
    ch, _ = chips(28, h - 26, c["tech"], col, w - 48); o.append(ch)
    o.append('</svg>')
    return "".join(o)

# ---------- stack ----------
STACK = [
 ("AI & LLM", CYAN, ["OpenAI GPT-4", "Google Gemini", "Ollama (local LLMs)", "VEO 3", "Prompt engineering"]),
 ("Automation", VIOLET, ["n8n", "Make.com", "Zapier", "Webhooks", "REST APIs"]),
 ("Dev & data", CYAN, ["JavaScript (ES6)", "Python", "SQL", "PostgreSQL", "NoSQL", "JSON", "Regex"]),
 ("CRM & business", AMBER, ["HubSpot", "GoHighLevel", "Google Sheets"]),
 ("Integrations", VIOLET, ["Telegram Bot API", "Gmail API", "ZeroBounce API", "Facebook Messenger", "Serper Maps", "Git / GitHub", "Replit"]),
]
def stack():
    W = 1000; rows = []; y = 34
    for name, col, items in STACK:
        cx, line, lines = 190, [], []
        for t in items:
            w = len(t) * 7.3 + 44
            if cx + w > W - 30: lines.append(line); line, cx = [], 190
            line.append((t, cx, w)); cx += w + 10
        lines.append(line)
        rows.append((name, col, lines, y)); y += len(lines) * 46 + 14
    H = y + 6
    o = [svg_open(W, H, "Technology stack", "Tools and technologies grouped by area."),
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{PANEL}" stroke="{LINE}"/>']
    for name, col, lines, y0 in rows:
        o.append(f'<text x="30" y="{y0+17}" {F} font-size="15" font-weight="700" fill="{TEXT}">{esc(name)}</text>')
        for li, line in enumerate(lines):
            yy = y0 + li * 46
            for t, cx, w in line:
                cb = Iso(cx + 18, yy + 15, a=7, b=4)
                o.append(f'<rect x="{cx}" y="{yy}" width="{w:.1f}" height="32" rx="16" fill="{INK}" stroke="{LINE}"/>'
                         f'<g>{cb.cube(0,0,.9,9,col)}</g>'
                         f'<text x="{cx+34}" y="{yy+21}" {F} font-size="13.5" fill="{TEXT}">{esc(t)}</text>')
        if name != STACK[-1][0]:
            o.append(f'<line x1="30" x2="{W-30}" y1="{y0 + len(lines)*46 + 3}" y2="{y0 + len(lines)*46 + 3}" stroke="{LINE}" stroke-opacity=".6"/>')
    o.append('</svg>'); return "".join(o)

# ---------- principles pipeline ----------
STATIONS = [
 ("Intake", "Webhooks, forms and sheets enter through one defined door", CYAN),
 ("Validate", "Schema checks, normalising and duplicate detection", CYAN),
 ("Decide", "The model returns validated JSON, grounded in evidence", VIOLET),
 ("Approve", "A person signs off on anything consequential", AMBER),
 ("Act", "Idempotent API calls, so a retry never repeats an action", CYAN),
 ("Record", "State, audit events and reconciliation of unsure outcomes", SLATE),
]
def pipeline():
    W, H, dur = 1000, 250, 12
    xs = [96 + i * 162 for i in range(6)]
    iso = Iso(0, 0, a=18, b=10.4)
    o = [svg_open(W, H, "How the workflows I build run", "Six stages: intake, validate, decide, approve, act, record. A data packet moves through them in order."),
         '<defs>' + GLOW + '</defs>',
         '<style>.lit{opacity:0;animation:lit %ss ease-in-out infinite}@keyframes lit{0%%{opacity:0}4%%{opacity:1}16%%{opacity:0}100%%{opacity:0}}'
         '@media (prefers-reduced-motion: reduce){.lit{animation:none;opacity:.4}}</style>' % dur,
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{PANEL}" stroke="{LINE}"/>']
    y0 = 78
    o.append(f'<line x1="40" x2="960" y1="{y0}" y2="{y0}" stroke="{dark(CYAN,.6)}" stroke-width="7" stroke-linecap="round"/>')
    o.append(f'<line x1="40" x2="960" y1="{y0}" y2="{y0}" stroke="{CYAN}" stroke-width="2" stroke-dasharray="3 13" stroke-linecap="round" opacity=".8"><animate attributeName="stroke-dashoffset" from="0" to="-16" dur="1.1s" repeatCount="indefinite"/></line>')
    for i, (t, d, col) in enumerate(STATIONS):
        x = xs[i]; frac = (x - 40) / 920; delay = max(0, frac * dur - 0.35)
        st = Iso(x, y0 + 6, a=18, b=10.4)
        if col == AMBER:
            body = st.box(-.95, -.55, -.9, .9, 0, 40, col) if False else (st.box(-.3, .3, -1.05, -.62, 0, 36, col) + st.box(-.3, .3, .62, 1.05, 0, 36, col) + st.box(-.3, .3, -1.05, 1.05, 36, 44, col))
        else:
            body = st.cube(0, 0, .9, 26, col)
        o.append(f'<ellipse class="lit" cx="{x}" cy="{y0+4}" rx="52" ry="28" fill="{col}" fill-opacity=".28" style="animation-delay:{delay:.2f}s"/>')
        o.append(f'<g>{body}</g>')
        o.append(f'<text x="{x}" y="156" text-anchor="middle" {F} font-size="16" font-weight="700" fill="{TEXT}">{t}</text>')
        for li, ln in enumerate(textwrap.wrap(d, 24)):
            o.append(f'<text x="{x}" y="{178 + li*17}" text-anchor="middle" {F} font-size="12.2" fill="{MUTED}">{esc(ln)}</text>')
    o.append(f'<circle r="4.2" fill="{CYAN}" filter="url(#glow)"><animateMotion dur="{dur}s" repeatCount="indefinite" path="M40 {y0} L960 {y0}"/></circle>')
    o.append('</svg>'); return "".join(o)

# ---------- buttons / status / divider / footer ----------
def button(text, color, w):
    cb = Iso(26, 21, a=7, b=4)
    return (svg_open(w, 42, text) + f'<rect x=".5" y=".5" width="{w-1}" height="41" rx="21" fill="{PANEL}" stroke="{LINE}"/>'
            f'<g>{cb.cube(0,0,1,10,color)}</g><text x="44" y="26" {F} font-size="14" font-weight="600" fill="{TEXT}">{esc(text)}</text></svg>')

def status():
    w = 290
    return (svg_open(w, 42, "Open to full-time remote roles") +
            '<style>.pulse{transform-box:fill-box;transform-origin:center;animation:p 2.2s ease-out infinite}@keyframes p{0%{transform:scale(.6);opacity:.9}100%{transform:scale(2.6);opacity:0}}@media (prefers-reduced-motion: reduce){.pulse{animation:none;opacity:.3}}</style>'
            f'<rect x=".5" y=".5" width="{w-1}" height="41" rx="21" fill="{PANEL}" stroke="{AMBER}" stroke-opacity=".55"/>'
            f'<circle class="pulse" cx="24" cy="21" r="5" fill="{AMBER}"/><circle cx="24" cy="21" r="5" fill="{AMBER}"/>'
            f'<text x="42" y="26" {F} font-size="14" font-weight="600" fill="{TEXT}">Open to full-time remote roles</text></svg>')

def divider():
    return (svg_open(1000, 24, "Section divider") + f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{LINE}" stop-opacity="0"/><stop offset=".5" stop-color="{LINE}"/><stop offset="1" stop-color="{LINE}" stop-opacity="0"/></linearGradient>{GLOW}</defs>'
            f'<rect x="40" y="11.5" width="920" height="1.5" fill="url(#g)"/>'
            f'<circle r="3" cy="12" fill="{AMBER}" filter="url(#glow)"><animate attributeName="cx" values="120;880;120" dur="14s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1" keyTimes="0;.5;1"/></circle></svg>')

def footer():
    W, H = 1000, 150
    st = Iso(0, 0, a=18, b=10.4)
    gate = st.box(-.3, .3, -1.05, -.62, 0, 36, AMBER) + st.box(-.3, .3, .62, 1.05, 0, 36, AMBER) + st.box(-.3, .3, -1.05, 1.05, 36, 44, AMBER)
    return (svg_open(W, H, "Open to full-time remote roles in AI automation") + '<defs>' + GLOW + f'<linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK2}"/></linearGradient></defs>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="url(#bg)" stroke="{LINE}"/>'
            f'<line x1="40" x2="960" y1="100" y2="100" stroke="{dark(CYAN,.6)}" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="40" x2="960" y1="100" y2="100" stroke="{CYAN}" stroke-width="2" stroke-dasharray="3 13" stroke-linecap="round"><animate attributeName="stroke-dashoffset" from="0" to="-16" dur="1.1s" repeatCount="indefinite"/></line>'
            f'<g transform="translate(884 106)">{gate}</g>'
            f'<text x="40" y="52" {F} font-size="22" font-weight="700" fill="{TEXT}">Open to full-time remote roles in AI automation and workflow engineering.</text>'
            f'<text x="40" y="128" {F} font-size="13.5" fill="{MUTED}">Contact links are at the top of this page.</text>'
            f'<circle r="4" cy="100" fill="{CYAN}" filter="url(#glow)"><animate attributeName="cx" values="40;876;876;960" keyTimes="0;.55;.7;1" dur="7s" repeatCount="indefinite"/><animate attributeName="fill" values="{CYAN};{CYAN};{AMBER};{CYAN}" keyTimes="0;.55;.7;1" dur="7s" repeatCount="indefinite"/></circle></svg>')
