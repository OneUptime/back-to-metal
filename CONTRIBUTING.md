# Contributing

The most valuable contribution to this book is a **correction**. If you ran a runbook and it did
not work as written, or a price is wrong for your region, or a project named here has been
archived since publication — that is worth an issue on its own, and it is worth more than a new
Move.

## Reporting something that did not work

Open an issue with the Move number and, if you can:

- what you ran and what happened
- the versions involved (the runbook should have pinned them; if it did not, that is also a bug)
- whether the rollback worked

You do not need a fix. A well-described failure is the contribution.

## Setting up

```bash
git clone https://github.com/OneUptime/back-to-metal
cd back-to-metal
make deps      # fonts, playwright, chromium
make           # verify, audit, book, site
```

Python 3.9 or newer. The Makefile prefers `.venv/bin/python3` if you make a virtualenv, so
`python3 -m venv .venv && make deps` works without activating anything.

## Changing a Move

1. Edit the file in `moves/`. Do not touch `dist/`, `site/` or `build/` — they are generated.
2. `make verify && make audit`. Both must report zero problems.
3. `make` to regenerate everything.
4. Look at the affected spread in `dist/Back-to-Metal.pdf`. The typesetter will always make
   a page fit; you are checking that what it did is reasonable.
5. Commit the source **and** the regenerated `dist/` and `site/`.

## Adding a Move

Read [AGENTS.md](AGENTS.md) first — it documents the file contract in full, and `verify.py` is
unforgiving about it. In short:

- Copy an existing Move as the template.
- Number it next in sequence, inside the right stage. Stages occupy contiguous number ranges.
- Add its prerequisites to `book/deps.py`. **Every dependency must be a lower-numbered Move**;
  the build refuses a forward reference.
- Fill `The numbers` honestly. The saving percentage is checked against the arithmetic, and the
  cutover cell is checked against the meta line.
- Write the `Rollback` section before you write the runbook. It has to name the point of no
  return, and if the Move touches persistent state it has to say how the state comes back.

Renumbering existing Moves is expensive — it changes filenames, the dependency map, the symptom
index and every cross-reference. Prefer replacing a Move within its stage: this edition is
twenty Moves on purpose, and a twenty-first has to earn its place against one already there.

## What gets rejected

- **Vendor advocacy.** A Move recommends a tool because of what it does, not because of who makes
  it. If you work on the project you are adding, say so in the pull request.
- **Runbooks nobody has run.** Every Move in this book is meant to be executable. If you have not
  executed it, mark the pull request as such and it will be labelled unverified rather than merged.
- **Optimism about downtime.** The `Cutover` field is the number a reader plans a maintenance
  window around. A Move claiming five minutes for a job that takes forty is the worst kind of
  mistake this book can make.
- **Marketing language.** `verify.py` has a banned-word list and it is not negotiable. "Simply"
  is on it.

## Style

British English. Plain, declarative sentences. Describe what happens to the system and why.
Metric first where a unit appears. No exclamation marks, no second person imperative stacked
three deep, no "just".

The house voice is: *somebody competent, telling you what they know, without selling you
anything.*

## Licences

By contributing you agree that your contribution is licensed under the same terms as the rest of
the repository: [MIT](LICENSE) for anything in `book/`, and
[CC BY 4.0](LICENSE-CONTENT) for the text of the Moves.
