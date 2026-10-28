"""Validate the 2026-10-28 complete reader corpus against its predecessors."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2026.10.28.1"
SOURCE_ID = "dikshitar-1949-project-madurai"
COMPLETED = {37, 184, 223, 268, 329, 354, 388}
PREDECESSORS = {
    "1-30": "ai-reviewed-1-30",
    "31-40": "ai-reviewed-31-40",
    "41-50": "ai-reviewed-41-50",
    "51-60": "ai-reviewed-51-60-20261027",
    "61-70": "ai-reviewed-61-70-20261027",
    "71-80": "ai-reviewed-71-80-20261027",
    "81-90": "ai-reviewed-81-90-20261027",
    "91-100": "ai-reviewed-91-100-20261027",
    "101-110": "ai-reviewed-101-110-20261027",
    "111-120": "ai-reviewed-111-120-20261027",
    "121-133": "ai-reviewed-121-133-20261027",
}


def validate():
    development = ROOT / "datasets/development"
    chapters = set()
    meanings = 0
    completed = set()
    iyals = {}

    for chapter_range, predecessor_name in PREDECESSORS.items():
        predecessor = development / predecessor_name
        selected = development / f"ai-reviewed-{chapter_range}-20261028"
        manifest = json.loads((selected / "manifest.json").read_text())
        assert manifest["dataset_version"] == VERSION
        assert manifest["coverage"]["idiomatic_candidates_withheld"] == 0
        assert manifest["structure"]["source_id"] == SOURCE_ID
        present = 0

        for name, checksum in manifest["chapter_files"].items():
            raw = (selected / name).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == checksum, name
            document = json.loads(raw)
            number = document["chapter"]["chapter_no"]
            before = json.loads((predecessor / name).read_text())
            assert number not in chapters
            chapters.add(number)
            assert document["dataset_version"] == VERSION
            assert document["chapter"]["name_ta"] == before["chapter"]["name_ta"]
            assert document["chapter"]["name_en"].strip()
            assert document["chapter"]["name_en_source_id"] == SOURCE_ID
            assert document["chapter"]["name_en_credit"].strip()
            iyal = document["chapter"]["iyal"]
            assert iyal["division_source_id"] == SOURCE_ID
            assert iyal["name_ta"].strip() and iyal["name_en"].strip()
            iyals[iyal["iyal_id"]] = (
                iyal["paal_no"], iyal["order_in_paal"], iyal["name_ta"], iyal["name_en"]
            )
            before_chapter = dict(before["chapter"])
            after_chapter = dict(document["chapter"])
            for key in ("name_en", "name_en_source_id", "name_en_source_locator", "name_en_credit", "iyal"):
                after_chapter.pop(key)
            assert after_chapter == before_chapter

            assert len(document["kurals"]) == 10
            for old, new in zip(before["kurals"], document["kurals"]):
                ident = new["kural_no"]
                assert old["tamil"] == new["tamil"]
                assert old["review"] == new["review"]
                text = new["idiomatic_translation"]["text"]
                assert isinstance(text, str) and text.strip(), ident
                meanings += 1
                present += 1
                if ident in COMPLETED:
                    assert old["idiomatic_translation"]["text"] is None
                    assert new["idiomatic_translation"]["status"] == "ai_assisted_draft"
                    assert new["review"]["status"] == "flagged"
                    assert new["review"]["needs_tamil_reviewer"] is True
                    assert f"https://thirukkural.io/kural/{ident}" in new["idiomatic_translation"]["additional_source_locators"]
                    completed.add(ident)
                else:
                    unchanged = dict(new)
                    assert unchanged == old, ident
        assert manifest["coverage"]["ai_idiomatic_translation_drafts"] == present

    assert chapters == set(range(1, 134))
    assert meanings == 1330
    assert completed == COMPLETED
    assert set(iyals) == set(range(1, 11))
    print("Validated 133 chapters / 1,330 English drafts / 10 sourced iyals / 133 sourced English chapter titles; Tamil and review findings preserved.")


if __name__ == "__main__":
    validate()
