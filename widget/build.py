import sys
core=open('../mac/core.js').read().replace('if(typeof module!=="undefined") module.exports=neetCore;','')
feed=open('feed_url.txt').read().strip() if __import__('os').path.exists('feed_url.txt') else "PASTE_FEED_URL_HERE"
src=open('widget.src.js').read().replace('__CORE__',core).replace('__FEED__',feed).replace('__TRACKER__','https://script.google.com/macros/s/AKfycbxJugNolxK03kTtyN_tRkYQI930QMcjd7_j5J-XZI60MQIElikv_n8H-pxbq3_FRC5M/exec')
open('NEET SS.js','w').write(src); print(len(src))
