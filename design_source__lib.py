"""Shared helpers for the profile assets: palette, isometric projection, primitives."""
import html, math

INK = "#080D1C"; INK2 = "#0E1630"; PANEL = "#111B38"; LINE = "#26345F"
TEXT = "#E8ECFF"; MUTED = "#93A0C8"
CYAN = "#4CC9F0"; VIOLET = "#8B7CFF"; AMBER = "#FFB547"; SLATE = "#6F83B8"
SANS = "Inter, 'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

def esc(s): return html.escape(s, quote=True)

def _rgb(h): h = h.lstrip('#'); return [int(h[i:i+2], 16) for i in (0, 2, 4)]
def mix(a, b, t):
    x, y = _rgb(a), _rgb(b)
    return '#%02x%02x%02x' % tuple(round(x[i] + (y[i] - x[i]) * t) for i in range(3))
def dark(c, t): return mix(c, "#04060f", t)
def light(c, t): return mix(c, "#ffffff", t)

class Iso:
    """Isometric projection: grid (gx, gy, z) -> screen (x, y)."""
    def __init__(self, ox, oy, a=44, b=25.5): self.ox, self.oy, self.a, self.b = ox, oy, a, b
    def p(self, gx, gy, z=0): return (self.ox + (gx - gy) * self.a, self.oy + (gx + gy) * self.b - z)
    def pts(self, *ps): return " ".join("%.1f,%.1f" % self.p(*q) for q in ps)

    def box(self, x0, x1, y0, y1, z0, z1, col, opacity=1, stroke=None):
        top, left, right = light(col, .22), dark(col, .30), dark(col, .52)
        st = ' stroke="%s" stroke-width="0.8" stroke-linejoin="round"' % (stroke or dark(col, .6))
        o = ' opacity="%s"' % opacity if opacity != 1 else ''
        return ('<g%s>'
                '<polygon points="%s" fill="%s"%s/>'
                '<polygon points="%s" fill="%s"%s/>'
                '<polygon points="%s" fill="%s"%s/></g>') % (
            o,
            self.pts((x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)), left, st,
            self.pts((x1, y0, z1), (x1, y1, z1), (x1, y1, z0), (x1, y0, z0)), right, st,
            self.pts((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)), top, st)

    def cube(self, gx, gy, s, h, col, **kw): return self.box(gx - s, gx + s, gy - s, gy + s, 0, h, col, **kw)

    def slab(self, gx, gy, s, col, fill_op=1, stroke=LINE, z=0):
        return '<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="1" stroke-linejoin="round"/>' % (
            self.pts((gx - s, gy - s, z), (gx + s, gy - s, z), (gx + s, gy + s, z), (gx - s, gy + s, z)), col, fill_op, stroke)

    def cylinder(self, gx, gy, r, h, col):
        cx, cy = self.p(gx, gy, 0); rx, ry = r * math.sqrt(2) * self.a, r * math.sqrt(2) * self.b
        top = cy - h
        s = ['<path d="M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 0 %.1f %.1f L%.1f %.1f Z" fill="%s" stroke="%s" stroke-width="0.8"/>' % (
            cx - rx, top, cx - rx, cy, rx, ry, cx + rx, cy, cx + rx, top, dark(col, .38), dark(col, .6))]
        for k in (1, 2):
            yy = top + (cy - top) * k / 3
            s.append('<path d="M%.1f %.1f A%.1f %.1f 0 0 0 %.1f %.1f" fill="none" stroke="%s" stroke-width="1.2" opacity=".7"/>' % (
                cx - rx, yy, rx, ry, cx + rx, yy, light(col, .15)))
        s.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="0.8"/>' % (cx, top, rx, ry, light(col, .22), dark(col, .5)))
        return "".join(s)

def pill(x, y, text, color, size=10.5, anchor="middle"):
    w = len(text) * size * 0.62 + 16
    x0 = x - w / 2 if anchor == "middle" else x
    return ('<g><rect x="%.1f" y="%.1f" width="%.1f" height="20" rx="10" fill="%s" fill-opacity=".88" stroke="%s" stroke-opacity=".7"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-family="%s" font-size="%s" fill="%s">%s</text></g>') % (
        x0, y - 14, w, INK, color, x0 + w / 2, y, MONO, size, color, esc(text))

def svg_open(w, h, title, desc=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-labelledby="t d">'
            '<title id="t">%s</title><desc id="d">%s</desc>') % (w, h, w, h, esc(title), esc(desc))

GLOW = ('<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3.2" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
