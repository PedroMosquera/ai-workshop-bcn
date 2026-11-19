---
title: Working With AI
output: playbook.html
extras: playbook
---

<!-- 01 TITLE -->
=== slide .title-slide .bg-img .bg-title

^ Organizer draft · for refinement

# A way of working ==with AI==.

> Habits, files and guards that turn AI output into something you can trust. Generic, copyable, and open for the organizers to change.

::: meta-row reveal
[[principles]] [[b: CLAUDE.md & rules]] [[v: spec & journal]] [[o: commands & guards]]
:::

Notes:
- One person's setup, written generically. Everything here is a proposal: cut, rename or replace whatever the organizers disagree with.
- Every code block has a copy button (top right).

<!-- 02 PRINCIPLES -->
=== slide

^ Five principles · everyone

## The rules behind everything else

::: cols-3 stagger
::: card accent-g
[[01]]

### Evidence over claims

"Done", "works", "fixed" only count with **what was run and what it printed**. "Should work" is not a status.
:::

::: card accent-o
[[o: 02]]

### A check that can't fail proves nothing

Make every test or check go red once, on purpose. A green you never saw red is a guess.
:::

::: card accent-b
[[b: 03]]

### Simple wins

The default answer to a new layer, option, flag or dependency is **no**. Complexity has to argue its way in.
:::

::: card accent-v
[[v: 04]]

### Say what you didn't check

Every "done" ends with what was **not** verified. Silence about a gap reads as "there is no gap".
:::

::: card accent-g
[[05]]

### Say it once

Preferences go in files that load every session, not in prompts you retype every day.
:::

::: card
[[o: and]]

### Remembered vs enforced

Files are **remembered** and can be ignored. Guards are **enforced**. Important rules get both.
:::
:::

Notes:
- If the audience keeps one slide, it is this one. Principles 01 and 02 are the CP3 message of the build deck.

<!-- 03 LAYERS -->
=== slide

^ Where things live · everyone

## Put each instruction at the right level

::: layers stagger
- `your prompt` | This message only. Gone next session. | [[o: once]]
- `spec.md` | This task: what to build and how we know it's done. | [[v: this task]]
- `CLAUDE.md` | This project: how to run it, project rules. Loads every session. | [[b: remembered]]
- `~/.claude/rules/*.md` | All your projects: personal habits, one file per topic. Loads every session. | [[b: remembered]]
- `skills / commands` | Saved prompts you start on purpose, like `/bug`. | [[on demand]]
- `hooks (guards)` | Scripts that run on every tool call and can block it. | [[g: enforced]]
:::

~ Rule of thumb: if you have typed the same instruction three times, it belongs one level down.

Notes:
- Verified against the Claude Code memory docs: every .md in ~/.claude/rules/ and .claude/rules/ loads at launch; CLAUDE.md is context, not enforcement.

<!-- 04 CLAUDE.md -->
=== slide

^ CLAUDE.md · everyone

## A project file the AI reads every time

::: cols-2
``` {.reveal}
# Parking app
**Run:**  npm run dev      **Test:** npm test
**Stack:** (one line)

## Rules
- Run the app and tests after every change.
  Report what you ran and what it printed.
- No new dependencies without asking me.
- Fake data only. Never real names or secrets.
- One story at a time, then stop and show me.
- End every reply with "Waiting on you:" and
  numbered questions, or "nothing".
```

::: stagger {style="display:flex; flex-direction:column; gap:clamp(.5rem,1.4vh,.9rem)"}
::: card accent-g
### Short beats complete

It loads every session and costs tokens every time. The docs suggest **under 200 lines**. Start with ten.
:::

::: card accent-b
### Start from `/init`

It drafts one from your repo. Then delete half of it.
:::

::: card accent-o
### It is a request, not a law

The AI can still ignore a line. Anything that must never happen gets a guard too.
:::
:::
:::

Notes:
- The last rule ("Waiting on you") is the one non-coders like most: questions never get lost in a long reply.

<!-- 05 RULES FOLDER -->
=== slide

^ ~/.claude/rules/ · intermediate

## Personal rules: one small file per habit

::: cols-2
::: filelist stagger
- `evidence.md` | No "done" without proof. Name what was not checked.
- `writing-style.md` | Lead with the answer. Short replies. Plain words.
- `comment-style.md` | Keep a code comment only if deleting it would lose something.
- `questions-waiting.md` | Open questions go in a numbered block at the end.
- `private-data.md` | My email and personal data never leave the machine.
- `version-bumps.md` | Never bump a version unless I ask.
:::

``` {.reveal}
# ~/.claude/rules/evidence.md
Never report "done", "works" or "fixed"
without naming the command you ran and
what its output proved.

A test only counts once you have seen it
fail on its assertion.

Every completion ends with a
**Not verified:** line.
```
:::

~ Every `.md` in this folder loads in every project. Add `paths:` frontmatter to load a rule only for matching files.

Notes:
- Each file is a pet peeve turned into an instruction. The value is that they are small and separate: easy to share, easy to delete.

<!-- 06 SPEC -->
=== slide

