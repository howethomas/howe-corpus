# vCon shape used in this repo

Each file under `vcons/**/*.vcon.json` conforms to the IETF vCon container
draft (v0.0.2), with the repo-specific conventions below.

## Top-level

- `vcon`       — always `"0.0.2"`
- `uuid`       — stable UUID; once assigned, never change it
- `created_at` — ISO-8601 date the item was produced (talk given,
                 patent issued, article published)
- `updated_at` — ISO-8601 date the vCon file was last edited
- `subject`    — human-readable title of the item

## parties[]

One entry per person associated with the item. Common roles:

- `inventor` — for patents
- `author`   — for writing
- `speaker`  — for talks
- `host` / `interviewer` — for podcasts
- `editor`   — for publications
- `judge`    — for hackathons

Each party SHOULD have at least `name`; add `role` and per-party
`meta` (e.g. `{"authorship": "primary"}`) as needed.

## dialog[]

At minimum one entry of type `text` with the abstract / description /
transcript. Additional entries may point to recordings, slide decks,
or published files via `url` + `mediatype`.

## analysis[]

Use vendor `"corpus-report"` for themes and descriptions pulled from the
corpus research reports. Suggested shape:

```json
{
  "type": "themes",
  "vendor": "corpus-report",
  "body": {
    "themes": ["..."],
    "description": "...",
    "confidence": "high",
    "source": "corpus_report"
  }
}
```

## attachments[]

Links to source material:

```json
{
  "type": "url",
  "url": "https://patents.google.com/patent/...",
  "mediatype": "text/html"
}
```

## meta

Repo-specific fields that mirror the `corpus.yaml` entry:

```json
{
  "corpus_id": "patent-us9762734-intermediary-device-2017",
  "corpus_type": "patent",
  "venue": "uspto",
  "date": "2017-09-12",
  "name_used": "Thomas Spencer McCarthy-Howe",
  "authorship": "co-author",
  "patent_number": "US 9,762,734",
  "assignee": "TEN DIGIT Communications LLC",
  "notes": "..."
}
```

## Corpus types

The `type` field on a `corpus.yaml` item (and `meta.corpus_type` on a vCon)
is one of:

`patent`, `essay`, `internet-draft`, `whitepaper`, `documentation`,
`code-repo`, `package`, `talk`, `podcast`, `judging`, `dataset`, `tool`,
`mailing-list-post`, `guide`.
