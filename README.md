# 中橋季刊 2026秋季號

中華民國橋藝協會《中橋季刊》2026年秋季號，雜誌級排版製作專案。

## 內容結構

封面 → 目錄 → 焦點快訊 → 橋海漫遊（人物專訪、牌局賞析、旅人筆記、經典重刊）→ **世青賽專題**（合肥世界青年橋牌錦標賽選手心得與教練講評）→ 橋藝教室（叫牌系統研究）→ 橋訊公告 → 版權頁。

## 目錄結構

```
output/     成品檔案（最終交付物）
  ├─ 中橋季刊_2026秋季號.pdf     雜誌級 PDF（雙欄排版、深藍／酒紅主題，70頁）
  ├─ 中橋季刊_2026秋季號.pages   原生 Apple Pages 檔（可編輯）
  └─ 中橋季刊_2026秋季號.docx    Word 檔（.pages 轉存前的中間檔，亦可獨立使用）

src/        排版與內容處理程式
  ├─ docx_parser.py       解析來源 .docx，依文件順序擷取段落／標題／圖片，
  │                       並將表格自動分類為「手牌圖」「叫牌過程」「一般表格」
  │                       （直接讀取 Word XML，正確還原 Symbol 字型花色符號與
  │                       textbox 標題，避免人工謄打橋牌牌局造成的錯誤）
  ├─ spingold_fix.py      將史賓果投稿一文中以純文字（S/H/D/C字母＋換行）
  │                       呈現的手牌，重建為與其他文章一致的結構化格式
  ├─ renderers.py         內容區塊 → HTML／CSS 渲染器（手牌羅盤圖、叫牌表、
  │                       名次名單表等元件）
  ├─ renderers_docx.py    內容區塊 → python-docx 渲染器（同上功能之 Word 版本）
  ├─ generate_magazine.py 組裝完整雜誌 HTML（封面／目錄／各章節／版權頁）
  ├─ generate_docx.py     組裝完整雜誌 .docx
  ├─ magazine.css         雜誌視覺主題（深藍酒紅配色、雙欄排版、手牌圖樣式）
  ├─ render_pdf.js        以 Puppeteer（無頭 Chrome）將 HTML 印製為高解析 PDF
  └─ essays.json          世青賽專題：16位選手／家長心得原文、文學潤飾版、
                          教練講評（原創寫作內容）

content/    由來源文件解析出的結構化內容（JSON），可重新產生雜誌而不需原始檔案
media/      內文所使用之圖片（自來源 .docx 擷取）
```

## 如何重新產生

```bash
# 產生 PDF
cd src
python3 generate_magazine.py        # 輸出 magazine.html
node render_pdf.js magazine.html output.pdf

# 產生 docx（可再用 Pages 開啟另存為 .pages）
python3 generate_docx.py
```

需求：Python 3（`python-docx`、`Pillow`）、Node.js（`puppeteer`，執行 `npm install puppeteer`）。

## 說明

- 橋牌牌局資料（手牌、叫牌過程）皆以程式直接讀取來源 `.docx` 的 XML 結構取得，
  未經人工謄打，以確保牌局數值正確無誤。
- 世青賽專題的心得潤飾與教練講評為原創撰寫內容，基於選手／家長問卷原始回覆
  改寫為適合刊登之雜誌文字，並附上對應之帶隊教練觀點講評。
- 本 repo 設為私人，因內容包含真實選手與家長姓名。
