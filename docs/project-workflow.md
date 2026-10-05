# Project Workflow with AI

One workflow for every project: software, video, documents, automation.
The core is the same; software adds its own steps in section 4.

---

## 1. Size the project first — it decides how many steps you run

| Size | Signs | Steps |
|---|---|---|
| **S — small** | A few hours, only you use it, breaking is fine | S1 (5 lines) → S5 → S6 |
| **M — medium** | A few days, a few users, data worth keeping | S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 |
| **L — large** | Real users, money, personal data, long-lived | All 8 steps + all of section 4 |

When unsure, pick one size up. If a project grows, upgrade it — don't restart.

---

## 2. The eight core steps

### S1. Define "done" — in a file

M and L projects: first capture the raw problem in `docs/intent.md` — customer words, user bug reports,
screenshots, verbatim, unanalyzed. Keeping it separate stops "what people need" from blurring into "what I plan to build".

Then write `docs/spec.md` (or `brief.md` for video), one page max:

```markdown
# <Project name>
Problem:      <who has what problem>
Users:        <who, where, on what device>
Deliverable:  <what file/app/video, in what format>
MVP includes: <3–5 features/parts>
NOT this time: <list explicitly>
Done when:    <MEASURABLE criteria, one per line>
Constraints:  <deadline, budget, required tools>
```

"Done" criteria must be checkable by a machine or by eye, never vague:
- ❌ "the app runs smoothly" → ✅ "home page loads in under 2 seconds on 4G"
- ❌ "a good video" → ✅ "16:9, under 90 seconds, subtitles match the voice, strict QA PASS"

**Check:** someone else (or a fresh AI session) reads the spec and restates the goal correctly.

### S2. Research — don't rebuild what exists

- Is there a tool / library / template / skill that already does 70% of it?
- Record each choice and **why** in the spec (one line per choice).
- Prefer popular, maintained, well-documented options — the AI knows them better too.

**Check:** every choice has a reason; you have run the tool's smallest example.

### S3. Design — sketch the frame before building

Answer 4 questions in `docs/architecture.md` (skip for S projects):
1. What **parts** does it have? (software: UI / logic / data / auth / file storage —
   video: sources / edit / audio / graphics / export)
2. How does data **flow** from where to where?
3. What is the **core data**, and where does it live?
4. Where is the **highest risk** (fragile, hard to fix, touches money/permissions/copyright)?

**Check:** you can point at the diagram and trace one feature end to end.

### S4. Break it down — tasks small enough for the AI to get right in one pass

```
Project → Phase → Feature → Task
```

Every task meets all 3 conditions:
- Touches **few files / parts** (ideally 1–3 files, or 1 video scene).
- Has its own **done criteria**.
- Is **usable/checkable immediately** when finished, without waiting on another task.

List them in `docs/plan.md` with `[ ]` / `[x]`. Order: **a working skeleton first, polish later.**

**Check:** no task reads like "build the backend".

### S5. The build loop — repeat for EACH task

```
┌─► 1. Give the AI the task + its done criteria
│   2. AI does it
│   3. YOU review the change (code diff / frames / draft)
│   4. Run checks (tests / QA / proofread)
│   5. Pass → SAVE (git commit) → tick [x] in the plan
└── 6. Fail → fix, max 3 rounds → still broken: STOP, see section 5
```

Loop rules:
- **One task at a time.** Never hand over "build all of feature X".
- **Save after every passing task.** A commit is a save point: when the AI goes astray, roll back instead of untangling.
- **Not reviewed by you = not done.** The AI saying "done" doesn't make it done.
- **A second reviewer (person or agent)** for M and L projects (software: `/review`; video: `/review-video`).

### S6. Test like a real user

Forget the code; use the product like a stranger:
- Walk the main flow start to finish.
- Try wrong input, random clicks, slow network, a phone screen.
- Video: watch it fully on a phone, with sound on and off.

Check every "Done when" line in the spec — any line not met means not shipped.

### S7. Deliver

- The deliverable must run in the **recipient's** environment, not just yours.
- Include short instructions: how to use it, known limitations.
- Tag every release (git tag `v1.0`, `v1.1`…) and keep the previous one so you can
  **roll back immediately** if the new one breaks. Video: keep the previous file, never overwrite.
- Irreversible actions (publishing online, sending to a client, posting) → **ask the decision-maker first**.