^ spec.md · everyone

## Write it before you build it

::: cols-2
``` {.reveal}
# <Feature>: spec
**Problem:**  what hurts, for whom, today
**Users:**    who uses it, how often
**Stories:**  As a ... I want ... so that ...
**Acceptance criteria:**
  Given ... When ... Then ...
  (someone else could check each one)
~~Out of scope:~~ what we are NOT building
**Constraints:**  stack, data, time box
**Open questions / assumptions:**
**Not verified:** (filled in when done)
```

::: stagger {style="display:flex; flex-direction:column; gap:clamp(.5rem,1.4vh,.9rem)"}
::: card accent-g
### The test for a criterion

Could **someone else** close the task against it without asking you? If not, rewrite it.
:::

::: card accent-o
### Out of scope saves money

The AI loves adding features. Naming what you won't build keeps it, and the bill, small.
:::

::: card accent-b
### Let it interview you

"Read spec.md and ask me up to 5 questions before you plan." Then edit the spec with the answers.
:::
:::
:::

Notes:
- Same shape as the build deck's spec, generalized for any feature or ticket.

<!-- 07 JOURNAL -->
=== slide

^ journal.md · everyone

## Keep a log of how the AI was used

::: cols-2
``` {.reveal}
# journal.md
**Task:**
**Tools & models:**    e.g. Claude Code, Sonnet
**Usage:**             before ___  after ___
**Best prompt:**       (paste it)
**Where it went wrong:**
**How I caught it:**
**What I'd change next time:**
**Rule to add?**       (CLAUDE.md / rules / guard)
```

::: stagger {style="display:flex; flex-direction:column; gap:clamp(.5rem,1.4vh,.9rem)"}
::: card accent-g
### Cost is part of the result

Note usage before the first prompt and after the last. Compare tasks, not feelings.
:::

::: card accent-v
### The last line is the point

Every "where it went wrong" is a candidate rule or guard. That is how the setup grows.
:::
:::
:::

Notes:
- In the workshop the Journalist role keeps this per team. Outside the workshop, one per task is enough.

<!-- 08 COMMANDS -->
=== slide

^ Commands · intermediate

## Start each kind of work the same way

::: cols-3 stagger
::: card accent-g
[[/feature]]

Agree what "done" means, name what could break, slice it small. **Before** any code.
:::

::: card accent-o
[[o: /bug]]

Reproduce it and get a **failing test** first. Only then fix it.
:::

::: card accent-v
[[v: /idea]]

Challenge the premise before designing anything. Is this the right problem?
:::

::: card accent-b
[[b: /research]]

Name the decision it informs and **when to stop**, before reading anything.
:::

::: card accent-g
[[/review]]

Decide what you are reviewing for, then verify each claim instead of trusting it.
:::

::: card accent-o
[[o: /feedback]]

Check each review comment is actually true before acting on it, or pushing back.
:::
:::

~ Each one is a short saved prompt. The point is that the first five minutes of each kind of work always go the same, good way.

Notes:
- These six exist in the presenter's setup. Pick one or two to show live; /bug is the easiest to explain.

<!-- 09 MAKE A COMMAND -->
=== slide

^ Commands · make your own

## A command is one markdown file

::: cols-2
``` {.reveal}
# .claude/skills/bug/SKILL.md
---
**name:** bug
**description:** Start a bug fix. Use when
  the user reports a bug.
---
Before changing any code:
1. Reproduce the bug. Show steps and output.
2. Write a test that fails because of it.
   Show it failing.
3. Fix it. Show the same test passing.
4. List what you did not verify.

Bug: *$ARGUMENTS*
```

::: stagger {style="display:flex; flex-direction:column; gap:clamp(.5rem,1.4vh,.9rem)"}
::: card accent-b
### Where it goes

`.claude/skills/<name>/SKILL.md` for the project, `~/.claude/skills/` for you. Then type `/bug the date picker shows yesterday`.
:::

::: card accent-g
### Older style still works

Files in `.claude/commands/<name>.md` keep working. The docs recommend skills for new ones.
:::

::: card accent-v
### Good first commands

The steps you keep forgetting: run the tests, check the spec, write the PR summary.
:::
:::
:::

Notes:
- Checked against the Claude Code skills docs: custom commands were merged into skills; $ARGUMENTS is the placeholder for what you type after the command.

<!-- 10 HAZARDS -->
=== slide

^ How careful? · everyone

## Name what a change could break, then pick the rigor

::: hazards stagger
- **Visibility** | who can see which records
- **Access** | who can do what (login, permissions)
- **Secrets** | keys, tokens, passwords
- **Money** | anything that charges or pays
- **Data loss** | deletes, destructive migrations
- **Contract** | a shape other code depends on
- **Hard to undo** | no flag, hard to roll back
- **Silent regression** | no test would catch it breaking
- **Personal data** | retention, consent
:::

::: cols-2 stagger
::: card accent-o
**One or more?** More verification: tests that fail first, a second reviewer, a careful rollout. A small diff does not remove a hazard.
:::

