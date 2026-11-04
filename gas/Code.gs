// One Apps Script project serves all the trackers:
//   .../exec              -> NEET SS tracker           (NEET SS Tracker app.html     + neet-ss-tracker-progress.json)
//   .../exec?app=cardio   -> DM Cardiology tracker     (DM Cardiology Tracker app.html + dm-cardio-progress.json)
//   .../exec?app=mge      -> DM Gastroenterology       (DM MGE Tracker app.html        + dm-mge-progress.json)
//   .../exec?app=dm       -> a page with links to the two DM trackers (the old combined tracker's address)
// Each page is an HTML file in your Drive, so updating that file updates the app without redeploying.
const EXEC = 'https://script.google.com/macros/s/AKfycbxJugNolxK03kTtyN_tRkYQI930QMcjd7_j5J-XZI60MQIElikv_n8H-pxbq3_FRC5M/exec';
const APPS = {
  neet:   { html: 'NEET SS Tracker app.html', data: 'neet-ss-tracker-progress.json', title: 'NEET SS Highlighter Tracker' },
  cardio: { html: 'DM Cardiology Tracker app.html', data: 'dm-cardio-progress.json', title: 'DM Cardiology Tracker' },
  mge:    { html: 'DM MGE Tracker app.html', data: 'dm-mge-progress.json', title: 'DM Gastroenterology Tracker' }
};

function doGet(e) {
  const key = (e && e.parameter && e.parameter.app) || 'neet';
  if (key === 'dm') {
    return HtmlService.createHtmlOutput('<div style="font-family:sans-serif;padding:24px;font-size:18px;line-height:2">' +
      '<b>Residency trackers</b><br><a target="_top" href="' + EXEC + '?app=cardio">DM Cardiology tracker</a><br>' +
      '<a target="_top" href="' + EXEC + '?app=mge">DM Gastroenterology tracker</a></div>')
      .setTitle('Residency trackers').addMetaTag('viewport', 'width=device-width, initial-scale=1');
  }
  const app = APPS[key] || APPS.neet;
  const files = DriveApp.getFilesByName(app.html);
  if (!files.hasNext()) {
    return HtmlService.createHtmlOutput('<p style="font-family:sans-serif;padding:24px">Put the file "' + app.html + '" in your Google Drive, then reload.</p>');
  }
  return HtmlService.createHtmlOutput(files.next().getBlob().getDataAsString())
    .setTitle(app.title)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1, viewport-fit=cover');
}

function load_(name) { const f = DriveApp.getFilesByName(name); return f.hasNext() ? f.next().getBlob().getDataAsString() : null; }
function save_(name, json) {
  const lock = LockService.getUserLock();
  lock.waitLock(10000);
  try {
    const f = DriveApp.getFilesByName(name);
    if (f.hasNext()) f.next().setContent(json);
    else DriveApp.createFile(name, json, 'application/json');
    return new Date().toISOString();
  } finally { lock.releaseLock(); }
}

/** NEET SS tracker */
function loadProgress() { return load_(APPS.neet.data); }
function saveProgress(json) { return save_(APPS.neet.data, json); }
/** DM Cardiology tracker */
function loadCardio() { return load_(APPS.cardio.data); }
function saveCardio(json) { return save_(APPS.cardio.data, json); }
/** DM Gastroenterology tracker */
function loadMge() { return load_(APPS.mge.data); }
function saveMge(json) { return save_(APPS.mge.data, json); }
/** Old combined DM tracker (kept so an old open tab can still save) */
function loadDm() { return load_('dm-residency-progress.json'); }
function saveDm(json) { return save_('dm-residency-progress.json', json); }
