# Sanitization checklist (public template repo)

Goal: keep this repo **100% safe to publish**. It must show the system without exposing personal, medical, employer, or job-search pipeline data.

## What is allowed in this public repo
- Architecture docs (`docs/architecture/**`)
- Scripts (`scripts/**`)
- Example workflows + **dummy** context files (`examples/**`)
- Placeholder values like:
  - `ExampleCo`, `SampleCorp`, `Recruiter A`, `Hiring Manager`, `you@example.com`
  - generic time windows (e.g., `19:00–20:00`) with no personal patterns

## What must NEVER be in this public repo
- Real names (yours or other people), real emails, phone numbers, addresses
- Real company pipelines / recruiter threads / interview dates tied to real companies
- Any medical/clinical details (sleep meds, anxiety notes, therapy transcripts)
- Any private ZIPs, transcripts, chat exports, screenshots containing sensitive info
- Tokens, API keys, secrets, access links, private repo URLs

---

## Pre-commit checklist (run every time)

### 1) Visual scan (fast)
- Search the diff for anything that looks like:
  - a real person's name
  - a real company you're interviewing with
  - an exact calendar date/time you wouldn't share publicly
  - personal constraints that are too specific (medical, finances, relationships)
- Confirm the examples use placeholders (`ExampleCo`, `SampleCorp`).

### 2) Run these local searches
Run from repo root:

- Find emails:
  - `git grep -nE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"`

- Find phone-like patterns:
  - `git grep -nE "(\+?\d[\d\s().-]{7,}\d)"`

- Find obvious secrets:
  - `git grep -nE "(api[_-]?key|secret|token|password|bearer\s+|PRIVATE KEY|BEGIN RSA|BEGIN OPENSSH)"`

- Find "too real" job-search artifacts:
  - `git grep -nE "(offer|onsite|codesignal|leetcode|recruiter|hiring manager|interview scheduled)" examples/`
  - If present, ensure it's generic and not tied to real companies/people.

### 3) Ensure you're not accidentally committing packs/exports
- Confirm `.gitignore` blocks:
  - `*.zip`
  - `*.txt` (optional if you ever export transcripts)
- Confirm you are not committing:
  - `Project_Pack*.zip`
  - transcript files
  - screenshots

### 4) Commit-history safety check (important)
If you ever committed sensitive content and then deleted it, it can still exist in git history.

- If this repo has EVER had sensitive content committed:
  - Prefer: create a fresh clean repo and re-push sanitized content only.
  - Or use `git filter-repo` to purge history (advanced).

---

## Safe placeholder rules (recommended)
Use these placeholders everywhere:
- People: `Recruiter A`, `Hiring Manager`, `Engineer`
- Companies: `ExampleCo`, `SampleCorp`, `FinTechCo`
- Links: `https://example.com/job`, `https://linkedin.com/in/example`
- Dates: prefer relative or generic dates in examples (e.g., `2026-01-19` is fine if it's clearly demo-only)

---

## Release checklist (before tagging v0.1.0)
- README matches the repo description ("About")
- `docs/sanitization_checklist.md` exists
- Examples contain placeholders only
- Scripts run:
  - `python scripts/validate_context.py` (if applicable to the template)
- No sensitive strings found by the grep checks above

---

## If you want extra safety (optional)
Add a CI check later:
- run `git grep` patterns in a GitHub Action and fail if any match.
