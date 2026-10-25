# Original lace envelope artwork for the Dani Hill e-card (procedurally drawn).
import math, random
R = random.Random(11)
f = lambda v: f"{v:.1f}"

STYLE = """<style>
.lf{fill:#FCF7EC;fill-opacity:.78;stroke:#FFFDF8;stroke-width:.55}
.ln{fill:url(#net2);stroke:#FFFBF2;stroke-width:1.1}
.lo{fill:none;stroke:#E4D6BB;stroke-width:.45}
.cord{fill:none;stroke:#FFFBF2;stroke-linecap:round;stroke-linejoin:round}
.thin{fill:none;stroke:#FFFBF2;stroke-width:.8}
.dot{fill:#FFFCF5}
.hole{fill:none;stroke:#FFFBF2;stroke-width:.9}
</style>"""

def petal(r, w):
    return f"M0,0 C{f(w)},{f(-r*.35)} {f(w*.9)},{f(-r*.92)} 0,{f(-r)} C{f(-w*.9)},{f(-r*.92)} {f(-w)},{f(-r*.35)} 0,0Z"

DEFS = f"""<defs>{STYLE}
<pattern id="tulle" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0,0 L7,7 M7,0 L0,7" stroke="#F8F0E0" stroke-opacity=".55" stroke-width=".45"/></pattern>
<pattern id="net2" width="5" height="4.4" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.2" r="1.45" fill="none" stroke="#FFFBF2" stroke-opacity=".8" stroke-width=".55"/></pattern>
<linearGradient id="paperP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EADCC3"/><stop offset="1" stop-color="#DCC9A8"/></linearGradient>
<linearGradient id="paperF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2E8D5"/><stop offset="1" stop-color="#E8DABF"/></linearGradient>
<filter id="relief" x="-2%" y="-2%" width="104%" height="104%">
  <feGaussianBlur in="SourceAlpha" stdDeviation=".7" result="b"/><feOffset in="b" dx=".9" dy="1.5" result="o"/>
  <feFlood flood-color="#5A4026" flood-opacity=".42"/><feComposite in2="o" operator="in" result="sh"/>
  <feMerge><feMergeNode in="sh"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="drop" x="-5%" y="-5%" width="110%" height="120%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="5" result="b"/><feOffset in="b" dy="5" result="o"/>
  <feFlood flood-color="#4A3726" flood-opacity=".38"/><feComposite in2="o" operator="in" result="sh"/>
  <feMerge><feMergeNode in="sh"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<g id="fl">{''.join(f'<path class="lf" d="{petal(10,5.4)}" transform="rotate({72*k})"/>' for k in range(5))}
 {''.join(f'<path class="lo" d="{petal(6.4,3)}" transform="rotate({72*k})"/>' for k in range(5))}
 <circle class="lf" r="2.4"/>{''.join(f'<circle class="dot" r=".55" cx="{f(3.7*math.cos(k*math.pi/4))}" cy="{f(3.7*math.sin(k*math.pi/4))}"/>' for k in range(8))}
 {''.join(f'<circle class="dot" r=".85" cx="{f(11.4*math.sin(math.radians(72*k)))}" cy="{f(-11.4*math.cos(math.radians(72*k)))}"/>' for k in range(5))}</g>
<g id="fs">{''.join(f'<circle class="lf" r="2.3" cx="{f(2.9*math.sin(math.radians(72*k)))}" cy="{f(-2.9*math.cos(math.radians(72*k)))}"/>' for k in range(5))}<circle class="lo" r="1.1" style="fill:#E9DCC3"/></g>
<g id="lv"><path class="lf" d="M0,0 C3,-3.8 7,-3.4 10,0 C7,3.4 3,3.8 0,0Z"/><path class="lo" d="M1.2,0 L8.6,0"/></g>
<g id="bd"><path class="lf" d="M0,0 C2.6,-2 2.4,-6 0,-8.5 C-2.4,-6 -2.6,-2 0,0Z"/><path class="lo" d="M0,-1 L0,-6.5"/></g>
</defs>"""

def use(id_, x, y, rot=0, s=1):
    return f'<use href="#{id_}" transform="translate({f(x)} {f(y)}) rotate({f(rot)}) scale({s:.2f})"/>'

