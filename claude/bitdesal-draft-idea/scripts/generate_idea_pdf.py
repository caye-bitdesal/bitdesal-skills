#!/usr/bin/env python3
"""Generate Spanish and English idea-brief PDFs, plus a download HTML page.

Reads a bilingual idea JSON and writes:

  <out>/<slug>-idea-es.pdf
  <out>/<slug>-idea-en.pdf
  <out>/<slug>-download.html

The HTML page embeds both PDFs so the user can download them and pick a
save location in the browser dialog. Standard library only.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
from pathlib import Path

# US Letter — same geometry as Cayetano_Ruiz_Cover_Letter_Fever.pdf
# Header at x=72; body at x=78; hairline under the letterhead; body starts
# ~124pt from the top of the page.
PAGE_W = 612.0
PAGE_H = 792.0
HEADER_X = 72.0
BODY_X = 78.0
MARGIN_R = 78.0
MARGIN_B = 56.0
CONTENT_W = PAGE_W - BODY_X - MARGIN_R
NAME_SIZE = 16.0
META_SIZE = 9.0
BODY_SIZE = 10.0
BODY_LEADING = 16.0

# Helvetica AFM widths, 32-126, in 1/1000 em
_HELV = [
    278, 278, 355, 556, 556, 889, 667, 222, 333, 333, 389, 584, 278, 333,
    278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278,
    584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278,
    500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944,
    667, 667, 611, 278, 278, 278, 469, 556, 222, 556, 556, 500, 556, 556,
    278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500,
    278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584,
]


def _char_width(ch: str) -> float:
    o = ord(ch)
    if 32 <= o <= 126:
        return _HELV[o - 32]
    if ch in "áéíóúñüÁÉÍÓÚÑÜ¿¡":
        base = {
            "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n",
            "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N",
            "¿": "?", "¡": "!",
        }[ch]
        return _char_width(base)
    if ch == "€":
        return 556
    return 556


def string_width(text: str, size: float, bold: bool = False) -> float:
    scale = 1.04 if bold else 1.0
    return sum(_char_width(c) for c in text) * size / 1000.0 * scale


def sanitize(text: str) -> str:
    if text is None:
        return ""
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
        "\u2192": "->",
    }
    out = str(text)
    for src, dst in replacements.items():
        out = out.replace(src, dst)
    return out.replace("\r\n", "\n").replace("\r", "\n")


def wrap_text(text: str, size: float, width: float, bold: bool = False) -> list[str]:
    text = sanitize(text).strip()
    if not text:
        return []
    lines: list[str] = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            lines.append("")
            continue
        words = para.split()
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if string_width(trial, size, bold) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                if string_width(word, size, bold) <= width:
                    current = word
                else:
                    # Hard-break very long tokens (URLs)
                    chunk = ""
                    for ch in word:
                        if string_width(chunk + ch, size, bold) <= width:
                            chunk += ch
                        else:
                            if chunk:
                                lines.append(chunk)
                            chunk = ch
                    current = chunk
        if current:
            lines.append(current)
    return lines or [""]


def pdf_escape(text: str) -> str:
    encoded = sanitize(text).encode("cp1252", errors="replace").decode("latin-1")
    return encoded.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    return f"{r:.3f} {g:.3f} {b:.3f}"


LABELS = {
    "es": {
        "kicker": "Brief de idea",
        "lang": "Español",
        "slug": "Slug",
        "date": "Fecha",
        "status": "Estado",
        "gap": "Veredicto de hueco",
        "total": "Puntuación total",
        "thesis": "Tesis",
        "idea": "Idea",
        "problem": "Problema",
        "solution": "Solución",
        "who": "Para quién",
        "primary": "Principal",
        "secondary": "Secundario",
        "not_for": "No es para",
        "why_now": "Por qué ahora",
        "scope_in": "Alcance v1 — entra",
        "scope_out": "Alcance v1 — queda fuera",
        "requirements": "Requisitos",
        "mobile": "Mobile",
        "backend": "Backend",
        "cross": "Transversal",
        "competition": "Análisis de la competencia",
        "method": "Método",
        "competitors": "Competidores",
        "type": "Tipo",
        "url": "URL",
        "what": "Qué hacen",
        "strengths": "Fortalezas",
        "weaknesses": "Debilidades / huecos",
        "pricing": "Precio",
        "relevance": "Relevancia",
        "positioning": "Posicionamiento",
        "gap_section": "Veredicto",
        "monetization": "Monetización",
        "who_pays": "Quién paga",
        "how": "Cómo funciona",
        "short": "Corto plazo",
        "long": "Largo plazo",
        "v1_fit": "Encaje en v1",
        "why_score": "Por qué esta nota",
        "recommended": "Recomendado para v1",
        "risks": "Riesgos",
        "technical": "Técnicos",
        "product": "Producto",
        "market": "Mercado",
        "legal": "Legal y cumplimiento",
        "business": "Negocio y operaciones",
        "action": "Plan de acción",
        "phase0": "Fase 0 - Validar (antes de construir)",
        "phase1": "Fase 1 - MVP",
        "phase2": "Fase 2 - Después de señal",
        "next14": "Próximos 14 días",
        "scorecard": "Cuadro de puntuaciones",
        "section": "Sección",
        "score": "Nota (1-5)",
        "meaning1": "Significado del 1",
        "meaning5": "Significado del 5",
        "open": "Preguntas abiertas",
        "score_why": "Justificación",
        "footer": "Bitdesal  ·  brief de idea",
        "page": "Página",
        "gap_values": {
            "real gap": "hueco real",
            "partial gap": "hueco parcial",
            "no clear gap": "sin hueco claro",
        },
        "score_rows": [
            ("Requisitos", "Muy compleja", "Muy poco compleja"),
            ("Competencia", "Mucha competencia", "Ninguna competencia"),
            ("Monetización", "Poco potencial económico", "Alto potencial corto y largo plazo"),
            ("Riesgos", "Mucho riesgo", "Sin riesgo"),
            ("Plan de acción", "Lento / difícil de implementar", "Relativamente rápido"),
        ],
        "total_row": "Total (media)",
        "total_meaning": "Media de las cinco notas",
    },
    "en": {
        "kicker": "Idea brief",
        "lang": "English",
        "slug": "Slug",
        "date": "Date",
        "status": "Status",
        "gap": "Gap verdict",
        "total": "Total score",
        "thesis": "Thesis",
        "idea": "Idea",
        "problem": "Problem",
        "solution": "Solution",
        "who": "Who it is for",
        "primary": "Primary",
        "secondary": "Secondary",
        "not_for": "Not for",
        "why_now": "Why now",
        "scope_in": "v1 scope — in",
        "scope_out": "v1 scope — out",
        "requirements": "Requirements",
        "mobile": "Mobile",
        "backend": "Backend",
        "cross": "Cross-cutting",
        "competition": "Competitive analysis",
        "method": "Method",
        "competitors": "Competitors",
        "type": "Type",
        "url": "URL",
        "what": "What they do",
        "strengths": "Strengths",
        "weaknesses": "Weaknesses / openings",
        "pricing": "Pricing",
        "relevance": "Relevance",
        "positioning": "Positioning",
        "gap_section": "Verdict",
        "monetization": "Monetization",
        "who_pays": "Who pays",
        "how": "How it works",
        "short": "Short term",
        "long": "Long term",
        "v1_fit": "Fit for v1",
        "why_score": "Why this score",
        "recommended": "Recommended for v1",
        "risks": "Risks",
        "technical": "Technical",
        "product": "Product",
        "market": "Market",
        "legal": "Legal & compliance",
        "business": "Business & operations",
        "action": "Action plan",
        "phase0": "Phase 0 - Validate (before building)",
        "phase1": "Phase 1 - MVP",
        "phase2": "Phase 2 - After signal",
        "next14": "Next 14 days",
        "scorecard": "Scorecard",
        "section": "Section",
        "score": "Score (1-5)",
        "meaning1": "Meaning of 1",
        "meaning5": "Meaning of 5",
        "open": "Open questions",
        "score_why": "Rationale",
        "footer": "Bitdesal  ·  idea brief",
        "page": "Page",
        "gap_values": {
            "real gap": "real gap",
            "partial gap": "partial gap",
            "no clear gap": "no clear gap",
        },
        "score_rows": [
            ("Requirements", "Very complex", "Very little complexity"),
            ("Competition", "Lots of competition", "No competition"),
            ("Monetization", "Little economic potential", "High potential short + long term"),
            ("Risks", "High risk", "No risk"),
            ("Action plan", "Slow / hard to implement", "Relatively fast to implement"),
        ],
        "total_row": "Total (average)",
        "total_meaning": "Average of the five scores",
    },
}


class Page:
    def __init__(self) -> None:
        self.ops: list[str] = []

    def add(self, op: str) -> None:
        self.ops.append(op)

    def stream(self) -> str:
        return "\n".join(self.ops) + "\n"


class IdeaPDF:
    def __init__(self, lang: str, meta: dict, loc: dict, scores: dict) -> None:
        self.lang = lang
        self.L = LABELS[lang]
        self.meta = meta
        self.loc = loc
        self.scores = scores
        self.pages: list[Page] = []
        self.page: Page | None = None
        self.y = 0.0
        self.new_page()

    def new_page(self) -> None:
        self.page = Page()
        self.pages.append(self.page)
        self._draw_header()

    def ensure(self, height: float) -> None:
        if self.y - height < MARGIN_B + 18:
            self.new_page()

    def _draw_header(self) -> None:
        """Letterhead: 16pt name, two 9pt meta lines, hairline, then body gap.

        Coordinates copied from Cayetano_Ruiz_Cover_Letter_Fever.pdf (Letter).
        """
        name = sanitize(
            self.loc.get("working_name")
            or self.meta.get("working_name")
            or self.meta.get("slug")
            or ""
        )
        gap_key = self.meta.get("gap_verdict", "")
        gap_label = self.L["gap_values"].get(gap_key, gap_key)
        total = self.scores.get("total", "")
        meta1 = f"Bitdesal  |  {self.L['kicker']}  |  {self.L['lang']}"
        meta2 = (
            f"{self.meta.get('slug', '')}  |  {self.meta.get('date', '')}  |  "
            f"{gap_label}  |  {total}/5"
        )
        # Baselines from the reference bbox (PDF y, origin bottom-left)
        self.raw_text(HEADER_X, PAGE_H - 39.73, name, NAME_SIZE, bold=True, color="#000000")
        self.raw_text(HEADER_X, PAGE_H - 58.13, meta1, META_SIZE, color="#000000")
        self.raw_text(HEADER_X, PAGE_H - 70.37, meta2, META_SIZE, color="#000000")
        rule_y = PAGE_H - 78.4
        assert self.page is not None
        self.page.add("0 0 0 RG")
        self.page.add("0.6 w")
        self.page.add(
            f"{HEADER_X:.2f} {rule_y:.2f} m {PAGE_W - HEADER_X:.2f} {rule_y:.2f} l S"
        )
        # Body first-line top matches the cover letter (~124pt from the page top)
        self.y = PAGE_H - 124.16

    def rect(self, x: float, y: float, w: float, h: float, fill: str) -> None:
        assert self.page is not None
        self.page.add(f"{rgb(fill)} rg")
        self.page.add(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")

    def line(self, x1: float, y1: float, x2: float, y2: float, color: str = "#e5e7eb") -> None:
        assert self.page is not None
        self.page.add(f"{rgb(color)} RG")
        self.page.add("0.6 w")
        self.page.add(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def raw_text(
        self,
        x: float,
        y: float,
        text: str,
        size: float,
        bold: bool = False,
        color: str = "#000000",
    ) -> None:
        assert self.page is not None
        font = "/F2" if bold else "/F1"
        self.page.add("BT")
        self.page.add(f"{font} {size:.1f} Tf")
        self.page.add(f"{rgb(color)} rg")
        self.page.add(f"1 0 0 1 {x:.2f} {y:.2f} Tm")
        self.page.add(f"({pdf_escape(text)}) Tj")
        self.page.add("ET")

    def heading(self, text: str, level: int = 1) -> None:
        sizes = {1: 12, 2: 11, 3: 10}
        size = sizes[level]
        gap_before = {1: 18, 2: 14, 3: 10}[level]
        if abs(self.y - (PAGE_H - 124.16)) > 0.8:
            self.y -= gap_before
        lines = wrap_text(text, size, CONTENT_W, bold=True)
        h = len(lines) * (size + 4) + 4
        self.ensure(h)
        for line in lines:
            self.raw_text(BODY_X, self.y - size, line, size, bold=True, color="#000000")
            self.y -= size + 4
        self.y -= 4

    def para(self, text: str, size: float = BODY_SIZE, color: str = "#000000") -> None:
        text = sanitize(text)
        if not text.strip():
            return
        leading = BODY_LEADING if size == BODY_SIZE else size + 4
        lines = wrap_text(text, size, CONTENT_W)
        self.ensure(leading * max(len(lines), 1) + 8)
        for line in lines:
            if line == "":
                self.y -= leading * 0.5
                continue
            self.ensure(leading)
            self.raw_text(BODY_X, self.y - size, line, size, color=color)
            self.y -= leading
        self.y -= 12

    def bullets(self, items: list[str], size: float = BODY_SIZE) -> None:
        leading = BODY_LEADING if size == BODY_SIZE else size + 4
        for item in items:
            item = sanitize(str(item)).strip()
            if not item:
                continue
            wrapped = wrap_text(item, size, CONTENT_W - 16)
            self.ensure(leading * len(wrapped) + 2)
            self.raw_text(BODY_X, self.y - size, "-", size, bold=True, color="#000000")
            for i, line in enumerate(wrapped):
                self.ensure(leading)
                self.raw_text(BODY_X + 14, self.y - size, line, size)
                self.y -= leading
            self.y -= 2
        self.y -= 8

    def kv_block(self, pairs: list[tuple[str, str]]) -> None:
        for key, value in pairs:
            value = sanitize(value)
            if not value:
                continue
            self.para(f"{key}: {value}")

    def score_chip(self, label: str, score: float | int, why: str = "") -> None:
        self.ensure(BODY_LEADING + 8)
        text = f"{label}: {score}/5"
        self.raw_text(BODY_X, self.y - BODY_SIZE, text, BODY_SIZE, bold=True, color="#000000")
        self.y -= BODY_LEADING
        if why:
            self.para(f"{self.L['score_why']}: {why}", size=9, color="#000000")

    def table(self, headers: list[str], rows: list[list[str]]) -> None:
        col_n = len(headers)
        col_w = CONTENT_W / col_n
        row_h = 26
        header_h = 20
        min_block = header_h + row_h * min(len(rows), 2) + 8
        self.ensure(min_block)
        self.line(BODY_X, self.y, BODY_X + CONTENT_W, self.y, "#000000")
        self.y -= 6
        for i, h in enumerate(headers):
            label = wrap_text(h, 8, col_w - 8, True)
            if label:
                self.raw_text(
                    BODY_X + 4 + i * col_w,
                    self.y - 10,
                    label[0],
                    8,
                    bold=True,
                    color="#000000",
                )
        self.y -= header_h
        self.line(BODY_X, self.y + 8, BODY_X + CONTENT_W, self.y + 8, "#000000")
        for r_i, row in enumerate(rows):
            self.ensure(row_h)
            for i, cell in enumerate(row):
                lines = wrap_text(str(cell), 8, col_w - 8)
                cy = self.y - 10
                for line in lines[:2]:
                    self.raw_text(BODY_X + 4 + i * col_w, cy - 6, line, 8, color="#000000")
                    cy -= 10
            self.y -= row_h
            self.line(BODY_X, self.y + 6, BODY_X + CONTENT_W, self.y + 6, "#cccccc")
        self.y -= 10

    def footer_all(self) -> None:
        total = len(self.pages)
        for i, page in enumerate(self.pages, start=1):
            label = f"{i} / {total}"
            lw = string_width(label, 9)
            page.add("BT")
            page.add("/F1 9 Tf")
            page.add("0 0 0 rg")
            page.add(f"1 0 0 1 {PAGE_W - MARGIN_R - lw:.2f} 36.00 Tm")
            page.add(f"({pdf_escape(label)}) Tj")
            page.add("ET")

    def build(self) -> None:
        loc = self.loc
        meta = self.meta
        scores = self.scores
        L = self.L
        gap_key = meta.get("gap_verdict", "")
        gap_label = L["gap_values"].get(gap_key, gap_key)
        total = scores.get("total", 0)

        idea = loc.get("idea", {})
        req = loc.get("requirements", {})
        comp = loc.get("competition", {})
        mon = loc.get("monetization", {})
        risks = loc.get("risks", {})
        plan = loc.get("action_plan", {})

        self.heading(L["thesis"], 1)
        self.para(loc.get("thesis", ""))

        self.heading(L["idea"], 1)
        self.heading(L["problem"], 2)
        self.para(idea.get("problem", ""))
        self.heading(L["solution"], 2)
        self.para(idea.get("solution", ""))
        self.heading(L["who"], 2)
        self.kv_block(
            [
                (L["primary"], idea.get("who_primary", "")),
                (L["secondary"], idea.get("who_secondary", "")),
                (L["not_for"], idea.get("who_not", "")),
            ]
        )
        self.heading(L["why_now"], 2)
        self.para(idea.get("why_now", ""))
        self.heading(L["scope_in"], 2)
        self.bullets(idea.get("scope_in") or [])
        self.heading(L["scope_out"], 2)
        self.bullets(idea.get("scope_out") or [])

        self.heading(L["requirements"], 1)
        self.heading(L["mobile"], 2)
        self.para(req.get("mobile", ""))
        self.heading(L["backend"], 2)
        self.para(req.get("backend", ""))
        self.heading(L["cross"], 2)
        self.para(req.get("cross_cutting", ""))
        self.score_chip(L["requirements"], scores.get("requirements", 0), req.get("score_why", ""))

        self.heading(L["competition"], 1)
        self.heading(L["method"], 2)
        self.para(comp.get("method", ""))
        self.heading(L["competitors"], 2)
        for c in comp.get("competitors") or []:
            self.heading(c.get("name", "Competitor"), 3)
            self.kv_block(
                [
                    (L["type"], c.get("type", "")),
                    (L["url"], c.get("url", "")),
                    (L["what"], c.get("what", "")),
                    (L["strengths"], c.get("strengths", "")),
                    (L["weaknesses"], c.get("weaknesses", "")),
                    (L["pricing"], c.get("pricing", "")),
                    (L["relevance"], c.get("relevance", "")),
                ]
            )
        self.heading(L["positioning"], 2)
        self.para(comp.get("positioning", ""))
        self.heading(L["gap_section"], 2)
        self.para(f"{gap_label}. {comp.get('gap_verdict_text', '')}")
        self.score_chip(L["competition"], scores.get("competition", 0), comp.get("score_why", ""))

        self.heading(L["monetization"], 1)
        for m in mon.get("models") or []:
            name = m.get("name", "Model")
            self.heading(f"{name}  —  {m.get('score', '?')}/5", 3)
            self.kv_block(
                [
                    (L["who_pays"], m.get("who_pays", "")),
                    (L["how"], m.get("how", "")),
                    (L["short"], m.get("short_term", "")),
                    (L["long"], m.get("long_term", "")),
                    (L["v1_fit"], m.get("v1_fit", "")),
                    (L["why_score"], m.get("why_score", "")),
                ]
            )
        self.heading(L["recommended"], 2)
        self.para(mon.get("recommended_v1", ""))
        self.score_chip(L["monetization"], scores.get("monetization", 0), mon.get("score_why", ""))

        self.heading(L["risks"], 1)
        for key, title in (
            ("technical", L["technical"]),
            ("product", L["product"]),
            ("market", L["market"]),
            ("legal", L["legal"]),
            ("business", L["business"]),
        ):
            self.heading(title, 2)
            items = []
            for r in risks.get(key) or []:
                if isinstance(r, dict):
                    items.append(f"[{r.get('level', '')}] {r.get('text', '')}")
                else:
                    items.append(str(r))
            self.bullets(items)
        self.score_chip(L["risks"], scores.get("risks", 0), risks.get("score_why", ""))

        self.heading(L["action"], 1)
        self.heading(L["phase0"], 2)
        self.para(plan.get("phase0", ""))
        self.heading(L["phase1"], 2)
        self.para(plan.get("phase1", ""))
        self.heading(L["phase2"], 2)
        self.para(plan.get("phase2", ""))
        self.heading(L["next14"], 2)
        self.bullets(plan.get("next_14_days") or [])
        self.score_chip(L["action"], scores.get("action_plan", 0), plan.get("score_why", ""))

        self.heading(L["scorecard"], 1)
        headers = [L["section"], L["score"], L["meaning1"], L["meaning5"]]
        keys = ["requirements", "competition", "monetization", "risks", "action_plan"]
        rows = []
        for key, (name, m1, m5) in zip(keys, L["score_rows"]):
            rows.append([name, str(scores.get(key, "")), m1, m5])
        rows.append([L["total_row"], str(total), "", L["total_meaning"]])
        self.table(headers, rows)

        questions = loc.get("open_questions") or []
        if questions:
            self.heading(L["open"], 1)
            self.bullets(questions)

        self.footer_all()

    def write(self, path: Path) -> None:
        fonts = [
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
        ]
        objects: list[bytes] = []

        def add(body: bytes) -> int:
            objects.append(body)
            return len(objects)

        font1 = add(fonts[0])
        font2 = add(fonts[1])
        content_ids: list[int] = []
        for page in self.pages:
            stream = page.stream().encode("latin-1", errors="replace")
            content_ids.append(
                add(
                    f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
                    + stream
                    + b"endstream"
                )
            )
        pages_obj_num = len(objects) + len(self.pages) + 1
        page_ids: list[int] = []
        for cid in content_ids:
            page_ids.append(
                add(
                    (
                        f"<< /Type /Page /Parent {pages_obj_num} 0 R "
                        f"/MediaBox [0 0 {PAGE_W:.2f} {PAGE_H:.2f}] "
                        f"/Resources << /Font << /F1 {font1} 0 R /F2 {font2} 0 R >> >> "
                        f"/Contents {cid} 0 R >>"
                    ).encode("ascii")
                )
            )

        kids = " ".join(f"{n} 0 R" for n in page_ids)
        add(
            f"<< /Type /Pages /Count {len(page_ids)} /Kids [{kids}] >>".encode("ascii")
        )
        # pages_obj_num should match
        assert len(objects) == pages_obj_num
        catalog = add(f"<< /Type /Catalog /Pages {pages_obj_num} 0 R >>".encode("ascii"))

        buf = bytearray()
        buf.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for i, obj in enumerate(objects, start=1):
            offsets.append(len(buf))
            buf.extend(f"{i} 0 obj\n".encode("ascii"))
            buf.extend(obj)
            buf.extend(b"\nendobj\n")
        xref_pos = len(buf)
        buf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        buf.extend(b"0000000000 65535 f \n")
        for off in offsets[1:]:
            buf.extend(f"{off:010d} 00000 n \n".encode("ascii"))
        buf.extend(
            (
                f"trailer\n<< /Size {len(objects) + 1} /Root {catalog} 0 R >>\n"
                f"startxref\n{xref_pos}\n%%EOF\n"
            ).encode("ascii")
        )
        path.write_bytes(bytes(buf))


DOWNLOAD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title} — Bitdesal</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{
      margin: 0; min-height: 100vh; font-family: ui-sans-serif, system-ui, sans-serif;
      background: #0b1020; color: #e5e7eb;
      display: flex; align-items: center; justify-content: center; padding: 32px;
    }}
    .card {{
      max-width: 560px; width: 100%; background: #111827; border: 1px solid #1f2937;
      border-radius: 16px; padding: 32px; box-shadow: 0 20px 50px rgba(0,0,0,.4);
    }}
    h1 {{ margin: 0 0 8px; font-size: 1.6rem; }}
    p {{ color: #9ca3af; line-height: 1.5; }}
    .meta {{ font-size: .9rem; color: #d1d5db; margin: 16px 0 24px; }}
    .row {{ display: flex; flex-direction: column; gap: 12px; }}
    button {{
      appearance: none; border: 0; border-radius: 10px; padding: 14px 18px;
      font-size: 1rem; font-weight: 650; cursor: pointer; color: #fff;
    }}
    .es {{ background: #2563eb; }}
    .en {{ background: #0f766e; }}
    button:hover {{ filter: brightness(1.08); }}
    .hint {{ margin-top: 20px; font-size: .85rem; color: #6b7280; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>{title}</h1>
    <p>El brief está listo en PDF. Pulsa un botón para descargarlo y elige
    la carpeta donde quieres guardarlo. The brief is ready — pick a folder
    in the save dialog.</p>
    <div class="meta">
      Veredicto / verdict: <strong>{gap}</strong><br/>
      Total: <strong>{total}/5</strong>
    </div>
    <div class="row">
      <button class="es" type="button" onclick="save('es')">Descargar PDF en español</button>
      <button class="en" type="button" onclick="save('en')">Download English PDF</button>
    </div>
    <p class="hint">Si el dialogo no aparece, los PDF tambien estan en la carpeta
    del brief junto a este HTML. If the dialog does not open, the PDF files sit
    next to this page.</p>
  </div>
  <script>
    const FILES = {{
      es: {{ name: {es_name}, data: {es_b64} }},
      en: {{ name: {en_name}, data: {en_b64} }},
    }};
    function save(lang) {{
      const file = FILES[lang];
      const bin = atob(file.data);
      const bytes = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
      const blob = new Blob([bytes], {{ type: "application/pdf" }});
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = file.name;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    }}
  </script>
</body>
</html>
"""


