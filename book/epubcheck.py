"""Structural validation of the built EPUB.

Not a substitute for EPUBCheck or Kindle Previewer — run those before
publishing — but it catches the things that actually break a Kindle conversion
and it runs in the build with no Java dependency.
"""
import re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import PurePosixPath, Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'book'))
import imprint as IMP
from parse import load_all, inline
from kit import RULES
from equivalents import ROWS as EQ_ROWS
import why as WHY

EPUB = ROOT / 'dist' / IMP.EPUB_NAME
OPF_NS = {'o': 'http://www.idpf.org/2007/opf',
          'dc': 'http://purl.org/dc/elements/1.1/'}
NCX_NS = {'n': 'http://www.daisy.org/z3986/2005/ncx/'}
HTML_NS = {'h': 'http://www.w3.org/1999/xhtml'}
EPUB_TYPE = '{http://www.idpf.org/2007/ops}type'

# RFC 4122: the urn:uuid: scheme has to be followed by an actual UUID. Adobe's
# epubcheck rejects anything else; this checker used not to, which is how
# 'urn:uuid:twenty-minute-table-1.0.1' survived several releases. Asserting the
# shape here also rules out interpolating the version back in, since no version
# string can match it.
UUID_URN = re.compile(r'^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}'
                      r'-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)


def resolve(base, href):
    parts = []
    for seg in str((PurePosixPath(base).parent / href).as_posix()).split('/'):
        if seg == '..':
            parts and parts.pop()
        elif seg not in ('.', ''):
            parts.append(seg)
    return '/'.join(parts)


def content_problems(documents, moves):
    """Guard omissions that a valid EPUB package cannot detect."""
    problems = []
    for move in moves:
        name = f'OEBPS/m/{move["num"]}.xhtml'
        doc = documents.get(name)
        if doc is None:
            problems.append(f'{name}: missing Move document')
            continue
        text = ' '.join(' '.join(doc.itertext()).split())
        for origin in move['origins']:
            # Render only the shared inline syntax, not an EPUB template, so a
            # missing provider block remains visible to this check.
            fields = [origin['cloud'], origin['service'], origin['note']]
            for field in fields:
                fragment = ET.fromstring('<p>' + inline(field).replace('<br>', '<br/>') + '</p>')
                expected = ' '.join(' '.join(fragment.itertext()).split())
                if expected not in text:
                    problems.append(f'{name}: missing {origin["cloud"]} extraction content')
                    break

    kit = documents.get('OEBPS/kit.xhtml')
    if kit is None:
        problems.append('missing reference build')
    else:
        rules = kit.findall('.//h:ol[@id="rules"]/h:li', HTML_NS)
        if len(rules) != len(RULES):
            problems.append(f'reference build has {len(rules)} rules; expected {len(RULES)}')
        heading = f'{len(RULES)} rules for leaving the cloud'
        if not any(heading == ''.join(h.itertext()) for h in kit.findall('.//h:h2', HTML_NS)):
            problems.append('reference build rule heading disagrees with the rule count')

    equivalents = documents.get('OEBPS/replaces.xhtml')
    links = [] if equivalents is None else [a.get('href') for a in
                                             equivalents.findall('.//h:a', HTML_NS)]
    for number in {row[4] for row in EQ_ROWS if row[4]}:
        if f'm/{number}.xhtml' not in links:
            problems.append(f'equivalence table does not link Move {number}')

    decision = documents.get('OEBPS/decision.xhtml')
    if decision is None:
        problems.append('missing shared decision guidance')
    else:
        decision_text = ' '.join(decision.itertext())
        for heading in [WHY.HEADING, WHY.OURS_HEADING, WHY.COSTS_HEADING, WHY.STAY_HEADING]:
            if heading not in decision_text:
                problems.append(f'decision guidance omits {heading!r}')
    costs = documents.get('OEBPS/costs.xhtml')
    if costs is None:
        problems.append('missing financial comparison')
    else:
        ids = {node.get('id') for node in costs.iter() if node.get('id')}
        for route in ('cloud', 'owned', 'rented'):
            for prefix in ('monthly', 'cash'):
                if f'{prefix}-{route}-total' not in ids:
                    problems.append(f'financial comparison omits {prefix} total for {route}')
    return problems


def kindle_packaging_problems(documents):
    """A valid EPUB can still duplicate its cover or disable Kindle's Go To ToC."""
    problems = []
    package = documents.get('OEBPS/content.opf')
    if package is None:
        return ['missing EPUB package']
    items = package.findall('.//o:manifest/o:item', OPF_NS)
    covers = {resolve('OEBPS/content.opf', item.get('href', '')) for item in items
              if 'cover-image' in item.get('properties', '').split()}
    for name, doc in documents.items():
        if name.endswith('.xhtml'):
            for img in doc.findall('.//h:img', HTML_NS):
                if resolve(name, img.get('src', '')) in covers:
                    problems.append(f'{name}: HTML repeats the designated Kindle cover image')
    for item in items:
        if 'nav' not in item.get('properties', '').split():
            continue
        name = resolve('OEBPS/content.opf', item.get('href', ''))
        nav = documents.get(name)
        landmarks = [] if nav is None else [node for node in nav.findall('.//h:nav', HTML_NS)
                                            if 'landmarks' in node.get(EPUB_TYPE, '').split()]
        if not any('toc' in link.get(EPUB_TYPE, '').split()
                   for node in landmarks for link in node.findall('.//h:a', HTML_NS)):
            problems.append(f'{name}: missing Kindle table-of-contents landmark')
    return problems


def main():
    if not EPUB.exists():
        sys.exit('epubcheck: build the epub first (make epub)')
    # A build that fails before writing leaves the previous archive in place, and
    # validating that would report success for a file nobody just built. Compare
    # against the newest input instead of trusting whatever is on disk.
    built = EPUB.stat().st_mtime
    sources = (list((ROOT / 'moves').glob('*.md')) + list((ROOT / 'book').rglob('*.py'))
               + [ROOT / 'package.json'])
    cover = ROOT / 'dist' / 'cover-kindle.jpg'
    if cover.exists():
        sources.append(cover)
    newer = [p for p in sources if p.stat().st_mtime > built]
    if newer:
        rel = [str(p.relative_to(ROOT)) for p in sorted(newer)[:4]]
        sys.exit(f'epubcheck: {EPUB.name} is older than {len(newer)} of its sources '
                 f'({", ".join(rel)}). Rebuild it — the epub build probably failed.')

    z = zipfile.ZipFile(EPUB)
    names = z.namelist()
    problems = []

    if names[0] != 'mimetype':
        problems.append(f'first archive entry is {names[0]!r}; it must be "mimetype"')
    if z.getinfo('mimetype').compress_type != zipfile.ZIP_STORED:
        problems.append('mimetype must be stored uncompressed')
    if z.read('mimetype') != b'application/epub+zip':
        problems.append('mimetype content is wrong')

    documents = {}
    for n in names:
        if n.endswith(('.xhtml', '.opf', '.ncx', '.xml')):
            try:
                documents[n] = ET.fromstring(z.read(n))
            except ET.ParseError as e:
                problems.append(f'{n} is not well-formed XML: {e}')

    problems.extend(content_problems(documents, load_all()))
    problems.extend(kindle_packaging_problems(documents))

    pub_uid = None
    if 'OEBPS/content.opf' in names:
        root = ET.fromstring(z.read('OEBPS/content.opf'))
        items = root.findall('.//o:manifest/o:item', OPF_NS)
        missing = [i.get('href') for i in items if f"OEBPS/{i.get('href')}" not in names]
        if missing:
            problems.append(f'{len(missing)} manifest items are not in the archive: {missing[:4]}')
        ids = {i.get('id') for i in items}
        dangling = [r.get('idref') for r in root.findall('.//o:spine/o:itemref', OPF_NS)
                    if r.get('idref') not in ids]
        if dangling:
            problems.append(f'spine points at unknown ids: {dangling[:4]}')
        spine_ids = {r.get('idref') for r in root.findall('.//o:spine/o:itemref', OPF_NS)}
        for name in ('decision.xhtml', 'costs.xhtml'):
            matches = [i for i in items if i.get('href') == name]
            if len(matches) != 1 or matches[0].get('id') not in spine_ids:
                problems.append(f'{name} must appear in the manifest and reading order')
        navs = [i for i in items if 'nav' in (i.get('properties') or '')]
        if len(navs) != 1:
            problems.append(f'{len(navs)} items declare properties="nav"; EPUB3 needs exactly one')
        covers = [i for i in items if 'cover-image' in (i.get('properties') or '')]
        if len(covers) != 1:
            problems.append(f'{len(covers)} items declare cover-image; need exactly one')

        # The publication identifier: well-formed, and the one the package points at.
        # It is deliberately NOT checked against a literal, so imprint.py stays the
        # single source of truth — only its form and its internal agreement matter.
        uid_id = root.get('unique-identifier')
        idents = {e.get('id'): (e.text or '').strip()
                  for e in root.findall('.//dc:identifier', OPF_NS)}
        if uid_id not in idents:
            problems.append(f'package unique-identifier={uid_id!r} names no dc:identifier '
                            f'(have {sorted(k for k in idents if k)})')
        else:
            pub_uid = idents[uid_id]
            if not UUID_URN.match(pub_uid):
                problems.append(f'dc:identifier {pub_uid!r} is not urn:uuid: followed by a '
                                f'UUID; it must be EPUB_ID from imprint.py, and must never '
                                f'be derived from the version')

    # toc.ncx carries the same identifier as dtb:uid. Kindle's converter reads the
    # NCX, so the two disagreeing is worse than either being wrong alone.
    if 'OEBPS/toc.ncx' in names:
        ncx = ET.fromstring(z.read('OEBPS/toc.ncx'))
        uids = [m.get('content') for m in ncx.findall('.//n:head/n:meta', NCX_NS)
                if m.get('name') == 'dtb:uid']
        if len(uids) != 1:
            problems.append(f'toc.ncx declares {len(uids)} dtb:uid values; need exactly one')
        elif pub_uid is not None and uids[0] != pub_uid:
            problems.append(f'toc.ncx dtb:uid {uids[0]!r} does not match dc:identifier '
                            f'{pub_uid!r}')

    dead = []
    for n in names:
        if n.endswith('.xhtml'):
            for href in re.findall(rb'(?:href|src)="([^"#:]+)"', z.read(n)):
                t = resolve(n, href.decode())
                if t not in names:
                    dead.append(f'{n} -> {href.decode()}')
    if dead:
        problems.append(f'{len(dead)} dead internal links, e.g. {dead[:3]}')

    # KDP forbids transparency in EPUB images
    pngs = [n for n in names if n.lower().endswith('.png')]
    if pngs:
        problems.append(f'{len(pngs)} PNGs present; KDP wants no alpha — prefer JPEG: {pngs[:3]}')

    mb = EPUB.stat().st_size / 1e6
    if problems:
        print('epubcheck: FAILED')
        for p in problems:
            print('  -', p)
        sys.exit(1)
    print(f'epubcheck: OK — {len(names)} entries, {sum(n.endswith(".xhtml") for n in names)} documents, '
          f'{mb:.2f} MB')
    print('           still run EPUBCheck and Kindle Previewer 3 before publishing')


if __name__ == '__main__':
    main()
