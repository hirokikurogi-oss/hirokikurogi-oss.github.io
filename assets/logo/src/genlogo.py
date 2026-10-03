import sys, os
from fontTools.ttLib import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

OUT = sys.argv[1]
FONT_FILE, FONT_IDX = sys.argv[2], int(sys.argv[3])
INK, BLUE = "#1C1F22", "#005EB8"

# ---- 弧の当てはめ（端点固定の3次ベジェ、最小二乗） ----
U = [(280,707),(310,673),(340,646),(370,623),(400,604),(430,585),(460,568),(490,553),(520,539),(550,525),(580,513),(610,501),(640,490),(670,479),(700,468),(730,458),(760,449),(790,441),(820,434),(850,427),(880,422),(910,418),(940,416),(970,414),(1000,414),(1030,414),(1060,416)]
L = [(280,724),(310,703),(340,684),(370,665),(400,647),(430,631),(460,615),(490,601),(520,587),(550,574),(580,562),(610,550),(640,540),(670,526),(700,510),(730,496),(760,482),(790,470),(820,460),(850,451),(880,442),(910,437),(940,431),(970,426),(1000,423),(1030,420),(1060,419)]
T0, T1 = (261, 737), (1100, 417)

def spline(pts):
    """測定点をすべて通る Catmull-Rom 曲線を 3 次ベジェの C コマンド列にする"""
    P = pts
    out = []
    for i in range(len(P) - 1):
        p0 = P[i-1] if i > 0 else P[i]
        p1, p2 = P[i], P[i+1]
        p3 = P[i+2] if i + 2 < len(P) else P[i+1]
        c1 = (p1[0] + (p2[0]-p0[0])/6, p1[1] + (p2[1]-p0[1])/6)
        c2 = (p2[0] - (p3[0]-p1[0])/6, p2[1] - (p3[1]-p1[1])/6)
        out.append(f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    return "".join(out)

def sh(pts, dy): return [(x, y + dy) for x, y in pts]
def polyfit(pts, deg=5, tipw=30.0):
    """端点（先端）を重く見た重み付き最小二乗で y=多項式(x) を当てはめる"""
    data = [(T0[0], T0[1], tipw)] + [(x, y, 1.0) for x, y in pts] + [(T1[0], T1[1], tipw)]
    n = deg + 1
    A = [[0.0]*n for _ in range(n)]; r = [0.0]*n
    for x, y, w in data:
        t = (x - 680) / 420
        v = [t**k for k in range(n)]
        for i in range(n):
            r[i] += w*v[i]*y
            for j in range(n): A[i][j] += w*v[i]*v[j]
    for i in range(n):  # ガウスの消去法
        piv = max(range(i, n), key=lambda k: abs(A[k][i])); A[i], A[piv] = A[piv], A[i]; r[i], r[piv] = r[piv], r[i]
        for k in range(i+1, n):
            m = A[k][i]/A[i][i]
            for j in range(i, n): A[k][j] -= m*A[i][j]
            r[k] -= m*r[i]
    c = [0.0]*n
    for i in reversed(range(n)):
        c[i] = (r[i] - sum(A[i][j]*c[j] for j in range(i+1, n))) / A[i][i]
    return lambda x: sum(c[k]*((x-680)/420)**k for k in range(n))

fu, fl = polyfit(U), polyfit(L)
XS = [T0[0]] + list(range(280, 1100, 20)) + [T1[0]]
UP = [T0] + [(x, fu(x)) for x in XS[1:-1]] + [T1]
LP = [T0] + [(x, fl(x)) for x in XS[1:-1]] + [T1]
print("最大誤差 U", max(abs(fu(x)-y) for x, y in U), "L", max(abs(fl(x)-y) for x, y in L))
f = lambda p: f"{p[0]:.1f} {p[1]:.1f}"
GAP_UP, GAP_DOWN = 21, 23
GAPS = [(261,30),(280,29),(340,23),(400,22),(520,22),(640,21),(820,18),(900,17),(1100,17)]
def gap_at(x):
    for (x0,g0),(x1,g1) in zip(GAPS, GAPS[1:]):
        if x0 <= x <= x1: return g0 + (g1-g0)*(x-x0)/(x1-x0)
    return GAPS[-1][1]
G = [(x, y - gap_at(x)) for x, y in UP]; D = sh(LP, GAP_DOWN)
Gr, Lr, Dr = G[::-1], LP[::-1], D[::-1]

defs = f'''<defs>
<clipPath id="above"><path d="M0 0H1254V{Gr[0][1]:.1f}L{f(Gr[0])}{spline(Gr)}L0 {G[0][1]:.1f}Z"/></clipPath>
<clipPath id="below"><path d="M0 1254H1254V{Lr[0][1]:.1f}L{f(Lr[0])}{spline(Lr)}L0 {LP[0][1]:.1f}Z"/></clipPath>
<clipPath id="belowgap"><path d="M0 1254H1254V{Dr[0][1]:.1f}L{f(Dr[0])}{spline(Dr)}L0 {D[0][1]:.1f}Z"/></clipPath>
</defs>'''

mark = f'''<g clip-path="url(#above)" fill="{INK}">
<rect x="270" y="340" width="98" height="374"/>
<rect x="368" y="497" width="184" height="71"/>
<rect x="552" y="340" width="98" height="374"/>
<path d="M826 340H950L762 520H628Z"/>
</g>
<rect clip-path="url(#below)" fill="{INK}" x="552" y="340" width="98" height="374"/>
<path clip-path="url(#belowgap)" fill="{BLUE}" d="M601 440H746L981 714H820Z"/>
<path fill="{BLUE}" d="M{f(T0)}{spline(UP)}{spline(Lr)}Z"/>'''

# ---- 文字（フォントのアウトラインを図形化） ----
font = TTCollection(FONT_FILE).fonts[FONT_IDX]
gs = font.getGlyphSet(); cmap = font.getBestCmap(); hmtx = font['hmtx']
upm = font['head'].unitsPerEm
cap = font['OS/2'].sCapHeight
TEXT = "HK Work"
CAP_PX, BASE, LEFT, RIGHT = 125, 922, 225, 1033
s = CAP_PX / cap
# 元画像で測った各文字の左右端に、1文字ずつ合わせて置く（高さはキャップハイトで固定）
TARGETS = [('H',225,343),('K',373,498),('W',547,733),('o',735,841),('r',859,918),('k',936,1033)]
pen = SVGPathPen(gs)
for ch, a, b_ in TARGETS:
    g = cmap[ord(ch)]
    bp = BoundsPen(gs); gs[g].draw(bp); x0, _, x1, _ = bp.bounds
    sx = (b_ - a) / (x1 - x0)
    gs[g].draw(TransformPen(pen, (sx, 0, 0, -s, a - x0*sx, BASE)))
track = 0
word = f'<path fill="{INK}" d="{pen.getCommands()}"/>'

def svg(vb, body, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}"><title>{title}</title>{defs}{body}</svg>\n'

os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/full_1254.svg","w").write(svg("0 0 1254 1254", mark+word, "HK Work"))
open(f"{OUT}/hkwork-logo.svg","w").write(svg("200 300 920 660", mark+word, "HK Work"))
open(f"{OUT}/hkwork-mark.svg","w").write(svg("250 325 870 430", mark, "HK Work"))
print("track", round(track,1), "font", font['name'].getDebugName(4))
