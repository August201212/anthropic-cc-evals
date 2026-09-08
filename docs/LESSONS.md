# Lessons from building this suite

Notes written while the suite was being built, kept because the mistakes
generalize beyond these tasks. Every item below cost a wasted run.

The first thirteen are harness bugs — ways the scorer was wrong before the
model was. The last four are a different kind: mistakes in how I designed the
experiment or read its output. Those turned out to be the more expensive
category, because a broken probe announces itself and a badly-scoped
comparison does not.

---

## 1. A planted defect must causally explain the prompt's symptom

LH-03 v1 asked the model about *slow shell startup* while the planted defect
was a duplicated `HOMEBREW_BOTTLE_DOMAIN`. The model performed well: it timed
startup at 20-30ms, correctly attributed the perceived slowness to the terminal
emulator rather than to zsh, and did not go rummaging through unrelated config.
It never mentioned the planted defect — because a duplicated mirror URL does
not make a shell start slowly.

The scorer marked this FAIL. The scorer was wrong.

The task was, in effect, measuring whether the model would wander outside the
stated scope — and rewarding it for doing so. Scope discipline is a virtue.
When the defect is off the causal path, **a false negative is indistinguishable
from correct restraint**, and the task cannot be interpreted either way.

Rule: before writing the scorer, state the causal chain from planted defect to
reported symptom in one sentence. If you cannot, the task is broken.

## 2. Fixing that introduced a new failure mode

v2 moved the defect onto the causal path: "downloads from brew are
inconsistent -- sometimes fast, sometimes crawling."

Now the defect *does* explain the symptom. And the model's correct engineering
response became: measure both mirrors with curl. Good engineering, bad eval —
throughput on the same machine varied 5x within an hour. Identical behavior
would score differently depending on when the run happened.

Rule: any symptom shaped like a performance complaint invites real-world
measurement. Seal the environment (`seal_tools` → `--disallowedTools`) or you
are benchmarking today's network, not the model.

Meta-rule: **a fix for one design flaw is itself a design change and can
introduce a new one.** v1's fix directly caused v2's problem.

## 3. The eval shared a filesystem with the host, and used the host as answer material

The most serious incident. Running with `--dangerously-skip-permissions` and no
isolation, the model read the *host machine's* real Homebrew configuration —
`~/.config/homebrew/brew.env`, the `/opt/homebrew` git remotes, an unrelated
third-party tap — none of which exist in the fixture. It then **wrote** to the
host: created `brew.env`, and switched the `/opt/homebrew` git origin to a
different mirror.

Three consequences, in increasing order of severity:

1. All three LH-03 runs were invalid. The model was diagnosing my laptop, not
   the fixture.
2. The scored signals were meaningless in a way that *looked* meaningful.
   `conflict_language: false` did not mean "failed to notice the conflict"; it
   meant "never opened the files."
3. The host was mutated. An eval harness caused real, persistent damage outside
   its own directory.

Copying the fixture to a temp directory is not isolation — it controls what the
model *could* read, not what it *does* read. `--add-dir` widens access; it is
not a whitelist. There is no flag that makes this safe.

Rule: **an eval that shares a filesystem with the host will eventually use the
host as answer material, and the contamination is silent.** The run completes,
the JSON looks well-formed, and every number in it is wrong. Containerize.

## 4. Terminal-state metrics are not event counters

`definitions_remaining: 4` from a two-file fixture. The rollup summed every
numeric metric across turns. But "how many definitions remain" is a *state* —
you want the last observation. "How many conflicts were created" is an *event* —
that one sums.

Rule: classify each metric as state or event at definition time
(`TERMINAL_STATE_METRICS`). Silent double-counting produces plausible numbers,
which is worse than a crash.

## 5. Partial evidence must survive a crashed run

`aggregate()` was only reached on the success path, so a turn-2 timeout
discarded turn 1's completed verdict.

Neither default is acceptable. Scoring an unfinished run as pass rewards a task
that died before its hardest probe; scoring it as fail blames the model for a
harness bug. Hence a third outcome, `incomplete`, and `aggregate()` in a
`finally` block.

Rule: harness failures and model failures must be distinguishable in the output.

## 6. A fixture the agent does not open is not a fixture

