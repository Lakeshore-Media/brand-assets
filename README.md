# Lakeshore Media — Brand Assets

Hotlink-ready via **jsDelivr CDN** (empfohlen für E-Mails & externe Einbindung) oder **GitHub Pages**.

**Base URLs:**
- CDN: `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/`
- Pages: `https://lakeshore-media.github.io/brand-assets/`

> Für E-Mail-Signaturen und HTML-Mails immer die **CDN-URL** verwenden — zuverlässiger in Gmail, Apple Mail, Outlook.

---

## Logos

| Datei | CDN-Link |
|-------|----------|
| Icon — Artboard 1 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/icon/Artboard 1.png` |
| Icon — Artboard 2 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/icon/Artboard 2.png` |
| Icon — Artboard 3 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/icon/Artboard 3.png` |
| Icon — Artboard 4 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/icon/Artboard 4.png` |
| Icon — Artboard 5 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/icon/Artboard 5.png` |
| Icon — Artboard 6 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/icon/Artboard 6.png` |
| Icon — Artboard 7 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/icon/Artboard 7.png` |
| Icon — Artboard 1 (SVG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/icon/Artboard 1.svg` |
| Wordmark — Artboard 1 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/wordmark/Artboard 1.png` |
| Wordmark — Artboard 2 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/wordmark/Artboard 2.png` |
| Wordmark — Artboard 3 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/wordmark/Artboard 3.png` |
| Wordmark — Artboard 4 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/wordmark/Artboard 4.png` |
| Wordmark — Artboard 5 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/wordmark/Artboard 5.png` |
| Wordmark — Artboard 6 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/wordmark/Artboard 6.png` |
| Wordmark — Artboard 7 (PNG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/wordmark/Artboard 7.png` |
| Wordmark — Artboard 1 (SVG) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/wordmark/Artboard 1.svg` |

---

## Fotos

| Datei | CDN-Link |
|-------|----------|
| Raeto Portrait | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/photos/portrait/raeto-portrait.png` |
| Raeto Portrait (Alpha/Freigestellt) | `https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/photos/portrait/raeto-portrait-alpha.png` |

### E-Mail-Signatur — Empfohlene IMG-Tags

```html
<!-- Portrait -->
<img src="https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/photos/portrait/raeto-portrait.png" width="80" height="80" alt="Raeto Königsbauer" style="border-radius:50%">

<!-- Logo Wordmark (auf dunklem Hintergrund: Artboard 1, auf hellem: anpassen) -->
<img src="https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/logo/wordmark/Artboard 1.png" width="160" alt="Lakeshore Media">
```

---

## Illustrationen

40 SVG-Illustrationen unter `illustrations/Artboard 1.svg` bis `Artboard 40.svg`.

```
https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/illustrations/Artboard N.svg
```

---

## Fonts

### Aileron (OTF)

```
https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/fonts/Aileron/aileron/Aileron-Regular.otf
https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/fonts/Aileron/aileron/Aileron-Bold.otf
https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/fonts/Aileron/aileron/Aileron-SemiBold.otf
https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/fonts/Aileron/aileron/Aileron-Light.otf
https://cdn.jsdelivr.net/gh/Lakeshore-Media/brand-assets@main/fonts/Aileron/aileron/Aileron-Thin.otf
```

Alle Schnitte: Black, Heavy, Bold, SemiBold, Regular, Light, UltraLight, Thin — je Regular + Italic.

---

## Hinweise

- Leerzeichen in Dateinamen bleiben erhalten — in HTML ggf. als `%20` kodieren
- Für versionierte, unveränderte URLs einen **Release-Tag** verwenden statt `@main`: `@v1.0.0`
- SVGs können direkt als `<img src="...svg">` eingebunden werden (keine XSS-Risiken bei `img`-Tag)
