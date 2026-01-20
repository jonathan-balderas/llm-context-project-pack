Version: 1
LastUpdated: 2026-01-19

NOTE (Manual Use)
- This file documents **operating rules** for the Project Pack workflow.

These rules are NOT automatically active.
They only apply when:
- pasted into Project Instructions, or
- explicitly referenced in a chat.

Think of this file as a **playbook**, not automation.

## Thread Lifecycle (anti-visibility bottleneck)

LLMs have view limits. This workflow treats that as a real constraint.

Recommend a new chat when:
- the unit of work changes
- the chat becomes long
- a long paste is about to be introduced

When recommending a new chat, output:
1) **NEW CHAT BOOTSTRAP** (copy/paste block)
2) **Carryover summary** (1–3 bullets; decisions only)
3) **Relevant context files** (max 6 paths)

This keeps chats lightweight and avoids relying on unseen history.

---

## Patch Output Order (Canonical)

State updates should be explicit and deterministic.

Always emit patches in this order:
1) **TRACKER PATCH**
2) **REMINDER PATCH**
3) **SCHEDULE PATCH**

Rules:
- Do not skip earlier patches if later ones are present
- Keep patches minimal and directly applicable to files
- Prefer patch outputs over post-hoc extraction
