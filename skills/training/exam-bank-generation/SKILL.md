---
name: exam-bank-generation
title: "Secure Exam Question Bank Generation"
description: "Generate encrypted exam question banks for assessments."
tags: ["assessment", "exam", "question-bank", "encryption", "github"]
---

# Secure Exam Question Bank Generation & Encryption

## Trigger
Use this skill when building large exam/assessment question banks (100-1000 questions) with:
- ABCD multiple-choice format
- Encrypted answer keys separate from questions
- Private GitHub repo deployment
- Framework-mapped metadata (MITRE ATT&CK, NIST CSF, ISO 27001, OWASP)
- Controlled access to answer keys

## Core Workflow (5 phases)

### Phase 1: Question Generation & Structuring

**JSON Structure:**
```json
{
  "id": 1,
  "q": "Question text (max 200 chars)",
  "category": "offensive|defensive|governance|mixed",
  "difficulty": "Easy|Medium|Hard|Expert",
  "correct": "A|B|C|D",
  "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
  "tags": ["framework:mitre-t1595", "nist:DE.AE-1"],
  "created": "YYYY-MM-DD"
}
```

**Validation:**
- All questions have ID, text, category, difficulty, options A/B/C/D, correct answer
- No duplicates
- Randomize question order (don't sequence answers A→B→C→D)
- No missing fields

**Output:** `<name>_questions.json` (questions only, no answers yet)

---

### Phase 2: Answer Key Extraction & Encryption

**Process:**

1. Extract answer key only (remove from question file):
   ```json
   {
     "soal_1": {
       "question": "Question text",
       "correct_answer": "A|B|C|D",
       "category": "...",
       "difficulty": "..."
     }
   }
   ```

2. Encrypt using Fernet (AES-128):
   ```python
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()
   cipher = Fernet(key)
   encrypted = cipher.encrypt(answer_key_json.encode())
   ```

3. Save:
   - `kunci_jawaban.bin` — encrypted binary (unreadable without key)
   - `ENCRYPTION_KEY.txt` — key storage (KEEP OFFLINE!)

4. Destroy plaintext answers from memory

**Pitfall:** Never commit encryption key to GitHub (public or private). Store separately.

---

### Phase 3: Directory Structure & Documentation

**Directory layout:**
```
exam-bank-<name>/
├── soal/
│   └── <N>_questions.json         # Questions only (shareable)
├── kunci-jawaban/
│   ├── kunci_jawaban.bin          # Encrypted answers
│   └── ENCRYPTION_KEY.txt         # Key (offline storage)
├── metadata/
│   └── questions_metadata.json    # Breakdown per category/difficulty
└── README.md                       # Documentation
```

**README content:**
- Total question count + category/difficulty breakdown
- Security notice: key not in repo, answers encrypted
- Decryption instructions (Python + Fernet)
- Access control guidelines
- Last updated timestamp

**Pitfall:** Never include key in README. Reference as "obtained separately from administrator."

---

### Phase 4: GitHub Private Repo Setup

**Process:**

1. Initialize local repo:
   ```bash
   cd exam-bank-<name>
   git init
   git config user.email "bot@localhost"
   git config user.name "automation"
   git add -A
   git commit -m "Initial: <N> questions + encrypted answer key"
   ```

2. Add remote:
   ```bash
   git remote add origin https://github.com/vanderstark/exam-bank-<name>.git
   git branch -M main
   ```

3. Push:
   ```bash
   git push -u origin main
   ```

4. Verify:
   - GitHub repo is PRIVATE (not public)
   - All files uploaded (.bin included)
   - No key in plaintext files

**Pitfall:** Verify PRIVATE status before pushing. Verify in GitHub web UI.

---

### Phase 5: Access Control & Key Distribution

**Pattern:**

1. Store encryption key OFFLINE:
   - Encrypted disk
   - Password manager
   - Local machine only (never cloud)

2. Distribute key separately from repo link:
   - In-person handoff
   - Encrypted message (GPG, Signal)
   - Never via email/Slack/unencrypted channels

3. Provide decryption script:
   ```python
   from cryptography.fernet import Fernet
   key = b'<PASTE_KEY_HERE>'
   cipher = Fernet(key)
   encrypted_data = open('kunci_jawaban.bin', 'rb').read()
   plaintext = cipher.decrypt(encrypted_data).decode()
   # Save to secure location (offline file, not screen)
   print(plaintext)
   ```

4. Document access log:
   - Who has key
   - When granted
   - When revoked

---

## Validation Checklist

Before release:

- [ ] Question count correct
- [ ] No duplicate questions
- [ ] All fields present (ID, text, category, difficulty, options, correct answer)
- [ ] Answer key encrypted (verify .bin is binary/unreadable)
- [ ] Encryption key present & valid
- [ ] GitHub repo PRIVATE
- [ ] README has decryption instructions (no key included)
- [ ] Questions JSON has NO correct answers
- [ ] Decryption script tested locally
- [ ] Access log created

---

## Common Patterns

### Multi-tier Exam Banks
For different difficulty levels:
```
exam-bank-<domain>/
├── easy/
│   └── <50>_questions.json
├── medium/
│   └── <75>_questions.json
├── hard/
│   └── <75>_questions.json
└── kunci-jawaban/
    ├── answers_all.bin
    ├── answers_easy.bin
    ├── answers_medium.bin
    └── answers_hard.bin
```
Encrypt each tier separately; enable staged access.

### Framework-Mapped Tags
Link questions to compliance frameworks:
```json
"tags": [
  "mitre-attck:T1595",
  "nist-csf:DE.AE-1",
  "owasp:A03:2021-Injection",
  "iso27001:A.6.1.1"
]
```
Generate coverage reports per framework.

### Scoring Metadata
Add points if exam is weighted:
```json
"points": 5,
"bonus": 1
```

---

## Troubleshooting

**cryptography module not found:**
```bash
pip3 install cryptography
```

**GitHub push auth error:**
```bash
gh auth login
gh repo create exam-bank-<name> --private
git push -u origin main
```

**Key accidentally committed:**
- Remove from history immediately (git filter-branch / BFG Repo Cleaner)
- Regenerate key
- Rotate all access

**Questions too long / formatting issues:**
- Max 200 chars per question
- Standardize terminology
- Use bullet lists in options for complex scenarios

---

## Performance

| Task | Time |
|------|------|
| Generate 200 questions | 30-45 sec |
| Encrypt answers | <1 sec |
| GitHub push | 5-10 sec |
| Decrypt answers | <1 sec |

Scales to 1000+ questions; split files beyond 500 for organization.

---

## Security Best Practices

✅ **DO:**
- Keep key offline
- Distribute key separately from repo
- Use Fernet (AES-128) or stronger
- Test decryption before delivery
- Document access log
- Rotate key annually or after revocation

❌ **DON'T:**
- Commit key to GitHub
- Share key via email/chat/Slack
- Use hardcoded keys in scripts
- Store key on shared drives
- Reuse same key across banks

---

**Last updated:** 2026-08-16 | **Status:** Production-ready