def vine(out, x, y, ang, length, w, depth):
    seg = 6; n = max(3, int(length/seg)); pts = [(x, y)]; curv = R.uniform(-.05, .05)
    for _ in range(n):
        ang += curv + R.uniform(-.035, .035); x += seg*math.cos(ang); y += seg*math.sin(ang); pts.append((x, y))
    out.append(f'<path class="cord" stroke-width="{f(w)}" d="M' + ' L'.join(f"{f(a)},{f(b)}" for a, b in pts) + '"/>')
    side = 1
    for i in range(2, n, 2):
        px, py = pts[i]; a = math.atan2(py-pts[i-1][1], px-pts[i-1][0])
        if R.random() < .85:
            out.append(use('lv', px, py, math.degrees(a + side*.8), w*1.15*R.uniform(.8, 1.15)))
        side *= -1
        r = R.random()
        if depth > 0 and r < .3 and i < n-3:
            vine(out, px, py, a + side*R.uniform(.55, .95), length*R.uniform(.35, .55), w*.72, depth-1)
        elif r < .42:
            out.append(use('fs', px + side*6*math.cos(a+1.57), py + side*6*math.sin(a+1.57), 0, w*1.0))
    ex, ey = pts[-1]; a = math.degrees(ang)
    if R.random() < .6: out.append(use('fl', ex, ey, R.uniform(0, 72), w*1.15))
    else:
        for k in (-35, 0, 35): out.append(use('bd', ex, ey, a + 90 + k, w*1.05))

def band(out, A, B, bw, scallop=0, sc_len=26, motif=True):
    (ax, ay), (bx, by) = A, B; dx, dy = bx-ax, by-ay; L = math.hypot(dx, dy)
    ux, uy = dx/L, dy/L; nx, ny = uy, -ux          # outward normal
    ix, iy = -nx, -ny                               # inward
    P = lambda t, o: (ax + ux*t + ix*o, ay + uy*t + iy*o)
    poly = [P(0, 0), P(L, 0), P(L, bw), P(0, bw)]
    out.append('<path fill="url(#net2)" d="M' + ' L'.join(f"{f(a)},{f(b)}" for a, b in poly) + 'Z"/>')
    for o, sw in ((0, 1.7), (bw, 1.7), (bw-4, .7), (4, .7)):
        a1, a2 = P(0, o), P(L, o)
        out.append(f'<path class="cord" stroke-width="{sw}" d="M{f(a1[0])},{f(a1[1])} L{f(a2[0])},{f(a2[1])}"/>')
    if motif:
        k = int(L/24)
        for i in range(k):
            t = (i+.5)*L/k; x, y = P(t, bw/2)
            if i % 2 == 0: out.append(use('fs', x, y, 0, bw/16))
            else:
                out.append(f'<circle class="hole" r="{f(bw*.12)}" cx="{f(x)}" cy="{f(y)}"/>')
                ang = math.degrees(math.atan2(uy, ux))
                out.append(use('lv', x, y, ang+20, bw/26)); out.append(use('lv', x, y, ang+200, bw/26))
    if scallop:
        k = max(1, round(L/sc_len)); step = L/k; d = []
        for i in range(k):
            p0 = P(i*step, 0); p1 = P((i+1)*step, 0); m = P((i+.5)*step, 0)
            c = (m[0]+nx*scallop*2, m[1]+ny*scallop*2)
            d.append(f"M{f(p0[0])},{f(p0[1])} Q{f(c[0])},{f(c[1])} {f(p1[0])},{f(p1[1])}")
            ci = (m[0]+nx*scallop*1.2, m[1]+ny*scallop*1.2)
            out.append(f'<path class="thin" d="M{f(p0[0]+ux*step*.18)},{f(p0[1]+uy*step*.18)} Q{f(ci[0])},{f(ci[1])} {f(p1[0]-ux*step*.18)},{f(p1[1]-uy*step*.18)}"/>')
            for j, q in ((-1, .25), (0, .5), (1, .75)):
                t = (i+q)*step; bx_, by_ = P(t, 0); h = scallop*(1.0 if j == 0 else .78) + 3.2
                out.append(f'<circle class="dot" r="1.15" cx="{f(bx_+nx*h)}" cy="{f(by_+ny*h)}"/>')
        out.append(f'<path class="lf" style="fill-opacity:.55" d="' + ' '.join(d) + ' Z"/>')
        out.append(f'<path class="cord" stroke-width="1.5" d="' + ' '.join(d) + '"/>')

def rosette(out, cx, cy, r):
    g = [f'<g transform="translate({f(cx)} {f(cy)})">']
    n = 18
    for k in range(n):
        g.append(f'<path class="ln" d="{petal(r*.36, r*.15)}" transform="rotate({360*k/n}) translate(0 {f(-r*.62)})"/>')
        g.append(f'<path class="lo" d="{petal(r*.22, r*.08)}" transform="rotate({360*k/n}) translate(0 {f(-r*.66)})"/>')
        a = math.radians(360*k/n)
        g.append(f'<circle class="dot" r="1.4" cx="{f((r*1.02)*math.sin(a))}" cy="{f(-(r*1.02)*math.cos(a))}"/>')
    g.append(f'<circle fill="url(#net2)" r="{f(r*.62)}"/><circle class="cord" stroke-width="1.8" r="{f(r*.62)}"/>')
    for k in range(8):
        g.append(f'<path class="ln" d="{petal(r*.5, r*.19)}" transform="rotate({45*k+22.5})"/>')
        g.append(f'<path class="lo" d="{petal(r*.32, r*.1)}" transform="rotate({45*k+22.5})"/>')
    g.append(use('fl', 0, 0, 0, r*.028*10/10*1.0*1.6) if False else f'<use href="#fl" transform="scale({r*.026:.2f})"/>')
    g.append('</g>'); out += g

