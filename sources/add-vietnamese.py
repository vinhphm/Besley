#!/usr/bin/env python3
"""Add Vietnamese glyph support to Besley font SFD source files.

Adds:
- uni0309 (U+0309) Combining Hook Above
- uni031B (U+031B) Combining Horn
- uni01A0/uni01A1 (Ơ/ơ) O with Horn
- uni01AF/uni01B0 (Ư/ư) U with Horn
- All Latin Extended Additional Vietnamese precomposed characters (U+1EA0–U+1EF9)
"""

import re
import os
import sys

SFD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fontforge')

# ── Hookabovecomb spline shapes (one per master style) ───────────────────────
# Book/Condensed-Book: derived from existing uni0313 shifted up by +580
HOOKABOVE_BOOK = """\
394 2005 m 0
 394 2058 440 2100 501 2100 c 0
 563 2100 613 2050 613 1933 c 0
 613 1826 541 1690 409 1678 c 0
 397 1677 391 1676 391 1690 c 2
 391 1725 l 2
 391 1739 399 1741 411 1743 c 0
 484 1754 546 1828 537 1920 c 0
 535 1933 529 1927 520 1921 c 0
 507 1912 496 1911 479 1911 c 0
 426 1911 394 1952 394 2005 c 0"""

# Fatface/Condensed-Fatface: scaled from Fatface quoteright (scale 0.5, shifted up)
HOOKABOVE_FATFACE = """\
363 1847 m 0
 363 1920 427 1966 495 1966 c 0
 579 1966 635 1911 635 1803 c 0
 635 1663 492 1566 400 1554 c 0
 385 1552 381 1554 381 1570 c 2
 381 1630 l 2
 381 1640 385 1642 393 1643 c 0
 454 1649 514 1698 535 1732 c 0
 537 1736 534 1739 528 1737 c 0
 516 1732 498 1728 476 1728 c 0
 408 1728 363 1774 363 1847 c 0"""

# Italic/Condensed-Italic: scaled from Italic quoteright (scale 0.5, shifted up)
HOOKABOVE_ITALIC = """\
611 1833 m 0
 611 1866 640 1892 678 1892 c 0
 717 1892 748 1861 748 1798 c 0
 748 1711 663 1636 580 1629 c 0
 573 1629 569 1629 569 1637 c 2
 569 1659 l 2
 569 1668 574 1669 581 1670 c 0
 627 1676 701 1722 695 1779 c 0
 694 1787 690 1783 684 1779 c 0
 678 1776 669 1774 659 1774 c 0
 626 1774 611 1800 611 1833 c 0"""

# FatfaceItalic/Condensed-FatfaceItalic: scaled from FatfaceItalic quoteright
HOOKABOVE_FATFACE_ITALIC = """\
586 1822 m 0
 586 1894 644 1939 712 1939 c 0
 782 1939 852 1898 852 1785 c 0
 852 1655 697 1587 578 1581 c 0
 561 1580 559 1581 559 1598 c 2
 559 1651 l 2
 559 1663 563 1660 574 1661 c 0
 631 1665 719 1686 753 1724 c 0
 770 1743 757 1746 742 1737 c 0
 726 1728 706 1721 680 1721 c 0
 622 1721 586 1759 586 1822 c 0"""

# ── Combining horn spline shapes (origin = attachment point) ──────────────────
# Small curved arc representing the Vietnamese horn diacritic.
# Sized for upright Book weight; scaled up for Fatface.
HORN_BOOK = """\
0 0 m 2
 15 50 65 105 120 115 c 0
 165 124 185 96 176 60 c 0
 168 28 140 6 106 3 c 2
 113 18 l 2
 140 22 162 42 168 68 c 0
 174 95 155 115 120 107 c 0
 78 98 32 52 17 5 c 2
 0 0 l 2"""

HORN_FATFACE = """\
0 0 m 2
 25 75 100 160 185 178 c 0
 260 194 290 148 275 92 c 0
 262 40 218 6 168 2 c 2
 178 26 l 2
 218 30 254 64 262 104 c 0
 270 145 244 180 186 165 c 0
 116 148 48 84 24 14 c 2
 0 0 l 2"""

HORN_ITALIC = """\
0 0 m 2
 20 50 75 105 130 115 c 0
 175 124 195 96 186 60 c 0
 178 28 150 6 116 3 c 2
 123 18 l 2
 150 22 172 42 178 68 c 0
 184 95 165 115 130 107 c 0
 88 98 37 52 22 5 c 2
 0 0 l 2"""

