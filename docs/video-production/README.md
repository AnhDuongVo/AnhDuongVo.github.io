## Repository workflow replacements — 13 October 2026

Trial-matcher, csr-assistant and ai-scientist now record each full repository's `examples/workflow.py`. Trial-matcher executes FHIR extraction, criterion assessment, coordinator review and ResearchSubject export with scripted model responses. CSR-assistant executes source loading, ICH E3 structure checks, drafting/revision, writer review and report assembly with scripted model responses. AI-scientist executes the actual orchestration using SimulatedBioNeMo, with no retrieved literature and a placeholder target. It folds the binder alone. These are offline software demonstrations, not live inference or clinical/scientific validation.

Continuous Chrome tab MediaRecorder footage is cropped to the software. Recorded interaction coordinates drive an eased cursor and brief terracotta click rings. Idle middles are trimmed while preserving interactions and results; playback is slowed to a readable pace. There are no added captions, end cards or audio. `prototype-video-manifest.json` records source duration, click timelines, edits and output hashes. The replaced MP4s, posters and README GIFs are checksum-verified in `old-videos/2026-10-13-before-workflows/` in the relevant repositories. The older production notes below describe superseded recordings.

---

## SOAP workflow replacement — 12 October 2026

The consult-to-note MP4 now records `consult-to-note/examples/soap_workflow.py`, which runs the actual LangGraph extraction, drafting, grounding, revision and FHIR pipeline. Input transcript and output SOAP note appear side by side. All four SOAP sections, evidence findings and the correction of an 800 mg scripted error to 400 mg are shown. Synthetic input and scripted model responses are explicitly labeled in the app; this is not live model generation. No captions or end cards are added. Recorded click coordinates drive a smooth cursor overlay and click rings; long idle gaps are shortened. `soap-video-manifest.json` records provenance, click timings and the new video hash.

The immediately previous consultation MP4, poster and both repository GIFs are preserved in `old-videos/2026-10-12-before-soap/` with checksums. The other three recordings retain their prior simplified illustration scope and production method below.

---

## Current media format — 10 October 2026

Four clinical MP4s show real interactions with the running offline Streamlit illustration. The footage is recorded continuously, with the middle of long idle gaps removed and playback slowed to make interactions readable. A visible pointer approaches the actual recorded click positions smoothly; a brief terracotta ring marks each click. The cursor is composited from recorded interaction coordinates. No added captions, text overlays, audio or end cards appear. Matching README GIFs use the same footage. `smooth-video-manifest.json` records timing and hashes; `render_smooth.py` documents the rendering process.

Terminal projects use command/output PNGs; see `terminal-media-manifest.json`. The immediately previous videos, posters and repository GIFs are preserved in `old-videos/2026-10-10-before-smooth-cursor/`. Earlier archives remain intact. Archive folders are outside the website's published source tree.

The notes below describe the superseded montage workflow and are retained for history.

---


# Video refresh, 10 October 2026

Eight silent, edited walkthroughs replace the previous clips. Four use screenshots of actual interactions in the corrected Streamlit UI; four show successful output from the current offline tools. These are paced edited sequences, not uninterrupted screen recordings. Every clip establishes an action, an outcome and a limitation. The clinical clips retain an offline/synthetic label throughout.

The previous eight MP4s and eight posters are preserved in `old-videos/2026-10-10/`, with SHA-256 checksums. That archive is outside `src/content/projects`, so the site builder does not publish it. Previous repository GIFs are archived in each repository's `old-videos/2026-10-10/` folder.

`manifest.json` records new media checksums. `make_walkthroughs.py` documents composition and encoding; it expects the original local capture workspace and repository paths. Screenshots and command output are local production inputs, not fabricated interface states. No live NVIDIA API or scientific/clinical validation is implied. The separate interview walkthrough runs the real consult-to-note LangGraph pipeline with scripted models, then evaluates its selected dose using agenteval.
