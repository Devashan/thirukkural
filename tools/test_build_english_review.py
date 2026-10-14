import unittest
from pathlib import Path
import tempfile
import json
from build_english_review import extract_chapter, without_note_markers
import xml.etree.ElementTree as ET


class ExtractionTests(unittest.TestCase):
    def test_note_marker_removal_preserves_inline_text_and_tail(self):
        element = ET.fromstring('<p xmlns:epub="http://www.idpf.org/2007/ops">Before <i>word</i><a epub:type="noteref" href="notes#n">12</a> after.</p>')
        clean, notes = without_note_markers(element)
        self.assertEqual(''.join(clean.itertext()), 'Before word after.')
        self.assertEqual(notes, ['notes#n'])

    def test_saved_corpus_sources(self):
        archive = json.loads(Path('drafts/aiyar-source-snapshots.json').read_text())
        chapters = {f['chapter']: f['content'] for f in archive['files']}
        self.assertEqual(len(chapters), 133)
        all_rows = [extract_chapter(chapters[n], n) for n in range(1, 134)]
        self.assertEqual(sum(map(len, all_rows)), 1330)
        self.assertTrue(all_rows[7][1]['text'].startswith('Those that love not'))
        self.assertEqual([r['speaker_context'] for r in all_rows[112]], ['He'] * 5 + ['She'] * 5)
        self.assertEqual(all_rows[127][1]['speaker_context'], 'She Is Silent and He Addresses the Maid')
        self.assertEqual(all_rows[108][0]['source_note_locators'], ['endnotes.xhtml#note-43'])
        bad = chapters[113].replace('start="1126"', 'start="1127"')
        with self.assertRaisesRegex(ValueError, 'numbering'):
            extract_chapter(bad, 113)


if __name__ == '__main__':
    unittest.main()
