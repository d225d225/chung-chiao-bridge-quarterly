#!/usr/bin/env python3
"""
Parse a .docx in document order into structured content blocks,
classifying tables as bridge hand-diagrams, bidding sequences, or generic tables.

Reads run/w:sym XML directly (not python-docx's .text) so Symbol-font suit glyphs
(common in older bridge documents) are decoded correctly instead of silently dropped.
Also skips <mc:Fallback> subtrees: Word wraps drawings/textboxes in
<mc:AlternateContent><mc:Choice/><mc:Fallback/></mc:AlternateContent> with duplicate
content for compatibility, and naive tree-walks otherwise double- or triple-count text/images.
"""
import sys, os, json, re
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

SUIT_CHARS = set("♠♥♦♣")

SYM_MAP = {
    ("Symbol", "F0A7"): "♣",
    ("Symbol", "F0A8"): "♦",
    ("Symbol", "F0A9"): "♥",
    ("Symbol", "F0AA"): "♠",
}

FALLBACK_TAG = '{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback'
T_TAG = qn('w:t')
SYM_TAG = qn('w:sym')
TAB_TAG = qn('w:tab')
BR_TAG = qn('w:br')
CR_TAG = qn('w:cr')
BLIP_TAG = qn('a:blip')
R_EMBED = qn('r:embed')
TXBX_TAG = qn('w:txbxContent')

def walk_text(elem, parts):
    """Recursively collect display text from elem, skipping mc:Fallback subtrees."""
    for child in elem:
        tag = child.tag
        if tag == FALLBACK_TAG:
            continue
        if tag == T_TAG:
            parts.append(child.text or '')
        elif tag == SYM_TAG:
            parts.append(SYM_MAP.get((child.get(qn('w:font')), child.get(qn('w:char'))), ''))
        elif tag == TAB_TAG:
            parts.append('\t')
        elif tag in (BR_TAG, CR_TAG):
            parts.append('\n')
        else:
            walk_text(child, parts)

def elem_text(elem):
    parts = []
    walk_text(elem, parts)
    return ''.join(parts)

def walk_split(elem, out):
    """Like walk_text, but pulls the text of any nested <w:txbxContent> (floating
    title/caption textboxes) into separate 'textbox' tokens instead of inlining it
    into the surrounding paragraph's own body text."""
    for child in elem:
        tag = child.tag
        if tag == FALLBACK_TAG:
            continue
        if tag == TXBX_TAG:
            tb_text = elem_text(child).strip()
            if tb_text:
                out.append(('textbox', tb_text))
            continue
        if tag == T_TAG:
            out.append(('text', child.text or ''))
        elif tag == SYM_TAG:
            out.append(('text', SYM_MAP.get((child.get(qn('w:font')), child.get(qn('w:char'))), '')))
        elif tag == TAB_TAG:
            out.append(('text', '\t'))
        elif tag in (BR_TAG, CR_TAG):
            out.append(('text', '\n'))
        else:
            walk_split(child, out)

def paragraph_text_and_titles(p_elem):
    tokens = []
    walk_split(p_elem, tokens)
    body = ''.join(t for k, t in tokens if k == 'text').strip()
    titles = []
    for k, t in tokens:
        if k == 'textbox' and (not titles or titles[-1] != t):
            titles.append(t)
    return body, titles

def walk_images(elem, part, media_dir, counter, out):
    for child in elem:
        tag = child.tag
        if tag == FALLBACK_TAG:
            continue
        if tag == BLIP_TAG:
            rId = child.get(R_EMBED)
            if rId:
                try:
                    image_part = part.related_parts[rId]
                except KeyError:
                    image_part = None
                if image_part is not None:
                    ext = image_part.content_type.split('/')[-1]
                    ext = {'jpeg': 'jpg'}.get(ext, ext)
                    counter[0] += 1
                    fname = f"img_{counter[0]:04d}.{ext}"
                    with open(os.path.join(media_dir, fname), 'wb') as f:
                        f.write(image_part.blob)
                    out.append(fname)
        walk_images(child, part, media_dir, counter, out)

def paragraph_text(p_elem):
    return elem_text(p_elem).strip()

def cell_full_text(tc_elem):
    lines = [elem_text(p) for p in tc_elem.findall(qn('w:p'))]
    return "\n".join(lines).strip()

def get_images_in_paragraph(p_elem, part, media_dir, counter):
    out = []
    walk_images(p_elem, part, media_dir, counter, out)
    return out

