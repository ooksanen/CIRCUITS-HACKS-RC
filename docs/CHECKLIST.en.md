<!-- translated-from: docs/CHECKLIST.md @ 700c798 -->
# On-device checklist (2026-10-06)

> Translation of upstream's `docs/CHECKLIST.md`. It is the upstream author's own checklist, last updated around
> SC23–SC35, so it predates RC0.2. Ticks are the author's results, not ours.
> **†** = the line starts with `#=====` in the original (it looks like an archived / done mark).

Collects what `README.md` / `CLAUDE.md` mark as **pending test** (⏳), grouped by function rather than by build. Mark
each box with what you have checked: `[x]` fine, `[!]` fails (note what you see), `[ ]` not tested. The "test" column
is the minimum action; the detail is in the build's `PRUEBA.md`.

Already confirmed (no need to repeat): SC02–SC16 (including the sidechain), SC17.3, SC17.6 / SC17.7 (song pointer),
SC20D.1 (modes 5 and 6 work), SC21D (DSP program RAM reaches `P:$3FFF`).

## 0. Boot and basics
- [x] A recent build (the last one you flash) **boots normally** and does not hang at power-on (the fix is `FIX_LOCK`, SC19.3 onwards).
- [x] After power off / on, **saved settings come back** (SC19.4: copy of the session record when a project loads; patch change).

## 1. Drums
| Status | Function (build) | Test |
|---|---|---|
| [x] | Chromatic step recording: each pitch only on its step (SC18) | record a bar in chromatic mode and leave it recording |
| [x] | Drum knobs as printed on the panel: K1 pitch … K8 FX (SC19.8) and their **brightness by value** (SC19.6) | turn every knob, with and without Shift |
| [x] | Distortion type per drum (Shift + FX) (SC19.9) | change type and save / load the project |
| [x] | Scale in three rows; K1 = pitch bias; **Clear** on the new knobs (SC20.1) | scale view; Clear + knob (red / blue) |
| [x] | Drum squares duplicated in the Note view (SC21.3) | pads 25-28 = drums 1-4 |
| [x] | Drum settings, Master FX assignments and synth modes **per PACK or session** (SC19) | save, power off, load; copy project; clean new project |

## 2. Master FX and FX view
| Status | Function (build) | Test |
|---|---|---|
| [x] | Correct knob LEDs in Master FX (SC17.4) and brightness by value (SC19.9) | open Master FX |
| [x] | Pad 8: switches off latched effects and the song pointer (SC17.8, SC18.1) | latch an effect and press |
| [x] | Pad 7: instant jump that repeats the step while held (SC19.7 / SC19.9) | press and hold; Shift + pad 7 latches |
| [x] | On state and song pointer reset to 0 on load / boot (SC19) | loading a project with Master FX active switches Master FX off |
| [x] | FX view: Octave ▲ / ▼ = delay / reverb sends, **Octave, Duplicate and 1-16/17-32 LEDs lit** (SC18.2 / SC18.3) | FX button |
| [x] | FX view: Duplicate = reset sends; 1-16/17-32 = master filter resonance (SC17.5 / SC19) | press them |
| [x] | **Shift + knob in the FX view = reverb and delay parameters** (SC21.2) | reverb and delay pages, LEDs by brightness with Shift |
| [x] | Setup FX returns (pad 22 / 23) reach the synth source (SC19.5) | Setup, return on strip 3 / 4, synth source 1-4 |
| [x] | Feedback of the returns (SC21.1) | return on strip 3 / 4 and raise its send |

## 3. Synth source and line input
| Status | Function (build) | Test |
|---|---|---|
| [x] | Line input ×2 and phase-inverted modes (SC16.1) | pads 26-29: confirm which one is the inverted signal |
| [x] | Synth source view: pressing Synth 1 / 2 twice opens pads 25-29; any button closes it; Shift + pads are stock (SC19.1) | same |
| [x] | Modes 5 / 6 (delay / reverb return) in the normal build | decide whether to bring them back (now only in diagnostic SC20D.1) |