HORN_FATFACE_ITALIC = """\
0 0 m 2
 35 75 115 160 200 178 c 0
 280 194 310 148 295 92 c 0
 282 40 238 6 188 2 c 2
 198 26 l 2
 238 30 274 64 282 104 c 0
 290 145 264 180 206 165 c 0
 126 148 58 84 34 14 c 2
 0 0 l 2"""

# ── Master configuration ──────────────────────────────────────────────────────
# circ_top: max y of circumflex shape (for stacking tone marks above circumflex)
# breve_top: max y of breve shape (for stacking above breve)
MASTER_CFG = {
    'Besley-Book.sfd':                  ('book',          500, 1949, 1938, HOOKABOVE_BOOK,          HORN_BOOK),
    'Besley-Fatface.sfd':               ('fatface',       499, 2019, 1938, HOOKABOVE_FATFACE,       HORN_FATFACE),
    'Besley-FatfaceItalic.sfd':         ('fatface_italic',705, 2019, 1938, HOOKABOVE_FATFACE_ITALIC, HORN_FATFACE_ITALIC),
    'Besley-Italic.sfd':                ('italic',        658, 1949, 1938, HOOKABOVE_ITALIC,        HORN_ITALIC),
    'BesleyCondensed-Book.sfd':         ('book',          500, 1949, 1938, HOOKABOVE_BOOK,          HORN_BOOK),
    'BesleyCondensed-Fatface.sfd':      ('fatface',       499, 2019, 1938, HOOKABOVE_FATFACE,       HORN_FATFACE),
    'BesleyCondensed-FatfaceItalic.sfd':('fatface_italic',705, 2019, 1938, HOOKABOVE_FATFACE_ITALIC, HORN_FATFACE_ITALIC),
    'BesleyCondensed-Italic.sfd':       ('italic',        658, 1949, 1938, HOOKABOVE_ITALIC,        HORN_ITALIC),
}

