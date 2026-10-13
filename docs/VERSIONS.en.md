<!-- translated-from: CLAUDE.md @ 700c798 (summary of the version list) -->
<!-- translated-from: docs/NOTAS.md @ 700c798 (summary of the version headings) -->
# How the versions stack up

A summary for readers without Spanish, written for this fork. Detail per version: the `### SCnn` sections of
`docs/NOTAS.md` (Spanish, newest first) and the version list in `git show upstream/main:CLAUDE.md`. What each release
candidate and beta added or fixed, in English: upstream's `CHANGELOG.md` (bilingual, from RC0.3).

The master effects view is called **Master FX** (upstream renamed it on 2026-10-12; the earlier name is a trademark
and is not used anywhere, which is also why upstream republished its repository without history).

## Naming
- **`SCnn` / `SCnn.m`** — a normal build. Each one is the previous one plus something: "SC24 = SC23.6 + …".
- **`…D`** (`SC17D`, `SC35DB`) — a **diagnostic** build: it probes the device (memory maps, CPU headroom, the SD
  card API) and reports through pad LEDs or MIDI. Upstream used these to settle what emulation could not.
- **`…S`** (`SC361S`, `RC0S`, `RC0.3S`) — the "safer" variant: no code of the mod writes to the SD card.
- **`RCn` / `RCn.m`** — release candidates: an `SC` build renamed (only the marker changes), or since RC0.4 the
  previous RC plus selected fixes. RC0.2 = SC37.5, RC0.3 = SC38, RC0.4 = RC0.3 + the fixes of SC38.2–SC38.6, RC0.5 =
  RC0.4 + the captured sample in front of the Master FX effects.
- **`BETAn`** — betas: an `SC` build renamed, with features not yet tested on the device, released next to the RCs
  (no `S` variant). BETA0 = SC38.7, BETA1 = SC39, BETA2 = SC39.1, BETA3 = SC39.2, BETA4 = SC39.4, BETA5 = SC39.6.

## The builder chain
- Every version has a builder `tools/build_<name>.py`. A builder **imports the previous version's builder**,
  switches on options and adds code. `build_rc0_2.py` reaches the base through ~35 imports
  (`B.B4.B2.B1.B.B.b33 … b18.b6.b5`).
- Builders change behaviour only through options (`use_…()` functions, module flags), so every old version still
  rebuilds byte-for-byte: `tools/verify_builds.py` checks all 150 against `firmware/<dir>/manifest.json`.
- Each builder runs in its own process because builders patch module globals of earlier builders at import time.