def mirror(inner, cx):
    return f'<g id="m{id(inner)}">{inner}</g><g transform="translate({2*cx} 0) scale(-1 1)">{inner}</g>'

# ---------------- POCKET 1200x800 ----------------
W, H = 1200, 800
out = []
out.append(f'<rect width="{W}" height="{H}" fill="url(#paperP)"/><rect width="{W}" height="{H}" fill="url(#tulle)"/>')
lace = []
# side flaps (left; mirrored to right)
left = []
for (x, y, a, L) in [(30, 400, -.35, 330), (30, 420, .32, 320), (30, 190, -.05, 220), (30, 630, .1, 230), (30, 300, -.55, 170), (30, 520, .45, 170), (30, 110, .05, 140), (30, 720, .05, 140)]:
    vine(left, x, y, a, L, 1.35, 3)
lace.append('<clipPath id="cl"><path d="M28,0 L590,400 L28,790Z"/></clipPath>')
lace.append(mirror(f'<g clip-path="url(#cl)">{"".join(left)}</g>', 600))
# bottom flap
bot = []
for (x, y, a, L) in [(600, 780, -math.pi/2, 300), (520, 780, -1.85, 280), (420, 780, -2.05, 240), (300, 780, -2.35, 180), (180, 780, -2.6, 120)]:
    vine(bot, x, y, a, L, 1.4, 3)
lace.append('<clipPath id="cb"><path d="M40,782 L600,412 L1160,782Z"/></clipPath>')
lace.append(mirror(f'<g clip-path="url(#cb)">{"".join(bot)}</g>', 600))
# borders + seams
b = []
band(b, (12, 788), (12, 12), 22, motif=True)
band(b, (1188, 788), (12, 788), 22, motif=True)
band(b, (1188, 12), (1188, 788), 22, motif=True)
band(b, (0, 800), (600, 400), 20, scallop=7, sc_len=22)
band(b, (600, 400), (1200, 800), 20, scallop=7, sc_len=22)
b.append('<path class="cord" stroke-width="2.2" d="M0,5 L600,421 L1200,5"/>')
lace.append(''.join(b))
out.append(f'<g filter="url(#relief)">{"".join(lace)}</g>')
pocket = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*2}" height="{H*2}">{DEFS}{"".join(out)}</svg>'

# ---------------- FLAP 1200x560 (body to y≈424, rosette hangs below) ----------------
FH = 560; TIP = (600, 424); TL = (14, 0); TR = (1186, 0)
fo = []
body = f"M0,0 L1200,0 L{TR[0]},0 L{TIP[0]},{TIP[1]} L{TL[0]},0Z"
fl = []
fl.append(f'<path d="{body}" fill="url(#paperF)"/><path d="{body}" fill="url(#tulle)"/>')
lace = []
half = []
for (x, y, a, L) in [(600, 14, math.pi/2+.55, 360), (430, 12, math.pi/2+.4, 270), (320, 10, math.pi/2+.35, 200), (200, 10, math.pi/2+.3, 120), (600, 14, math.pi/2, 260), (520, 12, math.pi/2+.15, 230)]:
    vine(half, x, y, a, L, 1.4, 3)
lace.append('<clipPath id="cf"><path d="M70,8 L1130,8 L600,370Z"/></clipPath>')
lace.append(mirror(f'<g clip-path="url(#cf)">{"".join(half)}</g>', 600))
b = []
band(b, TR, TIP, 30, scallop=10, sc_len=27)
band(b, TIP, TL, 30, scallop=10, sc_len=27)
band(b, (1200, 4), (0, 4), 14, motif=False)
lace.append(''.join(b))
rosette(lace, 600, 418, 112)
fl.append(f'<g filter="url(#relief)">{"".join(lace)}</g>')
fo.append(f'<g filter="url(#drop)">{"".join(fl)}</g>')
flap = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {FH}" width="2400" height="{FH*2}">{DEFS}{"".join(fo)}</svg>'

open('/home/claude/lace/pocket.svg', 'w').write(pocket)
open('/home/claude/lace/flap.svg', 'w').write(flap)
print(len(pocket)//1024, len(flap)//1024, 'KB svg')
