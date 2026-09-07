"""The release gate, and the notes that go with it.

`make verify` checks the shape of the book and `make audit` checks its content.
This checks the shape of the *release*: that the version was bumped, that
somebody wrote down what changed, that the tag is not already pointing somewhere
else, and that the one identifier which must never move has not moved.

It is a separate gate from CI on purpose. CI runs on every push and must stay
green while work is in progress, which means it cannot demand a bumped version
or a written changelog entry. The release workflow runs this instead, once, on
the commit that is about to become a release, where those demands are exactly
right.

    python3 book/release.py                  # check, and say what it found
    python3 book/release.py --notes FILE     # check, then write the notes

Every check is derived from a file in the repository. Nothing here is a figure
somebody has to keep up to date by hand.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from version import VERSION
import imprint as IMP

CHANGELOG = ROOT / 'CHANGELOG.md'
SEMVER = re.compile(r'^\d+\.\d+\.\d+$')


def git(*args):
    """Run a git command, or return None where there is no usable repository.

    The gate has to work from a source tarball as well as from a checkout, so
    anything that needs history is skipped rather than failed when there is no
    history to read.
    """
    try:
        out = subprocess.run(('git',) + args, cwd=ROOT, capture_output=True,
                             text=True, check=False)
    except OSError:
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def git_ok(*args):
    """Whether a git command succeeded, for the ones whose answer is the exit code."""
    try:
        return subprocess.run(('git',) + args, cwd=ROOT, capture_output=True,
                              check=False).returncode == 0
    except OSError:
        return False


def sections(text):
    """CHANGELOG.md split into `## [heading]` -> body, in file order."""
    parts = re.split(r'^## +\[([^\]]+)\][^\n]*$', text, flags=re.M)
    return list(zip(parts[1::2], parts[2::2]))


def notes_for(version):
    """The body of this version's changelog section, or None if it has none."""
    if not CHANGELOG.exists():
        return None
    for name, body in sections(CHANGELOG.read_text(encoding='utf-8')):
        if name == version:
            return body.strip() or None
    return None


def unreleased(text):
    """What is still sitting under `## [Unreleased]`, if anything."""
    for name, body in sections(text):
        if name.lower() == 'unreleased':
            return body.strip()
    return ''


def epub_id_at(ref):
    """The EPUB identifier as it was at some earlier commit."""
    src = git('show', f'{ref}:book/imprint.py')
    if not src:
        return None
    m = re.search(r'^EPUB_ID\s*=\s*[\'"]([^\'"]+)[\'"]', src, re.M)
    return m.group(1) if m else None


def previous_tag():
    """The newest vN.N.N tag that is not this version."""
    tags = git('tag', '--list', 'v*.*.*', '--sort=-v:refname')
    if not tags:
        return None
    for t in tags.splitlines():
        if t.strip() and t.strip() != f'v{VERSION}':
            return t.strip()
    return None


def main():
    args = sys.argv[1:]
    notes_path = None
    if '--notes' in args:
        i = args.index('--notes')
        if i + 1 >= len(args):
            sys.exit('release: --notes needs a path to write to')
        notes_path = Path(args[i + 1])

    problems = []
    said = []

    # 1. A version somebody meant.
    if not SEMVER.match(VERSION):
        problems.append(f'package.json version {VERSION!r} is not a semantic version')
    elif VERSION == '0.0.0':
        problems.append('package.json version is still 0.0.0 — version.py returns that '
                        'when it cannot read package.json at all')
    else:
        said.append(f'version      {VERSION}')

    # 2. Somebody wrote down what changed. A release whose changelog entry is
    #    missing is a release nobody can read the diff of a year later.
    notes = notes_for(VERSION)
    if notes is None:
        problems.append(f'CHANGELOG.md has no entry for {VERSION}. Add a '
                        f'`## [{VERSION}] - YYYY-MM-DD` section saying what changed.')
    else:
        said.append(f'changelog    {len(notes.splitlines())} lines for {VERSION}')

    # 3. Nothing is still filed as unreleased. Anything left under that heading
    #    ships in this release without being attributed to it, which is how a
    #    changelog starts lying.
    if CHANGELOG.exists():
        left = unreleased(CHANGELOG.read_text(encoding='utf-8'))
        if left:
            first = left.splitlines()[0].strip()
            problems.append(f'CHANGELOG.md still has content under [Unreleased] '
                            f'({first!r}). Move it into the {VERSION} section, or it '
                            f'ships without being written down as part of anything.')

    # 4. The identifier that names the work rather than the build. A new string
    #    presents the next version to retailers and libraries as a different
    #    book, so this is the one value in the repository that must survive
    #    every release byte for byte.
    prev = previous_tag()
    if prev:
        was = epub_id_at(prev)
        if was is None:
            said.append(f'epub id      not checked ({prev} has no readable imprint.py)')
        elif was != IMP.EPUB_ID:
            problems.append(f'EPUB_ID changed since {prev}: {was!r} -> {IMP.EPUB_ID!r}. '
                            f'It names the work, not the build, and must not move.')
        else:
            said.append(f'epub id      unchanged since {prev}')
    else:
        said.append('epub id      not checked (no earlier release tag)')

    # 5. A tag that already points somewhere else means this version was
    #    released from a different commit, and one of the two is wrong.
    #
    #    Merging into the release branch is allowed to make a new commit - a
    #    `--no-ff` merge does, and that is the documented way to release - so a
    #    tag that this commit descends from is fine as long as the merge changed
    #    nothing. What is not fine is a tag on content that differs from what is
    #    about to be published under its name.
    tag = f'v{VERSION}'
    at = git('rev-list', '-n', '1', tag)
    if at:
        head = git('rev-parse', 'HEAD')
        if not head or at == head:
            said.append(f'tag          {tag} already at this commit')
        elif git_ok('merge-base', '--is-ancestor', tag, 'HEAD') and \
                git_ok('diff', '--quiet', tag, 'HEAD'):
            said.append(f'tag          {tag} is at {at[:9]}, which this commit '
                        f'descends from with no change')
        else:
            problems.append(f'{tag} already exists at {at[:9]} and this commit '
                            f'({head[:9]}) differs from it. Bump the version, or move '
                            f'the tag on purpose.')
    else:
        said.append(f'tag          {tag} is free')

    for line in said:
        print(f'release: {line}')

    if problems:
        for p in problems:
            print(f'release: {p}', file=sys.stderr)
        sys.exit(f'release: {len(problems)} problem'
                 f'{"" if len(problems) == 1 else "s"} — not releasable')

    if notes_path:
        notes_path.parent.mkdir(parents=True, exist_ok=True)
        notes_path.write_text(
            f'{notes}\n\n---\n\n'
            f'The book is {IMP.TITLE}: a step-by-step roadmap off AWS, Google Cloud '
            f'or Azure and onto Kubernetes you run yourself.\n\n'
            f'- Attached: the print interior `{IMP.PDF_NAME}`, the Kindle edition '
            f'`{IMP.EPUB_NAME}`, the paperback wrap and the Kindle cover.\n'
            f'- The website is rebuilt from the same Move files and published with '
            f'this release.\n',
            encoding='utf-8')
        print(f'release: notes -> {notes_path}')

    print(f'release: {VERSION} is releasable')


if __name__ == '__main__':
    main()
