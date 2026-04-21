# Howe Corpus

The (sometimes stupid) stuff I've said.

A structured archive of the talks, writing, patents, and code of Thomas J. Howe
(inventor-of-record and primary byline: **Thomas Spencer McCarthy-Howe**; also
published as **Thomas Howe**).

Every item — a talk, a blog post, a patent, an IETF draft — is represented as a
[vCon](https://datatracker.ietf.org/doc/draft-ietf-vcon-vcon-container/)
(virtual conversation) JSON document and indexed in [`corpus.yaml`](./corpus.yaml).

## Layout

```
howe-corpus/
├── README.md               ← you are here
├── corpus.yaml             ← master index of every item
├── schema/
│   └── vcon.md             ← how vCons are used in this repo
└── vcons/
    ├── patents/            ← patent filings & grants
    ├── talks/              ← conference talks, podcasts, interviews
    └── writing/            ← essays, drafts, docs, whitepapers
```

## What is a vCon?

A **vCon** is an IETF-draft JSON container for conversation data: `parties`,
`dialog`, `analysis`, and `attachments`. This repo repurposes the container
as a universal home for corpus items:

| vCon field    | Corpus meaning                                            |
| ------------- | --------------------------------------------------------- |
| `parties`     | inventors, authors, speakers, interviewers                |
| `dialog`      | the primary content (abstract, transcript, text body)     |
| `analysis`    | themes, summary, confidence, sourcing                     |
| `attachments` | links to source URLs, PDFs, slides, recordings            |
| `meta`        | type-specific metadata (patent #, venue, assignee, etc.)  |

See [`schema/vcon.md`](./schema/vcon.md) for the exact shape used here.

## Adding a new item

1. Copy [`vcons/patents/_template.vcon.json`](./vcons/patents/_template.vcon.json)
   (or a similar existing file) into the right subdirectory.
2. Save it at `vcons/<category>/<id>.vcon.json` using a stable `id` that
   matches the `id` field of its `corpus.yaml` entry.
3. Add a matching entry under `items:` in [`corpus.yaml`](./corpus.yaml).
4. If you know of missing material, note it under `gaps:` in the same file.

## Status

| Category  | Indexed in `corpus.yaml` | Full vCon files              |
| --------- | ------------------------ | ---------------------------- |
| Patents   | 11 entries (8 families)  | Yes — under `vcons/patents/` |
| IETF      | ~10 drafts + WG activity | Index only                   |
| Writing   | ~80+ entries             | Index only                   |
| Talks     | ~25 entries              | Index only                   |
| Code      | ~10 repos/tools          | Index only                   |

The master index in `corpus.yaml` is the single source of truth. Full vCon
JSON files are seeded for patents; other categories carry the same `id`
scheme and can be lifted into full vCons as they're authored.
