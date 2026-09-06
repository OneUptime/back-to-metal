# Changelog

All notable changes to this book are recorded here. The version lives in `package.json` and
nothing else; `book/version.py` reads it.

## [Unreleased]

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