::: card accent-g
**None?** That is the usual answer. Normal tests, lint, done. Over-checking a routine change is waste too.
:::
:::

Notes:
- Name the hazards, do not grade them. A grade invites "it's only a little risky".

<!-- 11 GUARDS -->
=== slide

^ Guards (hooks) · advanced

## Files are remembered. Guards are enforced.

::: cols-2
::: stagger {style="display:flex; flex-direction:column; gap:clamp(.45rem,1.2vh,.8rem)"}
::: card accent-g
### Examples from a real setup

- Block commit or PR text that carries AI attribution lines or banned characters
- Block any request that contains my email address
- When an agent stops, list the comments it added and ask if each one earns its place
- Warn when UI code uses emoji as icons
:::

::: card accent-o
### How it works

A script runs before a tool call. **Exit code 2 blocks the call**, and its message goes back to the AI so it can fix the attempt.
:::
:::

``` {.reveal}
// .claude/settings.json
{ "hooks": { "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{ "type": "command",
      "command": "~/.claude/hooks/no-force-push.sh" }]
}]}}

# ~/.claude/hooks/no-force-push.sh
cmd=$(jq -r '.tool_input.command // ""')
if grep -qE 'git push.*(--force|-f)' <<<"$cmd"; then
  echo "Blocked: no force-push. Ask a human." >&2
  exit 2
fi
```
:::

Notes:
- Checked against the hooks docs: PreToolUse gets the tool input as JSON on stdin, exit 2 blocks and stderr is shown to Claude.
- The example needs jq installed. New software follows the normal approval process.

<!-- 12 DELEGATION -->
=== slide

^ Sub-agents · intermediate

## Fresh eyes and side work

::: cols-3 stagger
::: card accent-b
### Side work goes to a side agent

Long test runs, doc lookups, wide searches: a sub-agent does them and returns **the short answer**. Your main conversation stays small and cheap.
:::

::: card accent-g
### Don't grade your own homework

Review with an agent that has not seen your reasoning. Give it the code and the spec, not your conclusion.
:::

::: card accent-v
### Real example

Preparing these decks, a docs-checking agent caught **three wrong commands** on the slides before anyone saw them.
:::
:::

::: card accent-o reveal
**Parallel work (advanced):** one git worktree per independent task, so two agents never edit the same checkout. Clean them up when the task merges.
:::

Notes:
- The example is true: /usage, the double-Esc rewind condition and /mcp were corrected after a docs check.

<!-- 13 CONVERSATION HABITS -->
=== slide

^ Day to day · everyone

## Small habits, big difference

::: cols-4 stagger
::: card accent-g
[[ask]]

"Ask me questions first." Interviews beat guesses.
:::

::: card accent-g
[[answer first]]

Ask for the answer, then the reasoning. Short replies.
:::

::: card accent-g
[[waiting on you]]

Open questions in a numbered block at the end, repeated until answered.
:::

::: card accent-b
[[b: point]]

Give file paths and the 10 relevant lines. Don't paste whole logs.
:::

::: card accent-b
[[b: /clear]]

New task, new context. Old chat is re-read, and paid for, every turn.
:::

::: card accent-b
[[b: models]]

Sonnet by default. Opus to plan, only when Sonnet isn't enough.
:::

::: card accent-o
[[o: offload]]

Before pulling a huge thread or doc into the chat, ask if a cheaper tool can summarize it.
:::

::: card accent-o
[[o: stop the loop]]

Third failed try? Interrupt, rethink, give a better hint.
:::
:::

Notes:
- All of these are one-liners that can go straight into CLAUDE.md or a rules file.

<!-- 14 LEVELS -->
=== slide

^ Where to start

## Pick your level, adopt two things

::: cols-3 stagger
::: card accent-g
[[Everyone]]

- [ ] The evidence rule: "what did you run?"
- [ ] A spec with checkable criteria
- [ ] A journal per task
- [ ] "Waiting on you" block
:::

::: card accent-b
[[b: Intermediate]]

- [ ] A 10-line CLAUDE.md
- [ ] One command, e.g. `/bug`
- [ ] Fresh-eyes review by a sub-agent
- [ ] Name the hazards
:::

::: card accent-v
[[v: Advanced]]

- [ ] A personal rules folder
- [ ] One guard for your worst habit
- [ ] Side agents for verbose work
- [ ] Worktrees for parallel tasks
:::
:::

Notes:
- Ask the room at the end: which two will you adopt this week?

<!-- 15 FOR THE ORGANIZERS -->
=== slide .title-slide .bg-img .bg-closing

^ For the organizers

## Questions to settle together {style="font-size:clamp(1.6rem,4.5vw,3.2rem)"}

{.stagger style="max-width:70ch"}
- Which of these go into a **starter kit** teams copy at the start of the build?
- Which guards are safe to recommend to everyone, and which stay personal?
- Do we keep a **shared rules repo** people can borrow from?
- Where does this deck live: the general presentation, or the pit stop?
- Who demos what, and with whose setup?

Notes:
- Capture the answers in the organizers' channel, then update this deck.
