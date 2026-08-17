#!/usr/bin/env python3
"""HTML renderers for parsed docx content blocks."""
import html, re, os

def esc(s):
    return html.escape(s or "", quote=False)

def suit_span(text):
    """Wrap suit glyphs in colored spans."""
    out = []
    for ch in text:
        if ch in "♥♦":
            out.append(f'<span class="suit-red">{ch}</span>')
        elif ch in "♠♣":
            out.append(f'<span class="suit-black">{ch}</span>')
        else:
            out.append(esc(ch))
    return "".join(out)

def render_hand(data, media_dir=None):
    def lines(key):
        return "".join(f'<div class="hl">{suit_span(l)}</div>' for l in data.get(key, []))
    label = " ／ ".join(data.get("label", []))
    label_html = f'<div class="hand-label">{esc(label)}</div>' if label else ""
    return f'''<div class="hand-diagram">
  {label_html}
  <div class="compass">
    <div class="c-blank"></div><div class="c-north">{lines("north")}</div><div class="c-blank"></div>
    <div class="c-west">{lines("west")}</div><div class="c-rose">N<br>W&nbsp;&nbsp;E<br>S</div><div class="c-east">{lines("east")}</div>
    <div class="c-blank"></div><div class="c-south">{lines("south")}</div><div class="c-blank"></div>
  </div>
</div>'''

def render_bidding(data):
    header = data.get("header", ["W","N","E","S"])
    rows = data.get("rows", [])
    footnotes = data.get("footnotes", [])
    thead = "".join(f"<th>{esc(h)}</th>" for h in header)
    trs = []
    for r in rows:
        tds = "".join(f"<td>{suit_span(r.get(h,''))}</td>" for h in header)
        trs.append(f"<tr>{tds}</tr>")
    fn = "".join(f'<div class="bid-note">{suit_span(f)}</div>' for f in footnotes)
    return f'''<div class="bidding-block">
  <table class="bidding-table"><thead><tr>{thead}</tr></thead><tbody>{"".join(trs)}</tbody></table>
  {fn}
</div>'''

def render_mini_diagram(grid):
    """萬事起頭難-style compact 2/3-hand single-suit teaching diagrams."""
    footnote_rows = [r for r in grid if len(r) == 1]
    data_rows = [r for r in grid if len(r) > 1]
    cells = []
    for r in data_rows:
        r = (r + ["", "", ""])[:3]
        cells.append(r)
    grid_html = ""
    for r in cells:
        tds = "".join(f'<div class="md-cell">{suit_span(c)}</div>' for c in r)
        grid_html += f'<div class="md-row">{tds}</div>'
    fn = "".join(f'<div class="md-note">{suit_span(f)}</div>' for f in footnote_rows)
    return f'<div class="mini-diagram">{grid_html}{fn}</div>'

def looks_like_roster(grid):
    ncols = max((len(r) for r in grid), default=0)
    return ncols == 2

def render_generic_table(grid, mini=False):
    if mini:
        return render_mini_diagram(grid)
    if looks_like_roster(grid):
        parts = ['<div class="roster-table">']
        for r in grid:
            if len(r) == 1:
                parts.append(f'<div class="roster-section">{esc(r[0])}</div>')
            else:
                label, val = r[0], r[1] if len(r) > 1 else ""
                val_html = esc(val).replace("\n", "<br>")
                parts.append(f'<div class="roster-row"><div class="roster-label">{esc(label)}</div><div class="roster-value">{val_html}</div></div>')
        parts.append('</div>')
        return "".join(parts)
    # wide data table with header row
    if not grid:
        return ""
    header, *body = grid
    ncols = max(len(r) for r in grid)
    thead = "".join(f"<th>{esc(c).replace(chr(10),'<br>')}</th>" for c in (header + [""]*ncols)[:ncols])
    trs = []
    for r in body:
        r = (r + [""]*ncols)[:ncols]
        tds = "".join(f"<td>{esc(c).replace(chr(10),'<br>')}</td>" for c in r)
        trs.append(f"<tr>{tds}</tr>")
    return f'<div class="table-wrap"><table class="data-table"><thead><tr>{thead}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'

def img_tag(fname, media_dir, cls="fig"):
    path = os.path.join(media_dir, fname)
    return f'<img class="{cls}" src="file://{path}">'

def render_para(text, media_dir=None, images=None, cls="p"):
    out = []
    for seg in text.split("\n"):
        seg = seg.strip()
        if not seg:
            continue
        if seg.startswith("恭喜") or "冠軍" in seg[:4] or "亞軍" in seg[:4]:
            out.append(f'<p class="{cls} award-line">{suit_span(seg)}</p>')
        else:
            out.append(f'<p class="{cls}">{suit_span(seg)}</p>')
    if images and media_dir:
        for im in images:
            out.append(img_tag(im, media_dir))
    return "".join(out)

def render_block(b, media_dir, mini_table=False, heading_level=3):
    t = b["type"]
    if t == "para":
        return render_para(b.get("text",""), media_dir, b.get("images"))
    if t == "heading":
        html_out = f'<h{heading_level} class="sub-heading">{suit_span(b["text"])}</h{heading_level}>'
        if b.get("images") and media_dir:
            for im in b["images"]:
                html_out += img_tag(im, media_dir)
        return html_out
    if t == "title":
        return f'<p class="inline-title">{suit_span(b["text"])}</p>'
    if t == "hand":
        return render_hand(b["data"], media_dir)
    if t == "bidding":
        return render_bidding(b["data"])
    if t == "table":
        return render_generic_table(b["data"], mini=mini_table)
    if t == "note":
        return f'<div class="note-box">{suit_span(b.get("text",""))}</div>'
    return ""

def render_blocks(blocks, media_dir, mini_table=False, heading_level=3):
    return "".join(render_block(b, media_dir, mini_table, heading_level) for b in blocks)
