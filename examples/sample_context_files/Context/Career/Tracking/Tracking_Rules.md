Version: 1
LastUpdated: 2026-01-19

# Patch formats (canonical order)

TRACKER PATCH
- File: Context/Career/Tracking/Job_Search_Tracker.md
- Change: update
- Key: <Company> | <Role>
- Stage: <Outreach/Scheduling/Assessment/Technical Screen/Onsite/Offer/Closed>
- LastTouch: <YYYY-MM-DD> (<what happened>)
- NextAction: <one line>
- DueDate: <YYYY-MM-DD or None>
- Notes: <max 1 line>

REMINDER PATCH
- Entity: <Company | Role>
- Action: <what to do>
- DueDate: <YYYY-MM-DD>
- Priority: High/Med/Low
- Source: <why this reminder exists>

SCHEDULE PATCH
- File: Context/Global/Active_Schedule.md
- Change: add/update
- Date: <YYYY-MM-DD>
- Window: <time range or TBD>
- Task: <one line>
- Duration: <minutes>
- Priority: High/Med/Low
