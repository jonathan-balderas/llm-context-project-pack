# Deterministic patch output preview

This file is a public-safe, illustrative preview for the current public repository.

The goal is to show the shape of deterministic outputs:
- structured
- reviewable
- copy/paste-friendly
- safer than free-form operational summaries

---

## TRACKER PATCH
```text
Company|Role|Pipeline|Stage|Updated|Notes
Acme Analytics|Senior Backend Engineer|Top|Recruiter Screen Scheduled|2026-03-14|Recruiter=Jane Doe; Channel=LinkedIn; NextStep=Recruiter screen on 2026-03-18 11:00 ET
```

## REMINDER PATCH
```text
Date|Time|Type|Target|Action|Details
2026-03-17|10:00 ET|follow_up|Acme Analytics|Follow up with recruiter if no reply|Recruiter=Jane Doe; Channel=LinkedIn
```

## SCHEDULE PATCH
```text
Date|Start|End|Category|Task|Details
2026-03-18|19:00|20:00|interview_prep|Prepare for Acme Analytics recruiter screen|Review resume story, company notes, and role fit
```

---

### Why this matters
Instead of burying workflow state in long conversational text, the system can emit deterministic artifacts that are easier to review, compare, and apply.