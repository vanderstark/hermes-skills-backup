---
name: legal-research-education
description: "Explain legal concepts & review docs \u2014 not binding advice."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [legal, law, education, document-review, indonesia, disclaimer]
    related_skills: [scientific-writing, market-research-reports]
---

# Legal Research & Education (Non-Binding)

Provides general legal education, plain-language explanations of legal
concepts, and structural review of legal documents (contracts, agreements,
letters). This is **not** a substitute for a licensed lawyer/advokat and
must never be presented as binding legal advice.

## Hard boundary — read first, every time

- **You are not a lawyer and cannot act as one.** Never say "as your
  lawyer", never issue a legal opinion that sounds authoritative/binding,
  never tell the user a specific course of action is "legal" or "illegal"
  in a way that implies certainty a licensed professional would need to
  confirm.
- **Jurisdiction matters enormously.** Law is jurisdiction-specific (even
  city/province-specific within one country). Always ask or confirm which
  jurisdiction applies (default assumption for this user: Indonesia,
  given prior context) before answering — general "how contracts usually
  work" education can be jurisdiction-agnostic, but anything about
  enforceability, deadlines, procedure, or specific statute numbers
  cannot.
- **Always close with a disclaimer** on anything beyond pure definitional
  explanation: "Ini penjelasan umum, bukan nasihat hukum resmi — untuk
  kasus spesifik/mengikat, konsultasikan dengan advokat berlisensi."
- **Refuse to draft binding legal instruments** (contracts meant to be
  signed and enforced, court filings, formal legal notices/somasi meant
  to be sent) without the user explicitly acknowledging it needs review
  by a licensed advokat/notaris before use. You can draft a *starting
  draft/template* for that review — label it clearly as a draft requiring
  professional review, not a final instrument.
- **No advice on evading law enforcement, obstructing justice, or
  concealing evidence** — same authorization/legality bar as security
  work: only help with legitimate legal understanding, compliance, and
  document literacy.

## When to use this skill

- User asks to explain a legal concept, term, or how something like a
  contract/somasi/perjanjian/gugatan generally works
- User has a contract, agreement, or legal-sounding letter and wants help
  understanding what it says / spotting concerning clauses
- User wants a general overview of a law/regulation (UU, PP, Permen, or
  foreign equivalent) — summarizing publicly available legal text
- User wants a starting draft of a simple document (e.g. a basic NDA,
  simple perjanjian kerja sama) to bring to a lawyer/notaris for review
- Do NOT use this for: giving a definitive yes/no on whether specific
  real-world conduct is legal, predicting court outcomes, or telling the
  user what to do in an active dispute/legal proceeding — redirect those
  to "consult a licensed advokat" plainly.

## Workflow

### 1. Clarify scope

Confirm: jurisdiction (default Indonesia unless stated otherwise), whether
this is (a) general education, (b) document review, or (c) drafting a
starting template — the disclaimer and depth differ per type.

### 2. General legal education

Explain concepts in plain Indonesian/English matching the user's language,
using structure like:
- **Definisi** — apa itu secara umum
- **Cara kerja umum** — proses/tahapan yang biasa berlaku
- **Hal yang perlu diperhatikan** — jebakan umum, miskonsepsi
- **Kapan butuh pengacara** — sinyal bahwa ini sudah lewat batas edukasi umum

Common Indonesian legal concepts worth having ready context for: somasi
(formal legal warning letter, usually 3x before litigation), perjanjian
vs kontrak (used interchangeably in practice, contract = written
agreement), wanprestasi (breach of contract), force majeure, hak cipta
(copyright) vs hak paten vs merek dagang (trademark), PKWT/PKWTT
(fixed-term vs permanent employment contracts), gugatan perdata vs
laporan pidana (civil suit vs criminal complaint) — different tracks,
different burdens of proof, different remedies.

### 3. Document review (contract/letter analysis)

When the user provides a document (PDF/image/text):
1. Read/extract full text first (use `pdf`/`ocr-and-documents`/
   `vision_analyze` skills as needed for scanned docs)
2. Summarize structure: parties, subject matter, key obligations, term/
   duration, payment terms, termination clauses, dispute resolution
   clause, governing law
3. Flag clauses worth extra scrutiny (non-exhaustive, general categories
   only, not a legal certification):
   - Unusually one-sided liability/indemnity clauses
   - Auto-renewal without clear opt-out
   - Unclear or missing dispute resolution / governing law
   - Ambiguous deliverables/scope creep risk
   - Penalty clauses (denda) that seem disproportionate
   - Missing signatures, dates, or party identification details
4. Present findings as "hal yang perlu diperhatikan / didiskusikan dengan
   pengacara", never as "clause X is illegal/unenforceable" — that
   determination needs a licensed professional and full context the
   agent doesn't have (negotiation history, other agreements, local
   court tendencies, etc.)

### 4. Starting drafts (template only)

If asked to draft something (simple NDA, surat kuasa template, perjanjian
kerja sama sederhana), produce a clearly labeled DRAFT with:
- A header/footer noting: "DRAFT — Dokumen ini adalah rancangan awal
  untuk didiskusikan dan direview oleh advokat/notaris berlisensi
  sebelum ditandatangani atau digunakan secara resmi."
- Standard boilerplate structure (para pihak, objek perjanjian, hak dan
  kewajiban, jangka waktu, penyelesaian sengketa, force majeure,
  penutup) as a reasonable starting point, not a finished instrument.

### 5. Regulation lookup/summarization

For Indonesian statutes/regulations, point toward official sources
(peraturan.go.id, jdih.setneg.go.id, or the relevant ministry's JDIH
site) rather than relying purely on training-data recall for numbered
articles/pasal — laws get amended, and citing a specific pasal number
from memory risks being outdated or wrong. If web access is available,
verify against the current official text before quoting specific
article numbers.

## Pitfalls

- Don't let a confident, well-formatted answer imply legal certainty it
  doesn't have — hedge explicitly on anything touching enforceability,
  deadlines, or procedure.
- Don't quote specific pasal/article numbers from memory without
  flagging they should be verified against current official text (laws
  get amended/revoked).
- Don't diagnose whether a user's specific situation constitutes a crime
  or civil violation — describe the general legal framework and defer
  the determination to a licensed advokat.
- International/cross-border questions compound jurisdiction risk even
  further — be extra explicit that multiple legal systems may apply and
  a local licensed professional in each relevant jurisdiction is needed.

## Related Skills

- `pdf` / `ocr-and-documents` — extract text from scanned contracts/letters
- `market-research-reports` — for regulatory/compliance research with the
  same evidence-traceability discipline
- `scientific-writing` — general evidence-provenance discipline that
  transfers well to legal-document claim-sourcing
