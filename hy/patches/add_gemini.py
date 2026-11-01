p='tracker.tpl.html'; t=open(p).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:90],t.count(a)); t=t.replace(a,b)
rep(".co-ai{display:grid;gap:8px}", """.co-ai{display:grid;gap:8px}
.co-gem-txt summary{cursor:pointer;color:var(--accent);font-weight:700;font-size:13px}
.co-gem-txt textarea{width:100%;margin-top:6px;font-family:var(--f-mono);font-size:12px;line-height:1.45;color:var(--ink);background:var(--surface-2);border:1.5px solid var(--line);border-radius:10px;padding:8px 10px;resize:vertical}
a.btn{display:inline-block;text-decoration:none;color:var(--ink)}""")
rep('''function aiBlock(){ return SAMPLE?`<div class="co-ai"><div><button class="btn co-ai-btn">Ask Claude for a deeper review</button></div><div class="co-ai-out" hidden></div></div>`:""; }''',
'''const IS_GAS = typeof google!=="undefined" && !!(google.script && google.script.run);
function aiBlock(){
  if(SAMPLE) return `<div class="co-ai"><div><button class="btn co-ai-btn">Ask Claude for a deeper review</button></div><div class="co-ai-out" hidden></div></div>`;
  if(IS_GAS) return `<div class="co-ai"><div><a class="btn co-gem" href="https://gemini.google.com/app" target="_blank" rel="noopener">Send to Gemini for a deeper review</a></div><p class="note co-gem-note" hidden></p><details class="co-gem-txt"><summary>Show the text that gets copied</summary><textarea readonly rows="8" aria-label="Tracker summary for Gemini"></textarea></details></div>`;
  return "";
}
function reviewPrompt(){ return `You are a concise, practical study coach for a doctor preparing for NEET-SS (Medical group, India). Using ONLY the data below from their study tracker, give an honest assessment in 2 sentences, then 5 numbered, specific actions for the rest of today and this week (each under 30 words). Mention module names and times where useful. No preamble.\\n\\nDATA (from my NEET SS tracker)\\n${aiSummary()}`; }
function copyText(txt){
  let ok=false;
  try{ const ta=document.createElement("textarea"); ta.value=txt; ta.setAttribute("readonly",""); ta.style.cssText="position:fixed;top:-1000px;left:0;opacity:0"; document.body.appendChild(ta); ta.focus(); ta.select(); ok=document.execCommand("copy"); ta.remove(); }catch(e){ ok=false; }
  if(!ok && navigator.clipboard){ return navigator.clipboard.writeText(txt).then(()=>true,()=>false); }
  return Promise.resolve(ok);
}''')
rep('''function bindAI(root){
  if(!root||!SAMPLE) return;''','''function bindAI(root){
  if(!root) return;
  const gem=root.querySelector(".co-gem");
  if(gem){
    const note=root.querySelector(".co-gem-note"), det=root.querySelector(".co-gem-txt"), ta=det&&det.querySelector("textarea");
    if(det) det.addEventListener("toggle",()=>{ if(det.open&&ta){ ta.value=reviewPrompt(); ta.focus(); ta.select(); } });
    gem.onclick=()=>{ const txt=reviewPrompt(); if(ta) ta.value=txt;
      copyText(txt).then(ok=>{ note.hidden=false;
        note.textContent = ok ? "Copied your tracker summary. In the Gemini tab, paste it into the message box (long-press → Paste on a phone, Ctrl/⌘+V on a computer) and send." : "Couldn't copy automatically. Open \\"Show the text that gets copied\\" below, select all, copy it, then paste it in Gemini.";
        if(!ok && det){ det.open=true; if(ta){ ta.focus(); ta.select(); } } }); };
  }
  if(!SAMPLE) return;''')
open(p,'w').write(t); print('template ok')
