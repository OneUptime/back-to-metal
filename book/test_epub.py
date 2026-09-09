"""Regression checks for shared prose crossing into the Markdown EPUB renderer."""
import unittest
import xml.etree.ElementTree as ET

import epub
from parse import load_all


class SharedProseTests(unittest.TestCase):
    def test_mission_preserves_readable_text_and_emphasis(self):
        count = len(load_all())
        doc = ET.fromstring(epub.mission_xhtml(count))
        ns = {'h': 'http://www.w3.org/1999/xhtml'}
        paragraphs = doc.findall('.//h:body/h:div/h:p', ns)
        expected = [ET.fromstring(f'<p>{p}</p>')
                    for p in epub.MISSION.paras(epub.IMP.REPO, count)]
        self.assertEqual([''.join(p.itertext()) for p in paragraphs],
                         [''.join(p.itertext()) for p in expected])
        self.assertEqual([node.text for node in doc.findall('.//h:strong', ns)],
                         ['open source'])

    def test_markdown_code_keeps_literal_html(self):
        doc = ET.fromstring('<p>' + epub.rich('Use `<b>literal</b>` as text.') + '</p>')
        self.assertEqual(doc.find('code').text, '<b>literal</b>')
        self.assertEqual(doc.findall('.//b'), [])


if __name__ == '__main__':
    unittest.main()
