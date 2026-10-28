"""Check the completion against the exact preceding selected snapshots."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {37, 184, 223, 268, 329, 354, 388}


def validate():
    changed, chapters, divisions = set(), set(), {}
    total = 0
    for batch in sorted((ROOT / 'datasets/development').glob('*-20261028')):
        manifest = json.loads((batch / 'manifest.json').read_text())
        old = ROOT / manifest['supersedes_dataset_path']
        present = 0
        for name, checksum in manifest['chapter_files'].items():
            raw = (batch / name).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == checksum
            doc = json.loads(raw)
            before = json.loads((old / name).read_text())
            assert doc['dataset_version'] == '2026.10.28.1'
            chapter = doc['chapter'].copy()
            assert chapter.pop('name_en').strip()
            assert chapter.pop('name_en_review')['human_tamil_review'] == 'pending'
            iyal = chapter.pop('iyal')
            assert chapter == before['chapter']
            number = chapter['chapter_no']
            assert number not in chapters
            chapters.add(number)
            assert iyal['chapter_range'][0] <= number <= iyal['chapter_range'][1]
            assert iyal['division_source_id'] == 'tamilvu-parimelalagar-divisions'
            assert iyal['source_locator'].startswith('https://www.tamilvu.org/')
            divisions.setdefault(iyal['iyal_id'], []).append(number)
            assert len(doc['kurals']) == 10
            for position, (new, prior) in enumerate(zip(doc['kurals'], before['kurals']), 1):
                n = new['kural_no']
                assert n == (number - 1) * 10 + position
                assert new['idiomatic_translation']['text'].strip()
                present += 1
                if n in EXPECTED:
                    assert prior['idiomatic_translation']['text'] is None
                    assert new['idiomatic_translation']['status'] == 'ai_assisted_draft'
                    assert new['review']['needs_tamil_reviewer'] is True
                    a, b = new.copy(), prior.copy()
                    a.pop('idiomatic_translation'); b.pop('idiomatic_translation')
                    a['review'] = a['review'].copy(); b['review'] = b['review'].copy()
                    a['review'].pop('reason_in_plain_english')
                    b['review'].pop('reason_in_plain_english')
                    assert a == b, n
                    changed.add(n)
                else:
                    assert new == prior, n
        assert present == manifest['coverage']['ai_idiomatic_translation_drafts']
        assert manifest['coverage']['idiomatic_candidates_withheld'] == 0
        total += present
    assert changed == EXPECTED
    assert chapters == set(range(1, 134))
    assert total == 1330
    expected_ranges = [(1, 4), (5, 24), (25, 37), (38, 38), (39, 63),
                       (64, 95), (96, 108), (109, 115), (116, 133)]
    assert len(divisions) == len(expected_ranges)
    for ident, (start, end) in enumerate(expected_ranges, 1):
        assert sorted(divisions[ident]) == list(range(start, end + 1))
    print('1330 meanings, 133 English titles, nine sourced divisions; exactly seven additions; prior meanings, Tamil and review findings preserved.')


if __name__ == '__main__':
    validate()