# ── Vietnamese precomposed character table ────────────────────────────────────
# (unicode, name, base, above, below, use_circ, use_breve)
# base: the glyph name to use as base letter
# above/below: mark names or None
# use_circ: primary diacritic is circumflex (tone mark stacked above it)
# use_breve: primary diacritic is breve (tone mark stacked above it)
VIET_CHARS = [
    # ── A/a-based ────────────────────────────────────────────────────────────
    (0x1EA0, 'uni1EA0', 'A',        None,        'dotbelow', False, False),
    (0x1EA1, 'uni1EA1', 'a',        None,        'dotbelow', False, False),
    (0x1EA2, 'uni1EA2', 'A',        'hookabove', None,       False, False),
    (0x1EA3, 'uni1EA3', 'a',        'hookabove', None,       False, False),
    (0x1EA4, 'uni1EA4', 'A',        'acute',     None,       True,  False),
    (0x1EA5, 'uni1EA5', 'a',        'acute',     None,       True,  False),
    (0x1EA6, 'uni1EA6', 'A',        'grave',     None,       True,  False),
    (0x1EA7, 'uni1EA7', 'a',        'grave',     None,       True,  False),
    (0x1EA8, 'uni1EA8', 'A',        'hookabove', None,       True,  False),
    (0x1EA9, 'uni1EA9', 'a',        'hookabove', None,       True,  False),
    (0x1EAA, 'uni1EAA', 'A',        'tilde',     None,       True,  False),
    (0x1EAB, 'uni1EAB', 'a',        'tilde',     None,       True,  False),
    (0x1EAC, 'uni1EAC', 'A',        None,        'dotbelow', True,  False),
    (0x1EAD, 'uni1EAD', 'a',        None,        'dotbelow', True,  False),
    (0x1EAE, 'uni1EAE', 'A',        'acute',     None,       False, True),
    (0x1EAF, 'uni1EAF', 'a',        'acute',     None,       False, True),
    (0x1EB0, 'uni1EB0', 'A',        'grave',     None,       False, True),
    (0x1EB1, 'uni1EB1', 'a',        'grave',     None,       False, True),
    (0x1EB2, 'uni1EB2', 'A',        'hookabove', None,       False, True),
    (0x1EB3, 'uni1EB3', 'a',        'hookabove', None,       False, True),
    (0x1EB4, 'uni1EB4', 'A',        'tilde',     None,       False, True),
    (0x1EB5, 'uni1EB5', 'a',        'tilde',     None,       False, True),
    (0x1EB6, 'uni1EB6', 'A',        None,        'dotbelow', False, True),
    (0x1EB7, 'uni1EB7', 'a',        None,        'dotbelow', False, True),
    # ── E/e-based ────────────────────────────────────────────────────────────
    (0x1EB8, 'uni1EB8', 'E',        None,        'dotbelow', False, False),
    (0x1EB9, 'uni1EB9', 'e',        None,        'dotbelow', False, False),
    (0x1EBA, 'uni1EBA', 'E',        'hookabove', None,       False, False),
    (0x1EBB, 'uni1EBB', 'e',        'hookabove', None,       False, False),
    (0x1EBC, 'uni1EBC', 'E',        'tilde',     None,       False, False),
    (0x1EBD, 'uni1EBD', 'e',        'tilde',     None,       False, False),
    (0x1EBE, 'uni1EBE', 'E',        'acute',     None,       True,  False),
    (0x1EBF, 'uni1EBF', 'e',        'acute',     None,       True,  False),
    (0x1EC0, 'uni1EC0', 'E',        'grave',     None,       True,  False),
    (0x1EC1, 'uni1EC1', 'e',        'grave',     None,       True,  False),
    (0x1EC2, 'uni1EC2', 'E',        'hookabove', None,       True,  False),
    (0x1EC3, 'uni1EC3', 'e',        'hookabove', None,       True,  False),
    (0x1EC4, 'uni1EC4', 'E',        'tilde',     None,       True,  False),
    (0x1EC5, 'uni1EC5', 'e',        'tilde',     None,       True,  False),
    (0x1EC6, 'uni1EC6', 'E',        None,        'dotbelow', True,  False),
    (0x1EC7, 'uni1EC7', 'e',        None,        'dotbelow', True,  False),
    # ── I/i-based (use dotlessi for lowercase so dot doesn't clash) ───────────
    (0x1EC8, 'uni1EC8', 'I',        'hookabove', None,       False, False),
    (0x1EC9, 'uni1EC9', 'dotlessi', 'hookabove', None,       False, False),
    (0x1ECA, 'uni1ECA', 'I',        None,        'dotbelow', False, False),
    (0x1ECB, 'uni1ECB', 'dotlessi', None,        'dotbelow', False, False),
    # ── O/o-based ────────────────────────────────────────────────────────────
    (0x1ECC, 'uni1ECC', 'O',        None,        'dotbelow', False, False),
    (0x1ECD, 'uni1ECD', 'o',        None,        'dotbelow', False, False),
    (0x1ECE, 'uni1ECE', 'O',        'hookabove', None,       False, False),
    (0x1ECF, 'uni1ECF', 'o',        'hookabove', None,       False, False),
    (0x1ED0, 'uni1ED0', 'O',        'acute',     None,       True,  False),
    (0x1ED1, 'uni1ED1', 'o',        'acute',     None,       True,  False),
    (0x1ED2, 'uni1ED2', 'O',        'grave',     None,       True,  False),
    (0x1ED3, 'uni1ED3', 'o',        'grave',     None,       True,  False),
    (0x1ED4, 'uni1ED4', 'O',        'hookabove', None,       True,  False),
    (0x1ED5, 'uni1ED5', 'o',        'hookabove', None,       True,  False),
    (0x1ED6, 'uni1ED6', 'O',        'tilde',     None,       True,  False),
    (0x1ED7, 'uni1ED7', 'o',        'tilde',     None,       True,  False),
    (0x1ED8, 'uni1ED8', 'O',        None,        'dotbelow', True,  False),
    (0x1ED9, 'uni1ED9', 'o',        None,        'dotbelow', True,  False),
    # ── Ohorn/ohorn-based ────────────────────────────────────────────────────
    (0x1EDA, 'uni1EDA', 'Ohorn',    'acute',     None,       False, False),
    (0x1EDB, 'uni1EDB', 'ohorn',    'acute',     None,       False, False),
    (0x1EDC, 'uni1EDC', 'Ohorn',    'grave',     None,       False, False),
    (0x1EDD, 'uni1EDD', 'ohorn',    'grave',     None,       False, False),
    (0x1EDE, 'uni1EDE', 'Ohorn',    'hookabove', None,       False, False),
    (0x1EDF, 'uni1EDF', 'ohorn',    'hookabove', None,       False, False),
    (0x1EE0, 'uni1EE0', 'Ohorn',    'tilde',     None,       False, False),
    (0x1EE1, 'uni1EE1', 'ohorn',    'tilde',     None,       False, False),
    (0x1EE2, 'uni1EE2', 'Ohorn',    None,        'dotbelow', False, False),
    (0x1EE3, 'uni1EE3', 'ohorn',    None,        'dotbelow', False, False),
    # ── U/u-based ────────────────────────────────────────────────────────────
    (0x1EE4, 'uni1EE4', 'U',        None,        'dotbelow', False, False),
    (0x1EE5, 'uni1EE5', 'u',        None,        'dotbelow', False, False),
    (0x1EE6, 'uni1EE6', 'U',        'hookabove', None,       False, False),
    (0x1EE7, 'uni1EE7', 'u',        'hookabove', None,       False, False),
    # ── Uhorn/uhorn-based ────────────────────────────────────────────────────
    (0x1EE8, 'uni1EE8', 'Uhorn',    'acute',     None,       False, False),
    (0x1EE9, 'uni1EE9', 'uhorn',    'acute',     None,       False, False),
    (0x1EEA, 'uni1EEA', 'Uhorn',    'grave',     None,       False, False),
    (0x1EEB, 'uni1EEB', 'uhorn',    'grave',     None,       False, False),
    (0x1EEC, 'uni1EEC', 'Uhorn',    'hookabove', None,       False, False),
    (0x1EED, 'uni1EED', 'uhorn',    'hookabove', None,       False, False),
    (0x1EEE, 'uni1EEE', 'Uhorn',    'tilde',     None,       False, False),
    (0x1EEF, 'uni1EEF', 'uhorn',    'tilde',     None,       False, False),
    (0x1EF0, 'uni1EF0', 'Uhorn',    None,        'dotbelow', False, False),
    (0x1EF1, 'uni1EF1', 'uhorn',    None,        'dotbelow', False, False),
    # ── Y/y-based (Ỳ/ỳ U+1EF2/U+1EF3 already in font) ───────────────────────
    (0x1EF4, 'uni1EF4', 'Y',        None,        'dotbelow', False, False),
    (0x1EF5, 'uni1EF5', 'y',        None,        'dotbelow', False, False),
    (0x1EF6, 'uni1EF6', 'Y',        'hookabove', None,       False, False),
    (0x1EF7, 'uni1EF7', 'y',        'hookabove', None,       False, False),
    (0x1EF8, 'uni1EF8', 'Y',        'tilde',     None,       False, False),
    (0x1EF9, 'uni1EF9', 'y',        'tilde',     None,       False, False),
]

