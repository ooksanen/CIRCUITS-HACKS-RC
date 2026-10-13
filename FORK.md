# About this fork

Fork of [Ghillermo/CIRCUITS-HACKS-RC](https://github.com/Ghillermo/CIRCUITS-HACKS-RC), firmware patches for the
Novation Circuit Tracks. Upstream documents mostly in Spanish; this fork adds English documentation.

This public fork carries one branch, `main`: upstream, unchanged, plus English additions only, so upstream merges
cleanly. A separate focused firmware is developed privately and is not published yet.

English additions:
- [`docs/VERSIONS.en.md`](docs/VERSIONS.en.md) — how the ~115 versions stack up and what was confirmed on the device.
- [`docs/CHECKLIST.en.md`](docs/CHECKLIST.en.md) — upstream's on-device test checklist.
- [`fork/ct_uploader.en.html`](fork/ct_uploader.en.html) — upstream's firmware uploader (`tools/ct_uploader.html`) with an
  English interface; its list of accepted builds keeps upstream's labels.
- [`CLAUDE.md`](CLAUDE.md) — English context for Claude Code (upstream's Spanish one: `git show upstream/main:CLAUDE.md`).
- Already English upstream: the second half of [`README.md`](README.md#english), [`LEEME.md`](LEEME.md),
  [`docs/MANUAL.en.md`](docs/MANUAL.en.md), [`docs/LOCAL.en.md`](docs/LOCAL.en.md), the second half of
  [`docs/RECURSOS.md`](docs/RECURSOS.md#resources), [`docs/DEPENDENCIAS.md`](docs/DEPENDENCIAS.md).

After cloning: `bash fork/setup.sh` (`upstream` / `fork` remotes, `CLAUDE.md` merge rule). Translation freshness:
`python fork/translation_status.py`.

Back up the SD card before flashing anything; recovery is **Scales + Preset + Note** at power-on, then the official
firmware. The MIT licence and the notices of the upstream [`README.md`](README.md) apply.
