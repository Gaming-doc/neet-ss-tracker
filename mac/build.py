core=open('core.js').read().replace('if(typeof module!=="undefined") module.exports=neetCore;','')
render=open('render.js').read().replace('if(typeof module!=="undefined") module.exports=neetRender;','')
import os
# Your web-app link: set NEET_TRACKER_URL, or put it in mac/tracker_url.txt (not committed).
URL=os.environ.get("NEET_TRACKER_URL") or (open("tracker_url.txt").read().strip() if os.path.exists("tracker_url.txt") else "https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec")
main='''
ObjC.import('Foundation');
function readText(p){ try{ var s=$.NSString.stringWithContentsOfFileEncodingError(p,$.NSUTF8StringEncoding,null); var u=ObjC.unwrap(s); return (typeof u==="string")?u:null; }catch(e){ return null; } }
function listDir(p){ try{ return ObjC.deepUnwrap($.NSFileManager.defaultManager.contentsOfDirectoryAtPathError(p,null))||[]; }catch(e){ return []; } }
function main(){
  var home=ObjC.unwrap($.NSHomeDirectory()), cs=home+"/Library/CloudStorage", F="neet-ss-tracker-progress.json", cands=[];
  listDir(cs).filter(function(n){ return n.indexOf("GoogleDrive")===0; })
    .forEach(function(n){ cands.push(cs+"/"+n+"/My Drive/"+F); listDir(cs+"/"+n).forEach(function(m){ if(m!=="My Drive") cands.push(cs+"/"+n+"/"+m+"/"+F); }); });
  cands.push(home+"/Google Drive/My Drive/"+F);
  var txt=null; for(var i=0;i<cands.length&&!txt;i++) txt=readText(cands[i]);
  var info={url:"%s"};
  if(!txt){ info.err="Couldn't find "+F+" in Google Drive. Is Google Drive for desktop running and signed in to the Google account that owns the tracker?"; return neetRender(null,info); }
  var D; try{ D=JSON.parse(txt); }catch(e){ info.err="The progress file is being synced. Try again in a moment."; return neetRender(null,info); }
  try{ return neetRender(neetCore(D,Date.now()),info); }catch(e){ info.err="Error: "+e; return neetRender(null,info); }
}
main();
''' % URL
sh='''#!/bin/bash
# <xbar.title>NEET SS study timer</xbar.title>
# <xbar.desc>Live studied / awake / break time from the NEET SS tracker (reads the progress file Google Drive syncs to this Mac).</xbar.desc>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
/usr/bin/osascript -l JavaScript <<'JXA'
'''+core+'\n'+render+'\n'+main+'''JXA
'''
open('neetss.1s.sh','w').write(sh)
# node-testable copy: replace ObjC bits with a stub to check the whole script parses
test=core+'\n'+render+'\n'+main.replace("ObjC.import('Foundation');","")
open('../tests/plugin_body.js','w').write(test) if os.path.isdir('../tests') else None
print(len(sh))
