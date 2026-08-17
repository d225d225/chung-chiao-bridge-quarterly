#!/usr/bin/env python3
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from renderers import render_blocks, render_block, suit_span, esc, img_tag

BUILD = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(BUILD, "content")
MEDIA = os.path.join(BUILD, "media")

def load(name):
    with open(os.path.join(CONTENT, f"{name}.json"), encoding="utf-8") as f:
        return json.load(f)

main_blocks = load("main")
gonggao_blocks = load("gonggao")
spingold_blocks = load("spingold_fixed")
xiaocai_blocks = load("xiaocai")
manguan_blocks = load("manguan")
jingque2c_blocks = load("jingque2c")
essays = json.load(open(os.path.join(BUILD, "essays.json"), encoding="utf-8"))

def article_html(title, author, blocks, media_dir, kicker="", mini_table=False, single=False):
    col_cls = "article-body single" if single else "article-body"
    return f'''<div class="article">
  <div class="article-head">
    {f'<div class="kicker">{esc(kicker)}</div>' if kicker else ''}
    <h2>{suit_span(title)}</h2>
    <div class="byline">文｜<span class="name">{esc(author)}</span></div>
    <div class="rule"></div>
  </div>
  <div class="{col_cls}">{render_blocks(blocks, media_dir, mini_table=mini_table)}</div>
</div>'''

def page(inner, extra_cls=""):
    return f'<section class="page {extra_cls}">{inner}</section>'

def section_header(tag):
    return f'<div class="section-tag"><span>中橋季刊．2026秋季號</span><span>{tag}</span></div>'

pages = []

# ============ COVER ============
cover = f'''<div class="cover">
  <div class="cover-top"><span>CHUNG CHIAO BRIDGE QUARTERLY</span><span>2026 · AUTUMN</span></div>
  <div class="cover-mast">
    <div class="en">C H U N G&nbsp; C H I A O&nbsp; B R I D G E</div>
    <h1>中橋季刊</h1>
    <div class="sub">2026　秋季號</div>
    <div class="cover-rule"></div>
    <div class="cover-tagline">中華民國橋藝協會　發行</div>
  </div>
  <div class="cover-highlights">
    <ul>
      <li>捷報：第五屆亞洲盃橋藝錦標賽喜獲兩金</li>
      <li>橋壇人物專訪：亞洲橋王黃光輝　．　理事長沈乃正</li>
      <li>萬事起頭難——談夢家的第一磴出牌／沈乃正</li>
      <li>世青賽專題：合肥世界青年橋牌錦標賽　選手心得與教練講評</li>
      <li>橋藝教室：精確2C系統改良、低花黑木氏8S9C法、Bridge Coups</li>
    </ul>
  </div>
  <div class="cover-bottom"><span>中華民國115年10月3日出版</span><span>發行人｜沈乃正　主編｜楊欣龍</span></div>
</div>'''
pages.append(page(cover, "full-bleed"))

# ============ TOC ============
def toc_item(title, author):
    return f'<div class="toc-item"><span class="title">{esc(title)}</span><span class="leader"></span><span class="author">{esc(author)}</span></div>'

toc = f'''<div class="toc-page">
  <h2 class="toc-title">目　　錄</h2>
  <div class="toc-sub">C O N T E N T S</div>
  <div class="toc-section">
    <div class="toc-section-title">焦點快訊</div>
    {toc_item("捷報！第五屆亞洲盃橋藝錦標賽喜獲兩金","本刊報導")}
    {toc_item("捷報！第二屆亞洲雙人錦標賽傳佳績","本刊報導")}
    {toc_item("2026亞洲雙人錦標賽介紹","Doris")}
    {toc_item("香港城市橋牌錦標賽","本刊收錄")}
    {toc_item("2026嘉興台灣青年橋藝交流活動","楊欣龍")}
  </div>
  <div class="toc-section">
    <div class="toc-section-title">橋海漫遊</div>
    {toc_item("弔顏永南橋友","沈乃正")}
    {toc_item("數風流人物·橋壇人物專訪——黃光輝","許君薇")}
    {toc_item("數風流人物·橋壇人物專訪——沈乃正","許君薇")}
    {toc_item("萬事起頭難——談夢家的第一磴出牌","沈乃正")}
    {toc_item("中曾盃滿貫大戰","楊欣龍")}
    {toc_item("驚技之國之櫻雪橋記（上）","潘正全")}
    {toc_item("續胡說橋牌","胡希真")}
    {toc_item("小材大用","沈乃正")}
    {toc_item("滿貫滿天飛——橋協盃混合組記趣","洪乙安")}
    {toc_item("2026 Summer NABC－Spingold史賓果淘汰賽","渡鴉")}
    {toc_item("經典重刊：第十六屆大專盃橋賽","徐嘉華．傅依俊")}
  </div>
  <div class="toc-section">
    <div class="toc-section-title">世青賽專題．合肥紀行</div>
    {toc_item("十六位選手與家長的合肥心得","本刊採訪整理")}
  </div>
</div>'''
pages.append(page(toc))

