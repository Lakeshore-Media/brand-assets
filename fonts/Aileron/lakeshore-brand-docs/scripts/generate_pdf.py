#!/usr/bin/env python3
"""
Lakeshore Media — On-Brand PDF Generator
Generates professional PDFs following the Lakeshore Media brand guidelines.

Usage:
    python generate_pdf.py --type proposal --output proposal.pdf --data data.json
    python generate_pdf.py --type freebie --output freebie.pdf --data data.json
    python generate_pdf.py --type mailing --output mailing.pdf --data data.json

The --data flag points to a JSON file with the document content.
See the examples in this file's docstrings for the expected JSON structure.
"""

import json
import sys
import os
import math
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.units import mm, cm, inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle

# ── Brand Colors ──────────────────────────────────────────────────────────────

NEAR_BLACK = HexColor('#0F1114')
STEEL_BLUE = HexColor('#2E3D51')
WARM_GRAY = HexColor('#6B7280')
OFF_WHITE = HexColor('#ECEAE4')
CREAM_WHITE = HexColor('#F5F3ED')
ACCENT_ORANGE = HexColor('#E8860C')
DARK_CHARCOAL = HexColor('#1E2328')

# ── Font Registration ─────────────────────────────────────────────────────────

def find_font_dir(base_paths, sub_path):
    """Search multiple base paths for a font directory."""
    for base in base_paths:
        full = os.path.join(base, sub_path)
        if os.path.exists(full):
            return full
    return None

def convert_otf_to_ttf(otf_path, ttf_path):
    """Convert an OTF font with CFF outlines to TTF with TrueType outlines.

    Reportlab's TTFont doesn't support PostScript/CFF outlines, so we need
    to convert the cubic Bézier curves to quadratic splines (TrueType format).
    """
    try:
        from fontTools.ttLib import TTFont as FTFont
        from fontTools.pens.cu2quPen import Cu2QuPen
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        from fontTools.ttLib.tables._g_l_y_f import table__g_l_y_f, Glyph as EmptyGlyph
        from fontTools.ttLib.tables._l_o_c_a import table__l_o_c_a

        font = FTFont(otf_path)
        if 'CFF ' not in font:
            font.close()
            return otf_path  # Already TrueType, use as-is

        glyphOrder = font.getGlyphOrder()
        glyphSet = font.getGlyphSet()

        glyf = table__g_l_y_f()
        glyf.glyphs = {}
        glyf.glyphOrder = glyphOrder

        for gn in glyphOrder:
            ttPen = TTGlyphPen(glyphSet)
            cu2quPen = Cu2QuPen(ttPen, max_err=1.0, reverse_direction=True)
            try:
                glyphSet[gn].draw(cu2quPen)
                glyf.glyphs[gn] = ttPen.glyph()
            except Exception:
                glyf.glyphs[gn] = EmptyGlyph()

        del font['CFF ']
        font['glyf'] = glyf
        font['loca'] = table__l_o_c_a()
        font['head'].indexToLocFormat = 1

        # Fix sfntVersion from OTTO → TrueType
        font.sfntVersion = '\x00\x01\x00\x00'

        # Fix maxp table: CFF uses version 0x00005000, TrueType needs 0x00010000
        maxp = font['maxp']
        maxp.tableVersion = 0x00010000
        for attr, default in [
            ('maxZones', 2), ('maxTwilightPoints', 0), ('maxStorage', 0),
            ('maxFunctionDefs', 0), ('maxInstructionDefs', 0),
            ('maxStackElements', 0), ('maxSizeOfInstructions', 0),
            ('maxComponentElements', 0), ('maxComponentDepth', 0),
            ('maxPoints', 0), ('maxContours', 0),
            ('maxCompositePoints', 0), ('maxCompositeContours', 0),
        ]:
            if not hasattr(maxp, attr):
                setattr(maxp, attr, default)

        os.makedirs(os.path.dirname(ttf_path), exist_ok=True)
        font.save(ttf_path)
        font.close()
        return ttf_path
    except ImportError:
        print("Warning: fonttools/cu2qu not available — install with: pip install fonttools cu2qu")
        return None
    except Exception as e:
        print(f"Warning: Could not convert {otf_path}: {e}")
        return None