# Unicode values for already-present glyphs (skip these)
ALREADY_PRESENT = {0x1EF2, 0x1EF3}  # Ỳ/ỳ


def parse_glyphs(content):
    """Return dict: glyph_name → {enc, uni, slot, width, anchors}."""
    glyphs = {}
    for sc_m in re.finditer(r'^StartChar: (\S+)$', content, re.MULTILINE):
        name = sc_m.group(1)
        # Extract up to the EndChar marker (or next StartChar)
        start = sc_m.start()
        end_m = re.search(r'^EndChar$', content[start:], re.MULTILINE)
        block = content[start: start + (end_m.end() if end_m else 1000)]

        enc_m  = re.search(r'^Encoding: (\d+) (-?\d+) (\d+)$', block, re.MULTILINE)
        wid_m  = re.search(r'^Width: (\d+)$', block, re.MULTILINE)
        if not enc_m or not wid_m:
            continue

        enc, uni, slot = enc_m.groups()
        width = wid_m.group(1)
        anchors = {}
        for am in re.finditer(r'AnchorPoint: "Anchor-(\d)" (\d+) (-?\d+) (\w+)', block):
            aid, ax, ay, atype = am.groups()
            anchors[int(aid)] = (int(ax), int(ay), atype)
        glyphs[name] = {
            'enc': int(enc),
            'uni': int(uni),
            'slot': int(slot),
            'width': int(width),
            'anchors': anchors,
        }
    return glyphs


def mark_dx_dy(glyphs, base_name, mark_name, anchor_id=0):
    """Compute (dx, dy) to place mark's anchor_id at base's anchor_id."""
    base = glyphs.get(base_name, {}).get('anchors', {}).get(anchor_id)
    mark = glyphs.get(mark_name, {}).get('anchors', {}).get(anchor_id)
    if base is None or mark is None:
        return 0, 0
    return base[0] - mark[0], base[1] - mark[1]


def make_hookabovecomb(slot, anchor_x, shape):
    return f"""StartChar: uni0309
Encoding: 777 777 {slot}
Width: 0
Flags: MW
AnchorPoint: "Anchor-0" {anchor_x} 1500 mark 0
LayerCount: 2
Fore
SplineSet
{shape}
EndSplineSet
EndChar

"""


def make_combining_horn(slot, shape):
    return f"""StartChar: uni031B
Encoding: 795 795 {slot}
Width: 0
Flags: W
LayerCount: 2
Fore
SplineSet
{shape}
EndSplineSet
EndChar

"""


