## Current media format — 10 October 2026

Four clinical MP4s show real interactions with the running offline Streamlit illustration. The footage is recorded continuously, with the middle of long idle gaps removed and playback slowed to make interactions readable. A visible pointer approaches the actual recorded click positions smoothly; a brief terracotta ring marks each click. The cursor is composited from recorded interaction coordinates. No added captions, text overlays, audio or end cards appear. Matching README GIFs use the same footage. `smooth-video-manifest.json` records timing and hashes; `render_smooth.py` documents the rendering process.

Terminal projects use command/output PNGs; see `terminal-media-manifest.json`. The immediately previous videos, posters and repository GIFs are preserved in `old-videos/2026-10-10-before-smooth-cursor/`. Earlier archives remain intact. Archive folders are outside the website's published source tree.

The notes below describe the superseded montage workflow and are retained for history.

---


# Video refresh, 10 October 2026

Eight silent, edited walkthroughs replace the previous clips. Four use screenshots of actual interactions in the corrected Streamlit UI; four show successful output from the current offline tools. These are paced edited sequences, not uninterrupted screen recordings. Every clip establishes an action, an outcome and a limitation. The clinical clips retain an offline/synthetic label throughout.

The previous eight MP4s and eight posters are preserved in `old-videos/2026-10-10/`, with SHA-256 checksums. That archive is outside `src/content/projects`, so the site builder does not publish it. Previous repository GIFs are archived in each repository's `old-videos/2026-10-10/` folder.

`manifest.json` records new media checksums. `make_walkthroughs.py` documents composition and encoding; it expects the original local capture workspace and repository paths. Screenshots and command output are local production inputs, not fabricated interface states. No live NVIDIA API or scientific/clinical validation is implied. The separate interview walkthrough runs the real consult-to-note LangGraph pipeline with scripted models, then evaluates its selected dose using agenteval.
