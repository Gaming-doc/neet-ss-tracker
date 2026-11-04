# NEET SS Highlighter Tracker

A personal study tracker for NEET-SS 2026 (Medical group, exam 11 Dec 2026), built around DocTutorials QBanks and Marrow General Medicine.

It is one HTML page that runs in two places:

| Version | Where it runs | How progress is saved |
|---|---|---|
| `dist/NEET SS Tracker app.html` | Google Apps Script web app (`gas/Code.gs` serves this file from Google Drive) | `neet-ss-tracker-progress.json` in My Drive |
| `dist/neet-ss-tracker.html` | Claude artifact | Claude artifact database (`progress/state`) |

A macOS menu bar timer (`mac/`) reads the same Drive progress file and shows live studied / awake time.

## What the tracker does

- **Plan**: 28-day Phase 1 + 14-day Phase 2 revision, Main Harrison capped at 200 Qs/day, tough topics in the morning, ordered by Medical-group PYQ yield (Most asked / Asked / Light pass). Critical Care, Pulmonology and Oncology papers are de-emphasised.
- **Marrow**: 1,998 must-complete General Medicine Qs, about 1 h a day at 20:00.
- **Per module**: tick done, planned start–end times (a start time on a Main module auto-plans Blocks A–C at 30 min per 10 Qs; each end time becomes the next start), Start / Pause / Resume / End now (End now also ticks it), unlimited pauses with a log, accuracy, Move to… (carry forward), and a Break menu.
- **Breaks**: named breaks (Lunch, Dinner, Series, Short nap, Other) with guide lengths; all awake time not spent studying counts as a break. A pause spent studying another module counts as study.
- **Sleep and the day boundary**: "I'm up now" / "Going to sleep". The study day starts when you wake up (or 06:00 if not logged), so late nights still count toward the previous day.
- **Coach**: rule-based assessment and suggestions after every tap (pace, finish time vs 23:00 lights-out, what to move, break/sleep advice), a coach report in Stats, and a summary you can send to Gemini (Google version) or Claude (artifact version).
- **Stats**: Mock/PYQ score chart, accuracy by system, study hours, sleep and breaks, named breaks over 14 days.

## Layout

```
tracker.tpl.html      master template (all UI + logic); edit this
build.py              builds both versions into dist/ from the template + marrow/schedule4.json
dist/                 built pages (upload "NEET SS Tracker app.html" to Google Drive to update the web app)
gas/                  Apps Script project (Code.gs, appsscript.json)
mac/                  SwiftBar menu bar plugin: core.js (same day/break rules), render.js, build.py -> neetss.1s.sh
hy/                   PYQ yield pipeline (yieldmap.py, hybuild.py, tiers.py, gen2.py) and hy.json
hy/patches/           the one-off scripts that added each feature to the template, in order (history)
marrow/               Marrow module list and scheduler (mplan.py, merge.py, addsys.py -> schedule4.json)
pyq/map.xlsx          PYQ topic map used for yield tiers
tests/                Playwright tests (scenario, monkey/click-everything, menu-bar vs tracker comparison)
legacy/               first versions of the schedule generator
```

## Build

```
python3 build.py              # -> dist/neet-ss-tracker.html and dist/NEET SS Tracker app.html
cd mac && python3 build.py    # -> mac/neetss.1s.sh
```

Updating the Google web app: replace `NEET SS Tracker app.html` in My Drive with the new `dist/` file. No redeploy is needed because `Code.gs` reads the file on every load.

**Apps Script gotcha:** Google strips anything after `//` on a line of inline script (it treats it as a comment), even inside strings. Never write `https://` inside the page's JavaScript; use `https:\/\/`. `tests/h.js` simulates this.

## Mac menu bar timer

1. Install [SwiftBar](https://swiftbar.app).
2. Put `mac/neetss.1s.sh` in the SwiftBar plugin folder and make it executable (`chmod +x`).
3. Google Drive for desktop must be running and signed in; the plugin reads `~/Library/CloudStorage/GoogleDrive-*/My Drive/neet-ss-tracker-progress.json` every second.

## Tests

Needs Node, Playwright and Chromium.

```
cd tests
node -e "require('./h.js').gasSim('../dist/NEET SS Tracker app.html','sim2.html')"
cp '../dist/neet-ss-tracker.html' claude2.html
node scen.js sim2.html claude2.html     # 48 scenario checks
node monkey.js                          # clicks every control on every tab, checks errors and phone overflow
node cmp.js                             # menu-bar numbers vs tracker numbers
```

`tests/fixture-progress.json` is a snapshot of real progress used as test data.

## Since the first upload

- **Mac menu bar** (`mac/`): live studied / awake / break time with Pause, Resume, Break, End, own study, sleep and wake buttons, a study-ratio line (red < 50%, orange 50–75%, green ≥ 75%) with the time needed to reach the next level, and notifications (break over its guide, 90 min straight, 20 min idle, ratio milestones). `mac/build.py` builds `neetss.1s.sh` for SwiftBar.
- **iPhone widget** (`widget/`): a Scriptable widget fed by a small Apps Script feed. The feed's source lives in the private residency repo (`gas/feed.src.gs`); its key and URL are never committed (`widget/feed_url.txt` is gitignored).
- **Own study** (e.g. a Harrison chapter) counts as study.
- **Carried-over modules**: each stretch of study counts on the day it happened. A module paused overnight and resumed today counts today's part today, on the page, in the menu bar and in the widget.
- `gas/Code.gs` is the deployed web app. It also serves the DM residency trackers (`?app=cardio`, `?app=mge`).
- Tests: `bash tests/run_all.sh`.