toc2 = f'''<div class="toc-page">
  <h2 class="toc-title">目　　錄　（續）</h2>
  <div class="toc-sub">C O N T E N T S</div>
  <div class="toc-section">
    <div class="toc-section-title">橋藝教室</div>
    {toc_item("【專欄】Bridge Master解析　水平1：18～23","陳飛")}
    {toc_item("特約介紹——轉換叫後無王開叫者的大配合","楊欣龍")}
    {toc_item("低花黑木氏改良：8S9C法","任乘風")}
    {toc_item("Bridge Coups－4","黃光輝")}
    {toc_item("精確2C後續系統性改進","上海橋友投稿")}
  </div>
  <div class="toc-section">
    <div class="toc-section-title">橋訊公告</div>
    {toc_item("中華民國橋藝協會年度重要活動時程","秘書處")}
    {toc_item("各地例行橋藝活動聯絡資訊","秘書處")}
    {toc_item("2026世界跨國邀請賽／世界青年跨國錦標賽成績報告","秘書處．本刊彙整")}
    {toc_item("中華橋協重要比賽成績公告","秘書處")}
    {toc_item("中華民國橋藝協會志工招募","秘書處")}
    {toc_item("徵稿啟事暨版權資料","本刊敬啟")}
  </div>
</div>'''
pages.append(page(toc2))

# ============ SECTION 1: 焦點快訊 ============
divider1 = f'''<div class="divider">
  <div class="num">01</div>
  <div class="kicker">SECTION ONE</div>
  <h2>焦點快訊</h2>
  <div class="en">LATEST NEWS &amp; HIGHLIGHTS</div>
  <div class="desc">亞洲賽場捷報頻傳，兩金入袋；雙人賽、城市邀請賽接力登場；嘉興交流團跨海赴約，六天五夜寫下青年橋藝新篇章。</div>
</div>'''
pages.append(page(divider1, "full-bleed"))

def main_slice(a, b):
    return main_blocks[a:b]

fq1 = article_html("捷報！第五屆亞洲盃橋藝錦標賽喜獲兩金", "本刊報導", main_slice(3,6), MEDIA+"/main", kicker="焦點快訊")
fq2 = article_html("捷報！第二屆亞洲雙人錦標賽傳佳績", "本刊報導", main_slice(7,8), MEDIA+"/main", kicker="焦點快訊")
pages.append(page(section_header("焦點快訊") + fq1 + fq2))

fq3 = article_html("2026亞洲雙人錦標賽介紹", "Doris", main_slice(9,15), MEDIA+"/main", kicker="焦點快訊")
pages.append(page(section_header("焦點快訊") + fq3))

fq4 = article_html("香港城市橋牌錦標賽", "本刊收錄", main_slice(16,19), MEDIA+"/main", kicker="焦點快訊")
pages.append(page(section_header("焦點快訊") + fq4))

fq5 = article_html("2026嘉興台灣青年橋藝交流活動", "楊欣龍", main_slice(20,53), MEDIA+"/main", kicker="焦點快訊")
pages.append(page(section_header("焦點快訊") + fq5))

