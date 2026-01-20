# System overview

## Problem
Long chats get messy:
- "view limits" hide earlier context
- you repeat yourself
- tracking + follow-ups fall through cracks
- extraction prompts become a bottleneck

## Solution: Project Pack + ownership + patches
This system makes ChatGPT behave like a lightweight operating system:

1) **Project Pack ZIP (source of truth)**
- A ZIP containing `Context/` markdown files
- Uploaded to a ChatGPT Project (weekly or as needed)

2) **Context Index (directory + ownership map)**
- `Context/System/Context_Index.md` lists every file
- `Owns:` defines what belongs in each file (no duplicates)

3) **Thread lifecycle to avoid view-limit failures**
- The assistant recommends starting a new chat when a conversation becomes too long
- It provides a `NEW CHAT BOOTSTRAP` to continue cleanly

4) **Self-maintaining outputs (no heavy extraction)**
The assistant emits small, copy/paste updates automatically:
- `TRACKER PATCH` (single-row per company/role)
- `REMINDER PATCH` (action items with due dates)
- `SCHEDULE PATCH` (only when time blocking is required)

5) **Daily export**
- "End of day" produces a calendar-ready export of reminders with suggested times

6) **Weekly maintenance**
- Optional: a "Compression & Merge" prompt that rewrites context files and deduplicates content

## Design goals
- Low clutter
- Deterministic formats
- Easy to maintain
- Safe by default (no sensitive data in public repo)
