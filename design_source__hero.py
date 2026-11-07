from design_source__lib import *

W, H = 1000, 440

def build():
    iso = Iso(556, 100, a=44, b=25.5)
    P = iso.p
    o = [svg_open(W, H, "Anima Das, AI Automation Engineer and Systems Architect",
                  "Animated isometric automation scene: data packets flow from intake through validation to an AI agent, "
                  "pause at an amber human-approval gate, then reach email, CRM and a PostgreSQL store.")]
    o.append('<defs>' + GLOW + f'''
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK2}"/></linearGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="gateGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{AMBER}" stop-opacity=".5"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".38" stop-color="#fff" stop-opacity=".12"/><stop offset=".6" stop-color="#fff"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="floorMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
.n{{animation:rise .9s cubic-bezier(.2,.8,.2,1) both}}
@keyframes rise{{from{{transform:translateY(26px);opacity:0}}to{{transform:none;opacity:1}}}}
.bob{{animation:bob 3.6s ease-in-out infinite alternate;animation-delay:1.6s}}
@keyframes bob{{from{{transform:translateY(0)}}to{{transform:translateY(-5px)}}}}
.flow{{stroke-dasharray:3 13;animation:flow 1.1s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-16}}}}
.ring{{stroke-dasharray:9 7;animation:flow 2.2s linear infinite}}
.tw{{animation:tw 4s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.7}}}}
.gate{{animation:gate 4.8s ease-in-out infinite;animation-delay:3s}}
@keyframes gate{{0%,38%,100%{{opacity:.25}}50%,62%{{opacity:1}}}}
.in{{animation:fadein 1.2s ease-out both}}
@keyframes fadein{{from{{opacity:0;transform:translateX(-10px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion: reduce){{.n,.bob,.flow,.ring,.tw,.gate,.in{{animation:none}}}}
</style>''')
    o.append(f'<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="url(#bg)"/>')
    # twinkling dust
    import random; random.seed(7)
    for i in range(22):
        x, y = random.randint(40, 980), random.randint(20, 420)
        o.append(f'<circle class="tw" cx="{x}" cy="{y}" r="{random.choice([1,1,1.4])}" fill="{TEXT}" style="animation-delay:{random.random()*4:.1f}s"/>')

    # floor grid
    g = ['<g mask="url(#floorMask)" stroke="%s" stroke-width="1" fill="none" opacity=".75">' % LINE]
    for gx in range(-1, 10):
        g.append('<polyline points="%s"/>' % iso.pts((gx, -3.2), (gx, 3.4)))
    for gy in [x * 1.0 for x in range(-3, 4)] + [3.4]:
        g.append('<polyline points="%s"/>' % iso.pts((-1, gy), (9, gy)))
    g.append('</g>'); o.append("".join(g))

    # platforms under stations
    nodes = {"intake": (0, 0), "validate": (2, 0), "agent": (4, 0), "out": (8, 0)}
    for k, (gx, gy) in nodes.items():
        o.append(iso.slab(gx, gy, 0.82 if k == "agent" else 0.66, PANEL, .92))
    o.append(iso.slab(4, 2.6, .66, PANEL, .92)); o.append(iso.slab(6, -2.5, .66, PANEL, .92)); o.append(iso.slab(8, 2.4, .66, PANEL, .92))

    # conveyor paths (floor level)
    def poly(*ps): return " ".join("%.1f,%.1f" % P(*q) for q in ps)
    def path_d(*ps): return "M" + " L".join("%.1f %.1f" % P(*q) for q in ps)
    paths = {
        "main": ((0, 0), (8, 0), CYAN),
        "db": ((4, 0), (4, 2.6), VIOLET),
        "crm": ((8, 0), (8, 2.4), CYAN),
        "human": ((6, 0), (6, -2.5), AMBER),
    }
    for k, (a, b, c) in paths.items():
        o.append(f'<polyline points="{poly(a, b)}" stroke="{dark(c, .62)}" stroke-width="9" stroke-linecap="round" fill="none" opacity=".9"/>')
        o.append(f'<polyline class="flow" points="{poly(a, b)}" stroke="{c}" stroke-width="2.4" stroke-linecap="round" fill="none"/>')

    # glow under agent + gate
    ax, ay = P(4, 0)
    o.append(f'<ellipse class="tw" cx="{ax:.1f}" cy="{ay+4:.1f}" rx="96" ry="54" fill="url(#halo)"/>')
    gx_, gy_ = P(6, 0)
    o.append(f'<ellipse class="gate" cx="{gx_:.1f}" cy="{gy_-24:.1f}" rx="88" ry="76" fill="url(#gateGlow)"/>')

    # packets (behind the cubes so they appear to enter and leave each station)
    def packet(d, dur, begin, col, r=3.6):
        return (f'<circle r="{r}" fill="{col}" filter="url(#glow)"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" '
                f'path="{d}" rotate="0"/></circle>')
    main_d = path_d((0, 0), (8, 0))
    for i in range(3):
        o.append(packet(main_d, 9, 2.2 + i * 3, CYAN))
    o.append(packet(path_d((4, 0), (4, 2.6)), 3, 3.4, VIOLET)); o.append(packet(path_d((4, 0), (4, 2.6)), 3, 6.4, VIOLET))
    o.append(packet(path_d((8, 0), (8, 2.4)), 3, 4.4, CYAN))
    o.append(packet(path_d((6, 0), (6, -2.5)), 2.4, 5.2, AMBER)); o.append(packet(path_d((6, -2.5), (6, 0)), 2.4, 7.8, AMBER))

    # stations, back to front
    def label(gx, gy, h, text, col): 
        x, y = P(gx, gy, h + 24); return pill(x, y, text, col)
    items = []
    items.append((0, 0.0, f'<g class="n" style="animation-delay:.25s">{iso.cube(0, 0, .42, 30, CYAN)}{label(0, 0, 30, "intake", CYAN)}</g>'))
    chk = iso.pts((-.2, 0, 30), (-.04, .16, 30), (.22, -.2, 30))
    items.append((2, 0.0, f'<g class="n" style="animation-delay:.5s">{iso.cube(2, 0, .42, 38, CYAN)}<polyline points="{chk.replace(" ", " ")}" fill="none"/>{label(2, 0, 38, "validate", CYAN)}</g>'))
    # fix check mark: drawn at the validate top face
    vx, vy = P(2, 0, 38)
    items[-1] = (2, 0.0, f'<g class="n" style="animation-delay:.5s">{iso.cube(2, 0, .42, 38, CYAN)}'
                         f'<polyline points="{vx-9:.1f},{vy:.1f} {vx-2:.1f},{vy+5:.1f} {vx+10:.1f},{vy-6:.1f}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
                         f'{label(2, 0, 38, "validate", CYAN)}</g>')
    agx, agy = P(4, 0, 74)
    items.append((4, 0.0, f'<g class="n" style="animation-delay:.8s"><g class="bob">{iso.cube(4, 0, .62, 74, VIOLET)}'
                          f'<ellipse class="ring" cx="{agx:.1f}" cy="{agy:.1f}" rx="26" ry="15" fill="none" stroke="{INK}" stroke-width="2.4"/>'
                          f'<circle cx="{agx:.1f}" cy="{agy:.1f}" r="4.2" fill="{INK}"/>'
                          f'{label(4, 0, 74, "ai agent", VIOLET)}</g></g>'))
    # gate: two pillars and a beam
    gate = (iso.box(5.86, 6.14, -.74, -.46, 0, 66, AMBER) + iso.box(5.86, 6.14, .46, .74, 0, 66, AMBER) +
            iso.box(5.86, 6.14, -.74, .74, 66, 78, AMBER))
    items.append((6, 0.0, f'<g class="n" style="animation-delay:1.1s">{gate}{label(6, 0, 78, "approval gate", AMBER)}</g>'))
    items.append((6, -2.5, f'<g class="n" style="animation-delay:1.3s">{iso.cube(6, -2.5, .36, 26, AMBER)}{label(6, -2.5, 26, "telegram", AMBER)}</g>'))
    items.append((8, 0.0, f'<g class="n" style="animation-delay:1.5s">{iso.cube(8, 0, .42, 32, CYAN)}{label(8, 0, 32, "gmail", CYAN)}</g>'))
    items.append((4, 2.6, f'<g class="n" style="animation-delay:1.2s">{iso.cylinder(4, 2.6, .36, 40, VIOLET)}{label(4, 2.6, 40, "postgres", VIOLET)}</g>'))
    items.append((8, 2.4, f'<g class="n" style="animation-delay:1.7s">{iso.cube(8, 2.4, .36, 24, CYAN)}{label(8, 2.4, 24, "crm", CYAN)}</g>'))
    for _, _, s in sorted(items, key=lambda t: (t[0] + t[1])):
        o.append(s)

    # text block
    f = f'font-family="{SANS}"'
    o.append(f'<g class="in" style="animation-delay:.1s">'
             f'<text x="56" y="132" {f} font-size="14.5" fill="{MUTED}">Independent consultant since 2022, based in Sylhet</text>'
             f'<text x="52" y="212" {f} font-size="76" font-weight="700" fill="{TEXT}" letter-spacing="-2">Anima Das</text>'
             f'<text x="56" y="252" {f} font-size="21" font-weight="600" fill="{CYAN}">AI Automation Engineer &amp; Systems Architect</text>'
             f'<text x="56" y="292" {f} font-size="15.5" fill="{TEXT}" fill-opacity=".86">Business workflows that validate before they act,</text>'
             f'<text x="56" y="314" {f} font-size="15.5" fill="{TEXT}" fill-opacity=".86">ask a person before consequential steps,</text>'
             f'<text x="56" y="336" {f} font-size="15.5" fill="{TEXT}" fill-opacity=".86">and recover cleanly when something fails.</text></g>')
    # legend
    lx, ly = 56, 392
    leg = [(CYAN, "data flow"), (VIOLET, "AI agent"), (AMBER, "human approval")]
    x = lx
    for c, t in leg:
        o.append(f'<rect x="{x}" y="{ly-9}" width="11" height="11" rx="3" fill="{c}"/><text x="{x+18}" y="{ly}" {f} font-size="12.5" fill="{MUTED}">{t}</text>')
        x += 18 + len(t) * 7 + 22
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{LINE}"/></g></svg>')
    return "".join(o)

if __name__ == "__main__":
    import sys; open(sys.argv[1], "w").write(build())