# ============ SECTION 2: 橋海漫遊 ============
divider2 = f'''<div class="divider">
  <div class="num">02</div>
  <div class="kicker">SECTION TWO</div>
  <h2>橋海漫遊</h2>
  <div class="en">STORIES FROM THE BRIDGE WORLD</div>
  <div class="desc">悼念、專訪、牌局賞析與旅人筆記——橋壇的人情與牌藝，在這裡緩緩鋪展。</div>
</div>'''
pages.append(page(divider2, "full-bleed"))

bh1 = article_html("弔顏永南橋友", "沈乃正", main_slice(55,77), MEDIA+"/main", kicker="橋海漫遊")
pages.append(page(section_header("橋海漫遊") + bh1))

bh2 = article_html("數風流人物·橋壇人物專訪——黃光輝", "許君薇", main_slice(78,98), MEDIA+"/main", kicker="橋海漫遊")
pages.append(page(section_header("橋海漫遊") + bh2))

bh3 = article_html("數風流人物·橋壇人物專訪——沈乃正", "許君薇", main_slice(99,130), MEDIA+"/main", kicker="橋海漫遊")
pages.append(page(section_header("橋海漫遊") + bh3))

bh4 = article_html("萬事起頭難——談夢家的第一磴出牌", "沈乃正", main_slice(131,203), MEDIA+"/main", kicker="橋海漫遊", mini_table=True)
# split this long article across two pages worth of content by just letting column flow paginate naturally
pages.append(page(section_header("橋海漫遊") + bh4))

bh5 = article_html("中曾盃滿貫大戰", "楊欣龍", main_slice(204,239), MEDIA+"/main", kicker="橋海漫遊")
pages.append(page(section_header("橋海漫遊") + bh5))

bh6 = article_html("驚技之國之櫻雪橋記（上）", "潘正全", main_slice(240,294), MEDIA+"/main", kicker="橋海漫遊")
pages.append(page(section_header("橋海漫遊") + bh6))

bh7 = article_html("續胡說橋牌", "胡希真", main_slice(295,357), MEDIA+"/main", kicker="橋海漫遊")
pages.append(page(section_header("橋海漫遊") + bh7))

bh8 = article_html("小材大用", "沈乃正", xiaocai_blocks, MEDIA+"/xiaocai", kicker="橋海漫遊")
bh9 = article_html("滿貫滿天飛——橋協盃混合組記趣", "洪乙安", manguan_blocks[1:], MEDIA+"/manguan", kicker="橋海漫遊")
pages.append(page(section_header("橋海漫遊") + bh8))
pages.append(page(section_header("橋海漫遊") + bh9))

bh10 = article_html("2026 Summer NABC－Spingold史賓果淘汰賽", "渡鴉", spingold_blocks[1:], MEDIA+"/spingold", kicker="橋海漫遊")
pages.append(page(section_header("橋海漫遊") + bh10))

