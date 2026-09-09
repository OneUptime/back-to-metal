"""Kindle-specific faults that general EPUB validation permits."""
import unittest
import xml.etree.ElementTree as ET

import epubcheck


class KindlePackagingTests(unittest.TestCase):
    def documents(self, landmark=True, cover_page=False):
        docs = {'OEBPS/content.opf': ET.fromstring('''
            <package xmlns="http://www.idpf.org/2007/opf"><manifest>
              <item id="cover" href="img/cover.jpg" properties="cover-image"/>
              <item id="nav" href="nav.xhtml" properties="nav"/>
            </manifest></package>''')}
        body = ('<nav epub:type="landmarks"><ol><li><a epub:type="toc" '
                'href="nav.xhtml#toc">Contents</a></li></ol></nav>') if landmark else ''
        docs['OEBPS/nav.xhtml'] = ET.fromstring(
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops"><body>' + body + '</body></html>')
        if cover_page:
            docs['OEBPS/front/image.xhtml'] = ET.fromstring(
                '<html xmlns="http://www.w3.org/1999/xhtml"><body>'
                '<img src="../img/cover.jpg" alt="Cover"/></body></html>')
        return docs

    def test_designated_image_and_landmark_are_sufficient(self):
        self.assertEqual(epubcheck.kindle_packaging_problems(self.documents()), [])

    def test_extra_cover_page_is_rejected_regardless_of_filename(self):
        self.assertIn('HTML repeats', ' '.join(epubcheck.kindle_packaging_problems(
            self.documents(cover_page=True))))

    def test_missing_landmark_is_reported(self):
        self.assertIn('landmark', ' '.join(epubcheck.kindle_packaging_problems(
            self.documents(landmark=False))))


if __name__ == '__main__':
    unittest.main()
