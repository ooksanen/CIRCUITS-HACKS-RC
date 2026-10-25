<!-- translated-from: CLAUDE.md @ c79c1ca (adapted for this fork, not a 1:1 translation) -->
# CTPlay / CIRCUIT-HACKS (ooksanen) — context for Claude Code

Firmware patches for the **Novation Circuit Tracks**, official firmware 1.2.1 build 4486, derived from
[Ghillermo/CIRCUIT-HACKS-RC](https://github.com/Ghillermo/CIRCUIT-HACKS-RC). Upstream documents in Spanish; code
comments are in English. Upstream's original Spanish `CLAUDE.md`: `git show upstream/main:CLAUDE.md`.

## Remotes
- **`origin`** = `ooksanen/ctplay`, **private**, the primary repository: every branch lives here. Private so unfinished
  builds are never public.
- **`fork`** = `ooksanen/CIRCUITS-HACKS-RC`, the public GitHub fork: **`main` only** (upstream + the English additions).
  Never push other branches there.
- **`upstream`** = `Ghillermo/CIRCUIT-HACKS-RC` (no S), the original. Upstream renamed it on 2026-10-24; the old name
  `CIRCUITS-HACKS-RC` is now a separate stub repo ("Moved", no shared history): never merge it. The remote points at
  the new name since 2026-10-25 (`git remote set-url upstream https://github.com/Ghillermo/CIRCUIT-HACKS-RC.git` in
  another clone); its history continues RC2.06 (`395d9e6`, also pinned as `refs/archive/upstream-main-rc2.06`).
- Do not push to `origin` or `fork` without the user's approval. Upstream's publishing workflow (private branch,
  `public` remote, `gh-pages`, `commit-tree` onto `public/main`) does **not** apply here.

## Branches
- **`main`** = upstream + English additions only (this file, `*.en.md` translations, `fork/`). Never edit upstream's
  files on `main` (except this `CLAUDE.md`), so `git fetch upstream && git merge upstream/main` stays conflict-free.
  After merging upstream, push `main` to both `origin` and `fork`.
- **`slim`** = the focused firmware (product name **CTPlay**): its own C build system under `slim/`, own version names.
  Branched from `main`; takes upstream changes by merging `main` while it is mostly additive, by cherry-picking once it
  deletes / rewrites modules. Its `CLAUDE.md` may diverge from this one (protected by the same merge driver).
- **Upstream rewrote its public history on 2026-10-12** (`--orphan`, at RC0.5 / BETA5), so on 2026-10-13 `main` was
  rebuilt on top of it: `upstream/main` + our additions as new commits. The old `main` (upstream up to RC0.3 + our
  commits) is tag `main-pre-rc0.5`; `slim` joined the new `main` with a one-time bridge merge. Reason for the rewrite:
  the master effects view is now called **Master FX** everywhere; its earlier name is a trademark that upstream no
  longer writes in code, docs, commit messages or file names. Follow that in everything we write.
- **`CLAUDE.md` uses `merge=ours`**: run `bash fork/setup.sh` once per clone (sets the `upstream` / `fork` remotes,
  `.git/info/attributes` and the driver).

## Setup and commands
- Python: always `.venv/bin/python` (Ubuntu blocks system pip). First time: `python3 -m venv .venv`, then
  `.venv/bin/python tools/setup_dev.py` (official firmware → `stock/`, device dumps + dsp56300 → `ext/`, `re/app.asm`).
- `.venv/bin/python tools/verify_builds.py` — rebuild every version, compare to `firmware/<dir>/manifest.json`; must
  print **ALL IDENTICAL** (~2 min). The duplicate-marker check only runs once `firmware/*/*.bin` exist
  (`tools/patch_official.py stock/circuittracks-firmware-4486-STOCK.syx --all`).
- `bash tools/run_tests.sh [quick|full]` — emulation tests; quick ≈ 60 min, full ≈ 30 min more. Needs the built `.bin`s.
- `.venv/bin/python fork/translation_status.py [-d]` — which English translations are behind upstream (`-d` shows diffs).

## Docs map
- `docs/VERSIONS.en.md` — **start here**: how the 316 versions stack up and which were confirmed on the device.
- `docs/RECURSOS.md` (second half English) — resource budget: flash, RAM, saved state, both DSP cores, external memory.
  The latest builds are nearly full: SC46.5 / Beta 3.22 2,392 B at the image's end plus 18,670 B in the free zone
  (stock's unused copy of the DSP programs, `0x080101F0–0x0801865A`, `tools/hole.py`, from SC44.8), DSP core 0 9 words,
  core 1 177 words (SC44.7), heap 4 B. Its English half stops at SC39 / BETA1; the Spanish half has SC43.9–SC46.5.
- `docs/NOTAS.md` (Spanish, 750 KB, newest first) — technical detail of every patch and every finding. Read the
  section for the feature at hand rather than the whole file.
- `docs/CHANGELOG.md` (at the top level until RC2.08) — upstream's per-release changes, Spanish and English (RC0 → RC2.09 / RC2.09S,
  BETA0 → BETA5 and Beta 1.0 → Beta 3.22 = SC46.5, 2026-10-25). The feature list: `docs/FEATURES.md` (English) /
  `docs/CARACTERISTICAS.md`, out of `README.md` since RC2.08.
- `docs/CHECKLIST.en.md` — upstream's on-device test checklist. `firmware/<dir>/PRUEBA.md` — per-build test plan (Spanish).
- `LEEME.md`, `docs/DEPENDENCIAS.md`, `docs/LOCAL.en.md`, `docs/MANUAL.en.md` — already bilingual / English.
- `fork/ct_uploader.en.html` — the firmware uploader with an English interface (slim's uploader is generated from it).

## Rules (from upstream; they protect the device)
- **Never write the internal flash or the option bytes from patch code.** The bootloader (`0x08000000–0x0800FFFF`) is
  never touched. Recovery: hold **Scales + Preset + Note** at power-on, reinstall the official firmware.
- Every `.syx` comes from `tools/ct_fw.py` with a verified CRC. Nothing goes to the device without passing the emulation tests.
- **A new build must not change earlier ones**: `verify_builds.py` → ALL IDENTICAL. A builder that needs to behave
  differently gets an option (e.g. `use_mixer14()`, `use_full_leds()`, `DIAG`), never an in-place edit.
- **Version marker**: 6 bytes at offset 0x20 of the version block. The bootloader only installs an image whose version
  block (`0x1C8`, 0x26 B) differs from the installed one, and names are cut to 6 bytes: two names sharing their first
  6 characters will not install over each other (why upstream has `SC32D2`, not `SC32D.2`). Diagnostic builds end in `D`.
- A published build gets `firmware/<dir>/` (`manifest.json`, `PRUEBA.md`; `.syx` / `.bin` are gitignored), its section
  in the notes and its entry in `tools/verify_builds.py` (`BUILDS`).
- **From the DSP service tick** (chain head at `0x080213AA`; the main loop holds the semaphore `[ptr + 0xC]` via
  `0x08021064`) **never call `MARK_DIRTY` (`0x0803BDCC`) or anything that takes that semaphore**: the device hangs
  forever (this is what froze SC19 / SC19.1 / SC19.2 / SC20D at power-on). Mark with `0x08021FDC(type, index)`; write /
  read the DSP with `0x080292F8` / `0x08029344`. Emulation does not model the hang: tests count semaphore takes (`emu_sc19_3.py`).
- Identify views and buttons by what the code does with them, not by assumption. Tests must go through the real route
  (controller `0x08033320` / `0x08033282`), not call the presumed handler directly.
- Emulation passing is not device passing: several features worked in emulation and failed on the device
  (see `docs/VERSIONS.en.md`). Diagnostic builds that report through LEDs / MIDI are how upstream settled those.

## Platform summary
- **ARM:** STM32F745 (Cortex-M7). App at `0x08010000` (max 0x70000 B; stock image ends at `0x0805CDDC`, code caves
  from `0x0805CDE0`; upstream also fills the free zone `0x080101F0–0x0801865A` from SC44.8, see Docs map). SP `0x20050000`.
  - Block heap: limit `[0x20002B44]` = `0x20044E58`, current `[0x20002B48]` (`0x20044D68` on the device, 240 B free).
    The allocator `0x0801D7D8` hits `bkpt` when exhausted and never frees. Above the heap, `0x20044E58–0x2004FDFF` (≈ 44 KB) is free according to upstream SC44.2 (stock's own memory report
    `0x0801D426` counts it as remaining with a 512 B stack above; two RAM dumps show it never written), **not yet
    confirmed on the device**: upstream stays below `0x2004F000` and signs what it keeps there (RAM is not cleared at power-on).
  - SC14+ reserves the end of the heap (`c_gst`, `build_sc14.ST`).
- **Controller** `MGR` `0x20040B10` (vtable `0x0805A100`): button press `0x08033320(ctrl, id)` (`tbh` at `0x080333C4`),
  release `0x0803381A`, pad `0x08033282`, knob `0x08033848`.
  - Active view = `[ctrl+0x6C]`. Shift = p0 of `[ctrl+0xC]`; with Shift only buttons in mask `0x07DBBE00` pass (ids 9–13,
    15–17, 19, 20, 22–26, plus 0x1B). **Shift + Synth 1/2, MIDI 1/2, Drum 1–4, Preset, Mixer, 1-16/17-32 do nothing in
    stock** — hence "press Synth 1/2 twice" rather than Shift + button for new views.
  - Buttons → view id: 13 → 1 (not Mixer), **14 → 2 = Mixer** (`0x200447D4`, vtable `0x0805A668`), 15 → 3 = FX (`0x200443B4`, `ctrl+0x44`).
  - Other buttons: **16 Record (LED 48), 17 Play (49), 19 Octave ▼, 20 Octave ▲ (51 / 52), 21 = 1-16/17-32 (53)**,
    22 Tempo/Swing (54), 23 Clear, 24 Duplicate.
  - FX view: sub-views `[+0xC]` = delay sends, `[+0x10]` = reverb sends; active page `[fx+0x20]` p0 (1 = delay).
  - Project parameters (sends type 0x20: 0–7 reverb / 11–18 delay; master type 0x21: 0 filter, 1 resonance):
    `0x08034D92(this+4, type, index, value)` with `this = [[[0x200069E4]+0x10]]`, same path as MIDI.
- **LEDs:** task `0x08034196` reads 42 entries of the active view: 0–31 pads, 32–33 buttons, 34–41 knobs. Panel LEDs
  (69): 48 Record, 49 Play, 51/52 Octave, 53 1-16/17-32, 55 Clear, 56 Duplicate, 60–67 knobs, 68 master filter.
  Colours are Novation palette codes (palette `0x08056464`; the RGB table at `0x20003804` is B, G, R); pick and confirm on the device.
  Stock reads some colours from a **palette in RAM**, not the flash one: Clear's blue is 0x07 there, while flash entry
  0x46 renders dim red-orange (upstream SC37.9). Check a chosen code's RGB in emulation against stock's own LEDs.
  **35 codes animate on the device** (the RAM RGB table changes over time; the emulator's snapshot is static): `03 04 05
  06 10 11 15 16 19 1A 1B 1C 1D 27 28 2F 30 39 3A 42 43 47 48 4B 4C 4F 50 56 57 58 59 5A 5B 61 62` (hex). Families run
  "steady, dim, blink, pulse" (e.g. `49` / `4A` / `4B` / `4C`). Never use them for a steady colour: dim white is `0x02`,
  not `0x03` (upstream SC38.8 / SC39.5, measured with PATCHD).
- **DSP56724** (two DSP56300 cores, shared external SDRAM with 16 useful bits per 24-bit word):
  - Core 0 program relocated to the end of the image (SC16); load table `0x08029700`; ARM→DSP write `0x080292F8(core, v<<8, addr)`.
    Program RAM `P:$0000–$3FFF`. Voice table `X:$EB–$15A`: never touch. Current voice's synth = `x:$CC`.
  - Stack: 15 levels, stock uses 6. Never nest new `jsr` / `do` above stock's (SC13 hung); `emu_sc18_dsp.py` compares `SPMAX`.
  - Core 1: 2,048 program words, runs the granular synth and the Glitch; core 0 waits on it, so work goes in short tasks.
  - Free / used memory: `docs/RECURSOS.md`.
- **Own assemblers:** `tools/thumb.py` (Thumb-2) and `tools/dsp56.py` + `dsptool asm` (DSP; results cached in
  `tools/dsp_asm_cache.json`). No Keystone. Out of range: `zjmp` / `bc` (long branches), `ldrb_w`, `strh_w` / `ldrh_w`.
- **DSP56300 assembler traps** (each one bit upstream):
  - `mpy x0,y0,b` assembles to a long form that treats `y0` as **unsigned** → write `mpy y0,x0,b`. In general use the
    short-form operand orders: `mpy y1,x1`, `mpy y1,y0`, `mpy x1,x0`, `mpy x0,y1`, `mpy y0,x0`. `mpy y1,x0` is not legal.
  - `and` on a negative accumulator leaves `a2 = $FF` and `move a,rN` saturates: add a constant first to make it positive.
  - External memory keeps 16 bits per word (low byte 0). `M0 = $FFFF` at hook `P:$23C`: set `M` linear before buffer code.
- **Rate limits:** at most one message per voice to the DSP every 2 ms (plus heartbeat); MIDI sent from the UI task is
  cut at 64 messages per press.

## Tests (notes)
- Each ARM test takes minutes (Unicorn), DSP tests longer. Emulated clock does not advance; `sleep()` (`0x0801BE78`)
  is skipped in `emu_sc17.py`. DSP `do` loops execute in one interpreter step, so `WATCH` / `HIST` PCs inside a loop are the `do`'s.
- `tools/dspemu.py` and `tools/dsp_session.py` delete their temp directories after each run.
- `verify_builds.py` assembles DSP code from the cache only (`tools/dsp_asm_cache.json`); `DSP_ASM_CACHE_UPDATE=1` lets
  it call dsptool. Upstream's tests pick what to check from manifest labels (`emu_sc35.FEATURE_LABELS`), not marker lists.

## Translations
- English files carry `<!-- translated-from: PATH @ SHA -->` in their first lines (`.md` and `.html` files are checked). After merging upstream, run
  `fork/translation_status.py`; `NOTAS.md` and the version list are newest-first, so updates are mostly new top sections.
- Keep upstream file names (`PRUEBA`, `NOTAS`, `RECURSOS`): they are referenced throughout code and docs.