def make_horn_base(uni, name, base_name, base_slot, base_uni,
                   base_width, base_anchors,
                   horn_slot, horn_dx, horn_dy):
    """Generate Ơ, ơ, Ư, or ư as composite of base + horn."""
    a0 = base_anchors.get(0)
    a1 = base_anchors.get(1)
    anchor_lines = ''
    if a0:
        anchor_lines += f'AnchorPoint: "Anchor-0" {a0[0]} {a0[1]} basechar 0\n'
    if a1:
        anchor_lines += f'AnchorPoint: "Anchor-1" {a1[0]} {a1[1]} basechar 0\n'
    # slot numbering: assign after horn_slot
    return f"""StartChar: {name}
Encoding: {uni} {uni} {horn_slot + 1}
Width: {base_width}
Flags: M
{anchor_lines}LayerCount: 2
Fore
Refer: {horn_slot} 795 N 1 0 0 1 {horn_dx} {horn_dy} 2
Refer: {base_slot} {base_uni} N 1 0 0 1 0 0 3
EndChar

"""


def make_composite(uni, name, slot,
                   base_name, base_slot, base_uni, base_width,
                   above_name, above_slot, above_dx, above_dy,
                   below_name, below_slot, below_dx, below_dy,
                   circ_name=None, circ_slot=None, circ_dx=None,
                   breve_name=None, breve_slot=None, breve_dx=None):
    """Build SFD text for a composite Vietnamese glyph."""
    lines = []
    lines.append(f'StartChar: {name}')
    lines.append(f'Encoding: {uni} {uni} {slot}')
    lines.append(f'Width: {base_width}')
    lines.append('Flags: M')
    lines.append('LayerCount: 2')
    lines.append('Fore')
    # References: marks first (flag 2), base last (flag 3)
    if above_name and above_dx is not None:
        lines.append(f'Refer: {above_slot} {_mark_uni(above_name)} N 1 0 0 1 {above_dx} {above_dy} 2')
    if below_name and below_dx is not None:
        lines.append(f'Refer: {below_slot} 803 N 1 0 0 1 {below_dx} {below_dy} 2')
    if circ_name:
        lines.append(f'Refer: {circ_slot} 770 N 1 0 0 1 {circ_dx} 0 2')
    if breve_name:
        lines.append(f'Refer: {breve_slot} 728 N 1 0 0 1 {breve_dx} 0 2')
    lines.append(f'Refer: {base_slot} {base_uni} N 1 0 0 1 0 0 3')
    lines.append('EndChar')
    lines.append('')
    return '\n'.join(lines) + '\n'


def _mark_uni(mark_name):
    return {
        'grave': 768, 'acute': 769, 'tilde': 771,
        'hookabove': 777, 'dotbelow': 803,
    }.get(mark_name, 0)


