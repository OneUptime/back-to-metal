# Prefer a project virtualenv if one exists, so `make` works whether playwright
# was installed globally or into .venv (see README).
PY := $(shell [ -x .venv/bin/python3 ] && echo .venv/bin/python3 || echo python3)

.PHONY: all deps verify audit test webcheck agree releasable book covers epub pricing amazon artefacts site kdp readme clean

# The build is a chain of renders, none of which parallelises, and one of the
# links is an ordering nobody would guess from the dependency graph alone - see
# `artefacts` below. Serial is what this Makefile means, so it says so.
.NOTPARALLEL:

all: verify audit artefacts

deps:
	npm install
	$(PY) -m pip install -r requirements.txt
	$(PY) -m playwright install chromium

verify:
	$(PY) book/verify.py

audit:
	$(PY) book/audit.py

test:
	$(PY) -m unittest discover -s book -p 'test_*.py'

# The third gate, and the only one that opens the site in a browser. verify.py
# checks the shape of a Move and audit.py checks its content; neither of them
# can see that a chart rendered as an empty band, which is what shipped in
# 3.0.0. Needs site/ built, and playwright, which `make deps` installs.
webcheck: site
	$(PY) book/webcheck.py

# The fourth gate. The same figures are published by three different renderers
# into a website, a printed interior and a README, and the saving can honestly
# be divided by two denominators - so it has been divided by the wrong one
# three times, in three files, each caught by somebody reading two outputs side
# by side. This reads the built artefacts and fails if they disagree.
agree: epub site readme
	$(PY) book/agree.py

# The release gate: a bumped version, a written changelog entry, nothing left
# under [Unreleased], a tag that is free, and an EPUB identifier that has not
# moved. Deliberately not part of `all` — CI has to stay green while work is in
# progress, and this is the one check that must not be true until it is.
releasable:
	$(PY) book/release.py --notes build/release-notes.md

book:
	$(PY) book/build.py
	$(PY) book/render.py
	$(PY) book/kdpcheck.py

covers: book
	$(PY) book/cover.py

epub: covers
	$(PY) book/epub.py
	$(PY) book/epubcheck.py

pricing:
	$(PY) book/pricing.py

# Everything needed to submit to Amazon: interior, both wraps, the Kindle
# edition, and the margin check. You should not be able to prepare a submission
# whose economics do not work. CI builds the artefacts without this, so a
# business decision nobody has taken yet cannot turn the build red.
amazon: verify audit book covers epub
	$(PY) book/cover.py --require-hardback
	$(PY) book/pricing.py

# Everything a release publishes, in the order it has to be built.
#
# site.py copies the interior and the Kindle edition out of dist/ into site/,
# because the website offers both as downloads. So the EPUB has to exist before
# the site is generated, or site/ ships whichever one happened to be committed.
# `make book site covers epub` looks equivalent and is not: make walks goals
# left to right, and site.py would run first.
artefacts: test book covers epub site webcheck readme agree

site: epub
	$(PY) book/site.py

kdp:
	$(PY) book/kdpcheck.py

readme:
	$(PY) book/readme.py

clean:
	rm -rf build site
