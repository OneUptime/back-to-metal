# Prefer a project virtualenv if one exists, so `make` works whether playwright
# was installed globally or into .venv (see README).
PY := $(shell [ -x .venv/bin/python3 ] && echo .venv/bin/python3 || echo python3)

.PHONY: all deps verify audit book covers epub pricing amazon site kdp readme clean

all: verify audit book site readme

deps:
	npm install
	$(PY) -m pip install -r requirements.txt
	$(PY) -m playwright install chromium

verify:
	$(PY) book/verify.py

audit:
	$(PY) book/audit.py

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

site: book
	$(PY) book/site.py

kdp:
	$(PY) book/kdpcheck.py

readme:
	$(PY) book/readme.py

clean:
	rm -rf build site
