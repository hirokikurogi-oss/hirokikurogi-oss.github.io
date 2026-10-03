# HK Work サイト

Jekyll で作った静的サイト。GitHub Pages（`hirokikurogi-oss/hirokikurogi-oss.github.io`）で公開する。

## よく触るところ

| やりたいこと | 編集するファイル |
|---|---|
| 開発案件の受付を止める・再開する | `_config.yml` の `availability`（`open` / `closed`） |
| 稼働開始時期の表記 | `_config.yml` の `available_from` |
| スキルの年数・ツール | `_data/skills.yml` |
| 業務実績 | `_data/cases.yml` |
| サンプル記事（Zenn） | `_data/articles.yml` |
| トップページの文章 | `index.html` |
| hondana の事例ページ | `works/hondana/index.md` |
| 色・余白などの見た目 | `assets/css/main.css`（先頭の `:root` に色がまとまっている） |

## 手元で確認する

```
bundle install            # 初回だけ（vendor/bundle に入る）
LANG=en_US.UTF-8 bundle exec jekyll serve
```

http://localhost:4000 で見られる。`LANG` を付けないと、日本語のファイル名で文字コードのエラーになる。

## 公開しないもの

`構成案.md` は伏せている媒体名などを含むので、`.gitignore` と `_config.yml` の `exclude` の両方で外している。