# archival reprint
archival_note = '<div class="archival-banner">經典重刊．典藏自民國橋壇文獻，原載於《第十六屆大專盃橋藝錦標賽》紀念特刊，特此重刊以饗讀者。</div>'
archival_body = '''
<p class="p">第十六屆大專盃橋藝錦標賽，輪由東海大學橋藝社主辦，東海大學是在台中市的郊區，地處偏僻，交通不便，增加與賽橋友不少困擾，加之我們這群從無舉辦橋賽的經驗，籌劃難免欠週，服務不到之處，尚請各校橋友原諒。</p>
<p class="p">本屆橋賽，參加公開組者三十八隊，女子組十一隊，近四百橋友濟濟一堂，場面浩大，在中部地區，可謂少見，公開組分初賽和決賽，女子組單循環比賽，另舉行論對賽，亦分初賽與決賽，其戰況如下：</p>
<p class="inline-title">壹、公開組</p>
<p class="p">三十八隊分四組，計黑桃（S）紅心（H）方塊（D）及梅花（C）。S、H各十隊，D、C各九隊，每組單循環，各取前兩名晉入決賽。</p>
<p class="p">S組：東海東與中興商賽至最後一牌，前者始以剛好的比數（5:3）進入決賽。同組世新一路順風直入。</p>
<p class="p">H組：清華同樣情形，最後一場對中正險勝，以0.5勝分氣走東海風。同組高醫以分組冠軍入。</p>
<p class="p">D組：中興法、T.M.C以一路領先進入決賽。</p>
<p class="p">C組：B.T.U.T險遭滑鐵盧，情況如下：若政大、淡江最後一場均拿足7分以上，則台大回生乏術，結果，政大對中山未拿足，飲恨北歸、淡江、台大晉級。</p>
<p class="inline-title">一決　賽一</p>
<p class="p">先是東海東、中興法最有希望，二隊碰頭，中興法果然犀利而東海東牌運欠佳，加之調配失當，以8:-1飲恨，大失奪標希望。至最後二場有希望問鼎的有中興法、B.T.U.T、東海東、清華；結果清華力克中興法，B.T.U.T.拿8分，東海東雖以4:4平勝高醫，已與冠軍絕緣，最後一場，決定冠、亞、季、殿軍；東海東拿8分，坐三望二，清華-2:8輸給T.M.C.敬坐殿軍，B.T.U.T對中興法，如B.T.U.T贏足則冠軍，可惜以2:6敗北，只得退居季軍。</p>
<p class="inline-title">貳、女子組</p>
<p class="p">女子組最初幾場，尚不能看出誰高誰下，直到最後二場始明朗化：B.T.U.B穩第四，中興慧坐三望二，B.T.U.T與政大爭后，苦戰三小時餘，B.T.U.T技高一籌，政大落至季軍。</p>
<p class="inline-title">參、論對賽</p>
<p class="p">論對賽初賽，採密契爾制，分A、B兩組每組二十一桌，各取南北、東西前四名晉入決賽，決賽採浩威爾制，比賽結果如下：</p>
<p class="p">1. 冠軍：李龍秋、潘國昭（交通大學）　　2. 亞軍：陳全勇、葉建朝（政治大學）</p>
<p class="p">3. 季軍：范熙揚、黃志中（交通大學）　　4. 殿軍：鄭長榮、施慶賢（輔仁大學）</p>
<p class="p">5. 第五名：彭火龍、楊錢棟（文化學院）</p>
<p class="p">本屆賽事由救國團台中地區大專學生社團服務中心協辦，於四月二日至六日假東海大學體育館舉行，宗旨在切磋橋藝、增進友誼；比賽以中國橋藝協會一九七二年出版之複式橋規為比賽規則，公開組取六名、女子組取四名，各頒優勝獎及紀念品，冠軍主盃須連續獲得三屆冠軍，始得永久保留。</p>
<p class="p">（原文作者：徐嘉華、傅依俊；隊職員名單、決賽對戰紀錄等原始文獻，因年代久遠、原稿部分手跡漫漶，本刊謹擇要重刊上述文字紀錄，隊伍名單詳見原刊影本存檔，特此說明並向兩位原作者致謝。）</p>
'''
bh11 = f'''<div class="article">
  <div class="article-head">
    <div class="kicker">橋海漫遊．經典重刊</div>
    <h2>第十六屆大專盃橋賽</h2>
    <div class="byline">文｜<span class="name">徐嘉華．傅依俊</span></div>
    <div class="rule"></div>
  </div>
  {archival_note}
  <div class="article-body">{archival_body}</div>
</div>'''
pages.append(page(section_header("橋海漫遊") + bh11))

# ============ SECTION 3: 世青賽專題 ============
divider3 = f'''<div class="divider">
  <div class="num">03</div>
  <div class="kicker">SPECIAL FEATURE</div>
  <h2>世青賽專題</h2>
  <div class="en">2026 WORLD YOUTH TEAMS · HEFEI</div>
  <div class="desc">十六位選手與家長，寫下他們在合肥世界青年橋牌錦標賽中最真實的心情——緊張、失落、突破、感謝。本刊特邀資深帶隊教練逐篇講評，與孩子們一同回顧這趟橋藝成長之旅。</div>
</div>'''
pages.append(page(divider3, "full-bleed"))

