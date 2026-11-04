acts=open('actions.js').read().replace('if(typeof module!=="undefined") module.exports={neetAct:neetAct,neetHex:neetHex,neetUnhex:neetUnhex};','')
notif=open('notify.js').read().replace('if(typeof module!=="undefined") module.exports=neetNotify;','')
core=open('core.js').read().replace('if(typeof module!=="undefined") module.exports=neetCore;','')
render=open('render.js').read().replace('if(typeof module!=="undefined") module.exports=neetRender;','')
URL="https://script.google.com/macros/s/AKfycbxJugNolxK03kTtyN_tRkYQI930QMcjd7_j5J-XZI60MQIElikv_n8H-pxbq3_FRC5M/exec"
main='''
ObjC.import('Foundation');
function readText(p){ try{ var s=$.NSString.stringWithContentsOfFileEncodingError(p,$.NSUTF8StringEncoding,null); var u=ObjC.unwrap(s); return (typeof u==="string")?u:null; }catch(e){ return null; } }
function writeText(p,txt){ try{ return !!$.NSString.alloc.initWithUTF8String(txt).writeToFileAtomicallyEncodingError(p,false,$.NSUTF8StringEncoding,null); }catch(e){ return false; } }
function listDir(p){ try{ return ObjC.deepUnwrap($.NSFileManager.defaultManager.contentsOfDirectoryAtPathError(p,null))||[]; }catch(e){ return []; } }
function findFile(){
  var home=ObjC.unwrap($.NSHomeDirectory()), cs=home+"/Library/CloudStorage", F="neet-ss-tracker-progress.json", cands=[];
  listDir(cs).filter(function(n){ return n.indexOf("GoogleDrive")===0; }).sort(function(a,b){ return (b.indexOf("sadananth")>=0)-(a.indexOf("sadananth")>=0); })
    .forEach(function(n){ cands.push(cs+"/"+n+"/My Drive/"+F); listDir(cs+"/"+n).forEach(function(m){ if(m!=="My Drive") cands.push(cs+"/"+n+"/"+m+"/"+F); }); });
  cands.push(home+"/Google Drive/My Drive/"+F);
  for(var i=0;i<cands.length;i++){ var t=readText(cands[i]); if(t) return {path:cands[i],txt:t}; }
  return null;
}
function statePath(){ return ObjC.unwrap($.NSHomeDirectory())+"/Library/Caches/neetss-notify.json"; }
function loadState(){ try{ _stTxt=readText(statePath())||"{}"; return JSON.parse(_stTxt); }catch(e){ return {}; } }
var _stTxt=null;
function saveState(s){ var j=JSON.stringify(s); if(j!==_stTxt){ writeText(statePath(),j); _stTxt=j; } }
function notify(msgs){ if(!msgs.length) return; try{ var app=Application.currentApplication(); app.includeStandardAdditions=true;
  msgs.forEach(function(m){ app.displayNotification(m.body,{withTitle:"NEET SS",subtitle:m.title,soundName:"Glass"}); }); }catch(e){} }
function run(argv){
  var self=argv[0]||"", info={url:"%s",self:self}, f=findFile();
  if(argv[1]==="act" && argv[2]==="notif"){ var s0=loadState(); s0.off=!s0.off; saveState(s0); return ""; }
  if(argv[1]==="act"){
    if(!f) return "";
    var D; try{ D=JSON.parse(f.txt); }catch(e){ return ""; }
    var arg=argv[3]&&argv[3]!=="x"?neetUnhex(argv[3]):null;
    if(argv[2]==="own"){ try{ var app=Application.currentApplication(); app.includeStandardAdditions=true; app.activate();
      var r=app.displayDialog("What are you studying?",{defaultAnswer:"Harrison: ",buttons:["Cancel","Start"],defaultButton:"Start",cancelButton:"Cancel",withTitle:"NEET SS · Own study"}); arg=r.textReturned; }catch(e){ return ""; } }
    if(neetAct(D,argv[2],arg,Date.now())) writeText(f.path,JSON.stringify(D));
    return "";
  }
  if(!f){ info.err="Couldn't find neet-ss-tracker-progress.json in Google Drive. Is Google Drive for desktop running and signed in as dr.sadananth@gmail.com?"; return neetRender(null,info); }
  var D2; try{ D2=JSON.parse(f.txt); }catch(e){ info.err="The progress file is being synced. Try again in a moment."; return neetRender(null,info); }
  try{ var c=neetCore(D2,Date.now()), st=loadState(); info.notifOff=!!st.off;
    try{ var nres=neetNotify(c,Date.now(),st); notify(nres.msgs); saveState(nres.state); }catch(e){}
    return neetRender(c,info); }catch(e){ info.err="Error: "+e; return neetRender(null,info); }
}
''' % URL
sh='''#!/bin/bash
# <xbar.title>NEET SS study timer</xbar.title>
# <xbar.desc>Live studied / awake / break time from the NEET SS tracker (reads the progress file Google Drive syncs to this Mac).</xbar.desc>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
/usr/bin/osascript -l JavaScript - "$0" "$@" <<'JXA'
'''+acts+'\n'+notif+'\n'+core+'\n'+render+'\n'+main+'''JXA
'''
open('neetss.1s.sh','w').write(sh)
# node-testable copy: replace ObjC bits with a stub to check the whole script parses
test=acts+'\n'+notif+'\n'+core+'\n'+render+'\n'+main.replace("ObjC.import('Foundation');","")
open('../tests/plugin_body.js','w').write(test)
print(len(sh))
