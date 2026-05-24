# Lakeshore Media — Brand Reference

This file contains the complete brand identity for Lakeshore Media documents. Read this before generating any document.

## Company

- **Name**: Lakeshore Media
- **Owner**: Raeto Königsbauer
- **Contact**: +49 (0) 172 63670609 | raeto@lakeshoremedia.de
- **Location**: Ammersee · München, Deutschland
- **Website**: lakeshoremedia.de
- **Tagline**: "Deine Geschichte, Dein Weg" / "Your Story, Your Way"
- **What they do**: Hybrides Kreativstudio — Videoproduktion, Performance Marketing, Brand Storytelling. Sie verbinden Kreativität mit Technologie und Daten.

## Color Palette

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Near Black | `#0F1114` | Primary background for all dark documents |
| Steel Blue | `#2E3D51` | Organic decorative shapes, secondary backgrounds, section headers |
| Warm Gray | `#6B7280` | Secondary organic shapes, subtle accents |

### Secondary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Off-White | `#ECEAE4` | Light backgrounds (alternate pages), body text on dark |
| Cream White | `#F5F3ED` | Headings on dark backgrounds |
| Accent Orange | `#E8860C` | Accent arrows, CTAs, highlights (use sparingly) |
| Dark Charcoal | `#1E2328` | Slightly lighter dark areas for depth |

### Color Rules
- **Dark theme is default.** Most pages use Near Black background with Off-White text.
- **Light theme** is used for specific contrast pages (Brand Messaging, some Proposal sections like Overview).
- **Steel Blue and Warm Gray** are used for organic blob/leaf shapes that frame content — never as text color.
- **Accent Orange** is used very sparingly — for arrows, key highlights, link-like elements. Never for large areas.
- Avoid pure white (#FFFFFF) and pure black (#000000). Always use the brand variants.

## Typography

### Display Font: RL Aqva
- **Source**: Adobe Fonts (https://fonts.adobe.com/fonts/rl-aqva)
- **Weight**: 900 (Black/Extra Bold)
- **Style**: Normal
- **CSS**: `font-family: rl-aqva, sans-serif; font-weight: 900; font-style: normal;`
- **Usage**: Hero headlines, logo wordmark, section titles in pitch decks, large statement text
- **Character**: Chunky, retro-modern, rounded, all-caps. Very distinctive.
- **Fallback for PDF generation**: Since RL Aqva is a commercial Adobe font, use Aileron-Black or Aileron-Heavy as fallback in programmatically generated PDFs. For Canva output, use the RL Aqva font directly (it's in the Canva brand kit).

### Body Font: Aileron
- **Files**: Available as OTF in the brand assets folder
- **Weights available**: Thin, UltraLight, Light, Regular, SemiBold, Bold, Heavy, Black (plus all italic variants)
- **Usage**: Body copy, descriptions, smaller headings, UI text
- **Path**: `01_a_Lakeshore_Media/fonts/Aileron/aileron/`

### Secondary Body: Lato
- **Files**: Available as TTF in the brand assets folder
- **Weights**: Thin, Light, Regular, Bold, Black (plus italic variants)
- **Usage**: Alternative body text, captions, metadata, fine print
- **Path**: `01_a_Lakeshore_Media/fonts/Lato/Lato/`

### Typography Hierarchy (for documents)
| Level | Font | Weight | Size (relative) | Case |
|-------|------|--------|-----------------|------|
| Hero Title | RL Aqva / Aileron-Black | 900/Black | XXL | UPPERCASE |
| Section Header | Aileron-Bold | Bold | XL | UPPERCASE |
| Sub-Header | Aileron-SemiBold | SemiBold | L | Title Case |
| Body | Aileron-Regular | Regular | M | Sentence case |
| Caption/Meta | Lato-Regular | Regular | S | Sentence case |
| Fine Print | Lato-Light | Light | XS | Sentence case |

## Visual Elements

### Organic Shapes
The brand uses large, organic blob/leaf shapes as decorative framing elements. These appear:
- Along left edges (Steel Blue blobs)
- In corners (Warm Gray blobs)
- As subtle dark-on-dark texture in backgrounds
- They create a sense of flow and movement — fitting for a video production studio

### Logo
- **Icon**: Play button triangle with wave lines through it (video + lake/water reference)
- **Wordmark**: "LAKESHORE MEDIA" in RL Aqva font
- **Formats available**: SVG, PNG, JPG in both Icon and Wordmark variants
- **Path**: `01_a_Lakeshore_Media/Logos/`
- **Logo variants (by Artboard)**:
  - Artboard 1: Dark blue on transparent (main)
  - Artboard 2-7: Various color/background combinations
- **Footer placement**: Small icon centered at bottom of pages, flanked by "LAKESHORE MEDIA" left and document type right

### Illustrations
- 40+ custom SVG illustrations available in `01_a_Lakeshore_Media/Illustrations/`
- Style: Hand-drawn, sketch-like, warm and approachable
- Used in: Flyers, social media, lighter documents

### Photography
- Professional portrait photos in `01_a_Lakeshore_Media/Portrait/`
- Behind-the-scenes production photos in `01_a_Lakeshore_Media/BTS postprod/`

## Tone of Voice

### Tone
- Direkt, aber herzlich
- Sachkundig, ohne übermäßig technisch zu sein
- Gesprächig, nicht korporativ
- Konzentriert auf Klarheit und Ergebnisse

### Language
- Geradlinig und fesselnd
- Keine Floskeln, kein Füllmaterial — nur aussagekräftige Erzählungen
- Menschlich und nachvollziehbar, nicht übermäßig verkaufsorientiert oder starr
- Bilingual: Primarily German, but English is used for headings and international-facing documents

### Writing Rules for Documents
- Use short, punchy sentences for headlines
- Body text should be concise and value-focused
- Avoid corporate buzzwords — be specific about what Lakeshore delivers
- When writing proposals: focus on the client's goals, not Lakeshore's capabilities
- Use "Du/Dein" (informal) in most communications, "Sie/Ihr" for very corporate clients

## Brand Values (for content alignment)
1. **Innovation That Works** — Technology enhances storytelling, doesn't replace it
2. **Authenticity First** — Real stories that connect
3. **Collaboration Over Competition** — Long-term partnerships with clients

## Asset Paths (relative to mounted folder)
```
01_a_Lakeshore_Media/
├── Logos/
│   ├── Icon/ (SVG, PNG, JPG)
│   └── Wordmark/ (SVG, PNG, JPG)
├── Illustrations/ (40+ SVGs)
├── fonts/
│   ├── Aileron/aileron/ (OTF files)
│   ├── Lato/Lato/ (TTF files)
│   └── RL Aqva/ (reference only — Adobe Fonts)
├── Portrait/ (JPG portraits + heartbeat subfolder)
├── BTS postprod/ (JPG behind-the-scenes)
├── Lakeshore Media Brandbook German (1).pdf
├── PROPOSAL TEMPLATE.pdf
├── Content mit Tiefe. Strategie mit Wirkung..pdf
└── FINAL 10x ROAS Framework (1).pdf

Aileron/ (font files also in second mounted folder)
└── aileron/ (OTF files)
```
