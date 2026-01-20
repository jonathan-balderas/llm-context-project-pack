# Example workflow (end-to-end)

## Setup (weekly)
1) Update your private context files locally.
2) Run:
   - `python scripts/validate_context.py`
   - `python scripts/build_project_pack.py`
3) Upload the ZIP to your ChatGPT Project (Project files).
4) Paste Project Instructions from:
   - `Context/System/New_Chat_Start_Templates.md`

## Daily
### Recruiter replies batch
- Start a new chat using "Recruiter Replies - Batch (up to 10)"
- Paste R1..R10
- Receive:
  - reply options
  - TRACKER PATCH / REMINDER PATCH / (optional) SCHEDULE PATCH

### End-of-day export
- Send: `End of day`
- Receive calendar-ready reminders with suggested times

## Weekly maintenance (optional)
- Run the "Compression & Merge Prompt"
- Apply rewritten context files
- Rebuild ZIP
