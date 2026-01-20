# State management

## State lives in files (not memory)
This system assumes:
- ChatGPT does not reliably "remember everything"
- Long chats are partially invisible
- The source of truth must be external, stable, and versioned

## The 3 layers of state

### 1) Project state (Project Pack ZIP)
- Uploaded into the Project
- Contains all authoritative context files
- Updated weekly or after major changes

### 2) Chat state (current conversation)
- What's visible in the current chat
- May be incomplete due to view limits

### 3) Output patches (deterministic "diffs")
- Each response can emit compact patches that you apply to the Project Pack files
- This reduces the need for extraction

## Canonical patch order
Always emit:
1) TRACKER PATCH
2) REMINDER PATCH
3) SCHEDULE PATCH

## Thread lifecycle policy (view-limit aware)
Start a new chat when:
- new unit of work appears
- the chat is long and the user is about to paste large text
- earlier details may be missing and required for correctness

When recommending a new chat, output:
1) NEW CHAT BOOTSTRAP
2) carryover summary (1–3 bullets)
3) relevant files to consult (paths)