def register_fonts():
    """Register Aileron and Lato fonts from brand assets.

    Aileron ships as OTF with CFF (PostScript) outlines, which reportlab can't
    handle directly. We convert them to TTF on the fly and cache the result
    in a temp directory.
    """
    # Possible base paths where fonts might be
    base_paths = [
        '/sessions/admiring-festive-dirac/mnt/01_a_Lakeshore_Media',
        '/sessions/admiring-festive-dirac/mnt/Aileron',
        os.environ.get('BRAND_ASSETS_DIR', ''),
    ]

    # Directory for converted TTF fonts
    import tempfile
    ttf_cache = os.path.join(tempfile.gettempdir(), 'lakeshore_fonts_ttf')
    os.makedirs(ttf_cache, exist_ok=True)

    # Aileron (OTF → needs conversion to TTF)
    aileron_dir = find_font_dir(base_paths, 'fonts/Aileron/aileron')
    if not aileron_dir:
        aileron_dir = find_font_dir(base_paths, 'aileron')

    if aileron_dir:
        font_map = {
            'Aileron': 'Aileron-Regular.otf',
            'Aileron-Bold': 'Aileron-Bold.otf',
            'Aileron-Heavy': 'Aileron-Heavy.otf',
            'Aileron-Light': 'Aileron-Light.otf',
            'Aileron-SemiBold': 'Aileron-SemiBold.otf',
            'Aileron-Black': 'Aileron-Black.otf',
            'Aileron-Thin': 'Aileron-Thin.otf',
        }
        for name, filename in font_map.items():
            otf_path = os.path.join(aileron_dir, filename)
            if not os.path.exists(otf_path):
                continue
            ttf_path = os.path.join(ttf_cache, filename.replace('.otf', '.ttf'))
            # Use cached TTF if it exists and is newer than the OTF
            if not os.path.exists(ttf_path):
                ttf_path = convert_otf_to_ttf(otf_path, ttf_path)
            if ttf_path and os.path.exists(ttf_path):
                try:
                    pdfmetrics.registerFont(TTFont(name, ttf_path))
                except Exception as e:
                    print(f"Warning: Could not register {name}: {e}")

    # Lato (already TTF — register directly)
    lato_dir = find_font_dir(base_paths, 'fonts/Lato/Lato')
    if lato_dir:
        lato_map = {
            'Lato': 'Lato-Regular.ttf',
            'Lato-Bold': 'Lato-Bold.ttf',
            'Lato-Light': 'Lato-Light.ttf',
            'Lato-Black': 'Lato-Black.ttf',
        }
        for name, filename in lato_map.items():
            path = os.path.join(lato_dir, filename)
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont(name, path))
                except Exception as e:
                    print(f"Warning: Could not register {name}: {e}")

# ── Drawing Helpers ───────────────────────────────────────────────────────────

def draw_organic_shape(c, x, y, radius, color, rotation=0):
    """Draw an organic blob shape (approximated with overlapping circles)."""
    c.saveState()
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.translate(x, y)
    c.rotate(rotation)
    # Create organic shape with overlapping ellipses
    c.ellipse(-radius*0.8, -radius*0.6, radius*0.8, radius*0.6, fill=1, stroke=0)
    c.ellipse(-radius*0.6, -radius*0.8, radius*0.6, radius*0.8, fill=1, stroke=0)
    c.restoreState()

def draw_corner_accent(c, page_width, page_height, position='top-left', color=STEEL_BLUE):
    """Draw a large organic accent shape in a corner of the page."""
    r = min(page_width, page_height) * 0.25
    positions = {
        'top-left': (-r*0.3, page_height + r*0.3),
        'top-right': (page_width + r*0.3, page_height + r*0.3),
        'bottom-left': (-r*0.3, -r*0.3),
        'bottom-right': (page_width + r*0.3, -r*0.3),
        'left-center': (-r*0.4, page_height * 0.5),
    }
    x, y = positions.get(position, (0, 0))
    draw_organic_shape(c, x, y, r, color, rotation=15)

def draw_footer(c, page_width, page_height, doc_type=""):
    """Draw the standard Lakeshore footer."""
    y = 25
    c.setFont('Aileron-SemiBold' if 'Aileron-SemiBold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold', 7)
    c.setFillColor(OFF_WHITE)
    c.drawString(40, y, "LAKESHORE MEDIA")

    if doc_type:
        c.setFont('Aileron' if 'Aileron' in pdfmetrics.getRegisteredFontNames() else 'Helvetica', 7)
        c.drawRightString(page_width - 40, y, doc_type.upper())

    # Center logo placeholder (small play triangle)
    cx = page_width / 2
    c.setFont('Aileron' if 'Aileron' in pdfmetrics.getRegisteredFontNames() else 'Helvetica', 10)
    c.drawCentredString(cx, y - 1, "▶")

