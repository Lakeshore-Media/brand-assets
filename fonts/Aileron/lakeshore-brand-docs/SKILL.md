---
name: lakeshore-brand-docs
description: >
  Create on-brand documents for Lakeshore Media — proposals, pitch decks, lead magnets, mailings, and any other branded collateral.
  Use this skill whenever someone asks for a Lakeshore document, branded PDF, Angebot, Proposal, Pitch Deck, Freebie, Lead Magnet,
  Mailing, Anschreiben, or any document that should look and feel like Lakeshore Media. Also trigger when someone mentions
  "on brand", "brand guidelines", "Lakeshore style", or asks to create professional documents for a video production / creative agency context.
  Even if the request is vague like "mach mir ein Angebot für den Kunden" or "erstell ein PDF für den Lead Magnet" — use this skill.
---

# Lakeshore Brand Documents — Canva-Based Workflow

You are creating documents for **Lakeshore Media**, a hybrid creative studio based in Ammersee/München that combines video storytelling with data-driven strategy. Every document you create must feel confident, approachable, and premium — never corporate or generic.

## Core Principle

**All documents are created by duplicating and editing existing Canva templates.** This ensures perfect brand consistency — logos, fonts (RL Aqva, Aileron), colors, organic shapes, and imagery are already baked into the design. You never generate PDFs from code.

## First Steps

1. **Read the branding reference**: `references/branding.md` — colors, fonts, tone, company info.
2. **Read the template mapping**: `references/canva-templates.md` — which Canva design to use for each document type, and exactly which text fields map to which element IDs.
3. **Gather information** from the user (see below).
4. **Execute the Canva workflow** (see below).

## Document Types and Source Templates

| Document Type | Canva Source Design | Design ID | Pages |
|---|---|---|---|
| **Project Proposal** (Angebotsvorlage) | PROPOSAL TEMPLATE | `DAGiiePhUOY` | 15 |
| **Lead Magnet / Freebie** | FINAL 10x ROAS Framework | `DAGwzAKtVv8` | 18 |
| **Pitch Deck / Präsentation** | Generate from Canva Brand Kit | — | varies |
| **E-Mail Mailing / Anschreiben** | Generate from Canva Brand Kit | — | 1 |

## Gathering Information

Before creating any document, gather the essentials. Be smart — use what you know, ask only what you must. **Always speak German (Du-Form) unless the user writes in English.**

### For Proposals (most common)

**Must have:**
- Kundenname / Firma
- Projekttyp (welche Art von Video/Content?)
- Deliverables (was wird produziert?)

**Nice to have (can use smart defaults):**
- Budget / Preisrahmen
- Timeline
- Spezifische Ziele des Kunden
- Referenzen / Moodboard-Ideen

**Smart defaults if not provided:**
- Date: current month + year
- Website: www.lakeshoremedia.de
- Created by: Raeto Königsbauer
- Contact: raeto@lakeshoremedia.de | +49 172 63670609
- Payment terms: 50% bei Auftragsbestätigung, 50% bei finaler Lieferung
- Licensing: Digital License, 5 years

### For Lead Magnets / Freebies

**Must have:**
- Thema / Titel
- Zielgruppe
- 3-7 Hauptpunkte / Kapitel

**Nice to have:**
- CTA (wohin soll der Leser geleitet werden?)
- Tonalität (eher lehrreich, provokant, inspirierend?)

### For Pitch Decks

**Must have:**
- Ziel des Pitches (neuer Kunde gewinnen, Projekt vorstellen, etc.)
- Zielgruppe / Branche des Kunden

**Nice to have:**
- Referenzen aus bisherigen Projekten
- USPs die hervorgehoben werden sollen

## Canva Workflow — Step by Step

### 1. Copy the Template (CRITICAL — never mutate the master)

The master designs live in Raeto's Canva account. **Never commit changes to the master IDs** below:
- `DAGiiePhUOY` (PROPOSAL TEMPLATE)
- `DAGwzAKtVv8` (FINAL 10x ROAS Framework — Freebie)

**Use `copy-design` to create a fresh working copy automatically:**

```
copy-design(design_id="DAGiiePhUOY")
→ Returns a new design with its own design_id — edit this copy, never the master.
```

The returned design_id is what you pass to `start-editing-transaction` in step 2.

> **Safety rule:** If the design_id being edited equals one of the master IDs above, **stop immediately** — you should have copied first. Use `cancel-editing-transaction` to abort if in doubt.

### 2. Start Editing Transaction

```
start-editing-transaction(design_id="<design_id>")
→ Returns transaction_id + richtexts[] + pages[]
```

The response is the **source of truth** for this session. Always parse it fresh — do NOT reuse cached element IDs from `references/canva-templates.md`.

### 3. Find Elements by Placeholder Text

⚠️ **Element IDs are transaction-scoped.** The page-id prefix (e.g. `PBhSrkLCjzNQ7Kjz`) is stable across transactions, but the suffix after `-` changes every time you open a new editing session.

**This means:** `references/canva-templates.md` is a *placeholder-text map*, not a literal-ID lookup. Use it to know which slots exist on each page, then find the live element_id by matching the placeholder text in the current `richtexts` response.