def add_vietnamese(sfd_path):
    fname = os.path.basename(sfd_path)
    if fname not in MASTER_CFG:
        print(f'  Skipping unknown file: {fname}')
        return

    style, hookabove_anchor_x, circ_top, breve_top, hookabove_shape, horn_shape = MASTER_CFG[fname]

    with open(sfd_path, 'r') as f:
        content = f.read()

    glyphs = parse_glyphs(content)

    # Existing Unicode set (skip already-present Vietnamese chars)
    existing_unis = {g['uni'] for g in glyphs.values() if g['uni'] >= 0}

    # Current glyph count and next slot
    m = re.search(r'BeginChars: (\d+) (\d+)', content)
    total_slots, glyph_count = int(m.group(1)), int(m.group(2))
    next_slot = max(g['slot'] for g in glyphs.values()) + 1

    # Mark glyph slots/anchors
    def gslot(name):
        return glyphs[name]['slot'] if name in glyphs else None

    def gwidth(name):
        return glyphs[name]['width'] if name in glyphs else 0

    def ganchors(name):
        return glyphs[name]['anchors'] if name in glyphs else {}

    grave_slot   = gslot('gravecomb')
    acute_slot   = gslot('acutecomb')
    circ_slot    = gslot('uni0302')
    tilde_slot   = gslot('tildecomb')
    breve_slot   = gslot('breve')      # spacing breve U+02D8, used in composites
    dotbelow_slot = gslot('dotbelowcomb')

    grave_ax  = glyphs['gravecomb']['anchors'][0][0]
    acute_ax  = glyphs['acutecomb']['anchors'][0][0]
    circ_ax   = glyphs['uni0302']['anchors'][0][0]
    tilde_ax  = glyphs['tildecomb']['anchors'][0][0]
    breve_ax  = glyphs['breve']['anchors'][0][0]
    dotbelow_ax = glyphs['dotbelowcomb']['anchors'][1][0]

    new_glyphs = []
    added_unis = set()

    def add(text, uni):
        if uni not in existing_unis and uni not in added_unis:
            new_glyphs.append(text)
            added_unis.add(uni)

    # ── 1. hookabovecomb (U+0309) ─────────────────────────────────────────────
    hookabove_slot = next_slot
    add(make_hookabovecomb(hookabove_slot, hookabove_anchor_x, hookabove_shape), 0x0309)

    # ── 2. combining horn (U+031B) ────────────────────────────────────────────
    horn_slot = hookabove_slot + (0 if 0x0309 in existing_unis else 1)
    if 0x0309 in existing_unis:
        hookabove_slot = gslot('uni0309') or hookabove_slot
        horn_slot = next_slot
    horn_uni_slot = horn_slot
    add(make_combining_horn(horn_slot, horn_shape), 0x031B)

    def next_avail():
        """Return incrementing slot after last added."""
        return next_slot + len(new_glyphs)

    # Recalculate hookabove slot after possible additions
    if 0x0309 in existing_unis:
        hookabove_slot_actual = gslot('uni0309')
    else:
        hookabove_slot_actual = hookabove_slot

    if 0x031B in existing_unis:
        horn_slot_actual = gslot('uni031B')
    else:
        horn_slot_actual = horn_slot

    # ── 3. Ơ (U+01A0) ────────────────────────────────────────────────────────
    O_slot   = glyphs['O']['slot']
    O_width  = glyphs['O']['width']
    O_anchors = glyphs['O']['anchors']
    O_a0x = O_anchors[0][0] if 0 in O_anchors else O_width // 2
    horn_dx_O = int(O_width * 0.88)
    horn_dy_O = 1240

    ohorn_text = make_horn_base(
        0x01A0, 'Ohorn',
        'O', O_slot, 79, O_width, O_anchors,
        horn_slot_actual, horn_dx_O, horn_dy_O,
    )
    # Fix: make_horn_base uses horn_slot_actual + 1 for the Ohorn slot
    Ohorn_slot = next_slot + len(new_glyphs) + (0 if 0x01A0 in existing_unis else 0)
    add(ohorn_text, 0x01A0)
    Ohorn_slot_actual = (gslot('Ohorn') if 0x01A0 in existing_unis
                         else next_slot + new_glyphs.index(ohorn_text))

    # ── 4. ơ (U+01A1) ────────────────────────────────────────────────────────
    o_slot   = glyphs['o']['slot']
    o_width  = glyphs['o']['width']
    o_anchors = glyphs['o']['anchors']
    horn_dx_o = int(o_width * 0.90)
    horn_dy_o = 810

    ohorn_lc_text = make_horn_base(
        0x01A1, 'ohorn',
        'o', o_slot, 111, o_width, o_anchors,
        horn_slot_actual, horn_dx_o, horn_dy_o,
    )
    add(ohorn_lc_text, 0x01A1)

    # ── 5. Ư (U+01AF) ────────────────────────────────────────────────────────
    U_slot   = glyphs['U']['slot']
    U_width  = glyphs['U']['width']
    U_anchors = glyphs['U']['anchors']
    horn_dx_U = int(U_width * 0.94)
    horn_dy_U = 1260

    Uhorn_text = make_horn_base(
        0x01AF, 'Uhorn',
        'U', U_slot, 85, U_width, U_anchors,
        horn_slot_actual, horn_dx_U, horn_dy_U,
    )
    add(Uhorn_text, 0x01AF)

    # ── 6. ư (U+01B0) ────────────────────────────────────────────────────────
    u_slot   = glyphs['u']['slot']
    u_width  = glyphs['u']['width']
    u_anchors = glyphs['u']['anchors']
    horn_dx_u = int(u_width * 0.85)
    horn_dy_u = 800

    uhorn_text = make_horn_base(
        0x01B0, 'uhorn',
        'u', u_slot, 117, u_width, u_anchors,
        horn_slot_actual, horn_dx_u, horn_dy_u,
    )
    add(uhorn_text, 0x01B0)

    # Rebuild full glyph map after adding the horn-base glyphs (approximate slots)
    # The actual slots will be sequential from next_slot
    def slot_of(name, uni_val):
        if name in glyphs:
            return glyphs[name]['slot']
        # Compute from addition order
        for idx, (g_text) in enumerate(new_glyphs):
            if f'Encoding: {uni_val} {uni_val}' in g_text:
                return next_slot + idx
        return None

    Ohorn_s  = slot_of('Ohorn',  0x01A0)
    ohorn_s  = slot_of('ohorn',  0x01A1)
    Uhorn_s  = slot_of('Uhorn',  0x01AF)
    uhorn_s  = slot_of('uhorn',  0x01B0)
    hkabv_s  = slot_of('uni0309',0x0309) or hookabove_slot_actual

    # ── 7. Precomposed Vietnamese characters ──────────────────────────────────
    # Stacking dy: tone mark above circumflex or breve
    dy_stack_circ  = circ_top  - 1500
    dy_stack_breve = breve_top - 1500

    for uni, name, base_name, above_mark, below_mark, use_circ, use_breve in VIET_CHARS:
        if uni in ALREADY_PRESENT or uni in existing_unis or uni in added_unis:
            continue

        is_upper = base_name[0].isupper() or base_name in ('Ohorn', 'Uhorn')
        # Map internal name to actual glyph
        base_map = {
            'Ohorn': ('Ohorn', 0x01A0, Ohorn_s),
            'ohorn': ('ohorn', 0x01A1, ohorn_s),
            'Uhorn': ('Uhorn', 0x01AF, Uhorn_s),
            'uhorn': ('uhorn', 0x01B0, uhorn_s),
        }
        if base_name in base_map:
            actual_base, base_uni_val, bslot = base_map[base_name]
        else:
            actual_base = base_name
            base_uni_val = glyphs[base_name]['uni'] if base_name in glyphs else 0
            bslot = glyphs[base_name]['slot'] if base_name in glyphs else 0

        if bslot is None:
            print(f'  Warning: base glyph {base_name!r} not found, skipping {name}')
            continue

        bwidth = glyphs[actual_base]['width'] if actual_base in glyphs else (
            glyphs['O']['width'] if is_upper else glyphs['o']['width'])
        banchors = glyphs[actual_base]['anchors'] if actual_base in glyphs else {}

        base_a0 = banchors.get(0)
        base_a1 = banchors.get(1)
        b_a0x = base_a0[0] if base_a0 else bwidth // 2
        b_a0y = base_a0[1] if base_a0 else (1500 if is_upper else 1040)
        b_a1x = base_a1[0] if base_a1 else bwidth // 2
        b_a1y = base_a1[1] if base_a1 else 0

        # Compute above-mark position
        adx = ady = None
        am_slot = None
        if above_mark:
            mark_slot_map = {
                'grave':      (grave_slot,    grave_ax,  0),
                'acute':      (acute_slot,    acute_ax,  0),
                'tilde':      (tilde_slot,    tilde_ax,  0),
                'hookabove':  (hkabv_s,       hookabove_anchor_x, 0),
            }
            if above_mark in mark_slot_map:
                am_slot, am_ax, am_ay = mark_slot_map[above_mark]
                stack_dy = 0
                if use_circ:
                    stack_dy = dy_stack_circ
                elif use_breve:
                    stack_dy = dy_stack_breve
                adx = b_a0x - am_ax
                ady = (b_a0y - 1500) + stack_dy  # relative to mark anchor at y=1500

        # Compute below-mark position
        bdx = bdy = None
        bm_slot = None
        if below_mark == 'dotbelow' and dotbelow_slot is not None:
            bm_slot = dotbelow_slot
            bdx = b_a1x - dotbelow_ax
            bdy = b_a1y  # dotbelowcomb anchor is at y=0

        # Circumflex or breve component
        c_slot = c_dx = None
        bv_slot = bv_dx = None
        if use_circ:
            c_slot = circ_slot
            c_dx = b_a0x - circ_ax
        if use_breve:
            bv_slot = breve_slot
            bv_dx = b_a0x - breve_ax

        composite_slot = next_slot + len(new_glyphs)
        text = make_composite(
            uni, name, composite_slot,
            actual_base, bslot, base_uni_val, bwidth,
            above_mark, am_slot, adx, ady,
            below_mark, bm_slot, bdx, bdy,
            circ_name='uni0302' if use_circ else None,
            circ_slot=c_slot, circ_dx=c_dx,
            breve_name='breve' if use_breve else None,
            breve_slot=bv_slot, breve_dx=bv_dx,
        )
        add(text, uni)

    if not new_glyphs:
        print(f'  {fname}: no new glyphs needed')
        return

    # Fix slot numbers in generated glyph text (make_horn_base used wrong slot)
    # Rewrite all generated glyph texts with correct sequential slots
    corrected = []
    for idx, text in enumerate(new_glyphs):
        correct_slot = next_slot + idx
        # Replace the Encoding slot (third number) with correct value
        text = re.sub(
            r'^(Encoding: \d+ -?\d+ )\d+',
            lambda m2: m2.group(1) + str(correct_slot),
            text, flags=re.MULTILINE
        )
        corrected.append(text)

    new_content = ''.join(corrected)
    new_count = glyph_count + len(new_glyphs)

    # Update BeginChars count
    updated = content.replace(
        f'BeginChars: {total_slots} {glyph_count}',
        f'BeginChars: {total_slots} {new_count}'
    )
    # Append new glyphs at end of file
    updated = updated.rstrip() + '\n\n' + new_content

    with open(sfd_path, 'w') as f:
        f.write(updated)

    print(f'  {fname}: added {len(new_glyphs)} glyphs (total now {new_count})')