essay_cards = []
for e in essays:
    before_p = "".join(f"<p>{esc(l)}</p>" for l in e["before"].split("\n") if l.strip())
    after_p = "".join(f"<p>{esc(l)}</p>" for l in e["after"].split("\n") if l.strip())
    comment_p = "".join(f"<p>{esc(l)}</p>" for l in e["comment"].split("\n") if l.strip())
    card = f'''<div class="essay-card">
  <div class="essay-head"><span class="name">{esc(e["name"])}</span><span class="role">{esc(e["role"])}</span></div>
  <div class="essay-body">
    <div class="essay-label">賽前想像</div>
    <div class="essay-quote">{before_p}</div>
    <div class="essay-label">參賽心得</div>
    <div class="essay-text">{after_p}</div>
    <div class="coach-box"><div class="coach-label">教練講評</div>{comment_p}</div>
  </div>
</div>'''
    essay_cards.append(card)

# lay out essays 1 per page-ish, but let flow decide — group into pages of ~1-2 cards
intro = '''<div class="article-head" style="margin-bottom:6mm;">
  <div class="kicker">世青賽專題</div>
  <h2>合肥紀行——十六位選手與家長的心得</h2>
  <div class="byline">採訪整理｜<span class="name">本刊編輯部</span>　講評｜<span class="name">帶隊教練</span></div>
  <div class="rule"></div>
</div>
<p class="p" style="text-indent:2em; margin-bottom:6mm;">2026年8月，逐夢隊一行十餘位青少年選手，跟隨教練遠赴中國合肥，參加世界青年橋牌錦標賽。這是許多孩子生平第一次站上國際賽場，緊張與期待交織。賽後，本刊邀請選手與隨隊家長寫下心得，並特邀資深教練逐篇講評——不只是牌技的檢討，更是心理素質、團隊默契與挫折復原力的成長紀錄。</p>'''
pages.append(page(section_header("世青賽專題") + intro))

# place ~2 essay cards per page
i = 0
first = True
while i < len(essay_cards):
    chunk = essay_cards[i:i+2]
    pages.append(page(section_header("世青賽專題") + '<div class="article-body single">' + "".join(chunk) + '</div>'))
    i += 2

# ============ SECTION 4: 橋藝教室 ============
divider4 = f'''<div class="divider">
  <div class="num">04</div>
  <div class="kicker">SECTION FOUR</div>
  <h2>橋藝教室</h2>
  <div class="en">THE BRIDGE CLASSROOM</div>
  <div class="desc">從電腦解牌到滿貫問叫系統，從轉換叫大配合到跨海投稿的精確2C改良——技術與思辨，盡在此章。</div>
</div>'''
pages.append(page(divider4, "full-bleed"))

bt1 = article_html("【專欄】Bridge Master解析　水平1：18～23", "陳飛", main_slice(359,413), MEDIA+"/main", kicker="橋藝教室")
pages.append(page(section_header("橋藝教室") + bt1))

bt2 = article_html("特約介紹——轉換叫後無王開叫者的大配合", "楊欣龍", main_slice(414,462), MEDIA+"/main", kicker="橋藝教室")
pages.append(page(section_header("橋藝教室") + bt2))

bt3 = article_html("低花黑木氏改良：8S9C法", "任乘風", main_slice(463,469), MEDIA+"/main", kicker="橋藝教室")
pages.append(page(section_header("橋藝教室") + bt3))

bt4 = article_html("Bridge Coups－4", "黃光輝", main_slice(470,521), MEDIA+"/main", kicker="橋藝教室")
pages.append(page(section_header("橋藝教室") + bt4))

bt5 = article_html("精確2C後續系統性改進", "上海橋友投稿", jingque2c_blocks[1:], MEDIA+"/jingque2c", kicker="橋藝教室")
pages.append(page(section_header("橋藝教室") + bt5))

# ============ SECTION 5: 橋訊公告 ============
divider5 = f'''<div class="divider">
  <div class="num">05</div>
  <div class="kicker">SECTION FIVE</div>
  <h2>橋訊公告</h2>
  <div class="en">ANNOUNCEMENTS &amp; NOTICES</div>
  <div class="desc">年度賽事時程、各地例行活動、成績公告與志工招募——橋協秘書處為您彙整。</div>
</div>'''
pages.append(page(divider5, "full-bleed"))

