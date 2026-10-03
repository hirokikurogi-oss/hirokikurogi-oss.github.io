import sys
OUT = sys.argv[1]
INK, BLUE = "#1C1F22", "#005EB8"
GAP = int(sys.argv[2]) if len(sys.argv) > 2 else 26   # 上の腕と下の脚のあいだの白い隙間（y方向）

# K の上の腕：傾き dx/dy = -1.07 の2本の平行線で挟んだ帯を、縦棒の右端 x=650 で切る
k = 1.07
def arm_x(x_top, y): return x_top - k * (y - 340)
y_l = 340 + (826 - 650) / k          # 左の線が縦棒に当たる高さ
y_r = 340 + (950 - 650) / k          # 右の線が縦棒に当たる高さ
arm = f"M826 340H950L650 {y_r:.1f}V{y_l:.1f}Z"

# K の下の脚：元ロゴの脚と同じ傾き。上端は腕の下辺から GAP だけ離す
def leg_l(y): return 685 + 0.8 * (y - 545)
def leg_r(y): return 836 + 0.86 * (y - 545)
def cut(edge):
    # edge(y) = arm_x(950, y - GAP) となる y を二分法で求める
    lo, hi = 340.0, 714.0
    for _ in range(60):
        m = (lo + hi) / 2
        if edge(m) < arm_x(950, m - GAP): lo = m
        else: hi = m
    return edge(lo), lo
lx, ly = cut(leg_l); rx, ry = cut(leg_r)
leg = f"M{rx:.1f} {ry:.1f}L{leg_r(714):.1f} 714H{leg_l(714):.1f}L{lx:.1f} {ly:.1f}Z"

body = f'''<rect x="270" y="340" width="98" height="374" fill="{INK}"/>
<rect x="368" y="497" width="184" height="71" fill="{INK}"/>
<rect x="552" y="340" width="98" height="374" fill="{INK}"/>
<path d="{arm}" fill="{INK}"/>
<path d="{leg}" fill="{BLUE}"/>'''

# マークの外接: x 270–981, y 340–714 → 正方形に余白を付けて中央に置く
cx, cy = (270 + 981) / 2, (340 + 714) / 2
side = 711 + 2 * 45
x0, y0 = cx - side / 2, cy - side / 2
bg = f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{side}" height="{side}" rx="{side*0.18:.1f}" fill="#FFFFFF"/>'
svg = lambda b: f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {side} {side}" role="img" aria-label="HK Work"><title>HK Work</title>{b}</svg>\n'
open(f"{OUT}/favicon.svg", "w").write(svg(bg + body))
# apple-touch-icon 用は角丸なし（iOS 側で丸められる）
open(f"{OUT}/apple-touch-icon.svg", "w").write(svg(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{side}" height="{side}" fill="#FFFFFF"/>' + body))
print("leg", (lx, ly), (rx, ry))
