"""Gate the built PDF against Amazon KDP's interior requirements.

Fails the build rather than letting a non-compliant file reach an upload, because
KDP's own rejection messages are slow and vague. Everything checked here is
something KDP either states outright or silently rounds/rejects.
"""
import re, sys
from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import ArrayObject, ContentStream, DictionaryObject, StreamObject

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'book'))
import imprint as IMP

PDF = ROOT / 'dist' / IMP.PDF_NAME

# 8.375in x 11.25in = trim 8.25x11 plus 0.125in bleed on the outer edge and both
# ends. Chromium emits a width a hundredth of a point wide; that is 0.04mm against
# KDP's own 3.175mm paper-shift tolerance, so a tolerance is honest here where
# demanding an exact integer would only invite a pointless workaround.
WANT_W, WANT_H, TOL = 603.0, 810.0, 0.5


def embedded_font_problems(reader):
    """Check every page-resource font, including fonts inside forms/patterns.

    Type 3 embeds glyph content streams in CharProcs, not a FontFile. Merely
    finding one FontFile somewhere also misses other, unembedded fonts.
    PDF specification: https://pdf-issues.pdfa.org/32000-2-2020/clause09.html#9.6.4
    This verifies embedding; KDP's ingestion still decides font support.
    """
    problems, fonts, visited = [], set(), set()

    def stream_data(value):
        stream = value.get_object()
        if not isinstance(stream, StreamObject) or '/F' in stream:
            raise ValueError('font program is not an embedded stream')
        if not stream.get_data().strip():
            raise ValueError('font program is empty')
        return stream

    def check_font(value, label):
        try:
            font = value.get_object()
            if id(font) in fonts:
                return
            fonts.add(id(font))
            if not isinstance(font, DictionaryObject) or font.get('/Type') != '/Font':
                raise ValueError('invalid font dictionary')
            subtype = font.get('/Subtype')
            if subtype == '/Type0':
                descendants = font.get('/DescendantFonts')
                descendants = descendants.get_object() if descendants is not None else None
                if not isinstance(descendants, ArrayObject) or len(descendants) != 1:
                    raise ValueError('composite font has no single descendant font')
                check_font(descendants[0], label + ' descendant')
            elif subtype == '/Type3':
                glyphs = font.get('/CharProcs')
                glyphs = glyphs.get_object() if glyphs is not None else None
                if not isinstance(glyphs, DictionaryObject) or not glyphs:
                    raise ValueError('Type3 font has no embedded CharProcs')
                for name, glyph in glyphs.items():
                    stream = stream_data(glyph)
                    ops = ContentStream(stream, reader).operations
                    if not ops or ops[0][1] not in (b'd0', b'd1'):
                        raise ValueError(f'Type3 glyph {name} has no initial width operator')
                encoding = font.get('/Encoding')
                encoding = encoding.get_object() if encoding is not None else None
                if not isinstance(encoding, (DictionaryObject, str)):
                    raise ValueError('Type3 font has no encoding')
                if isinstance(encoding, DictionaryObject):
                    differences = encoding.get('/Differences', [])
                    differences = differences.get_object() if hasattr(differences, 'get_object') else differences
                    missing = {str(n) for n in differences if isinstance(n, str) and n not in glyphs}
                    if missing:
                        raise ValueError('Type3 encoding names missing glyph programs: ' + ', '.join(sorted(missing)))
            elif subtype in ('/Type1', '/MMType1', '/TrueType', '/CIDFontType0', '/CIDFontType2'):
                descriptor = font.get('/FontDescriptor')
                descriptor = descriptor.get_object() if descriptor is not None else None
                if not isinstance(descriptor, DictionaryObject):
                    raise ValueError('font has no embedded program descriptor')
                programs = [descriptor[k] for k in ('/FontFile', '/FontFile2', '/FontFile3') if k in descriptor]
                if not programs:
                    raise ValueError('font has no embedded program')
                for program in programs:
                    stream_data(program)
            else:
                raise ValueError(f'unsupported PDF font subtype {subtype}')
        except Exception as exc:
            problems.append(f'{label}: {exc}')

    def walk(value, label):
        obj = value.get_object() if hasattr(value, 'get_object') else value
        if not isinstance(obj, (DictionaryObject, ArrayObject)) or id(obj) in visited:
            return
        visited.add(id(obj))
        if isinstance(obj, ArrayObject):
            for child in obj:
                walk(child, label)
            return
        if obj.get('/Type') == '/Font':
            check_font(obj, label)
        for key, child in obj.items():
            if key == '/Font':
                entries = child.get_object()
                if isinstance(entries, DictionaryObject):
                    for name, font in entries.items():
                        check_font(font, f'{label} {name}')
                elif isinstance(entries, ArrayObject) and entries:
                    check_font(entries[0], label + ' graphics-state font')
                else:
                    problems.append(f'{label}: invalid font resources')
            walk(child, label)

    for i, page in enumerate(reader.pages, 1):
        try:
            walk(page.get('/Resources', {}), f'p{i}')
        except Exception as exc:
            problems.append(f'p{i}: cannot read font resources: {exc}')
    if not fonts:
        problems.append('no font resources found')
    return problems


def main():
    if not PDF.exists():
        sys.exit(f'kdp: {PDF} not built')
    d = PDF.read_bytes()
    problems = []

    boxes = set(re.findall(rb'/MediaBox\s*\[([^\]]*)\]', d))
    if len(boxes) != 1:
        problems.append(f'{len(boxes)} different MediaBox values; every page must be one size')
    for box in boxes:
        try:
            x0, y0, x1, y1 = (float(v) for v in box.split())
        except ValueError:
            problems.append(f'unparseable MediaBox: {box!r}')
            continue
        w, h = x1 - x0, y1 - y0
        if abs(w - WANT_W) > TOL or abs(h - WANT_H) > TOL:
            problems.append(f'page box {w:.2f} x {h:.2f}pt, want {WANT_W} x {WANT_H} (+/-{TOL})')

    pages = len(re.findall(rb'/Type\s*/Page[^s]', d))
    if pages % 2:
        problems.append(f'{pages} pages: odd, so KDP will append a blank of its own')

    # KDP requires a flattened interior. Ghostscript would flatten by rasterising,
    # so these are pre-composited at source instead — see book/flatten.py.
    for label, pat in [('transparency groups', rb'/S\s*/Transparency'),
                       ('soft masks', rb'/SMask(?!\s*/None)'),
                       ('annotations', rb'/Annots'),
                       ('encryption', rb'/Encrypt')]:
        n = len(re.findall(pat, d))
        if n:
            problems.append(f'{n} {label}')

    # /ca and /CA at 1 are the opaque default graphics state, not transparency.
    # Only a value below 1 is an actual alpha blend.
    for label, pat in [('fill-alpha', rb'/ca\s+([0-9.]+)'),
                       ('stroke-alpha', rb'/CA\s+([0-9.]+)')]:
        soft = [v for v in re.findall(pat, d) if float(v) < 1]
        if soft:
            problems.append(f'{len(soft)} {label} operators below 1: {sorted(set(v.decode() for v in soft))}')

    try:
        problems.extend(embedded_font_problems(PdfReader(PDF, strict=True)))
    except Exception as exc:
        problems.append(f'cannot parse PDF font resources: {exc}')

    if problems:
        print('kdp: interior does NOT meet the requirements')
        for p in problems:
            print('  -', p)
        sys.exit(1)

    print(f'kdp: interior OK — {pages} pages, '
          f'{sorted(boxes)[0].decode()}, flattened, fonts embedded')


if __name__ == '__main__':
    main()
