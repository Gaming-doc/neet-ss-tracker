#!/bin/bash
# Builds, prepares the test pages, then runs every NEET SS test. Needs Node and Playwright with Chromium.
set -e
cd "$(dirname "$0")/.."
python3 build.py
(cd mac && python3 build.py)          # also writes tests/plugin_body.js for mb.js
cd tests
# Apps Script cuts every inline-script line at "//": the sim pages simulate that.
node -e "const {gasSim}=require('./h.js'); const s=gasSim('../dist/NEET SS Tracker app.html','sim.html'); ['sim2.html','sim4.html'].forEach(f=>require('fs').copyFileSync('sim.html',f)); require('fs').copyFileSync('../dist/neet-ss-tracker.html','claude.html'); if(s.length){ console.log('lines Apps Script would cut:',s); process.exit(1); }"
node scen.js sim.html claude.html > scen.out; echo "scenario: $(grep -c ^PASS scen.out) pass, $(grep -c ^FAIL scen.out || true) fail"   # expect 48 pass, 0 fail
node cmp.js      # tracker page and menu bar core agree on studied / awake / breaks
node carry.js    # a module paused overnight and resumed today counts today's part today
node cont.js     # an ended module can be continued
node own.js | tail -1    # own study (e.g. a Harrison chapter)
node mb.js > mb.out && grep -c clicked mb.out    # menu bar clicks: pause, resume, lunch, end, sleep, wake