def generate(brief: dict, out_dir: Path) -> dict[str, Path]:
    slug = brief["slug"]
    scores = brief["scores"]
    meta = {
        "slug": slug,
        "working_name": brief.get("working_name", slug),
        "date": brief.get("date", ""),
        "status": brief.get("status", "draft"),
        "gap_verdict": brief.get("gap_verdict", ""),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for lang in ("es", "en"):
        pdf = IdeaPDF(lang, meta, brief[lang], scores)
        pdf.build()
        dest = out_dir / f"{slug}-idea-{lang}.pdf"
        pdf.write(dest)
        paths[lang] = dest

    es_b64 = base64.b64encode(paths["es"].read_bytes()).decode("ascii")
    en_b64 = base64.b64encode(paths["en"].read_bytes()).decode("ascii")
    html_path = out_dir / f"{slug}-download.html"
    html_path.write_text(
        DOWNLOAD_HTML.format(
            title=html.escape(str(meta["working_name"])),
            gap=html.escape(str(meta["gap_verdict"])),
            total=html.escape(str(scores.get("total", ""))),
            es_name=json.dumps(paths["es"].name),
            en_name=json.dumps(paths["en"].name),
            es_b64=json.dumps(es_b64),
            en_b64=json.dumps(en_b64),
        ),
        encoding="utf-8",
    )
    paths["html"] = html_path
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate bilingual idea-brief PDFs.")
    parser.add_argument("--brief", required=True, help="Path to idea.json")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args()
    brief_path = Path(args.brief)
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    paths = generate(brief, Path(args.out))
    for key, path in paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
