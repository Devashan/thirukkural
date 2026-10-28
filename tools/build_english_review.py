#!/usr/bin/env python3
"""Join the saved Tamil draft with a pinned Aiyar transcription for review."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

REPOSITORY = 'standardebooks/thiruvalluvar_the-kural_v-v-s-aiyar'
COMMIT = '0d14a398d6886391c369f0c3e00b0e9e1e7f4ee1'
SOURCE_ID = 'aiyar-1916-standardebooks'
NS = {'h': 'http://www.w3.org/1999/xhtml'}
EPUB_TYPE = '{http://www.idpf.org/2007/ops}type'


def without_note_markers(element):
    element = copy.deepcopy(element)
    notes = []
    for parent in element.iter():
        for child in list(parent):
            if 'noteref' in child.get(EPUB_TYPE, '').split():
                notes.append(child.get('href'))
                siblings = list(parent)
                index = siblings.index(child)
                if index:
                    previous = siblings[index - 1]
                    previous.tail = (previous.tail or '') + (child.tail or '')
                else:
                    parent.text = (parent.text or '') + (child.tail or '')
                parent.remove(child)
    return element, notes


def extract_chapter(data, chapter):
    root = ET.fromstring(data)
    section = root.find(f'.//h:section[@id="chapter-{chapter}"]', NS)
    if section is None:
        raise ValueError(f'Chapter {chapter}: missing section')
    parents = {child: parent for parent in section.iter() for child in parent}
    rows = []
    for ol in section.findall('.//h:ol', NS):
        if int(ol.get('start', '1')) != (chapter - 1) * 10 + len(rows) + 1:
            raise ValueError(f'Chapter {chapter}: unexpected English numbering')
        header = parents[ol].find('h:header', NS)
        speaker, context_notes = '', []
        if header is not None:
            clean_header, context_notes = without_note_markers(header)
            speaker = ' '.join(''.join(clean_header.itertext()).split())
        for item in ol.findall('h:li', NS):
            item, notes = without_note_markers(item)
            paragraphs = [' '.join(''.join(p.itertext()).split())
                          for p in item.findall('h:p', NS)]
            if not paragraphs or any(not p for p in paragraphs):
                raise ValueError(f'Chapter {chapter}: empty translation')
            rows.append({'position': len(rows) + 1, 'text': '\n\n'.join(paragraphs),
                         'speaker_context': speaker,
                         'source_note_locators': context_notes + notes})
    if len(rows) != 10:
        raise ValueError(f'Chapter {chapter}: expected ten English entries')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tamil_zip', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--snapshot-archive', type=Path,
                        help='Saved JSON archive of the pinned English source files')
    args = parser.parse_args()
    with zipfile.ZipFile(args.tamil_zip) as archive:
        candidates = [n for n in archive.namelist() if n.endswith('chapters.json')]
        if len(candidates) != 1:
            raise ValueError('Expected one Tamil chapters.json')
        tamil_bytes = archive.read(candidates[0])
        tamil = json.loads(tamil_bytes)
        chapters = tamil['chapters']
        if [c['chapter_no'] for c in chapters] != list(range(1, 134)):
            raise ValueError('Expected all 133 Tamil chapters in order')
        for chapter in chapters:
            snapshot = archive.read(chapter['snapshot'])
            if hashlib.sha256(snapshot).hexdigest() != chapter['source_checksum']:
                raise ValueError('Tamil snapshot checksum mismatch')
    source_dir = args.source_dir or args.output.parent / 'aiyar-snapshots'
    source_dir.mkdir(parents=True, exist_ok=True)
    if args.snapshot_archive:
        saved = json.loads(args.snapshot_archive.read_text(encoding='utf-8'))
        if saved['repository'] != REPOSITORY or saved['commit'] != COMMIT:
            raise ValueError('English snapshot archive identity mismatch')
        if [f['chapter'] for f in saved['files']] != list(range(1, 134)):
            raise ValueError('English snapshot archive coverage mismatch')
        for f in saved['files']:
            (source_dir / f"chapter-{f['chapter']}.xhtml").write_text(f['content'], encoding='utf-8')
        (source_dir / 'manifest.json').write_text(json.dumps(saved), encoding='utf-8')
    manifest_path = source_dir / 'manifest.json'
    source_manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    blobs = {f['chapter']: f['sha'] for f in source_manifest.get('files', [])}
    records, english_snapshots = [], []
    for chapter in chapters:
        number = chapter['chapter_no']
        path = f'src/epub/text/chapter-{number}.xhtml'
        locator = f'https://github.com/{REPOSITORY}/blob/{COMMIT}/{path}'
        local = source_dir / f'chapter-{number}.xhtml'
        if not local.exists():
            url = f'https://raw.githubusercontent.com/{REPOSITORY}/{COMMIT}/{path}'
            with urllib.request.urlopen(url, timeout=60) as response:
                local.write_bytes(response.read())
        raw = local.read_bytes()
        git_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if number in blobs and git_blob != blobs[number]:
            raise ValueError(f'English chapter {number}: Git blob checksum mismatch')
        english_snapshots.append({'chapter_no': number, 'source_locator': locator,
                                  'git_blob_sha': git_blob,
                                  'sha256': hashlib.sha256(raw).hexdigest()})
        translations = extract_chapter(raw, number)
        verses = chapter['kurals']
        if [v['position'] for v in verses] != list(range(1, 11)):
            raise ValueError(f'Tamil chapter {number}: unexpected positions')
        for verse, translation in zip(verses, translations, strict=True):
            if verse['chapter_no'] != number or verse['source_id'] != chapter['source_id']:
                raise ValueError('Tamil chapter identity mismatch')
            kural_no = (number - 1) * 10 + verse['position']
            records.append({
                'kural_no': kural_no, 'chapter_no': number, 'position': verse['position'],
                'chapter_name_ta': chapter['name_ta'],
                'tamil': {'line_1': verse['line_1'], 'line_2': verse['line_2'],
                          'source_id': verse['source_id'],
                          'source_printed_no': verse['source_printed_no'],
                          'source_revision_id': chapter['source_revision_id'],
                          'source_snapshot_sha256': chapter['source_checksum'],
                          'source_page': chapter['source_page']},
                'english_translations': [{
                    'set_id': SOURCE_ID, 'translator': 'V. V. S. Aiyar',
                    'year': '1916', 'form': 'prose', 'translation_strategy': 'unspecified',
                    'text': translation['text'],
                    'speaker_context': translation['speaker_context'],
                    'source_locator': locator + f'#chapter-{number}',
                    'source_list_number': kural_no,
                    'source_note_locators': [
                        f'https://github.com/{REPOSITORY}/blob/{COMMIT}/src/epub/text/{n}'
                        for n in translation['source_note_locators']],
                    'review_status': 'unreviewed'}],
                'idiomatic_translations': [],
                'idiomatic_status': 'no_verified_reusable_source_imported',
                'transliterations': [],
                'review': {'status': 'unreviewed', 'flags':
                    ['printed_number_mismatch_pending_scan_review']
                    if str(kural_no) != verse['source_printed_no'] else []}})
    if [r['kural_no'] for r in records] != list(range(1, 1331)):
        raise ValueError('Expected 1,330 unique records')
    result = {
        'format': 'kural-english-review-draft-1', 'status': 'unreviewed-draft',
        'counts': {'chapters': 133, 'kurals': 1330, 'english_translations': 1330,
                   'idiomatic_translations': 0, 'transliterations': 0},
        'tamil_input_sha256': hashlib.sha256(tamil_bytes).hexdigest(),
        'tamil_index_revision': tamil['source_index_revision'],
        'numbering_anomalies_pending_review': tamil['numbering_anomalies_pending_review'],
        'english_source': {
            'source_id': SOURCE_ID, 'title': 'The Kural or the Maxims of Tiruvalluvar',
            'translator': 'V. V. S. Aiyar', 'original_edition_year': '1916',
            'transcription_repository': REPOSITORY, 'commit': COMMIT,
            'edition': 'Standard Ebooks edited transcription of the 1916 translation',
            'rights_status': 'pending_release_review',
            'rights_notice_locator': f'https://github.com/{REPOSITORY}/blob/{COMMIT}/src/epub/content.opf',
            'rights_note': 'Standard Ebooks identifies the source as believed public domain in the US and dedicates its contributions under CC0. Other jurisdictions and the original edition remain subject to release review.',
            'transform_steps': ['Extract ten consecutively numbered list entries per chapter, including split lists',
                                'Retain edition speaker headings as separate context',
                                'Remove footnote reference markers; retain source note links',
                                'Collapse XML layout whitespace within paragraphs',
                                'Join to Tamil by chapter and position; preserve printed-number anomaly'],
            'snapshots': english_snapshots},
        'review_limits': ['Structural checks do not approve Tamil text or translation accuracy.',
                          'English is one historical witness, not a word-by-word gloss.',
                          'No verified reusable idiomatic translation has been imported.',
                          'This format is a review packet, not the published release schema.'],
        'records': records}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['counts']))


if __name__ == '__main__':
    main()