# gonggao.json verified block indices (checked by hand against content dump):
#  0 title 橋訊公告 (section name, skip)              1 table schedule            2 para note
#  3 table regional activities                        4 title caption (keep)      5 para note
#  6 table 2026世界跨國邀請賽 results                  7 table 2026世界青年跨國錦標賽 results
#  8 title caption (keep)                              9 para note
# 10 table 葉氏盃 roster                               11 title 中華橋協重要比賽成績公告 (H2, skip)
# 12 para note                                          13 table 中曾盃/橋協盃 roster
# 14 title 志工招募 (H2, skip)                          15-28 para volunteer/call-for-submissions
# 29 title 徵稿啟事 (caption, keep)                      30 title orphan (no body, drop)
g = gonggao_blocks

ann1 = article_html("中華民國橋藝協會年度重要活動時程", "秘書處", g[1:3], MEDIA+"/gonggao", kicker="橋訊公告", single=True)
pages.append(page(section_header("橋訊公告") + ann1))

ann2 = article_html("各地例行橋藝活動聯絡資訊", "秘書處", g[3:6], MEDIA+"/gonggao", kicker="橋訊公告", single=True)
pages.append(page(section_header("橋訊公告") + ann2))

ann3 = article_html("2026世界跨國邀請賽／世青賽成績報告", "秘書處．本刊彙整", g[6:10], MEDIA+"/gonggao", kicker="橋訊公告", single=True)
pages.append(page(section_header("橋訊公告") + ann3))

ann4 = article_html("中華橋協重要比賽成績公告", "秘書處", g[10:11] + g[12:14], MEDIA+"/gonggao", kicker="橋訊公告", single=True)
pages.append(page(section_header("橋訊公告") + ann4))

ann5_blocks = g[15:30]
ann5 = article_html("中華民國橋藝協會志工招募暨徵稿啟事", "秘書處", ann5_blocks, MEDIA+"/gonggao", kicker="橋訊公告", single=True)
pages.append(page(section_header("橋訊公告") + ann5))

# ============ BACK COVER / COLOPHON ============
colophon_rows = [
  ("發行人","沈乃正"), ("主編","楊欣龍　shon.yang@gmail.com"),
  ("出版者","中華民國橋藝協會　ctcba886@gmail.com"),
  ("地址","臺北市大安區忠孝東路三段217巷7弄7號B1"),
  ("電話","(02)2772-4510、(02)2772-4583"), ("傳真","(02)2772-4493"),
  ("橋協網站","https://www.ctcba.org.tw/"), ("文稿校對","陸怡如"),
  ("出版日期","中華民國115年10月3日"),
]
rows_html = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k,v in colophon_rows)
back = f'''<div class="back-cover">
  <div style="font-family:var(--sans); letter-spacing:4px; font-size:9pt; color:var(--gold-light);">CHUNG CHIAO BRIDGE QUARTERLY</div>
  <div>
    <div style="font-family:var(--serif); font-size:30pt; letter-spacing:8px; margin-bottom:6mm;">中橋季刊</div>
    <table class="colophon-table" style="color:#e8e0cc;">{rows_html}</table>
  </div>
  <div style="font-family:var(--sans); font-size:8pt; color:#b9ac8c; letter-spacing:1px;">本刊採電子版發行，歡迎海內外橋友踴躍投稿以饗讀者　｜　版權所有．轉載請註明出處</div>
</div>'''
pages.append(page(back, "full-bleed"))

css = open(os.path.join(BUILD, "magazine.css"), encoding="utf-8").read()

html_doc = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>中橋季刊 2026秋季號</title>
<style>{css}</style>
</head>
<body>
{"".join(pages)}
</body>
</html>'''

out_path = os.path.join(BUILD, "magazine.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_doc)
print(f"Wrote {out_path}, {len(pages)} page-sections, {len(html_doc)} bytes")
