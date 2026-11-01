const APP_FILE = 'NEET SS Tracker app.html';
const FILE_NAME = 'neet-ss-tracker-progress.json';

// Serves the tracker page. The page itself is the HTML file in your Drive,
// so updating that file updates the app without redeploying.
function doGet() {
  const files = DriveApp.getFilesByName(APP_FILE);
  if (!files.hasNext()) {
    return HtmlService.createHtmlOutput('<p style="font-family:sans-serif;padding:24px">Put the file "' + APP_FILE + '" in your Google Drive, then reload.</p>');
  }
  return HtmlService.createHtmlOutput(files.next().getBlob().getDataAsString())
    .setTitle('NEET SS Highlighter Tracker')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1, viewport-fit=cover');
}

function getFile_() {
  const files = DriveApp.getFilesByName(FILE_NAME);
  return files.hasNext() ? files.next() : null;
}

/** Returns the saved progress JSON, or null if nothing is saved yet. */
function loadProgress() {
  const file = getFile_();
  return file ? file.getBlob().getDataAsString() : null;
}

/** Saves progress JSON to neet-ss-tracker-progress.json in My Drive. */
function saveProgress(json) {
  const lock = LockService.getUserLock();
  lock.waitLock(10000);
  try {
    const file = getFile_();
    if (file) file.setContent(json);
    else DriveApp.createFile(FILE_NAME, json, 'application/json');
    return new Date().toISOString();
  } finally {
    lock.releaseLock();
  }
}