def draw_dark_page(c, w, h):
    """Fill page with near-black background."""
    c.setFillColor(NEAR_BLACK)
    c.rect(0, 0, w, h, fill=1, stroke=0)

def draw_light_page(c, w, h):
    """Fill page with off-white background."""
    c.setFillColor(OFF_WHITE)
    c.rect(0, 0, w, h, fill=1, stroke=0)

def draw_steel_blue_page(c, w, h):
    """Fill page with steel blue background."""
    c.setFillColor(STEEL_BLUE)
    c.rect(0, 0, w, h, fill=1, stroke=0)

def safe_font(preferred, fallback='Helvetica'):
    """Return preferred font name if registered, else fallback."""
    if preferred in pdfmetrics.getRegisteredFontNames():
        return preferred
    return fallback

def draw_wrapped_text(c, text, x, y, max_width, font_name, font_size, color, line_spacing=1.3, align='left'):
    """Draw text with word wrapping. Returns the y position after the last line."""
    c.setFont(font_name, font_size)
    c.setFillColor(color)

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if c.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        if align == 'center':
            c.drawCentredString(x + max_width/2, y, line)
        elif align == 'right':
            c.drawRightString(x + max_width, y, line)
        else:
            c.drawString(x, y, line)
        y -= font_size * line_spacing

    return y


# ── Proposal Generator ────────────────────────────────────────────────────────