def update_features_fea():
    """Add new Vietnamese glyphs to GDEF classes in features.fea."""
    fea_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'misc', 'features.fea')
    with open(fea_path, 'r') as f:
        content = f.read()

    # New mark glyphs
    new_marks = ' \\uni0309 \\uni031B'
    # New base glyphs (precomposed Vietnamese)
    new_bases = (
        ' \\Ohorn \\ohorn \\Uhorn \\uhorn'
        ' \\uni1EA0 \\uni1EA1 \\uni1EA2 \\uni1EA3'
        ' \\uni1EA4 \\uni1EA5 \\uni1EA6 \\uni1EA7'
        ' \\uni1EA8 \\uni1EA9 \\uni1EAA \\uni1EAB'
        ' \\uni1EAC \\uni1EAD \\uni1EAE \\uni1EAF'
        ' \\uni1EB0 \\uni1EB1 \\uni1EB2 \\uni1EB3'
        ' \\uni1EB4 \\uni1EB5 \\uni1EB6 \\uni1EB7'
        ' \\uni1EB8 \\uni1EB9 \\uni1EBA \\uni1EBB'
        ' \\uni1EBC \\uni1EBD \\uni1EBE \\uni1EBF'
        ' \\uni1EC0 \\uni1EC1 \\uni1EC2 \\uni1EC3'
        ' \\uni1EC4 \\uni1EC5 \\uni1EC6 \\uni1EC7'
        ' \\uni1EC8 \\uni1EC9 \\uni1ECA \\uni1ECB'
        ' \\uni1ECC \\uni1ECD \\uni1ECE \\uni1ECF'
        ' \\uni1ED0 \\uni1ED1 \\uni1ED2 \\uni1ED3'
        ' \\uni1ED4 \\uni1ED5 \\uni1ED6 \\uni1ED7'
        ' \\uni1ED8 \\uni1ED9 \\uni1EDA \\uni1EDB'
        ' \\uni1EDC \\uni1EDD \\uni1EDE \\uni1EDF'
        ' \\uni1EE0 \\uni1EE1 \\uni1EE2 \\uni1EE3'
        ' \\uni1EE4 \\uni1EE5 \\uni1EE6 \\uni1EE7'
        ' \\uni1EE8 \\uni1EE9 \\uni1EEA \\uni1EEB'
        ' \\uni1EEC \\uni1EED \\uni1EEE \\uni1EEF'
        ' \\uni1EF0 \\uni1EF1 \\uni1EF4 \\uni1EF5'
        ' \\uni1EF6 \\uni1EF7 \\uni1EF8 \\uni1EF9'
    )

    # Add to @GDEF_Mark if not already present
    if '\\uni0309' not in content:
        content = re.sub(
            r'(@GDEF_Mark = \[.*?)(\s*\];)',
            lambda m: m.group(1) + new_marks + m.group(2),
            content, flags=re.DOTALL
        )

    # Add Vietnamese bases to @GDEF_Simple if not already present
    if '\\uni1EA0' not in content:
        content = re.sub(
            r'(@GDEF_Simple = \[.*?)(\s*\];)',
            lambda m: m.group(1) + new_bases + m.group(2),
            content, flags=re.DOTALL
        )

    # Add 'viet' language system if not present
    if 'languagesystem latn VIT' not in content and 'viết' not in content:
        content = content.replace(
            'languagesystem latn dflt;',
            'languagesystem latn dflt;\nlanguagesystem latn VIT ;'
        )

    with open(fea_path, 'w') as f:
        f.write(content)
    print('  features.fea: updated GDEF classes')


def main():
    print('Adding Vietnamese glyph support to Besley SFD files...')
    for fname in sorted(MASTER_CFG.keys()):
        sfd_path = os.path.join(SFD_DIR, fname)
        if os.path.exists(sfd_path):
            add_vietnamese(sfd_path)
        else:
            print(f'  File not found: {sfd_path}')

    update_features_fea()
    print('Done.')


if __name__ == '__main__':
    main()
