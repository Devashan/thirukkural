import json
import unittest
from pathlib import Path

from collect_tamil import extract_chapter


class ChapterParsingTest(unittest.TestCase):
    def setUp(self):
        draft = json.loads((Path(__file__).resolve().parents[1] / "drafts/chapter-001.json").read_text(encoding="utf-8"))
        self.verses = draft["kurals"]

    def html(self, split=False):
        chunks = [f'{row["line_1"]}<br>{row["line_2"]}<span id="line{row["position"]}">{row["position"]}</span><br>' for row in self.verses]
        return '<div class="mw-parser-output"><p>' + ('</p><p>' if split else '').join(chunks) + '</p></div>'

    def test_split_and_single_paragraph_match(self):
        self.assertEqual(extract_chapter(self.html()), extract_chapter(self.html(split=True)))
        self.assertEqual(len(extract_chapter(self.html(split=True))[1]), 10)

    def test_missing_verse_rejected(self):
        self.verses.pop()
        with self.assertRaises(ValueError):
            extract_chapter(self.html(split=True))

    def test_printed_anomaly_preserved(self):
        html = self.html(split=True).replace('id="line2">2', 'id="line2">1')
        self.assertEqual(extract_chapter(html)[1][1][0], 1)


if __name__ == "__main__":
    unittest.main()