def dedupe_grid(tbl_elem):
    grid = []
    for tr in tbl_elem.findall(qn('w:tr')):
        row = []
        for tc in tr.findall(qn('w:tc')):
            tcPr = tc.find(qn('w:tcPr'))
            hmerge = tcPr.find(qn('w:hMerge')) if tcPr is not None else None
            if hmerge is not None and hmerge.get(qn('w:val')) == 'continue':
                continue
            row.append(cell_full_text(tc))
        grid.append(row)
    return grid

def classify_table(grid):
    nrows = len(grid)
    ncols = max((len(r) for r in grid), default=0)
    flat = "".join("".join(r) for r in grid)
    has_suit = any(ch in flat for ch in SUIT_CHARS)

    if nrows >= 1 and ncols >= 4:
        header = [c.strip().upper() for c in (grid[0] + ["", "", "", ""])[:4]]
        if set(header) == {"W", "N", "E", "S"}:
            return "bidding"

    if nrows == 3 and all(len(r) == 3 for r in grid) and has_suit:
        return "hand"

    if nrows <= 2 and ncols == 1:
        return "note"

    return "generic"

def parse_hand_table(grid):
    label = grid[0][0] if len(grid[0]) > 0 else ""
    north = grid[0][1] if len(grid[0]) > 1 else ""
    west = grid[1][0] if len(grid[1]) > 0 else ""
    east = grid[1][2] if len(grid[1]) > 2 else ""
    south = grid[2][1] if len(grid[2]) > 1 else ""
    return {
        "label": [l for l in label.split("\n") if l.strip()],
        "north": [l for l in north.split("\n") if l.strip()],
        "south": [l for l in south.split("\n") if l.strip()],
        "west": [l for l in west.split("\n") if l.strip()],
        "east": [l for l in east.split("\n") if l.strip()],
    }

def parse_bidding_table(grid):
    header = [c.strip().upper() for c in (grid[0] + ["", "", "", ""])[:4]]
    rows, footnotes = [], []
    for r in grid[1:]:
        if len(r) == 1:
            if r[0].strip():
                footnotes.append(r[0].strip())
            continue
        cells = (r + ["", "", "", ""])[:4]
        rows.append(dict(zip(header, cells)))
    return {"header": header, "rows": rows, "footnotes": footnotes}

def is_heading_paragraph(p_elem, text):
    if not text or len(text) > 40:
        return False
    runs = p_elem.findall(qn('w:r'))
    if not runs:
        return False
    bold_chars = 0
    total_chars = 0
    for r in runs:
        t = elem_text(r)
        total_chars += len(t)
        rpr = r.find(qn('w:rPr'))
        if rpr is not None and rpr.find(qn('w:b')) is not None:
            bold_chars += len(t)
    return total_chars > 0 and bold_chars / total_chars > 0.8

def parse_docx(path, media_dir):
    os.makedirs(media_dir, exist_ok=True)
    doc = Document(path)
    part = doc.part
    counter = [0]
    blocks = []
    body = doc.element.body
    for child in body.iterchildren():
        tag = child.tag
        if tag == qn('w:p'):
            text, titles = paragraph_text_and_titles(child)
            for t in titles:
                if len(t) <= 60:
                    blocks.append({"type": "title", "text": t})
                else:
                    for seg in t.split('\n'):
                        seg = seg.strip()
                        if seg:
                            blocks.append({"type": "para", "text": seg})
            imgs = get_images_in_paragraph(child, part, media_dir, counter)
            if not text and not imgs:
                continue
            btype = "heading" if is_heading_paragraph(child, text) else "para"
            block = {"type": btype, "text": text}
            if imgs:
                block["images"] = imgs
            blocks.append(block)
        elif tag == qn('w:tbl'):
            grid = dedupe_grid(child)
            kind = classify_table(grid)
            if kind == "hand":
                blocks.append({"type": "hand", "data": parse_hand_table(grid)})
            elif kind == "bidding":
                blocks.append({"type": "bidding", "data": parse_bidding_table(grid)})
            elif kind == "note":
                txt = "\n".join(c for r in grid for c in r if c.strip())
                blocks.append({"type": "note", "text": txt})
            else:
                blocks.append({"type": "table", "data": grid})
    return blocks

if __name__ == "__main__":
    src, media_dir, out_json = sys.argv[1], sys.argv[2], sys.argv[3]
    blocks = parse_docx(src, media_dir)
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(blocks, f, ensure_ascii=False, indent=1)
    print(f"Parsed {len(blocks)} blocks -> {out_json}")