## 4. VCA / VCF / FX mode of MIDI 1 / 2 (SC20 → SC23.2)
| Status | Function (build) | Test |
|---|---|---|
| [x] | The line input of MIDI 1 / 2 goes through VCF / VCA; the state **is saved with the signature** (SC20 / SC20.1) | enable, power off and on |
| [x] | **SC20.2** (without the mode): tells whether the external-input failure comes from the VCF | only if SC20 failed |
| [x] | Knobs reordered to match the panel; filter types; soft / hard / folding / wavefold FX (SC21) | step through the 16 values |
| [x] | 12 and 24 dB LP / HP filters (SC21.4) | Shift + K5 |
| [x] † | Ring mod / comb / chorus FX; K3 and Shift + K3 bipolar (SC22) | Shift + K8; K3 to both sides |
| [x] † | Oscillator: page B, pitch, shape, morph, env / LFO sends (SC22.1 → SC22.3) | |
| [x] † | Bottom-row pads: 25 CC, 26 patch flip, 27 source, 28 OSC view, 29 VCA-VCF view; distinct colours (SC22.4 / SC23.2) | the mode turns on when touching 28 or 29 and off when pressing the lit one |
| [x] † | Gate: notes from the pads and the sequencer open / close the VCA even when the view is not on screen | play with another view on screen |

## 5. CC editor (SC23 / SC23.1)
| Status | Function | Test |
|---|---|---|
| [x] | Touching a knob shows its CC on the 32 pads; turning changes it live | pad 25 |
| [x] | **Octave ▼ / ▲ cycle the fields** (CC → start → end, wrapping), without saving | |
| [x] | **Any view button, pad 25 or a template pad discards** | change and leave with Mixer |
| [ ] | 7- and 14-bit NRPN / RPN: four / six fields | template created in Components |
| [x] | With the editor off, Octave and the track button are stock | |
| [x] † | Drawing: digits (hundreds in two columns) are readable; **dirty LEDs remain on exit** (reported, fix pending in SC23.3) | |

## 6. Open (reported by you, not yet solved or published)
- [x] † **Erratically noisy oscillator**: in emulation the SC22.3 sine carried ~4 % harmonics (unrefined parabola); SC23.3 lowers it to ~1 % and fixes the neutral state (basic gate, unmodulated sine). To confirm on the device when SC23.3 is out.
- [x] † **Neutral default state + Clear + knob in red** (SC23.3, in development).
- [x] † **CC editor Octave LEDs** (▼ at the start, both in the middle, ▲ at the end) (SC23.3, in development).
- [x] † (marked `[xE]`) **Sends capped at half with "Effects to line in"** (SC23.3, in development; implemented and being tested in emulation).
- [x] † **Dirty LEDs on leaving the CC editor** (SC23.3, in development).
- [x] † **The sequencer automates the OSC / VCA-VCF parameters instead of sending CC** (requested; **not implemented**: needs hooking the macro CC emitter and automation recording; study pending).
- [ ] † MIDI-track toggle for reverb / delay + own NRPNs (old request, not started).
- [x] VCA with saturation + bipolar VCF for the external input: **done** in SC20+; to be confirmed (section 4).

## 7. Things that are not about the device
- [x] † `git push` of the local branches (needs your approval in the credentials window).

## Fixes requested for the next build (noted 2026-10-07; the pad 27 one is done in SC25, pending test)
| Build | Failure | Probable cause / planned fix |
|---|---|---|
| SC24 | When the VCA-VCF mode is switched off completely with pad 27 (oscillator → off), the top row (pads 1-8) **does not show the CC presets again** (the MIDI templates). | The stock Preset view only draws its template row when it is built and when the template changes (`T_DRAW = 0x0804D5CA`). With the mode on, `c_vleds` writes the page row into pads 1-8 (and 0 into pads 4-8); when it switches off, stock's content is not repainted. Fix: when the mode is off and the CC editor inactive, `c_vleds` calls `T_DRAW(view)` right after `c_tleds` (as `c_edclean` already does), or at least in `tr_off` of `vp_tri`; that also covers the mode being switched off another way (e.g. turning on patch flip). Emulation test: read the LED buffer after the pad 27 cycle and check pads 1-8 are those of the chosen template. |
| SC26 | Leaving step-drummer mode does not clear the LED rows (steps 9-16 and destinations). | **Done in SC27** (pending test): with the view closed `c_sdleds` writes 0 to pads 9-24 (the view's buffer is stock's and nobody repainted it). Test: `emu_sc27.py`. |