def generate_proposal(data, output_path):
    """
    Generate a 16:9 landscape Project Proposal PDF.

    Expected data structure:
    {
        "client_name": "Firma XYZ",
        "client_company": "XYZ GmbH",
        "project_title": "Brand Video Campaign",
        "date": "April 2025",
        "overview": "Brief description of the project concept...",
        "approach_1": {
            "title": "Content Package",
            "description": "The content package will feature..."
        },
        "approach_2": {
            "title": "Hero Video",
            "description": "A 60-second brand film..."
        },
        "goals": [
            "Create high-quality social media videos",
            "Educate audience on core product USPs",
            "Inspire and attract target audience",
            "Drive conversions"
        ],
        "deliverables": [
            {
                "title": "Video 1 - \"Brand Film\"",
                "description": "Features products 1, 2, and 3.",
                "specs": "Approx. 60sec | 16:9 | Website + POS",
                "price": "€2.500"
            }
        ],
        "timeline": [
            {"phase": "Pre-Production", "date": "Week 1-2", "details": "Briefing, Konzept, Planung"},
            {"phase": "Shoot Day", "date": "Week 3", "details": "1 Drehtag vor Ort"},
            {"phase": "Post-Production", "date": "Week 4-5", "details": "Schnitt, Color, Sound"},
            {"phase": "Delivery", "date": "Week 6", "details": "Finale Abnahme + Export"}
        ],
        "investment": {
            "total": "€5.300",
            "payment_terms": "50% bei Auftragsbestätigung, 50% bei Lieferung",
            "includes": "Konzept, Produktion, Post-Production, 2 Revisionsrunden"
        },
        "next_steps": "Lass uns in einem kurzen Call besprechen, wie wir dein Projekt umsetzen.",
        "website": "www.lakeshoremedia.de"
    }
    """
    W, H = landscape(A4)  # ~842 x 595 points
    c = canvas.Canvas(output_path, pagesize=(W, H))

    client = data.get('client_name', '[Client Name]')
    project_title = data.get('project_title', 'PROJECT PROPOSAL')
    date = data.get('date', 'April 2025')
    website = data.get('website', 'www.lakeshoremedia.de')

    # ── COVER PAGE ──
    draw_steel_blue_page(c, W, H)
    draw_corner_accent(c, W, H, 'bottom-left', WARM_GRAY)

    # Top rule
    c.setStrokeColor(OFF_WHITE)
    c.setLineWidth(0.5)
    c.line(40, H - 60, W - 40, H - 60)

    # Header text
    c.setFont(safe_font('Aileron'), 9)
    c.setFillColor(OFF_WHITE)
    c.drawString(40, H - 50, f"PRESENTED TO: {client.upper()}")
    c.drawRightString(W - 40, H - 50, "CREATED BY: RAETO KÖNIGSBAUER")

    # Main title
    title_font = safe_font('Aileron-Black', 'Helvetica-Bold')
    c.setFont(title_font, 72)
    c.setFillColor(CREAM_WHITE)
    c.drawString(40, H - 230, "PROJECT")
    c.drawString(40, H - 310, "PROPOSAL")

    # Orange accent arrow
    c.setFillColor(ACCENT_ORANGE)
    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 48)
    c.drawString(W - 160, H - 280, "↗")

    # Bottom rule + info
    c.setStrokeColor(OFF_WHITE)
    c.line(40, 65, W - 40, 65)
    c.setFont(safe_font('Aileron'), 8)
    c.setFillColor(OFF_WHITE)
    c.drawString(40, 50, date.upper())
    c.drawRightString(W - 40, 50, website.upper())

    draw_footer(c, W, H)
    c.showPage()

    # ── CONTENTS PAGE ──
    draw_light_page(c, W, H)

    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 24)
    c.setFillColor(NEAR_BLACK)
    c.drawString(40, H - 70, "CONTENTS")
    c.setStrokeColor(NEAR_BLACK)
    c.setLineWidth(1)
    c.line(40, H - 80, W - 40, H - 80)

    sections = [
        ("1", "OVERVIEW", "CONCEPT, FORMAT"),
        ("2", "PROJECT MISSION", "CONTENT GOALS"),
        ("3", "DELIVERABLES", "PRODUCTS, USAGE & PLACEMENT"),
        ("4", "MOOD BOARD", "EARLY IDEAS, REFERENCES"),
        ("5", "TONE/FEEL", "ART DIRECTION, EDITING STYLE"),
        ("6", "TIMELINE", "PRE-PRODUCTION, SHOOT DAYS"),
        ("7", "INVESTMENT", "QUOTE, PAYMENT TERMS"),
        ("8", "NEXT STEPS", "CONTACT DETAILS"),
    ]

    col1_x = 60
    col2_x = W/2 + 20
    y_start = H - 140
    spacing = 60

    for i, (num, title, sub) in enumerate(sections):
        col_x = col1_x if i < 4 else col2_x
        y = y_start - (i % 4) * spacing

        c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 14)
        c.setFillColor(NEAR_BLACK)
        c.drawString(col_x, y, num)

        c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 18)
        c.drawString(col_x + 30, y, title)

        c.setFont(safe_font('Aileron'), 8)
        c.setFillColor(WARM_GRAY)
        c.drawString(col_x + 30, y - 16, sub)

    # Orange arrow accent
    c.setFillColor(ACCENT_ORANGE)
    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 28)
    c.drawRightString(W - 50, H - 70, "↗")

    draw_footer(c, W, H, "PROJECT PROPOSAL")
    c.showPage()

    # ── OVERVIEW PAGE ──
    draw_light_page(c, W, H)

    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 11)
    c.setFillColor(STEEL_BLUE)
    c.drawString(40, H - 50, "1")
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 22)
    c.setFillColor(NEAR_BLACK)
    c.drawString(60, H - 50, "OVERVIEW")
    c.setFont(safe_font('Aileron'), 9)
    c.setFillColor(WARM_GRAY)
    c.drawString(60, H - 68, "CONCEPT, FORMAT")

    c.setStrokeColor(NEAR_BLACK)
    c.setLineWidth(0.5)
    c.line(40, H - 78, W - 40, H - 78)

    # Overview text
    overview_text = data.get('overview', 'This proposal outlines an early creative concept, production approach, and content package designed to meet your needs and exceed your expectations.')
    draw_wrapped_text(c, overview_text, 40, H - 120, W/2 - 60, safe_font('Aileron'), 10, NEAR_BLACK, line_spacing=1.5)

    # Approaches
    approach_1 = data.get('approach_1', {})
    approach_2 = data.get('approach_2', {})

    if approach_1:
        y_a = H - 280
        c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 10)
        c.setFillColor(NEAR_BLACK)
        c.drawString(40, y_a, f"[APPROACH 1 - {approach_1.get('title', 'GENERAL PACKAGE').upper()}]")
        draw_wrapped_text(c, approach_1.get('description', ''), 40, y_a - 20, W/2 - 80, safe_font('Aileron'), 9, WARM_GRAY, line_spacing=1.4)

    if approach_2:
        y_b = H - 280
        c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 10)
        c.setFillColor(NEAR_BLACK)
        c.drawString(W/2 + 20, y_b, f"[APPROACH 2 - {approach_2.get('title', 'VIDEO CONCEPT').upper()}]")
        draw_wrapped_text(c, approach_2.get('description', ''), W/2 + 20, y_b - 20, W/2 - 80, safe_font('Aileron'), 9, WARM_GRAY, line_spacing=1.4)

    draw_footer(c, W, H, "PROJECT PROPOSAL")
    c.showPage()

    # ── PROJECT MISSION PAGE ──
    draw_dark_page(c, W, H)
    draw_corner_accent(c, W, H, 'top-right', STEEL_BLUE)

    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 11)
    c.setFillColor(ACCENT_ORANGE)
    c.drawString(40, H - 50, "2")
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 22)
    c.setFillColor(CREAM_WHITE)
    c.drawString(60, H - 50, "PROJECT MISSION")
    c.setFont(safe_font('Aileron'), 9)
    c.setFillColor(OFF_WHITE)
    c.drawString(60, H - 68, "CONTENT GOALS")

    c.setStrokeColor(OFF_WHITE)
    c.setLineWidth(0.5)
    c.line(40, H - 78, W - 40, H - 78)

    goals = data.get('goals', [
        "Create high-quality, engaging content",
        "Educate audience on core USPs",
        "Inspire and attract target audience",
        "Drive conversions and engagement"
    ])

    col_width = (W - 120) / min(len(goals), 4)
    for i, goal in enumerate(goals[:4]):
        x = 50 + i * col_width
        y = H - 180

        # Number
        c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 28)
        c.setFillColor(ACCENT_ORANGE)
        c.drawString(x, y, str(i + 1))

        # Goal text
        draw_wrapped_text(c, goal, x, y - 40, col_width - 30, safe_font('Aileron'), 10, OFF_WHITE, line_spacing=1.4)

    draw_footer(c, W, H, "PROJECT PROPOSAL")
    c.showPage()

    # ── DELIVERABLES PAGE ──
    draw_dark_page(c, W, H)
    draw_corner_accent(c, W, H, 'bottom-right', STEEL_BLUE)

    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 11)
    c.setFillColor(ACCENT_ORANGE)
    c.drawString(40, H - 50, "3")
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 22)
    c.setFillColor(CREAM_WHITE)
    c.drawString(60, H - 50, "DELIVERABLES")
    c.setFont(safe_font('Aileron'), 9)
    c.setFillColor(OFF_WHITE)
    c.drawString(60, H - 68, "FEATURED PRODUCTS, USAGE & PLACEMENT")

    c.setStrokeColor(OFF_WHITE)
    c.setLineWidth(0.5)
    c.line(40, H - 78, W - 40, H - 78)

    deliverables = data.get('deliverables', [])
    col_width = (W - 120) / max(len(deliverables), 1)

    for i, deliv in enumerate(deliverables[:4]):
        x = 50 + i * col_width
        y = H - 130

        # Title
        c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 13)
        c.setFillColor(CREAM_WHITE)
        draw_wrapped_text(c, deliv.get('title', ''), x, y, col_width - 30, safe_font('Aileron-Bold', 'Helvetica-Bold'), 13, CREAM_WHITE)

        # Description
        y_desc = y - 50
        draw_wrapped_text(c, deliv.get('description', ''), x, y_desc, col_width - 30, safe_font('Aileron'), 9, OFF_WHITE, line_spacing=1.4)

        # Specs
        specs = deliv.get('specs', '')
        if specs:
            draw_wrapped_text(c, specs, x, y_desc - 60, col_width - 30, safe_font('Aileron-Light', 'Helvetica'), 8, WARM_GRAY)

        # Price badge
        price = deliv.get('price', '')
        if price:
            badge_y = y_desc - 90
            c.setFillColor(NEAR_BLACK)
            c.roundRect(x, badge_y - 5, 120, 18, 3, fill=1, stroke=0)
            c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 8)
            c.setFillColor(CREAM_WHITE)
            c.drawString(x + 8, badge_y, f"STARTING FROM {price}")

    # Licensing
    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 7)
    c.setFillColor(OFF_WHITE)
    c.drawString(40, 60, "LICENSING")
    c.setFont(safe_font('Aileron'), 7)
    c.setFillColor(WARM_GRAY)
    c.drawString(40, 48, "DIGITAL LICENSE: Website, paid and organic social media, EDMs, PR  |  DURATION: 5 years")

    draw_footer(c, W, H, "PROJECT PROPOSAL")
    c.showPage()

    # ── TIMELINE PAGE ──
    draw_dark_page(c, W, H)
    draw_corner_accent(c, W, H, 'left-center', STEEL_BLUE)

    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 11)
    c.setFillColor(ACCENT_ORANGE)
    c.drawString(40, H - 50, "6")
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 22)
    c.setFillColor(CREAM_WHITE)
    c.drawString(60, H - 50, "TIMELINE")
    c.setFont(safe_font('Aileron'), 9)
    c.setFillColor(OFF_WHITE)
    c.drawString(60, H - 68, "PRE-PRODUCTION, SHOOT DAYS, DEADLINES")

    c.setStrokeColor(OFF_WHITE)
    c.setLineWidth(0.5)
    c.line(40, H - 78, W - 40, H - 78)

    timeline = data.get('timeline', [])
    for i, phase in enumerate(timeline[:6]):
        y = H - 140 - i * 70

        c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 14)
        c.setFillColor(CREAM_WHITE)
        c.drawString(60, y, phase.get('phase', '').upper())

        c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 10)
        c.setFillColor(ACCENT_ORANGE)
        c.drawString(W/2, y, phase.get('date', ''))

        c.setFont(safe_font('Aileron'), 9)
        c.setFillColor(OFF_WHITE)
        c.drawString(W/2, y - 18, phase.get('details', ''))

    draw_footer(c, W, H, "PROJECT PROPOSAL")
    c.showPage()

    # ── INVESTMENT PAGE ──
    draw_dark_page(c, W, H)
    draw_corner_accent(c, W, H, 'top-right', WARM_GRAY)

    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 11)
    c.setFillColor(ACCENT_ORANGE)
    c.drawString(40, H - 50, "7")
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 22)
    c.setFillColor(CREAM_WHITE)
    c.drawString(60, H - 50, "INVESTMENT")
    c.setFont(safe_font('Aileron'), 9)
    c.setFillColor(OFF_WHITE)
    c.drawString(60, H - 68, "QUOTE, PAYMENT TERMS")

    c.setStrokeColor(OFF_WHITE)
    c.setLineWidth(0.5)
    c.line(40, H - 78, W - 40, H - 78)

    investment = data.get('investment', {})

    # Total
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 48)
    c.setFillColor(CREAM_WHITE)
    c.drawString(60, H - 200, investment.get('total', '€X.XXX'))

    # Includes
    includes = investment.get('includes', '')
    if includes:
        c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 11)
        c.setFillColor(OFF_WHITE)
        c.drawString(60, H - 250, "ENTHÄLT:")
        draw_wrapped_text(c, includes, 60, H - 270, W - 200, safe_font('Aileron'), 10, OFF_WHITE, line_spacing=1.4)

    # Payment terms
    terms = investment.get('payment_terms', '')
    if terms:
        c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 11)
        c.setFillColor(OFF_WHITE)
        c.drawString(60, H - 340, "ZAHLUNGSBEDINGUNGEN:")
        draw_wrapped_text(c, terms, 60, H - 360, W - 200, safe_font('Aileron'), 10, OFF_WHITE, line_spacing=1.4)

    draw_footer(c, W, H, "PROJECT PROPOSAL")
    c.showPage()

    # ── NEXT STEPS PAGE ──
    draw_dark_page(c, W, H)
    draw_corner_accent(c, W, H, 'bottom-left', STEEL_BLUE)
    draw_corner_accent(c, W, H, 'top-right', WARM_GRAY)

    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 11)
    c.setFillColor(ACCENT_ORANGE)
    c.drawString(40, H - 50, "8")
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 22)
    c.setFillColor(CREAM_WHITE)
    c.drawString(60, H - 50, "NEXT STEPS")

    c.setStrokeColor(OFF_WHITE)
    c.setLineWidth(0.5)
    c.line(40, H - 65, W - 40, H - 65)

    # CTA text
    next_steps = data.get('next_steps', 'Lass uns in einem kurzen Call besprechen, wie wir dein Projekt zum Leben erwecken.')
    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 18)
    c.setFillColor(CREAM_WHITE)
    draw_wrapped_text(c, next_steps, 60, H - 180, W - 200, safe_font('Aileron-Bold', 'Helvetica-Bold'), 18, CREAM_WHITE, line_spacing=1.5)

    # Contact details
    y_contact = H - 330
    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 12)
    c.setFillColor(OFF_WHITE)
    c.drawString(60, y_contact, "Raeto Königsbauer")
    c.setFont(safe_font('Aileron'), 10)
    c.drawString(60, y_contact - 22, "+49 (0) 172 63670609")
    c.drawString(60, y_contact - 40, "raeto@lakeshoremedia.de")
    c.drawString(60, y_contact - 58, "Ammersee · München, Deutschland")

    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 10)
    c.setFillColor(ACCENT_ORANGE)
    c.drawString(60, y_contact - 88, website.upper())

    draw_footer(c, W, H, "PROJECT PROPOSAL")
    c.showPage()

    c.save()
    print(f"✓ Proposal saved to: {output_path}")