## Eras
| Versions | What was added | Main modules |
|---|---|---|
| SC02–SC07 | ARM-only MIDI tweaks: shared MIDI channels, channel-16 Rx / Tx toggles, internal MIDI loopback without a cable, **patch flip** (notes as Program Change) on MIDI 1 / 2 | `build_shared_channels.py`, `build_sc03`–`sc06` |
| SC08–SC12 | Drums: chromatic Preset view (drums played in a scale), pitch in semitones, fine tune in cents | `build_sc08`–`sc12` |
| SC10 | **First DSP patch**: FX return through mixer strips 3 / 4 | `build_sc10` |
| SC13 → SC16 | Drum sidechain. SC13 **put the device in a reboot loop** (recovered with the bootloader); redone as SC16, which also **relocated the core-0 DSP program** to the end of the image so it could grow | `build_sc16` |
| SC14–SC15 | First Master FX (Gater, Auto-Filter) in the FX view; line input instead of the synth's noise source | `build_sc14`, `build_sc15`, `linein2/3` |
| SC17–SC17.8 | **Master FX view** (Mixer pressed twice): Gater, Auto-Filter LP / HP, Digitise, Phaser, Vinyl; knob LEDs; bottom row of assignable FX slots; **song pointer**; FX view keys | `build_sc17.py` (1,900 lines), `masterfx_dsp.py`, `fxkeys.py` |
| SC18–SC19.9 | Drum knobs redone to match the panel labels (ring mod, envelopes, filter modes, bitcrush, distortion); FX view LEDs; **mod settings saved in the project** (SC19); synth source view (Synth 1 / 2 pressed twice) | `drums18.py`, `drums2_dsp.py`, `leds18.py`, `persist19.py`, `srcview.py` |
| SC20–SC24 | **MIDI-track engine**: the audio input of MIDI 1 / 2 through a VCA / VCF / FX chain, then an oscillator source (morphing waves, second oscillator, FM / ring / sync, paraphony); reverb / delay parameters on Shift + knob; on-device **CC editor** for the MIDI macros | `vcf20*`, `vcf21.py` (3,300 lines), `vcf21_dsp.py`, `fxparams.py`, `drumnote.py` |
| SC25–SC31 | CC / NRPN in and out for the new values, automation recorded by the sequencer, **step-drummer** (paired-step sequencing on top of the pattern), NRPN for drums / Master FX, **VA-drum** engine, project-save fixes | `vcf21.py`, `nrpn28.py`, `persist19.py` |
| SC32–SC35 | New song pointer (phrases); **captured sample** (record the master, play it, use it as a drum); external DSP memory mapped by diagnostics; **pack files on the SD card** (save captures, swap samples, delete packs); remote diagnostics over USB SysEx (`ctremote.py`) | `build_sc17.py`, `sampler_dsp.py`, `drumrep.py`, `packio.py`, `rdiag.py`, `probe*` |
| SC35D–SC36.2 | **DSP core 1** (unused by stock) brought into play: **granular synth**, **Glitch** (tape-buffer effect on the master), FX sequencer | `granular_dsp.py`, `build_sc17.py`, `vcf21.py` |
| RC0, SC37–SC38, RC0.1–RC0.3 | Release candidates; copy / swap samples and synth patches between packs (in place when the sample fits), Duplicate in the Preset views, Glitch overload; Mixer Shift + knob = level 100 / 0, Clear + knob in Master FX, Clear + pad replaces a drum with the capture (Shift + pad is stock's silent sample select again) | `packio.py`, `sampler_dsp.py`, `granular_dsp.py`, `mixshift.py`, `drumrep.py`, `persist19.py` |
| SC38.1–SC39.6, RC0.4–RC0.5, BETA0–BETA5 | Fixes (armed capture from Play, latched Shift + pad 7 loop, Duplicate to empty slots between packs); granular **stretch** and source selector; **MIDI Thru Merge / Filter**; reset of the MIDI-track engine; synth patches coloured by voice mode; **split keyboard** (Synth 1 + Synth 2); **random-mutate per step** (row 4 of the probability view); own-synth patches of MIDI 1 / 2 in the padding of the pack's patch bank; saving the synth patch from the panel; macro-knob destination editor; type knobs as colours; copying projects between slots and packs; the captured sample in front of Master FX. `tools/patchtool.py` edits own-synth patches on the PC | `build_sc17.py`, `midithru.py`, `mutate39.py`, `mpatch.py`, `psave.py`, `macroed.py`, `typeleds.py`, `sesscopy.py`, `srcview.py`, `packio.py` |

## What has been confirmed on the device
Two upstream sources, which disagree:
- **`NOTAS.md` headings** mark as working on hardware: SC02–SC12, SC14 / SC14.2, SC15, SC16, SC17.3, and the
  diagnostics SC17D and SC21D (upstream's `CLAUDE.md` version list adds SC20D.1 and the SC35D–SC35DB diagnostics,
  tested 2026-10-08 / 09, though some of their headings still say pending). They mark as failed: SC13 (reboot loop), SC17 / SC17.2 (view did not open),
  SC34D (broke pack duplication), and SC19 / SC19.1 / SC19.2 / SC20D (hang at power-on, fixed in SC19.3). Nearly
  every other heading still says "⏳ pending test".
- **`docs/CHECKLIST.md`** (see `CHECKLIST.en.md`), updated by the author from the device, ticks most features through
  about SC23 as working: drums, Master FX, the FX view, the synth source, the VCA / VCF mode, the CC editor.
- Known device-only problems: SC23.3's OSC and VCA-VCF modes had no audible effect on the device although they worked
  in emulation (cause not recorded as found); SC37 / SC37.1's cross-pack swap deleted or mixed samples (fixed in SC37.2);
  SC37.3's Duplicate did nothing in the synth Preset view (fixed in SC37.4); SC37.4's Clear never lit in the packs view
  (fixed in SC37.5); SC37.7's packs went dark after a delete and Clear blinked (fixed in SC37.8); Clear + knob did
  nothing in Master FX and the drums' "default" LED showed dim red instead of blue (fixed in SC37.9: stock's Clear
  colours come from a palette in RAM, where blue is 0x07; the flash palette's 0x46 renders dim red-orange).
- **Little from about SC24 onwards** (step-drummer, VA-drum, captured sample, SD-card pack I/O, granular, Glitch,
  RC0–RC0.5) is recorded as confirmed on the device, although the reports above show the SC37 builds running there.
  The exception: **SC39 / BETA1** (random-mutate per step) is recorded as working (2026-10-12).
- Measured on the device with PATCHD: **35 palette codes animate** (pulse or blink) because the RGB table in RAM
  changes over time; SC38.8's "steady" purple pulsed. Upstream moved its dim white from `0x03` to `0x02` (SC39.5).
- The last build the original `CLAUDE.md` calls confirmed-safe to boot is **SC17.7**.

## Diagnostic builds worth knowing
| Build | Finding |
|---|---|
| SC21D | Core-0 DSP program RAM reaches `P:$3FFF` (2,048 more words than assumed) |
| SC32D–SC32D2 | External DSP memory stores 16 bits per 24-bit word; `M0 = $FFFF` at the hook |
| SC35D–SC35D3 | Core 1 runs custom code; free external memory `$337000–$57EFFF` and `$E80000–$FFEFFF`; stock writes `Y:$600000` |
| SC35D4–SC35DA | The stock SD-card content API (read / write / delete items) works from the UI task |
| SC35DB | Core 1 → core 0 audio works; budget ≤ 2,048 external reads per 32-sample block |
| SC34D | Hooking the generic file vtable breaks pack duplication: **do not** |
| PATCHD | The 172 B of padding after each synth patch in `Patches/NN_PATCHBANK.cpb` survive stock's saves, pack changes and power-off: usable storage |
| SEQWD | A DWT watchpoint (through the DebugMonitor vector) found the sequencer's note player: `0x08040E5A`, the note read at `0x08040EFC` |
