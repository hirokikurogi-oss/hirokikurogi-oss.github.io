# スクリーンショット配置場所

`index.html`、`works/hondana/index.md`、`works/taikyo-note/index.md`、`works/iryohi-memo/index.md` が参照するファイル。

## 本棚（hondana）

App Store に登録した画像（`~/Documents/Claude/hondana-screenshots/upload_1206x2622/`、架空の書名と自作の表紙）を 828×1800 に縮小したもの（2026-10-27 に差し替え）。

| ファイル名 | 内容 | 元のファイル |
|---|---|---|
| `01_shelf.png` | 本棚（表紙グリッド） | `01_shelf.png` |
| `03_series.png` | シリーズ詳細（抜け巻の表示） | `03_series_detail.png` |
| `04_detail.png` | 書籍詳細 | `04_book_detail.png` |

## 退去ノート

App Store に登録した画像（`~/Documents/Claude/taikyo_note/docs/screenshots/ja/`）を 414×900 に縮小したもの。

| ファイル名 | 内容 | 元のファイル |
|---|---|---|
| `taikyo_01_rooms.png` | 部屋一覧（撮影の進み具合） | `iphone_04_rooms.png` |
| `taikyo_02_compare.png` | 入居時と退去時の比較 | `iphone_03_compare.png` |
| `taikyo_03_pdf.png` | PDF の書き出し設定（`works/taikyo-note` のみ） | `iphone_07_pdf.png` |

## 医療費と交通費のメモ

`~/Documents/Claude/iryohi_memo/docs/screenshots/raw/`（見出しなしの素の画面、1206×2622）を 414×900 に縮小したもの。架空の家族・支払先のデータ。

| ファイル名 | 内容 | 元のファイル |
|---|---|---|
| `iryohi_01_home.png` | 年の合計と内訳 | `03_home.png` |
| `iryohi_02_edit.png` | 病院代と交通費の入力 | 2026-11-14 に撮り直し（`iryohi_memo/tool/demo/demo_main.dart` のデモデータ、iPhone 17 Pro のシミュレータ、1206×2622 を縮小）。ストア用の `01_edit.png` は上部が切れているため使わない |
| `iryohi_03_export.png` | 集計フォームへの書き出し | `02_export.png` |

## 配置ルール

- 縮小は `sips -z <高さ> <幅> <元> --out <先>` で行う（アスペクト比は 1206:2622 / 1320:2868 でほぼ同じ）
- 蔵書や物件が登録された状態で撮影する（空の画面では機能が伝わらない）
