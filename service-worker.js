'use strict';
// Cache version 4: invalidates old page after the full-reset and quiz-first update.
const NAME='itquiz-cntt-v4';
const SHELL=['./','./index.html','./manifest.webmanifest','./icon.svg','./icon-192.png','./icon-512.png'];
self.addEventListener('install',event=>{
  event.waitUntil(caches.open(NAME).then(cache=>cache.addAll(SHELL)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',event=>{
  event.waitUntil(caches.keys()
    .then(keys=>Promise.all(keys.filter(k=>k.startsWith('itquiz-cntt-')&&k!==NAME).map(k=>caches.delete(k))))
    .then(()=>self.clients.claim()));
});
self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;
  const url=new URL(event.request.url);
  if(url.origin!==self.location.origin || url.pathname.endsWith('.pdf'))return;
  if(event.request.mode==='navigate'){
    // On repeat visits, get the newly deployed code first instead of serving a stale quiz.
    event.respondWith(fetch(event.request).then(response=>{
      if(response.ok){const copy=response.clone();caches.open(NAME).then(cache=>cache.put('./index.html',copy)).catch(()=>{});}
      return response;
    }).catch(()=>caches.match('./index.html')));
    return;
  }
  event.respondWith(caches.match(event.request).then(hit=>hit||fetch(event.request).then(response=>{
    if(response.ok&&response.type==='basic'){
      const copy=response.clone();caches.open(NAME).then(cache=>cache.put(event.request,copy)).catch(()=>{});
    }
    return response;
  }).catch(()=>Response.error())));
});
