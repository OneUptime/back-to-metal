"""Regression tests for per-font PDF embedding, including Type 3 glyphs."""
import io
import unittest

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, DecodedStreamObject

from kdpcheck import embedded_font_problems


def dictionary(**entries):
    return DictionaryObject({NameObject('/' + k): v for k, v in entries.items()})


def stream(data):
    result = DecodedStreamObject()
    result.set_data(data)
    return result


def type3():
    return dictionary(
        Type=NameObject('/Font'), Subtype=NameObject('/Type3'),
        FontBBox=ArrayObject(map(NumberObject, (0, 0, 600, 700))),
        FontMatrix=ArrayObject(map(NumberObject, (1, 0, 0, 1, 0, 0))),
        FirstChar=NumberObject(65), LastChar=NumberObject(65),
        Widths=ArrayObject([NumberObject(600)]),
        Encoding=dictionary(Differences=ArrayObject([NumberObject(65), NameObject('/A')])),
        CharProcs=dictionary(A=stream(b'600 0 0 0 600 700 d1\n0 0 600 700 re f\n')),
    )


def program_font(embedded=True, subtype='/TrueType'):
    descriptor = dictionary(Type=NameObject('/FontDescriptor'))
    if embedded:
        descriptor[NameObject('/FontFile2')] = stream(b'font program bytes')
    return dictionary(Type=NameObject('/Font'), Subtype=NameObject(subtype),
                      BaseFont=NameObject('/Test'), FontDescriptor=descriptor)


def reader_with_resources(resources):
    writer = PdfWriter()
    page = writer.add_blank_page(width=603, height=810)
    page[NameObject('/Resources')] = resources
    data = io.BytesIO()
    writer.write(data)
    data.seek(0)
    return PdfReader(data, strict=True)


def check_fonts(*fonts):
    resources = dictionary(Font=dictionary(**{f'F{i}': f for i, f in enumerate(fonts)}))
    return embedded_font_problems(reader_with_resources(resources))


class FontEmbeddingTests(unittest.TestCase):
    def test_type3_embeds_glyphs_without_fontfile(self):
        font = type3()
        font['/CharProcs'][NameObject('/A')] = font['/CharProcs']['/A'].flate_encode()
        self.assertEqual(check_fonts(font), [])

    def test_every_font_must_be_embedded(self):
        issues = check_fonts(type3(), program_font(), program_font(embedded=False))
        self.assertEqual(len(issues), 1)
        self.assertIn('/F2', issues[0])
        self.assertIn('no embedded program', issues[0])

    def test_type3_missing_or_empty_glyph_program_is_rejected(self):
        for value in (dictionary(), dictionary(A=stream(b'')), dictionary(A=dictionary())):
            with self.subTest(value=value):
                font = type3()
                font[NameObject('/CharProcs')] = value
                self.assertTrue(check_fonts(font))

    def test_type3_encoding_cannot_reference_missing_glyph(self):
        font = type3()
        font['/Encoding']['/Differences'].append(NameObject('/B'))
        self.assertIn('missing glyph programs: /B', check_fonts(font)[0])

    def test_type3_requires_real_glyph_operations(self):
        font = type3()
        font['/CharProcs'][NameObject('/A')] = stream(b'0 0 m\n')
        self.assertIn('no initial width operator', check_fonts(font)[0])

    def test_composite_font_checks_descendant_embedding(self):
        for embedded in (True, False):
            with self.subTest(embedded=embedded):
                font = dictionary(Type=NameObject('/Font'), Subtype=NameObject('/Type0'),
                    DescendantFonts=ArrayObject([program_font(embedded, '/CIDFontType2')]))
                issues = check_fonts(font)
                self.assertEqual(bool(issues), not embedded)

    def test_fonts_inside_form_resources_are_checked(self):
        form = stream(b'')
        form.update(dictionary(Type=NameObject('/XObject'), Subtype=NameObject('/Form'),
            Resources=dictionary(Font=dictionary(Hidden=program_font(embedded=False)))))
        resources = dictionary(Font=dictionary(F1=type3()), XObject=dictionary(Form1=form))
        issues = embedded_font_problems(reader_with_resources(resources))
        self.assertEqual(len(issues), 1)
        self.assertIn('/Hidden', issues[0])

    def test_external_and_empty_program_streams_are_rejected(self):
        for data, external in ((b'', False), (b'font program bytes', True)):
            with self.subTest(external=external):
                font = program_font()
                program = stream(data)
                if external:
                    program[NameObject('/F')] = NameObject('/external.ttf')
                font['/FontDescriptor'][NameObject('/FontFile2')] = program
                self.assertTrue(check_fonts(font))

    def test_no_font_resources_does_not_pass(self):
        self.assertIn('no font resources found', check_fonts())


if __name__ == '__main__':
    unittest.main()