# ── Freebie/Lead Magnet Generator ─────────────────────────────────────────────

def generate_freebie(data, output_path):
    """
    Generate an A4 portrait Lead Magnet / Freebie PDF.

    Expected data structure:
    {
        "title": "10x ROAS Framework",
        "subtitle": "Wie du mit Video-Content deinen Return on Ad Spend verzehnfachst",
        "sections": [
            {
                "title": "Schritt 1: Audience Research",
                "content": "Bevor du auch nur eine Kamera anfasst..."
            }
        ],
        "cta": {
            "text": "Bereit, deinen ROAS zu maximieren?",
            "action": "Buch dir ein kostenloses Strategiegespräch",
            "url": "www.lakeshoremedia.de"
        }
    }
    """
    W, H = A4  # ~595 x 842 points
    c = canvas.Canvas(output_path, pagesize=A4)

    title = data.get('title', 'GUIDE')
    subtitle = data.get('subtitle', '')
    sections = data.get('sections', [])

    # ── COVER ──
    draw_dark_page(c, W, H)
    draw_corner_accent(c, W, H, 'top-right', STEEL_BLUE)
    draw_corner_accent(c, W, H, 'bottom-left', WARM_GRAY)

    # Title — use draw_wrapped_text which returns the y after the last line
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 36)
    c.setFillColor(CREAM_WHITE)
    title_end_y = draw_wrapped_text(c, title.upper(), 50, H - 250, W - 100, safe_font('Aileron-Black', 'Helvetica-Bold'), 36, CREAM_WHITE)

    # Subtitle — positioned dynamically below the title with breathing room
    if subtitle:
        draw_wrapped_text(c, subtitle, 50, title_end_y - 30, W - 100, safe_font('Aileron'), 14, OFF_WHITE, line_spacing=1.5)

    # Branding
    c.setFont(safe_font('Aileron-SemiBold', 'Helvetica-Bold'), 10)
    c.setFillColor(OFF_WHITE)
    c.drawString(50, 80, "LAKESHORE MEDIA")
    c.setFont(safe_font('Aileron'), 9)
    c.setFillColor(WARM_GRAY)
    c.drawString(50, 64, "lakeshoremedia.de")

    draw_footer(c, W, H, "GUIDE")
    c.showPage()

    # ── CONTENT PAGES ──
    for i, section in enumerate(sections):
        draw_dark_page(c, W, H)

        # Alternate accent positions
        if i % 2 == 0:
            draw_corner_accent(c, W, H, 'left-center', STEEL_BLUE)
        else:
            draw_corner_accent(c, W, H, 'top-right', STEEL_BLUE)

        # Section number
        c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 60)
        c.setFillColor(ACCENT_ORANGE)
        c.drawString(50, H - 120, f"{i + 1:02d}")

        # Section title
        c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 22)
        c.setFillColor(CREAM_WHITE)
        draw_wrapped_text(c, section.get('title', '').upper(), 50, H - 170, W - 100, safe_font('Aileron-Black', 'Helvetica-Bold'), 22, CREAM_WHITE)

        # Section content
        content = section.get('content', '')
        draw_wrapped_text(c, content, 50, H - 260, W - 100, safe_font('Aileron'), 11, OFF_WHITE, line_spacing=1.6)

        draw_footer(c, W, H, "GUIDE")
        c.showPage()

    # ── CTA PAGE ──
    cta = data.get('cta', {})
    draw_dark_page(c, W, H)
    draw_corner_accent(c, W, H, 'bottom-right', STEEL_BLUE)
    draw_corner_accent(c, W, H, 'top-left', WARM_GRAY)

    cta_text = cta.get('text', 'Bereit für den nächsten Schritt?')
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 28)
    c.setFillColor(CREAM_WHITE)
    draw_wrapped_text(c, cta_text.upper(), 50, H - 250, W - 100, safe_font('Aileron-Black', 'Helvetica-Bold'), 28, CREAM_WHITE)

    action = cta.get('action', '')
    if action:
        draw_wrapped_text(c, action, 50, H - 350, W - 100, safe_font('Aileron'), 14, OFF_WHITE, line_spacing=1.5)

    # Contact
    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 11)
    c.setFillColor(ACCENT_ORANGE)
    c.drawString(50, 120, cta.get('url', 'www.lakeshoremedia.de').upper())

    c.setFont(safe_font('Aileron'), 10)
    c.setFillColor(OFF_WHITE)
    c.drawString(50, 100, "raeto@lakeshoremedia.de | +49 (0) 172 63670609")

    draw_footer(c, W, H, "GUIDE")
    c.showPage()

    c.save()
    print(f"✓ Freebie saved to: {output_path}")


