# llm-context-project-pack

A public, sanitized workflow template for running repeatable ChatGPT work with external context packs, ownership-based routing, and deterministic patch outputs.

This project is built for people who want LLM-assisted workflows to stay structured, auditable, and maintainable instead of drifting into prompt sprawl and long-chat state loss.

## Start here

### For recruiters and hiring managers
- [What this proves about me](#what-this-proves-about-me)
- [60-second demo](#60-second-demo)
- [Architecture overview](#how-the-workflow-works-at-a-glance)

### For engineers
- [`scripts/`](scripts/) for build and validation utilities
- [`docs/`](docs/) for architecture and guardrails
- [`examples/`](examples/) for sample inputs and expected outputs

### For users who want to try it
- [Quick start](#quick-start-template-workflow)
- [`Context/`](Context/) for the sample pack
- `scripts/build_project_pack.py` to generate the ZIP

## Why this exists

Long-running chat workflows often break down because context is scattered, ownership is unclear, and state updates become hard to trust. This repo shows one way to keep the workflow stable by moving context outside the chat and making updates deterministic.

## How the workflow works (at a glance)

1. Keep context outside the chat in a versioned Project Pack ZIP
2. Define file ownership and scope through a Context Index
3. Work in lightweight threads that avoid long-chat visibility problems
4. Emit deterministic operational outputs instead of free-form summaries

`TRACKER PATCH -> REMINDER PATCH -> SCHEDULE PATCH`

This keeps state auditable, lowers maintenance overhead, and makes repeated workflows easier to reason about.

## 60-second demo

Recommended path:
1. Open the architecture diagram
2. Look at the sample `Context/` pack
3. Run the build script to generate a Project Pack ZIP
4. Review a sample deterministic patch output in `examples/`

> Important: this public repo includes dummy and sample content only.
> Do not commit personal, medical, or sensitive information.

## What this proves about me

This project demonstrates how I approach engineering work:

- I design systems with explicit ownership and source-of-truth boundaries.
- I reduce ambiguity by turning workflow state into structured, auditable outputs.
- I build tooling around reliability, validation, and repeatable execution.
- I think beyond code generation and focus on maintainability, operator experience, and change control.
- I can translate an abstract workflow problem into architecture, scripts, examples, and release-ready documentation.

---

## Repo layout

- `Context/` - runnable dummy Project Pack (recommended)
- `docs/architecture/` - how the system works
- `examples/` - sample files + example workflow
- `scripts/` - utilities (header bumping, validation, ZIP pack builder)
- `examples/sample_context_files/Context/` - dummy Project Pack content

---

## Quick start (template workflow)

1) Copy `Context/` directly into your own private repo. `examples/sample_context_files/Context/` is a duplicate copy. 
2) Edit `Context/System/Context_Index.md` to match your file inventory and ownership.
3) Use `scripts/build_project_pack.py` to create a Project Pack ZIP.
4) Upload the ZIP to a ChatGPT Project.
5) Paste a Project Instructions block from `Context/System/New_Chat_Start_Templates.md` into the Project instructions.
6) Work in lightweight chats. Let the system output:
   - `TRACKER PATCH → REMINDER PATCH → SCHEDULE PATCH`
7) End of day: "End of day" → calendar-ready export.

---

## Design decisions

### Why use a Project Pack ZIP?
A versioned ZIP gives the workflow a clear, portable source of truth that can be refreshed without depending on long chat history.

### Why keep context outside the chat?
Long-running chats drift, truncate, and mix concerns. External context makes the workflow easier to audit and maintain.

### Why use a Context Index?
A Context Index defines ownership and scope for each file so the assistant can load less, route better, and avoid duplication.

### Why deterministic patches instead of free-form summaries?
Structured patch outputs make state updates easier to review, compare, and apply with less ambiguity.

### Why keep the public repo sanitized?
The workflow is intended for real operational use, so the public version demonstrates architecture and tooling without exposing private or sensitive data.

### Why move toward structured state over pure markdown state?
Stable policy belongs in documents, but higher-churn operational state benefits from stricter schemas, better validation, and cleaner read/write boundaries.

---

## Safety & privacy

- Keep private content private. Use this repo as a **template**.
- Prefer **placeholders** in public demos.
- If you want to share your system publicly: publish only architecture, examples, and scripts.

See: `docs/architecture/guardrails.md`

---

## Status

Active public MVP.

This public repository currently exposes the sanitized template, example pack structure, architecture docs, and pack-building utilities. Some newer work from the current internal version is not public yet, including stricter validation, richer state-modeling patterns, and experimental MCP-oriented extensions.

## Roadmap

- [ ] Add validation tests for pack structure, ownership rules, and sample data
- [ ] Add a 60-second visual demo and expected-output examples
- [ ] Publish a public-safe validator CLI with clearer commands and exit codes
- [ ] Expose a small read-only slice of structured state validation
- [ ] Expand release notes so each version explains what changed and why

---

## License

MIT (see `LICENSE`).
