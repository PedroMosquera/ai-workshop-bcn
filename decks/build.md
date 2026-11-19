---
title: Parking App Build
output: build.html
extras: build
---

<!-- 01 TITLE -->
=== slide .title-slide .bg-img .bg-title

^ Build brief · Session 1

# The ==parking== app.

> Every team leaves today with a working parking booking app on a laptop. Any stack, any tool. Five checkpoints get us there together.

::: meta-row reveal
[[5 checkpoints]] [[b: 17:00 to 19:00, food included]] [[v: 4-5 teams]] [[o: runs locally]]
:::

Notes:
- This deck starts after the general presentation. It only covers the build.
- Clock times assume the general intro runs 17:00 to 17:15 while people grab food. If it runs long, every time after it shifts by the same amount.

<!-- 02 THE EVENING -->
=== slide

^ Thursday · 17:00 to 19:00

## Four sprints, a checkpoint after each

::: agenda reveal
- [text-3] 17:00 | Welcome, food and drinks | General intro while people grab pizza
- [blue] 17:15 | Build brief | Mission, ask the room, scope, form 4-5 teams
- [teal] 17:25 | Sprint 1 | Spec and plan, no code yet
- [purple] 17:40 | CP1 · spec & plan | Board call, spotlight team, catch-up
- [teal] 17:45 | Sprint 2 | Get it running
- [purple] 18:00 | CP2 · it runs | Board call, spotlight team, catch-up
- [teal] 18:05 | Sprint 3 | Book, release, keep
- [pink] 18:20 | CP3 · pit stop | Spotlight, lessons so far, food refill
- [teal] 18:30 | Sprint 4 | Rules hold, get demo-ready
- [blue] 18:45 | Demos · CP4 and CP5 | Every team, 2 minutes
- [text-3] 18:57 | Close | What happens next
:::

Notes:
- Food stays out the whole time. People eat during the intro and refill at the pit stop, so there is no separate meal break.
- Building time is 4 sprints of 15 minutes. If the intro overruns, shorten demos to 90 seconds, not a sprint.

<!-- 02 THE MISSION -->
=== slide

^ The mission

## "Is there a spot for me tomorrow?"

> Today nobody knows whether there is a free parking spot at the office until they get there. We build the app that answers that question, and lets people book and release spots.

::: cols-3 stagger
::: card accent-g
### See

Which spots are free for a given day.
:::

::: card accent-b
### Book

Take one spot for one day, without clashing with anyone.
:::

::: card accent-o
### Release

Give the spot back when plans change, so someone else can use it.
:::
:::

Notes:
- Three verbs. Every checkpoint maps to them.

<!-- 03 ASK THE ROOM -->
=== slide

^ Requirements · 5 minutes with the room

## The rules come from the people who park here

::: cols-2
> Before anyone opens an AI tool we collect the real rules. Shout out answers; organizers write them on a shared screen so every team builds against the same facts. {.reveal}

{.stagger}
- How many spots are there, and who can use them?
- First come, first served? Rotation? Fixed spots?
- Cars only, or motorbikes, bikes, EV chargers too?
- What happens when someone does not show up?
- How far ahead can you book?
- What do people do <span class="hl-pink">today</span>, and what hurts most?
:::

Notes:
- We do not know the real rules ourselves. That is the point: requirements come from users, not from the AI.
- Strictly 5 minutes. Unanswered questions become assumptions the team writes down in the spec.

<!-- 04 SCOPE -->
=== slide

^ Scope for today

## Build this, and only this

::: cols-2
::: card accent-g reveal
### In scope {.g}

- A list of spots and their status for a chosen date
- Book a spot for a date, under a (fake) name
- Release a booking
- The rules: no double booking, no past dates, one spot per person per day
- Data survives a refresh or a restart
:::

::: card accent-o reveal
### Out of scope {.o}

{.o}
- Login, SSO, user accounts
- Notifications, email, Slack
- Deploying anywhere, cloud anything
- Real names, plates or employee data
- Pretty. Working beats pretty today
:::
:::