## Requests for the next build (noted 2026-10-08) — **done in SC33** (pending test; the record button ended up as: hold / short press / Shift = one bar)
| Where | Request | Notes |
|---|---|---|
| Step-drummer (MIDI 1 / 2, Synth 1 / 2) | **Real-time recording:** with recording on and the transport running, playing a pad in rows 1-2 (the steps, which sound when played) **records a note on the step that is playing, with its micro-step** (the exact moment inside the step, like stock live recording). | The note is the one that sounds when that pad is played (its step's, `c_sdnnote`). Still to decide: does it replace the step's note or get added as another unit (today the step-drummer keeps one note per step)? velocity = the pad's or the pair's? Current step = parameter 1 of the track store; micro-step from the tick (parameter 2). |
| Master FX, captured sample | **Pad 6 stays Vinyl** (the redesign changes: it is no longer replaced). **Pad 7 = trigger** the sample. **Pad 32 = record** (red; while held it records the master output). | Pad 32 stops being an assignable bottom-row slot. The sample needs its own set of 4 parameters (pitch, mode, start, end): today there are 5 sets × 4 knobs and Vinyl keeps its own → 4 B more RAM (the Master FX block has had 4 B of margin since SC24). First: the buffer zone, per SC32D.1. |

## Pending test on the device: SC27, SC28, SC29 (2026-10-07)
In order; each `PRUEBA.md` has the numbered list.
- **SC27** (`firmware/sc27/PRUEBA.md`): rows cleared when closing the step-drummer; Octave ▲ / ▼ and 1-16 / 17-32 lit; knob of the playing pair in white; knob pages 4 / 5; step-drummer on Synth 1 / 2 (synth button twice → pad 30).
- **SC28** (`firmware/sc28/PRUEBA.md`): drum NRPN (channel 10, MSB 5-8) and Master FX NRPN (channel 16, MSB 9) with a MIDI monitor; input from a DAW; Setup CC Tx / Rx filters.
- **SC29** (`firmware/sc29/PRUEBA.md`): fourth state of pad 27 (VA-drum); one-shot hit; DEC / SUS / REL = VCA / pitch / filter decays, independent; LRATE = noise; pad 31; state kept across power off; the normal oscillator sounds as before.

## Requests for SC35 (noted 2026-10-09) — save the sample to the pack's SD card
- **Save the capture to the SD card** over a sample of the pack (folder `PCM/`, valid for every session of the pack), with confirmation. Route: the content API of the storage task (op 7 = write); SC35D4 / SC35D5 check reading.
- **Swap the position of two samples** of the pack (e.g. 3 and 10): read both files and write them crossed through the same API, or rename them if stock has an operation for that. Needs a buffer in ARM RAM or going through the DSP's external memory.
- **Delete a whole pack.** Destructive and cannot be undone, so it gets a clear confirmation on the device (double press or hold) and is never applied to the pack in use without warning. Lead: the string `DeleteItem: %s` (`0x080267B8`) and the API operations still unknown (2, 3, 5, 8). First a diagnostic that tries it on a duplicated test pack.
- **Import a sample or a patch from another pack** (noted 2026-10-09). The content API carries the pack number in each item (`0xFF` = current), so an item of another pack can be read (PCM = type 4, Patches = type 3) and written into the current pack. A sample is a whole file (`NN_*.wav`). A patch lives inside an `NN_PATCHBANK.cpb` (16 per pack): its format must be worked out to copy a single patch rather than the whole bank. Interface still to choose: source pack, item and destination.
- **Name of samples generated on the device: `CAP` + an identifier** (noted 2026-10-09), i.e. `PCM/NN_CAP<ID>.wav`, with `NN` = the position. To resolve:
  - the identifier: **2-digit sequential number** (`NN_CAP01.wav`, `NN_CAP02.wav`…; user's decision, 2026-10-09). Still to decide where it comes from: the next free one looking at the pack's `CAP` files, or a saved counter;
  - how to set the name: the content API builds the path with `%s/%02d%s` and the fixed suffix `_PCM.wav`, so it would create `NN_PCM.wav`. To write `NN_CAP<ID>.wav` we need to see whether stock looks files up by the `NN_` prefix (SC35D5 will tell) and how Components renames or creates them (the SysEx path carries the sample name).
  - When replacing a sample the previous `NN_*.wav` must be removed so two files never share a position.
