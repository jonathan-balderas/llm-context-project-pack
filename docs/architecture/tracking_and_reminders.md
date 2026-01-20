# Tracking + reminders + schedule

## Tracker
File: `Context/Career/Tracking/Job_Search_Tracker.md`

Rule:
- one current row per Company | Role
- update in place
- no historical log

## Reminders
File: `Context/Global/Reminders.md`

Rule:
- only outstanding reminders (unexported)
- cleared on "End of day" export (or when done)

## Schedule
File: `Context/Global/Active_Schedule.md`

Rule:
- short-horizon commitments + availability windows
- no stale history

## Daily export
Trigger:
- "End of day" or "daily closeout"

Output:
- calendar-ready list with suggested times