~ Out of scope is not "never". It is what keeps the AI from building things nobody asked for, and keeps your token bill down.

Notes:
- If a team asks for login: tell them a name field is enough for today.

<!-- 05 HOW WE BUILD -->
=== slide

^ How we build

## Free stack, fixed rules

::: cols-3 stagger
::: card accent-v
[[v: Any stack]]

Web app, CLI, Python script, spreadsheet with a form, a claude.ai artifact. **If it does the job, it counts.**
:::

::: card accent-b
[[b: Local only]]

Runs on one team laptop, with tools already installed. No cloud machines, no shared accounts.
:::

::: card accent-g
[[Fake data]]

Seed with made-up names and spots. No real people, plates or company data in any prompt.
:::

::: card accent-o
[[o: Your budget]]

Prompts spend your own Claude allocation. Sonnet by default, Opus only to plan.
:::

::: card accent-g
[[Commit often]]

Use git if you can. Every checkpoint you pass is a safe point to go back to.
:::

::: card accent-b
[[b: Show, don't tell]]

At each checkpoint we look at the app running, not at the AI saying it works.
:::
:::

Notes:
- Budget and data rules are covered in depth in the general deck. Here, one line each as a reminder.

<!-- 06 TEAMS & ROLES -->
=== slide

^ 18 people · 4-5 teams

## Everyone has a job, not just the driver

::: cols-4 stagger
::: card accent-g
[[Product]]

### Owns the spec

Writes `spec.md`, answers the AI's questions, cuts scope, calls each checkpoint.
:::

::: card accent-b
[[b: Driver]]

### Runs the build

Drives the AI tool on their laptop. Reads what it changes before accepting it.
:::

::: card accent-o
[[o: Breaker]]

### Tries to break it

Turns the rules into checks. Proves each checkpoint really works.
:::

::: card accent-v
[[v: Journalist]]

### Logs the AI use

Prompts, models, usage spent, what went wrong. Feeds the demo and retro.
:::
:::

> Team of 3? Breaker and Journalist merge. Team of 5? Two Breakers. Each team needs one laptop that can run the app.

Notes:
- 18 people: 4 teams of 4-5 or 5 teams of 3-4. Mix levels: at least one person who has built with AI before in each team.
- Ask each team for a name now. Type it into the status board.

<!-- 07 SPEC TEMPLATE -->
=== slide

^ Starting point · spec.md

## Adapt it with the room's answers

::: cols-2
``` {.reveal}
# Parking booking: MVP
**Problem:** drivers don't know if a spot
is free until they arrive.
**Users:** anyone driving to the BCN office.
**Stack:** (team decides)

**Stories**
- See free spots for a date
- Book one spot for one day
- Release my spot if plans change

~~Out of scope:~~ login, notifications, deploy
```

``` {.reveal}
# Acceptance criteria
*Given* spot 7 is booked for Thu
*When*  someone else books spot 7 for Thu
*Then*  it is refused with a clear message

- No bookings for past dates
- One booking per person per day
- Releasing frees the spot at once
- Data survives refresh / restart
- Seed: 10 spots, fake names only
```
:::

Notes:
- Product owners can ask the AI to draft the spec from the room's answers, then edit it hard. The editing is the skill.

<!-- 08 CHECKPOINT OVERVIEW -->
=== slide

^ Five checkpoints

## Same finish line, your own route

::: cp-track stagger
- CP1 · 17:40 | Spec & plan | spec.md written, stack chosen, plan agreed with the AI
- CP2 · 18:00 | It runs | App starts on a laptop and shows the spots for a date
- CP3 · 18:20 | Booking works | Book and release a spot; data survives a refresh
- [dashed] Pit stop · 18:20 | What we learned | CP3 spotlight, lessons so far, tips, food refill
- [pink] CP4 · 18:45 | Rules hold | Double booking, past dates and duplicates are refused
- [teal] CP5 · 18:45 | Demo-ready | Run command and journal ready, checked as you step up to demo
:::

::: cols-2 stagger
::: card accent-g
### Every team covers every checkpoint

How you get there is up to you. A spreadsheet that refuses a double booking passes CP4 as much as a React app does.
:::

::: card accent-b
### After each sprint: 5 minutes

Hands off keyboards. A board call, one team in the spotlight, then catch-up for anyone behind. CP4 and CP5 are shown in the demos.
:::
:::

Notes:
- Build starts 17:25. If the intro overruns, shift every checkpoint by the same amount rather than cutting the pit stop.
- Do not wait for every team before moving on. The board shows who is behind; organizers go to them.

<!-- HOW A CHECKPOINT RUNS -->
=== slide

^ Every checkpoint · 5 minutes, hands off keyboards

## Show, borrow, catch up

::: cols-3 stagger
::: card accent-g
[[1' · board call]]

### Where is everyone?

Each team calls **done**, **in progress** or **need help**. We mark the status board.
:::

::: card accent-b
[[b: 3' · spotlight]]

### One team shows how

Not a polished demo: the route. The prompt, tool or move that got them here, and where the AI went wrong. A different team each time.
:::

::: card accent-v
[[v: 1' · catch-up]]

### Behind? Say why

One sentence on what blocked you. The room or an organizer gives you one move to try, and you take it into the next sprint.
:::
:::

> Copying is allowed. If the spotlight team's spec, stack or prompt works, use it.

~ Spotlights at CP1, CP2 and the CP3 pit stop. Teams that have not had one open the demos.

Notes:
- Pick the spotlight team from the board: ahead, and not shown yet. With 5 teams, 3 get a spotlight and 2 open the demos. With 4 teams, 3 and 1.
- The catch-up minute is for teams marked need help. An organizer sits with them for the first 5 minutes of the next sprint.
- Hold the 5 minutes. Cut questions, not the next sprint.

<!-- 09 CP1 -->
=== slide style="--cp-color: var(--teal)"

::: cp-layout
::: cp-left reveal
!! CP1

::: cp-meta
[[17:40]] [[Spec & plan]]
:::

## We know what we are building

> No code yet. A short spec and a plan the whole team agrees with.
:::

::: cp-right stagger
::: card accent-g
### Must show

- [ ] `spec.md` with stories, acceptance criteria and out of scope
- [ ] Assumptions written down for questions the room did not answer
- [ ] Stack chosen, and the laptop that will run it
- [ ] A plan from the AI: data model, screens or commands, build order
:::

::: card
### How we check

Product owner reads the 3 stories and the plan's build order out loud in 30 seconds.
:::

::: card accent-o
### Behind?

Borrow the spotlight team's spec layout. Then: "Read spec.md and ask me up to 5 questions before proposing a plan. No code yet."
:::
:::
:::

Notes:
- Teams that start coding before CP1 usually come back to it at CP3. Hold the line.

<!-- 10 CP2 -->
=== slide style="--cp-color: var(--blue)"

::: cp-layout
::: cp-left reveal
!! CP2

::: cp-meta
[[b: 18:00]] [[b: It runs]]
:::

## Something is alive on a laptop

> The thinnest possible slice: start it, see the spots. Hard-coded data is fine.
:::

::: cp-right stagger
::: card accent-b
### Must show

- [ ] The app starts with one command (or one click)
- [ ] It lists the seeded spots, about 10, with fake data
- [ ] You can pick a date and see each spot as free or taken
- [ ] First commit (or a saved copy) done
:::

::: card
### How we check

Driver starts it from scratch while an organizer watches. No "it worked a minute ago".
:::

::: card accent-o
### Behind?

Take the stack the spotlight team got running, or the simplest one: one file, hard-coded spots, no framework.
:::
:::
:::

Notes:
- Most common blocker here is environment setup. Steer stuck teams to the simplest stack they already have installed.

<!-- 11 CP3 -->
=== slide style="--cp-color: var(--purple)"

::: cp-layout
::: cp-left reveal
!! CP3

::: cp-meta
[[v: 18:20]] [[v: Booking works]]
:::

## Book it, release it, keep it

> The core loop works end to end, and nothing is lost when the app reloads.
:::

::: cp-right stagger
::: card accent-v
### Must show

- [ ] Book a spot for a date under a fake name; it shows as taken
- [ ] Release that booking; the spot is free again
- [ ] Refresh or restart: the booking is still there
- [ ] Committed
:::

::: card
### How we check

Breaker books spot 3 for tomorrow, restarts the app, shows it is still booked, then releases it.
:::

::: card accent-o
### Behind?

Cut to book and persist only. A JSON file, SQLite, browser storage or a sheet: whichever your stack makes easiest.
:::
:::
:::

Notes:
- This is the checkpoint most teams should reach no matter what. If a team is far behind at 18:20, help them cut to just book + persist.

<!-- PIT STOP -->
=== slide style="--cp-color: var(--text-3)"

^ CP3 + pit stop · 18:20 · 10 minutes

## Hands off keyboards. What have we learned?

::: cols-3 stagger
::: card accent-b
[[b: 2' · hands up]]

### How are we using it?

- [ ] Asked for a plan before any code?
- [ ] Switched model, or stayed on Sonnet?
- [ ] Threw work away and started over?
- [ ] Caught the AI claiming something untrue?
:::

::: card accent-v
[[v: 4' · spotlight + catch-up]]

### One ahead, one stuck

The CP3 spotlight team (2 min), then the team furthest behind (1 min), plus a minute of questions:

- The prompt that moved you forward
- Where the AI went wrong
- What you would tell the other teams
:::

::: card accent-g
[[2' · journalists]]

### Write it down now

Best prompt so far, usage so far, one thing you would do differently. Memories fade by the demos.

[[o: 2' · organizer tips (next)]] {style="margin-top:auto"}
:::
:::

Notes:
- The spotlight goes to the third team to show. The stuck team's minute is the most useful story in the room: protect it.
- Mark the board from the tables while people refill. No separate board call here.
- Count the hands out loud and write the numbers in the shared notes; they feed the session 2 summary.
- Keep it to 10 minutes. It doubles as the food and drink refill, so say so: hands off keyboards, grab a slice, listen.
- CP4 needs the time. Sprint 4 starts at 18:30 sharp.

<!-- PIT STOP TIPS -->
=== slide

^ Pit stop · tips for the second half

## Habits from the organizers

::: cols-4 stagger
::: card accent-o
[[o: 01]]

### Make your check fail once

Building this deck, our slide checker said "all OK" for every slide. It was measuring a hidden frame. We only found out by planting a broken slide on purpose.
:::

::: card accent-g
[[02]]

### No output, no claim

"Done", "fixed", "tests pass": ask **what did you run, and what did it print?** If there is no output, it did not happen.
:::

::: card accent-b
[[b: 03]]

### Fresh eyes review

New session (or `/clear`), then: "Review this against spec.md and list what fails." A clean context has not heard the excuses.
:::

::: card accent-v
[[v: 04]]

### Say it once, in a rules file

Repeating yourself? Put it in `CLAUDE.md`: run the app after each change, no new dependencies without asking, fake data only.
:::
:::

> All four point at CP4: prove it works, do not take the AI's word for it.

Notes:
- Tip 01 is a true story from preparing this session. Tell it in 30 seconds.
- Swap a tip for something you saw at the tables if it is more relevant.

<!-- 12 CP4 -->
=== slide style="--cp-color: var(--pink)"

::: cp-layout
::: cp-left reveal
!! CP4

::: cp-meta
[[o: 18:45]] [[o: Rules hold]]
:::

## Try to break it, and fail

> The acceptance criteria, proven by the Breaker, not by the AI saying "all good".
:::

::: cp-right stagger
::: card accent-o
### Must show (each one refused, with a clear message)

- [ ] Two bookings for the same spot on the same day
- [ ] A booking for a date in the past
- [ ] A second booking by the same person on the same day
- [ ] Empty or nonsense input (no name, invalid date)
:::

::: card
### How we check

Breaker runs them live in your demo. Bonus: an automated test, shown failing on purpose.
:::

::: card accent-o
### Behind?

Paste the acceptance criteria and ask the AI to check each one against the code and tell you which fail, with evidence.
:::
:::
:::

Notes:
- Ask the AI "what did you run to verify that?" Teams that get a claim without output should not mark CP4 done.

<!-- 13 CP5 -->
=== slide style="--cp-color: var(--teal)"

::: cp-layout
::: cp-left reveal
!! CP5

::: cp-meta
[[18:45]] [[Demo-ready]]
:::

## Someone else could run it

> Wrap up so the work survives today and can be compared in session 2.
:::

::: cp-right stagger
::: card accent-g
### Must show

- [ ] A README with the one-line command to run it
- [ ] `journal.md` filled in: models, usage before/after, best prompt, where it went wrong
- [ ] A 2-minute demo planned: one booking, one refused double booking, one learning
- [ ] Final commit; code shared with the organizers (repo link or zip)
:::

::: card accent-b
### Done early?

Pick one: "my bookings" view, a week view, automated tests, or a nicer UI. Not login.
:::
:::
:::

Notes:
- Collect code and journals at the end. The journals are what we compare in session 2.

<!-- 14 STATUS BOARD -->
=== slide #board-slide

^ Status board

## Where every team is

@board

Notes:
- Marks are saved in this browser only. Run the deck from the same laptop all session.
- "Clear board" resets everything immediately, with no confirmation. Avoid it during the session.

<!-- 15 JOURNAL -->
=== slide

^ The Journalist's template

## journal.md

::: cols-2
``` {.reveal}
# journal.md
**Team / stack:**
**Tools & models:**   e.g. Claude Code, Sonnet
**Usage:**            before ___  after ___
**Checkpoints:**      CP1 __ CP2 __ CP3 __ CP4 __
**Best prompt:**      (paste it)
**Where it went wrong:**
**How we caught it:**
**Next time we would:**
```

::: reveal
> Apps will differ by stack. The journals show **how each team got there**, and what it cost.

~ Note the clock time you reached each checkpoint. It tells us where teams lose time. {style="margin-top:.8rem"}
:::
:::

Notes:
- Start the journal at 17:25, not at the end. Usage "before" must be noted before the first prompt.

<!-- 16 DEMOS -->
=== slide

^ 18:45 · demos · CP4 and CP5

## Two minutes per team

::: cols-3 stagger
::: card accent-g
[[60 s]]

### Show the app

One booking, one refused double booking. Live, on your laptop.
:::

::: card accent-b
[[b: 60 s]]

### One learning

The prompt that worked, or the moment the AI went wrong and how you caught it.
:::

::: card accent-v
[[v: Board]]

### Where you got to

Your last checkpoint passed, and the time it took. Usage spent, if you measured it.
:::
:::

> Applause for the best bug found, not only the best app.

Notes:
- 4-5 teams at 2 minutes is 8 to 10 minutes, 18:45 to about 18:57. Strict timer. Teams that had no spotlight go first.
- The demo is where CP4 (a refused double booking) and CP5 (run command, journal) are checked.

<!-- 17 NEXT SESSIONS -->
=== slide

^ After today

## The next checkpoints, in later sessions

::: cols-3 stagger
::: card accent-b
[[b: Session 2]]

### One app

Compare the team versions, pick a direction, merge into one codebase with tests.
:::

::: card accent-v
[[v: Session 3]]

### Run & observe

Run it somewhere shared and observe it with a Dynatrace tenant.
:::

::: card
[[o: Stretch]]

### On the platform?

If the pace allows: a Dynatrace App the office can actually use.
:::
:::

~ Later sessions get their own checkpoints, set from what today's board and journals show.

Notes:
- Infrastructure for session 3 is still open: no cloud machines are available today. Do not promise a date.

<!-- 18 CLOSE -->
=== slide .title-slide .bg-img .bg-closing

^ 17:25 · build starts now

# Go ==build==.

> CP1 at 17:40: spec and plan, no code. Then the first spotlight.

Notes:
- Start the timer. Leave the checkpoint overview or the status board on screen during the build.
