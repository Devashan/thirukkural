"""Validate the 2026-10-27 replacements against their immutable predecessors."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {543, 550, 614, 727, 808, 829, 918, 943, 1074, 1172, 1178, 1189, 1231, 1262, 1306}


def validate():
    changed = set()
    meanings = 0
    withheld = set()
    chapters = set()
    development = ROOT / 'datasets/development'
    batches = ('1-30', '31-40', '41-50', '51-60', '61-70', '71-80',
               '81-90', '91-100', '101-110', '111-120', '121-133')
    for batch in batches:
        original = development / ('ai-reviewed-' + batch)
        replacement = original.with_name(original.name + '-20261027')
        selected = replacement if replacement.exists() else original
        manifest = json.loads((selected / 'manifest.json').read_text())
        present = 0
        for name, checksum in manifest['chapter_files'].items():
            raw = (selected / name).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == checksum, (selected, name)
            document = json.loads(raw)
            assert document['dataset_version'] == manifest['dataset_version']
            number = document['chapter']['chapter_no']
            assert number not in chapters
            chapters.add(number)
            assert len(document['kurals']) == 10
            before = json.loads((original / name).read_text())
            assert document['chapter'] == before['chapter']
            for position, (old, new) in enumerate(zip(before['kurals'], document['kurals']), 1):
                ident = new['kural_no']
                assert ident == (number - 1) * 10 + position
                assert old['tamil'] == new['tamil']
                text = new['idiomatic_translation']['text']
                if isinstance(text, str) and text.strip():
                    meanings += 1
                    present += 1
                else:
                    withheld.add(ident)
                if ident in EXPECTED:
                    assert old['idiomatic_translation']['text'] is None
                    assert new['idiomatic_translation']['status'] == 'ai_assisted_draft'
                    assert new['review']['status'] == old['review']['status']
                    assert new['review']['needs_tamil_reviewer'] is True
                    assert new['review']['findings'] == old['review']['findings']
                    assert f'https://thirukkural.io/kural/{ident}' in new['idiomatic_translation']['additional_source_locators']
                    changed.add(ident)
                else:
                    assert new == old, ident
        if replacement.exists():
            assert manifest['coverage']['ai_idiomatic_translation_drafts'] == present
            assert manifest['coverage']['idiomatic_candidates_withheld'] == 0
    assert chapters == set(range(1, 134))
    assert changed == EXPECTED
    assert meanings == 1323
    assert withheld == {37, 184, 223, 268, 329, 354, 388}
    print('Validated 133 chapters / 1323 English meanings / 7 previously uncounted blanks; exactly 15 meanings added; Tamil and existing review findings preserved.')


if __name__ == '__main__':
    validate()