# ── Mailing Generator ─────────────────────────────────────────────────────────

def generate_mailing(data, output_path):
    """
    Generate an A4 portrait Mailing/Anschreiben PDF.

    Expected data structure:
    {
        "recipient_name": "Max Mustermann",
        "recipient_company": "Musterfirma GmbH",
        "subject": "Zusammenarbeit für euer nächstes Video-Projekt",
        "greeting": "Hey Max",
        "body": [
            "Danke für das tolle Gespräch letzte Woche...",
            "Wie besprochen, hier ein kurzer Überblick...",
            "Ich freue mich darauf, eure Geschichte zum Leben zu erwecken."
        ],
        "cta": "Lass uns nächste Woche einen kurzen Call machen — wann passt es dir?",
        "closing": "Beste Grüße",
        "date": "15. April 2025"
    }
    """
    W, H = A4
    c = canvas.Canvas(output_path, pagesize=A4)

    # Light background
    draw_light_page(c, W, H)

    # Header area with steel blue strip
    c.setFillColor(STEEL_BLUE)
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)

    # Logo text
    c.setFont(safe_font('Aileron-Black', 'Helvetica-Bold'), 16)
    c.setFillColor(CREAM_WHITE)
    c.drawString(50, H - 52, "LAKESHORE MEDIA")

    # Contact info in header
    c.setFont(safe_font('Aileron'), 8)
    c.setFillColor(OFF_WHITE)
    c.drawRightString(W - 50, H - 40, "raeto@lakeshoremedia.de")
    c.drawRightString(W - 50, H - 52, "+49 (0) 172 63670609")
    c.drawRightString(W - 50, H - 64, "Ammersee · München")

    # Date
    date = data.get('date', '')
    if date:
        c.setFont(safe_font('Aileron'), 9)
        c.setFillColor(WARM_GRAY)
        c.drawRightString(W - 50, H - 120, date)

    # Recipient
    recipient = data.get('recipient_name', '')
    company = data.get('recipient_company', '')
    y = H - 140
    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 10)
    c.setFillColor(NEAR_BLACK)
    if recipient:
        c.drawString(50, y, recipient)
        y -= 16
    if company:
        c.setFont(safe_font('Aileron'), 10)
        c.drawString(50, y, company)
        y -= 30

    # Subject line
    subject = data.get('subject', '')
    if subject:
        y -= 10
        c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 12)
        c.setFillColor(NEAR_BLACK)
        draw_wrapped_text(c, subject, 50, y, W - 100, safe_font('Aileron-Bold', 'Helvetica-Bold'), 12, NEAR_BLACK)
        y -= 30

    # Greeting
    greeting = data.get('greeting', 'Hallo')
    c.setFont(safe_font('Aileron'), 10)
    c.setFillColor(NEAR_BLACK)
    c.drawString(50, y, greeting + ",")
    y -= 25

    # Body paragraphs
    body = data.get('body', [])
    for para in body:
        y = draw_wrapped_text(c, para, 50, y, W - 100, safe_font('Aileron'), 10, NEAR_BLACK, line_spacing=1.6)
        y -= 12

    # CTA
    cta = data.get('cta', '')
    if cta:
        y -= 5
        y = draw_wrapped_text(c, cta, 50, y, W - 100, safe_font('Aileron-Bold', 'Helvetica-Bold'), 10, NEAR_BLACK, line_spacing=1.5)
        y -= 20

    # Closing
    closing = data.get('closing', 'Beste Grüße')
    c.setFont(safe_font('Aileron'), 10)
    c.setFillColor(NEAR_BLACK)
    c.drawString(50, y, closing + ",")
    c.setFont(safe_font('Aileron-Bold', 'Helvetica-Bold'), 10)
    c.drawString(50, y - 18, "Raeto Königsbauer")
    c.setFont(safe_font('Aileron'), 9)
    c.setFillColor(WARM_GRAY)
    c.drawString(50, y - 34, "Lakeshore Media")

    draw_footer(c, W, H)
    c.showPage()
    c.save()
    print(f"✓ Mailing saved to: {output_path}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Lakeshore Media PDF Generator')
    parser.add_argument('--type', choices=['proposal', 'freebie', 'mailing'], required=True)
    parser.add_argument('--output', required=True, help='Output PDF path')
    parser.add_argument('--data', required=True, help='JSON data file path')

    args = parser.parse_args()

    register_fonts()

    with open(args.data, 'r', encoding='utf-8') as f:
        data = json.load(f)

    generators = {
        'proposal': generate_proposal,
        'freebie': generate_freebie,
        'mailing': generate_mailing,
    }

    generators[args.type](data, args.output)