### S8. Monitor → Fix → Learn

- Log the problems users hit; prioritize by impact.
- Major bug or new request → write it into `intent.md` → **back to S1**. The workflow is a loop, not a line.
- Fix bugs by: **reproduce → fix → reproduce again and see it gone** (`/fix`).
- After every project/release, answer 3 questions and **anchor each lesson in something that runs**
  (a test, script, checklist, CLAUDE.md) — plain notes get forgotten (`/rut-kinh-nghiem`):
  1. What took the most time?
  2. Which bug reached users? Why did the checks miss it?
  3. What will change in the workflow next time?

---

## 3. Same workflow, different project types

| Step | Software | Video | Documents / content |
|---|---|---|---|
| S1 Done means | Features + measurable criteria | Aspect ratio, length, target platform | Reader, length, purpose |
| S2 Research | Frameworks, libraries, APIs | Footage, music, reference videos | Sources, data |
| S3 Design | Architecture, data model | Script, shot list | Outline |
| S4 Task | One small feature | One scene / segment | One section |
| S5 Check | Tests, lint, build | `video_qa.py --strict`, inspect frames | Proofread, verify sources |
| S6 As a user | Run the main flow | Watch on a phone | Someone else reads it |
| S7 Deliver | Deploy | Export to spec | Export PDF/DOCX |

---

## 4. Software only — additions by size

| Item | S | M | L |
|---|:-:|:-:|:-:|
| Git, commit after every task | ✅ | ✅ | ✅ |
| Project `CLAUDE.md` (run command, test command, prohibitions) | ✅ | ✅ | ✅ |
| Unit tests for important logic | — | ✅ | ✅ |
| Integration tests (API + database) | — | ✅ | ✅ |
| E2E tests for the main flow (Playwright…) | — | — | ✅ |
| Security review (`/security-check`) | — | ✅ | ✅ |
| Staging environment separate from production | — | — | ✅ |
| CI runs tests before every merge (GitHub Actions) | — | ✅ | ✅ |
| Production error tracking & logs (Sentry…) | — | — | ✅ |
| Database backups, with a tested restore | — | ✅ | ✅ |
| Deploy by tag, with a tested rollback command | — | — | ✅ |
| Evals — sample prompts + scoring criteria (only if the app calls an AI) | — | ✅ | ✅ |

**Security — always verify yourself, never trust the AI on these:**
- Secrets/API keys: only in `.env`, and `.env` is in `.gitignore`.
- Permissions: user A cannot read/edit user B's data (Supabase: RLS on every table).
- User input: always validated on the server, not just in the UI.
- New libraries: real, maintained, correctly named (AIs often invent package names).
- Delete / payment / email actions: confirmed and logged.

In this repo, the agent chain already covers S3–S5 for software:
`/build-feature` = `app-planner → app-builder → code-reviewer → app-tester → security-reviewer`.

---

## 5. Working with AI — rules that keep a project from drifting

1. **Context lives in files, not in your head.** `spec.md`, `architecture.md`, `plan.md`,
   `CLAUDE.md` — a new session only needs to read them to continue.
2. **State the criteria, not just the task.** "Add login; done when a wrong password shows
   an error and there is a test" beats "add login".
3. **3 failed fix rounds → change approach**, don't try a 4th:
   new session, restate the problem more tightly, split the task smaller, or read the error yourself.
4. **"Done" from the AI must come with evidence**: the command run + its real output.
5. **One heavy workstream at a time.** Several AIs editing the same place overwrite each other.
6. **Important decisions belong to a human**: goals, architecture, spending, publishing/sending anything out.

---

## 6. New project checklist (5 minutes)

```
[ ] Sized as S / M / L
[ ] docs/spec.md exists with measurable "Done when"
[ ] git init done, .gitignore exists (includes .env)
[ ] CLAUDE.md exists: how to run, how to check, prohibitions
[ ] docs/plan.md exists with a small enough first task
```

## 7. Pre-delivery checklist

```
[ ] Every "Done when" line in the spec checked and met — with evidence
[ ] Used it yourself like a real user (S6)
[ ] No secrets / real data left in code or deliverables
[ ] Runs in the recipient's environment
[ ] Unfinished / unverified parts are stated explicitly
[ ] Asked before any irreversible action
```