**Recommended matching flow:**
```python
# Pseudocode for the skill
richtexts = response["richtexts"]
def find_by_text(page_index, placeholder):
    for rt in richtexts:
        if rt["page_index"] != page_index: continue
        current_text = "".join(r["text"] for r in rt["regions"])
        if placeholder.strip().lower() in current_text.strip().lower():
            return rt["element_id"]
    return None

client_name_eid = find_by_text(1, "Presented to: [CLIENT NAME]")
```

Alternatively, match by `page_id` + `containerElement.position` (top, left) for elements whose text has already been replaced in a prior partial edit.

**What the reference file documents per template:**
- Proposal (`DAGiiePhUOY`) — pages 1-15, every cover/contents/overview/mission/deliverables/mood/tone/timeline/investment/next-steps/thank-you slot.
- Freebie (`DAGwzAKtVv8`) — pages 1-18, every chapter title, body block, case-study card, and CTA.

See `references/canva-templates.md` for the full inventory.

### 4. Perform Editing Operations

Use `perform-editing-operations` to replace text in each field. Use the `element_id` from the **current** transaction (looked up by placeholder text, step 3), and pass the full `pages` array from `start-editing-transaction` so the MCP can validate responsiveness.

Two operation types matter most:
- `replace_text` — replaces the entire contents of the element. Use for slots where the whole string changes (client name, goals, timeline phases).
- `find_and_replace_text` — token swap within an element. Use when only part of the element's text needs to change (e.g. swapping `[CLIENT NAME]` inside a longer sentence).

```json
{
  "transaction_id": "<live transaction id>",
  "page_index": 1,
  "pages": "<pages array from start-editing-transaction>",
  "operations": [
    {
      "type": "replace_text",
      "element_id": "<live element_id for client-name slot>",
      "text": "Presented to: TechVision GmbH"
    },
    {
      "type": "replace_text",
      "element_id": "<live element_id for creator slot>",
      "text": "Created by: Raeto Königsbauer"
    }
  ]
}
```

**Tips:**
- Batch multiple operations per call (Canva MCP prefers bulk ops).
- Replace ALL placeholder text — don't leave any `[CLIENT NAME]` or `[YOUR NAME]` in the final document.
- For multi-line fields, the `text` may include `\n` — keep structure close to the original.
- For German content: Du-Form unless the client context requires Sie.
- If a page object in `pages` has `is_responsive: true`, only these op-types are allowed: `update_title`, `update_fill`, `delete_element`, `find_and_replace_text`.

### 5. Replace Images (if applicable)

For mood board pages (7-10) and the overview hero image (page 3), you can:
- Use `upload-asset-from-url` to upload reference images
- Use `perform-editing-operations` with `replace_image` to swap placeholder images

### 6. Get Thumbnails for Preview

After making changes, show the user a preview:
```
get-design-thumbnail(transaction_id="<id>", page_index=1)
```
**ALWAYS show thumbnails to the user** so they can see the result before you commit.

### 7. Commit Changes

```
commit-editing-transaction(transaction_id="<id>")
```

### 8. Export if Needed

If the user wants a PDF:
```
export-design(design_id="<id>", format="pdf")
```

## Content Generation Guidelines

When writing content for the templates, follow these rules:

### Tone of Voice
- **German by default** (unless client context requires English)
- **Du-Form** — direkt, herzlich, professionell aber nicht steif
- Confident without being arrogant
- Data-informed, creatively driven
- Short sentences. Clear language. No marketing fluff.

### Writing the Overview (Page 3)
- First paragraph: Briefly describe the project concept and what will be produced
- Second paragraph: How it will benefit the client
- Approach 1: Usually the "Content Package" (multiple assets)
- Approach 2: Usually the "Hero Video" or primary deliverable
- Keep each approach description to 2-3 sentences

### Writing Goals (Page 4)
- Always provide exactly 4 goals
- Each goal should be 1-2 sentences
- Mix emotional and business objectives
- Tailor to the client's industry and needs

### Writing Deliverables (Pages 5-6)
- Use clear, scannable format
- Include: what it is, duration/specs, intended placement
- Prices in EUR with German formatting (€2.500)

### Writing Timeline (Page 12)
- Use realistic production timelines
- Typical: 1-2 weeks pre-production, 1-2 shoot days, 2-3 weeks post
- Include clear phase descriptions

### Writing Investment (Page 13)
- Link to quote/invoice if available
- Include what's included in the price
- Mention payment terms and revision rounds

### Writing Next Steps (Page 14)
- Always 3 clear steps
- Step 1: Contact / Questions
- Step 2: Deposit + Contract
- Step 3: We start working
- Include Raeto's actual contact details

## Quality Checklist

Before committing, verify:
- [ ] All `[CLIENT NAME]`, `[YOUR NAME]`, placeholder text is replaced
- [ ] Date is current
- [ ] Contact details are Raeto's real info (raeto@lakeshoremedia.de, +49 172 63670609, www.lakeshoremedia.de)
- [ ] Prices are in EUR with correct formatting
- [ ] Content is in the correct language (German default)
- [ ] All 4 goals are tailored to the client
- [ ] Deliverables match what was discussed
- [ ] Timeline is realistic
- [ ] Showed user a thumbnail preview before committing
