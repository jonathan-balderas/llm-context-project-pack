# Diagram: Project Pack Workflow Template (text explanation)

This diagram summarizes the core idea of the repo:

**Make ChatGPT workflows reliable by externalizing state and enforcing deterministic outputs.**

---

## The three pillars

### 1) Context Index (ownership)
A **Context Index** defines:
- what context files exist
- what each file *owns* (scope)
- where each rule/template belongs

This prevents drift and duplication. If something is "global", it has a single owner file. Everything else references it, not copies it.

---

### 2) Thread lifecycle (view-limit aware)
Long chats can hide earlier context ("view limits"). This system treats that as a real constraint and uses a thread lifecycle rule:

- When a chat becomes long or a new unit-of-work appears, the assistant recommends a new thread.
- It provides a **NEW CHAT BOOTSTRAP** (copy/paste) with:
  - the task
  - what to paste
  - which context files are relevant
  - 1–3 carryover bullets (decisions only)

Result: chats stay lightweight and correctness doesn't depend on unseen text.

---

### 3) Patch outputs (deterministic, low clutter)
Instead of relying on extraction prompts, the assistant emits small, deterministic "patches" that you can apply to your context files.

Canonical order:

**TRACKER PATCH → REMINDER PATCH → SCHEDULE PATCH**

- **TRACKER PATCH**
  - Updates a single current row per company/role
  - No history log (keeps it clean)

- **REMINDER PATCH**
  - Creates actionable follow-ups with a due date
  - Designed for daily accumulation and export

- **SCHEDULE PATCH**
  - Only produced when time-blocking is required
  - Keeps schedule short-horizon (no stale history)

---

## Why this works (in one sentence)
This system separates **reasoning** (LLM) from **state** (versioned Markdown), and uses deterministic outputs to keep workflows auditable and maintainable.

---

## 30-second talk track
"The key idea is separating reasoning from state. The Project Pack ZIP is the source of truth, the Context Index defines ownership so nothing drifts, and threads are view-limit-aware so I never depend on hidden context. Every session produces deterministic patches—tracker, reminders, schedule; which keeps workflows auditable and low-maintenance."

---

## How to use this repo (high level)
1) Edit `Context/` (dummy template here; your private version lives elsewhere).
2) Build a Project Pack ZIP from `Context/`.
3) Upload the ZIP to a ChatGPT Project.
4) Paste Project instructions from `Context/System/New_Chat_Start_Templates.md`.
5) Use the patches + daily export to maintain state without heavy extraction.