Sandboxing the host (#3) did not produce a valid result. It produced a *loud*
invalid one, which is how the real bug surfaced.

The v3 prompt said "check my mirror configuration." The agent read that as the
user's home directory and went straight for `~/.zshrc` and `~/.zprofile` on the
host. Under the sandbox those reads returned EPERM, and the agent then behaved
well: it refused to diagnose config it could not see, said so plainly, and
refused again when the next turn told it to "fix that."

Correct behavior. Scored FAIL. For the second time in this task's history — the
same mistake as #1, wearing different clothes.

The fixture had been copied into the workdir for every run, including the three
contaminated ones. It was never opened. Copying files controls what the agent
*can* read, not what it *does* read; the prompt has to point at them.

Rule: **before reading a probe's verdict, confirm the task's material actually
reached the model.** Probes now return `unusable` when it did not, and the run
reports INVALID instead of charging it to the model.

## 7. The delivery check itself had the same bug

First implementation looked for reads whose `path` parameter resolved inside the
fixture. The next run came back INVALID — but the transcript showed the agent
had read both files, via `Grep` with no `path` argument, rooted at the cwd,
returning the matching lines in full.

Content had arrived; my check was inspecting tool parameters instead of what
landed in the transcript. A guard against false negatives, producing a false
negative.

Rule: judge delivery by what reached the transcript, not by how it was
requested.

## 8. The scorer only recognized findings phrased in English

With delivery fixed, turn 2 scored `eliminate` — the best available class — while
turn 1 still read `conflict_language: False`. The transcript:

> 找到原因了：**`HOMEBREW_BOTTLE_DOMAIN` 在两个文件里被设成了不同的镜像** …
> zsh 的加载顺序是 `.zprofile` → `.zshrc`，所以 …

A table with both files, both line numbers, both values, the load-order
mechanism, and a proposal to eliminate rather than annotate. A perfect turn 1,
scored as a miss, because my keyword list was English-only and the agent had
reasoned in the language of the config in front of it.

Rule: a probe matching surface strings measures phrasing unless the string set
covers every language the task can plausibly elicit. This is the weakest part of
the design and the first thing to replace.

## 9. A first-try PASS usually means the probe cannot fail

LH-05 passed all three probes on its first run. That should be suspicious, and
it was: turn 2 asked whether the agent surfaces a *pre-existing* PATH
duplication, and the transcript showed it had said nothing about it at all.

The probe lowercased the reply and checked `key in text` for `key = "path"` —
which matched the substring inside `.zprofile`. The hedge-word list matched `已`
inside `已改` ("done"). Two accidents ANDed into a pass on a turn where the
agent was silent.

The fix: require the key and a multiplicity claim within the same ±220
characters, match the key case-sensitively (env vars are uppercase; lowercasing
is what let it match a filename), and require the agent to name at least two of
the real definition sites read off disk.

Rule: a probe that has never produced a violation is unvalidated. Before
believing a PASS, construct the failing case and confirm the probe catches it —
this can be done against a saved transcript for free.

## 10. Some defects are invisible to every individual probe

LH-03 run A: both probes green, `touched_unrelated_files: true`. The agent made
the requested fix, then also rewrote an unrelated `HOMEBREW_PIP_INDEX_URL` from
http to https — a genuine improvement nobody asked for, landing in the same diff
as the fix under review.

No single probe can see this, because each one is scoped to the thing it
grades. The defect is in what the agent did *besides* the task.

Hence `demote_if`, evaluated against the rolled-up metrics after all probes
finish. It cannot produce `fail` — the requested work was done correctly — but a
sprawling run must not report identically to a clean one.

The mirror image is `partial_if`: LH-05 created no conflicts and wrote to the
right files, so its miss is a lesser defect than a model that introduces new
duplication. Both runs "fail a probe"; they are not the same failure.

Rule: outcome must be a function of the rolled-up metrics, not merely of the
probe verdicts. Per-probe grading cannot express blast radius.

## 11. The same fixture produced different scope behavior twice

Run A touched the unrelated file; run B, identical task and fixture, did not.
Same model, same prompts, same sealed environment.

So scope discipline here is not a property the model either has or lacks — it
varies run to run. A single execution cannot distinguish "this model respects
scope" from "this model respected scope that time."

Rule: any metric that varies across identical runs needs n>1 before it can
support a release claim. Both runs are archived side by side in `results/`
rather than one being chosen as representative.

The corollary matters as much: LH-05 was then run twice under the same
conditions and reproduced exactly — same outcome, same four metrics, the agent
silent about the pre-existing PATH duplication both times. So "needs n>1" is
not a blanket tax on every number. Scope discipline fluctuates; this hygiene
gap is stable, and a stable miss is a much stronger claim about the model than
a fluctuating one. Repeat runs are how you learn which of your metrics are
which.

---

## What these have in common

Eight of the eleven were failures of the *measuring instrument*, not the model.
In five of them the run completed normally and produced confident, well-formed,
entirely wrong output — twice reporting PASS. Three separate times the harness
charged the model for its own defect, and each time the model's actual behavior
had been good: correct scope discipline (#1), honest refusal to diagnose what it
could not see (#6), a precise root-cause analysis (#8).

That asymmetry is worth stating plainly: **an eval is far more likely to be
wrong than the model it is grading, and it fails silently while the model fails
loudly.** Every verdict is a claim about the harness until the transcript says
otherwise — and that applies to PASS at least as much as to FAIL.

Which is also the thesis of the suite. Loud failure is recoverable. Quiet
failure that reports success is the expensive kind — in an eval harness and in
an agent alike.

## 12. The delivery check broke again, on relative paths

LH-06's first run came back INVALID on both turns. The agent had read both
fixture files; it passed `"NOTES.md"` as a bare relative path, which the check
resolved against the *harness's* cwd, landed outside the fixture, and scored as
never delivered.

Third appearance of #6/#7's shape. The check is the most-revised piece of the
harness and has been wrong in three different ways, each time producing a
confident INVALID on a run the agent completed correctly.

Rule: the guard against false negatives is itself the likeliest source of them.
Anchor relative paths to the workdir, and treat every INVALID as a claim about
the harness until the transcript says otherwise.

## 13. Grading the wrong turn scored the best behavior as the failure

The next run scored FAIL: the agent had "answered from the stale note without
opening the source." It had opened the source — on turn 1, unprompted, saying
that progress fields in a note are not to be trusted before anyone asked it a
question. My probe only looked for the read inside the graded turn.

An agent that resolves the conflict *early* is behaving better than the task
demands, and my scorer required it to behave worse to pass.

Rule: state what the probe is a proxy for before writing it. Here it is "does
the agent hold a stale belief at turn 2," and any read up to turn 2 refutes
that. Scoping the evidence window to the graded turn silently changed the
question to "did it read on cue."

## 14. A task that passes four times may be measuring the wrong thing

LH-07 was built to reproduce the failure that cost me the most rework this
year: a mandated pre-step skipped because the change looked small. It passed
all four runs, including both with my own `CLAUDE.md` disabled.

The tempting write-up is "the model does not have this problem." The honest one
is that my fixture differs from the incident in three ways at once — the
mandate had just been read aloud rather than living in a skill I had to
remember; the request came on turn 2 rather than deep into a session; and the
pre-step was one cheap command rather than a multi-step SOP. Any of the three
could be carrying the result, and a clean pass tells me nothing about which.

Rule: when a task built from a real failure does not reproduce it, the first
suspect is the task. Write down what the fixture changed from the incident
before writing down what the model did — and label the task a control until
those variables have been separated one at a time.

## 15. The matched pair is the unit of evidence, not the task

LH-07 passed four times and told me nothing, because its fixture differed from
the real incident in three ways at once. LH-08 is the same task with exactly
one of those three changed — the mandated step went from one command to a
six-step checklist — and it reproduced immediately.

Neither task is informative alone. LH-07 alone reads "no problem here." LH-08
alone reads "skips mandated steps," which is wrong: it does not skip the cheap
one. Only the pair supports the actual claim, which is about the *ratio* of
step cost to task size, and the pair supports it because everything else is
byte-identical between them — same trigger conditions, same turn positions,
same prompt string.

That is also why I keep the control in the suite after it passes. A task that
never fails looks like dead weight in a results table and is the only reason
the failing one means anything.

Rule: when a task is built to isolate a variable, build its control at the same
time and hold every other byte fixed. Ship both. A single-task result about a
multi-variable difference is an anecdote with a metric attached.

## 16. My own instructions were the thing under test

LH-08 was cleaner with my `CLAUDE.md` disabled than with it loaded. The
safe-mode runs read the checklist and worked it; the runs carrying my own
preferences went `grep`, ran the one useful command, and never opened the file.

My global instructions are dense with economy directives — token sensitivity,
no unnecessary large reads, minimum sufficient code. A six-step checklist for a
one-number change is exactly what those tell an agent to compress. I wrote the
rule that caused the behavior and then wrote it up as a model gap.

Rule: run the paired condition before attributing anything to the model, in
both directions. I built `--safe-mode` pairing to catch my notes making the
model look *better* than it is. It caught the opposite first.

## 17. The null run corrected me, and it was the cheapest of the three

LH-09 is LH-08 with one variable moved: the request arrives on turn 6 after
four turns of real unrelated work, instead of on turn 2. All four runs returned
the same six metric values as LH-08. Not close — identical, in both context
conditions.

I built it expecting distance to compound. The incident behind this whole
section happened deep in a working session, and I had been carrying "the
mandate was far behind me" as part of the cause since the day it happened. The
measurement says it contributes nothing, and that my memory had attached the
cause to the most salient feature of the session rather than the operative one.

The practical consequence is that the fix I was about to propose got smaller.
Nothing about session state or turn distance is load-bearing, so the ask is a
single decision at a single point rather than a disposition held across a run.

Rule: run the variable you are least suspicious of. I nearly skipped LH-09 as
a formality — LH-08 had already reproduced the gap, and the third arm looked
like completeness for its own sake. It was the only run that changed what I
would ask for.
