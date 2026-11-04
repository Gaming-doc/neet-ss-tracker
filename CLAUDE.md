# NEET SS Highlighter Tracker — notes for Claude Code

A personal NEET-SS 2026 study tracker (exam 11 Dec 2026), built around DocTutorials QBanks and Marrow. README.md has the feature list.

- **Edit `tracker.tpl.html`**, then run `python3 build.py`. That builds `dist/neet-ss-tracker.html` (Claude artifact) and `dist/NEET SS Tracker app.html` (Apps Script page). Never edit `dist/` by hand.
- **Google web app.**
  - The deployed project "NEET SS Tracker" serves `NEET SS Tracker app.html` from the root of My Drive. To update, upload with "Replace existing file"; no redeploy is needed.
  - Progress is saved in `neet-ss-tracker-progress.json`.
  - `gas/Code.gs` also serves the DM residency trackers, so keep `loadCardio/saveCardio/loadMge/saveMge` intact.
- **Claude artifact**: claude.ai/artifact/EVo1W8JU2b69P7D4Yt6ddf (artifact database doc `progress/state`).
- **Mac menu bar.**
  - Sources: `mac/core.js` (neetCore), `actions.js`, `notify.js`, `render.js`.
  - `cd mac && python3 build.py` builds `neetss.1s.sh` for `~/SwiftBar/`.
  - The same `neetCore` is copied into the phone feed (`gas/feed.src.gs` in the private repo Gaming-doc/dm-residency-tracker). Keep the copies in step.
- **Apps Script cuts any inline-script line at `//`**, even inside strings. Write `https:\/\/`. The tests simulate this.
- **Day rules (IST).**
  - The study day starts at wake-up, or 06:00 if no wake time is logged.
  - Each stretch of study counts on the day it happened: `dayWin` / `activeIntervals` in the template, and the `W0` clip in `mac/core.js`.
- **Tests**: `bash tests/run_all.sh`. Expect scenario 48 pass / 0 fail, cmp "all match", carry 19/0, own 0 failures, mb 8 clicks.
