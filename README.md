# Back to Metal

**How a company leaves the cloud, in twenty moves**, by the makers of
[OneUptime](https://oneuptime.com), published three ways: a printable
book, a reflowable EPUB, and a static website you can host anywhere.

Most writing about leaving the cloud is either an opinion piece or a programme plan for a
company with a platform team. This is neither. It is twenty jobs, in five stages, sized for a
company with two or three engineers and a cloud bill somewhere around $24,000 a month.

📕 **[dist/Back-to-Metal.pdf](dist/Back-to-Metal.pdf)** &nbsp;·&nbsp;
📖 **[dist/Back-to-Metal.epub](dist/Back-to-Metal.epub)** &nbsp;·&nbsp;
🌐 **[site/](site/)** — open `site/index.html`

## Twenty Moves, five stages

| | | |
|---|---|---|
| **1 · Decide** | 01–04 | Work out whether to do it at all |
| **2 · Buy** | 05–08 | Order the hardware and sign the space |
| **3 · Build** | 09–12 | Turn the boxes into a cluster |
| **4 · Move** | 13–16 | Move the app, then the data |
| **5 · Run** | 17–20 | Cut the traffic over, and keep it alive |

Each Move is one job, with a stated cutover in minutes of user-visible downtime, a stated
risk, and a rollback that names its point of no return. Each can be done on a Tuesday and
undone on a Wednesday, and you can stop after any of them and still be somewhere coherent.

## It is honest about the size of it

The first edition of this book had 122 Moves. It was correct, and it was 975 person-days and
four and a half years of elapsed time for three engineers, which is not a plan a company can
act on. This edition is the same argument at a size somebody can finish: the whole thing is
around eighty person-days — the table at the foot of this file has the exact figure, computed
from the Move files — and most of the calendar is waiting for hardware rather than working.

The exact figures are in the table at the foot of this file, and they are computed from the
Move files rather than typed.

## It is honest about what not to move

Move 04 concludes that you should keep paying somebody else for three things: a content
delivery network, outbound email deliverability, and denial-of-service scrubbing at the edge.
Each is a business other people run better than you will, and each is cheap next to what it
replaces. Move 03 gives you permission to read three Moves, do the arithmetic and stop, which
is a cheaper outcome than a programme abandoned in month five with two platforms running.

And the comparison counts the salary. Half an engineer of ongoing work is a larger line than
the hardware, and a comparison that omits it is the reason repatriations get approved and then
regretted.

## Three clouds, one runbook

Every Move covers **AWS, Google Cloud and Azure**. The job is the same whichever you are
leaving; only the extraction differs, so only the extraction is written three times. Each Move
opens with three lines naming the real product on each provider and the one thing that is
genuinely different there — a flag that needs a reboot, a tier that cannot do it at all, a
resource that outlives its parent. The runbook itself is written once.

## The dependency invariant

Every Move's prerequisites are **lower-numbered Moves**. A reader who has reached Move 14 has,
by construction, met every prerequisite of Move 14. That is not a stylistic choice — the build
refuses to compile a book where it does not hold, and it is what lets the website's checklist
read top to bottom rather than search a graph.

## Layout

```
moves/       the twenty Move files, numbered from 01 — the source of truth
book/        the typesetter and the site generator
  parse.py       markdown -> structured Move data
  verify.py      structure: the contract, the arithmetic, the house style
  audit.py       content: undeclared tools, unguarded destructive steps,
                 unpinned installs, drifted service names, repeated prose
  build.py       Move data -> a self-contained book.html
  render.py      html -> PDF via headless Chromium, vertically justified
  site.py        Move data -> a static website in site/
  epub.py        Move data -> a reflowable EPUB3
  cover.py       the paperback wrap, the Kindle cover, the hardback case
  deps.py        which Moves must be finished before which
  kit.py         the reference build, the laptop kit, the seven rules
  costs.py       the cost model, with the salary line in it
  equivalents.py AWS to Google Cloud to Azure to what you run instead
  rollback_data.py  the safety page every Move's rollback derives from
  symptoms.py    the symptom index — "which Move do I need"
  icons.py       stage glyphs, the cutover gauge, the risk bars
  style.css      the print stylesheet
  web/           the site's stylesheet and script
dist/        the built PDF, EPUB and covers
site/        the built website
build/       intermediate HTML (gitignored)
```

## Building

```bash
make deps       # fonts, playwright, chromium
make verify     # structure — must be clean
make audit      # content — must be clean
make book       # markdown -> HTML -> PDF -> KDP compliance check
make site       # markdown -> static website
make            # all of it, and the tables in this README
```

Python 3.9 or newer with `playwright` and a Chromium build available to it. The Makefile prefers
`.venv/bin/python3` when it exists, so `python3 -m venv .venv && make deps` works without
activating anything.

`verify.py` and `audit.py` are the gate and both must come back clean. `verify.py` checks the
shape of every Move: the sections, the three-cloud block, the cost arithmetic, and that no Move
moving persistent state ships without saying how the state comes back. `audit.py` goes after the
things that are actually wrong in infrastructure writing — a runbook calling a tool the
prerequisites never mentioned, a destructive command with nothing standing behind it, software
installed without a version, a service spelled four ways, prose copy-pasted between Moves.

## The website

`site/` is self-contained — the fonts are embedded in the stylesheet and nothing is fetched at
runtime — so it drops onto any static host unchanged. It is five pages and one page per Move:
**the guide** is the whole plan on one page, **what it costs** is the arithmetic, **your
checklist** is where you are and what is next, **before you start** is the safety page, and
**about** is the book. Every page carries one link to the next Move you have not ticked.

## Contributing

The most valuable contribution is a **correction**. If you ran a runbook and it did not work as
written, that is worth an issue on its own. [CONTRIBUTING.md](CONTRIBUTING.md) covers the
workflow; [AGENTS.md](AGENTS.md) documents the Move contract, the house style the build
enforces, and what not to hand-edit.

## Licence

Two licences, because this repository is two things:

- **The software** — the toolchain in `book/`, the print stylesheet, the site's stylesheet and
  script — is [MIT](LICENSE).
- **The content** — the Moves, the written text of the book — is
  [CC BY 4.0](LICENSE-CONTENT).

So you may share and adapt any of it, for any purpose including commercially, as long as you
give credit.

<!-- generated: everything below this line is written by book/readme.py -->

## The book at a glance

| | |
|---|---|
| Moves | 20 |
| Stage 1 · Decide | 4, 01–04 |
| Stage 2 · Buy | 4, 05–08 |
| Stage 3 · Build | 4, 09–12 |
| Stage 4 · Move | 4, 13–16 |
| Stage 5 · Run | 4, 17–20 |
| Work | 80 person-days |
| End to end, two engineers | 32 weeks, most of it waiting for hardware |
| At zero downtime | 18 of 20 |
| Whole book, end to end | 25 minutes of user-visible outage |
| Cannot be undone | 0 |
| Risk | 3 low, 7 medium, 10 high |
| Dependencies | 31, every one pointing backwards |
| Line savings across the Moves | $20,123 a month, before the salary and the cage |
| Saving, with everything counted | $16,625 a month &mdash; $199,500 a year, 69 per cent of a $24,000 bill |

Every Move names the real service on AWS, Google Cloud and Azure, and the one thing that differs on each.

## Stage 1 · Decide

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 01 | [The bill, and the three lines that are most of it](moves/01-the-bill-and-the-three-lines-that-are-most-of-it.md) | — | Low | 0 min | Immediately |
| 02 | [What you actually run](moves/02-what-you-actually-run.md) | — | Low | 0 min | Immediately |
| 03 | [The number that decides it](moves/03-the-number-that-decides-it.md) | — | Medium | 0 min | Immediately |
| 04 | [The three things you keep renting](moves/04-the-three-things-you-keep-renting.md) | Nothing — this Move decides what stays rented | Low | 0 min | Immediately |

## Stage 2 · Buy

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 05 | [From rented vCPUs to cores you own](moves/05-from-rented-vcpus-to-cores-you-own.md) | The vCPU as a unit of purchase | Medium | 0 min | Until the order is signed |
| 06 | [Five machines, and the one on the shelf](moves/06-five-machines-and-the-one-on-the-shelf.md) | Elastic node capacity and cluster autoscaling | High | 0 min | Until the order is signed |
| 07 | [A cage, not a data centre](moves/07-a-cage-not-a-data-centre.md) | The region-and-zone abstraction | High | 0 min | Until the contract is signed |
| 08 | [The order, and the weeks you cannot compress](moves/08-the-order-and-the-weeks-you-cannot-compress.md) | Provider-assigned addresses and managed transit | Medium | 0 min | Until the order is signed |

## Stage 3 · Build

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 09 | [Racking day](moves/09-racking-day.md) | The provider's serial console and boot diagnostics | Medium | 0 min | Immediately |
| 10 | [The network, and the way back in when it breaks](moves/10-the-network-and-the-way-back-in-when-it-breaks.md) | Cloud-managed private networking | High | 0 min | Immediately |
| 11 | [A cluster, in an afternoon](moves/11-a-cluster-in-an-afternoon.md) | The managed Kubernetes control plane | High | 0 min | Immediately |
| 12 | [Disks: what goes local, what goes on Ceph](moves/12-disks-what-goes-local-what-goes-on-ceph.md) | Managed block and shared-file storage | High | 0 min | Immediately |

## Stage 4 · Move

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 13 | [Images, secrets and one-command deploys](moves/13-images-secrets-and-one-command-deploys.md) | Managed registries, secret stores and hosted CI runners | Medium | 0 min | Immediately |
| 14 | [The first service, end to end](moves/14-the-first-service-end-to-end.md) | Managed container compute | Medium | 0 min | Immediately |
| 15 | [Buckets, cache and queues](moves/15-buckets-cache-and-queues.md) | Managed object storage, Redis and queues | High | 0 min | 30 days |
| 16 | [Postgres, the one that matters](moves/16-postgres-the-one-that-matters.md) | Managed PostgreSQL | High | 15 min | 7 days |

## Stage 5 · Run

| # | Move | Leaving | Risk | Cutover | Back out for |
|---|---|---|---|---|---|
| 17 | [The front door](moves/17-the-front-door.md) | Managed layer-7 balancers and certificate services | Medium | 0 min | Immediately |
| 18 | [Go-live, and how you abort](moves/18-go-live-and-how-you-abort.md) | Weighted DNS and the parallel managed edge | High | 10 min | 7 days |
| 19 | [Backups you have restored, and the pager](moves/19-backups-you-have-restored-and-the-pager.md) | Managed backup, alarms and a rented paging service | High | 0 min | Immediately |
| 20 | [Closing the account](moves/20-closing-the-account.md) | The provider organisation, its audit trail and its support plan | High | 0 min | 30 days |
