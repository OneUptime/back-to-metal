# Changelog

All notable changes to this book are recorded here. The version lives in `package.json` and
nothing else; `book/version.py` reads it.

## [Unreleased]

## [1.1.0] - 2026-09-07

The website, laid out so it can be used rather than read. No Move changed; the book,
the PDF and the EPUB are the same 122 Moves. This is all presentation.

### Changed
- **The front page answers one question.** It used to be the whole checklist — seven
  stages, every Move, and five or six figures on every row, all of it on screen before
  the reader had decided anything. It now shows the single Move to do next: its number,
  its title, its hook, the five figures that decide whether it can start today, and a
  button to open it or tick it off. The build renders that answer, so it is correct with
  no JavaScript; script only substitutes a later Move once there is a tick to substitute
  it from.
- **The 122 rows moved to `checklist.html`,** which is the page you work down. A row is a
  tick box, a number and a title, and the title is the link. The six figures that used to
  sit on every row are still rendered on every row and hidden until asked for, because a
  column that reads `0 min` on 110 rows out of 122 is not information.
- **A row carries one flag, and only where the fact changes what you do:** `no way back`
  on the 13 Moves that cannot be undone, `NN min down` on the 12 that take the site off
  the air. The other 109 rows say nothing.
- **Each stage names the Moves with a lead time**, because nobody is working during a
  wait and a Move ordered late holds up everything behind it.
- **The symptom index moved to the front page,** which is where somebody who arrived with
  a problem rather than a programme will look. It was below the schedule drawing.
- **The masthead carries five figures instead of eight** and the navigation five links
  instead of ten. Person-days and weeks-at-three now live only on the roadmap page, which
  is the page that question belongs to; the reference pages and the downloads moved to
  the footer.
- **The rail appears only where the reader is inside the sequence** — the checklist and a
  Move — and its links point at the checklist.
- The "how to use this" box is gone, along with the only bordered tinted panel on the
  site. The page does the three things it described instead of describing them.

### Fixed
- The planner did nothing at all: `plan.html` never emitted the `.picker` root that
  `plan.js` requires, so every click was ignored.
- An author `display` rule outranked the user agent's `[hidden]`, so the planner's summary
  showed while it was still empty.

## [1.0.0] - 2026-09-06

The book itself. All **122 Moves** are written, across seven Parts, each one a complete
runbook rather than a placeholder: three named cloud services with the one thing that
genuinely differs on each, why the approach works, grouped prerequisites, a numbered
runbook, four operator's notes, a rollback that names its point of no return, a six-cell
numbers strip and a list of what can then be switched off.

### Added
- Part I, Iron (01-20): measurement, derating a vCPU, cores against licensing, memory,
  chassis and draw, management controllers, drives, capacity, the fabric, cards, cabling,
  out-of-band, suppliers, acceptance testing, spares, and the bill of materials.
- Part II, Site (21-38): what a desk cluster cannot prove, the four landing options,
  the on-premises room, the second site, the address, cross-connects, tier ratings,
  the power schedule, service credits, the exit, the cabinet, feeds, cooling, importing,
  access, the first rack, the as-built, and decommissioning.
- Part III, Cluster (39-54): addressing and the three clocks, the management VLAN, Talos,
  netboot, the control plane, Cilium, BGP, cluster DNS, local NVMe, encryption at rest,
  Ceph under Rook, OIDC, the second cluster, the restore drill, the links, and the object store.
- Part IV, Platform (55-70): workload identity, secrets, the root of trust, the registry,
  signing and admission, east-west policy and encryption, metrics, logs and traces, builds,
  Argo CD, provider-native templates, the first stateless service, the non-Kubernetes
  container services, the fixed fleet, and the workloads that stay virtual machines.
- Part V, Data (71-90): the Postgres pre-flight, the verification gate, Postgres, pgBackRest,
  quorum commit and fencing, the proprietary engines, MySQL, the licensed databases, Redis,
  brokers, queues, the event bus, Kafka, application buckets, the archive that stays, batch,
  search, document stores, the serverless estate, and orchestrated workflows.
- Part VI, Edge (91-107): your own ASN, dual-stack, transit, egress, the first VIP, BGP VIPs,
  TLS, Envoy Gateway, route translation, the API front door, edge authentication, the shadow
  edge, go-live, authoritative DNS, CDN, DDoS, and email.
- Part VII, Watch (108-122): the upgrade calendar, the fleet roll, the inventory, the 03:00
  disk, support contracts, the rota, alerting, backups and the rebuild drill, capacity
  planning, patch SLAs, audit logs, the auditor, what it costs, aborting, and the last account.
- A `Wait` column in every numbers strip, so the roadmap separates somebody's labour from
  calendar time that simply has to pass, and stops under-forecasting the programme.
- A plain "How to use this" block and one card per stage on the front page.

### Changed
- The symptom index and the equivalence table now point at the real Moves.
- `verify.py` accepts three-digit Move numbers; the website, the planner and the roadmap
  sort Move numbers numerically rather than as strings.


### Added
- The toolchain: `parse.py`, `verify.py`, `audit.py`, `build.py`, `render.py`, `site.py`,
  `epub.py`, `cover.py`, `kdpcheck.py`, `epubcheck.py`, `pricing.py`.
- The two gates. `verify.py` enforces the Move file contract, the cost arithmetic and the house
  style; `audit.py` enforces undeclared tools, unused prerequisites, unguarded destructive steps,
  unpinned installs, drifted AWS service names, the dependency invariant and repeated prose.
- Shared data modules: `deps.py`, `kit.py`, `costs.py`, `rollback_data.py`, `equivalents.py`,
  `symptoms.py`, `mission.py`, `imprint.py`.
- The website, including the migration planner: pick the Moves you need and it closes the
  dependency set, orders it, and totals the downtime, the effort and the saving.
- Print geometry for KDP at 8.25x11 with bleed, mirrored margins, spread invariants asserted at
  build time, and a vertical-justification pass in headless Chromium.
