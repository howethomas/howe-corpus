# Writing

Essays, Internet-Drafts, whitepapers, documentation, guides, and
mailing-list posts — each as a structured vCon.

Entries are indexed in [`../../corpus.yaml`](../../corpus.yaml) under
`items:` with `type` one of `essay`, `internet-draft`, `whitepaper`,
`documentation`, `guide`, or `mailing-list-post`. When you lift an index
entry into a full vCon, save it here as `<id>.vcon.json`, reusing the
same `id`.

See [`../../schema/vcon.md`](../../schema/vcon.md) for the expected shape.
For writing, `parties` should include all authors/editors with
`meta.authorship` (`sole`, `primary`, `co-author`, `editor`);
`attachments` should link to the canonical URL; `dialog` should include
the abstract or lede.
