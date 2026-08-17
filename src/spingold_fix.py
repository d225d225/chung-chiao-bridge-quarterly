#!/usr/bin/env python3
"""
The Spingold article encodes hand diagrams as plain paragraphs using letter suits
(S/H/D/C) instead of a real Word table, e.g.:
  S A9 / H 874 / D QJ7 / C AK532   (North)
  北
  S QJ642 S -  / H A92 H KJ653 / D T D A98432 / C J976 C Q4   (West / East)
  南
  S KT8753 / H QT / D K65 / C T8   (South)
This reconstructs those into the same {"type":"hand", "data":{...}} shape the
docx_parser produces for real tables, so the HTML renderer can treat them identically.
"""
import json, re, sys

SUIT_MAP = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
SOLO_RE = re.compile(r'^(S|H|D|C)\s+(\S*)$')
PAIR_RE = re.compile(r'^(S|H|D|C)\s+(\S*)\s+\1\s+(\S*)$')

def to_lines(quad):
    out = []
    for suit, val in quad:
        v = '' if val == '-' else val
        out.append(f"{SUIT_MAP[suit]}{v}")
    return out

def fix(blocks):
    out = []
    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        if b['type'] == 'para' and b['text'].strip() == '北' and i >= 4 and i + 9 < n:
            north_src = [blocks[i - 4 + k] for k in range(4)]
            we_src = [blocks[i + 1 + k] for k in range(4)]
            south_marker = blocks[i + 5]
            south_src = [blocks[i + 6 + k] for k in range(4)]
            north_m = [SOLO_RE.match(x['text'].strip()) for x in north_src if x['type'] == 'para']
            we_m = [PAIR_RE.match(x['text'].strip()) for x in we_src if x['type'] == 'para']
            south_m = [SOLO_RE.match(x['text'].strip()) for x in south_src if x['type'] == 'para']
            if (south_marker.get('text', '').strip() == '南'
                    and len(north_m) == 4 and all(north_m)
                    and len(we_m) == 4 and all(we_m)
                    and len(south_m) == 4 and all(south_m)):
                north = to_lines([(m.group(1), m.group(2)) for m in north_m])
                west = to_lines([(m.group(1), m.group(2)) for m in we_m])
                east = to_lines([(m.group(1), m.group(3)) for m in we_m])
                south = to_lines([(m.group(1), m.group(2)) for m in south_m])
                # remove the 4 north paragraphs we already appended to out
                del out[-4:]
                out.append({"type": "hand", "data": {
                    "label": [], "north": north, "south": south, "west": west, "east": east
                }})
                i = i + 6 + 4
                continue
        out.append(b)
        i += 1
    return out

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    blocks = json.load(open(src, encoding='utf-8'))
    fixed = fix(blocks)
    json.dump(fixed, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(b['type'] for b in fixed))
