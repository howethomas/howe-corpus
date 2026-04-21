#!/usr/bin/env python3
"""Emit vcons/talks/*.vcon.json and vcons/writing/*.vcon.json from corpus.yaml.

Run from repo root: python3 scripts/generate_vcons_from_corpus.py
"""

from __future__ import annotations

import json
import uuid
from datetime import date, datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = REPO_ROOT / "corpus.yaml"
TALKS_DIR = REPO_ROOT / "vcons" / "talks"
WRITING_DIR = REPO_ROOT / "vcons" / "writing"

TALK_TYPES = frozenset({"talk", "podcast", "judging"})
WRITING_TYPES = frozenset(
    {
        "essay",
        "mailing-list-post",
        "whitepaper",
        "documentation",
        "guide",
        "internet-draft",
    }
)

VCON_UUID_NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL, "https://github.com/howethomas/howe-corpus/vcon"
)
UPDATED_AT = "2026-04-21T00:00:00Z"


def _date_to_meta_value(d: object) -> str | None:
    if d is None:
        return None
    if isinstance(d, datetime):
        return d.date().isoformat()
    if isinstance(d, date):
        return d.isoformat()
    if isinstance(d, str):
        return d
    return str(d)


def iso_created_at(d: object) -> str:
    if d is None:
        return "1970-01-01T00:00:00Z"
    if isinstance(d, datetime):
        d = d.date()
    if isinstance(d, date):
        return d.isoformat() + "T00:00:00Z"
    if isinstance(d, str):
        s = d.strip()
        if len(s) == 10 and s[4] == "-" and s[7] == "-":
            return s + "T00:00:00Z"
        if len(s) == 7 and s[4] == "-" and s[:4].isdigit():
            return s + "-01T00:00:00Z"
        if len(s) == 4 and s.isdigit():
            return s + "-01-01T00:00:00Z"
    return "1970-01-01T00:00:00Z"


def party_role(item_type: str, authorship: str) -> str:
    if item_type in ("talk", "podcast"):
        return "speaker"
    if item_type == "judging":
        return "judge"
    if authorship == "editor":
        return "editor"
    return "author"


def display_name(name_used: str) -> str:
    if name_used == "unknown":
        return "Thomas McCarthy-Howe"
    return name_used


def build_vcon(item: dict, out_dir: Path) -> dict:
    cid = item["id"]
    item_type = item["type"]
    title = item["title"]
    name_used = item.get("name_used") or "Thomas McCarthy-Howe"
    authorship = item.get("authorship") or "primary"
    role = party_role(item_type, authorship)

    parties: list[dict] = [
        {
            "name": display_name(name_used),
            "role": role,
            "meta": {"authorship": authorship},
        }
    ]
    for ca in item.get("co_authors") or []:
        parties.append({"name": str(ca), "role": "author"})

    description = item.get("description") or title
    dialog = [
        {
            "type": "text",
            "mimetype": "text/plain",
            "body": description,
        }
    ]

    analysis_body: dict = {
        "themes": list(item.get("themes") or []),
        "confidence": item.get("confidence") or "medium",
        "source": item.get("source") or "corpus_yaml",
    }

    analysis = [
        {
            "type": "themes",
            "vendor": "corpus-report",
            "body": analysis_body,
        }
    ]

    attachments: list[dict] = []
    url = item.get("url")
    if url:
        path = url.lower().split("?", 1)[0]
        mediatype = (
            "application/pdf" if path.endswith(".pdf") else "text/html"
        )
        attachments.append(
            {
                "type": "url",
                "url": url,
                "mediatype": mediatype,
            }
        )

    meta: dict = {
        "corpus_id": cid,
        "corpus_type": item_type,
        "venue": item.get("venue"),
        "name_used": name_used,
        "authorship": authorship,
    }
    meta_date = _date_to_meta_value(item.get("date"))
    if meta_date is not None:
        meta["date"] = meta_date
    if item.get("notes"):
        meta["notes"] = item["notes"]
    if item.get("date_approximate"):
        meta["date_approximate"] = True
    if item.get("publication"):
        meta["publication"] = item["publication"]
    meta = {k: v for k, v in meta.items() if v is not None}

    vcon_id = str(uuid.uuid5(VCON_UUID_NAMESPACE, cid))

    return {
        "vcon": "0.0.2",
        "uuid": vcon_id,
        "created_at": iso_created_at(item.get("date")),
        "updated_at": UPDATED_AT,
        "subject": title,
        "parties": parties,
        "dialog": dialog,
        "analysis": analysis,
        "attachments": attachments,
        "meta": meta,
    }


def main() -> None:
    data = yaml.safe_load(CORPUS_PATH.read_text())
    items = data["items"]
    written = 0
    for item in items:
        t = item["type"]
        if t in TALK_TYPES:
            path = TALKS_DIR / f"{item['id']}.vcon.json"
        elif t in WRITING_TYPES:
            path = WRITING_DIR / f"{item['id']}.vcon.json"
        else:
            continue
        doc = build_vcon(item, path.parent)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        written += 1
    print(f"Wrote {written} vCon files under vcons/talks and vcons/writing.")


if __name__ == "__main__":
    main()
