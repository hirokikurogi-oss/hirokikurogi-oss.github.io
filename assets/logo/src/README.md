# ロゴの SVG 化

元画像 `../hkwork-logo.webp`（1254px 四方）から、形を測って作り起こしたもの。

- `genlogo.py`：マーク（H・K・青い弧）と文字「HK Work」の SVG を出力する。弧は測定点に多項式を当てはめた曲線、文字は Avenir Next Bold のアウトラインを1文字ずつ元画像の位置と幅に合わせて配置
- `genfav.py`：ファビコン用の簡略版（弧なしの HK、白い角丸の下地つき）を出力する

再生成（fontTools が必要）：

    python genlogo.py <出力先> "/System/Library/Fonts/Avenir Next.ttc" 0
    python genfav.py <出力先>

元画像との一致度：マーク部分の不一致 約4%（縁の数 px）、文字部分 約9%。
