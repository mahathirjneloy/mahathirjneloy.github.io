(function(){
function $(i){return document.getElementById(i)}
function all(q){return Array.prototype.slice.call(document.querySelectorAll(q))}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}

/* marks to grade */
var m=$('marks');
if(m){var rows=all('#gt tbody tr'),res=$('res');
 var show=function(){rows.forEach(function(r){r.className=''});var v=m.value.trim();
  if(v===''){res.textContent='Your grade shows here.';return}
  var n=+v;if(!(n>=0&&n<=100)){res.textContent='Type a number from 0 to 100.';return}
  var i=0;while(n<+rows[i].getAttribute('data-min'))i++;var r=rows[i];r.className='hit';
  var t=n+' marks = '+r.cells[1].textContent+' ('+r.cells[2].textContent+' points).';
  if(i>0){var u=rows[i-1],d=Math.ceil(+u.getAttribute('data-min')-n);t+=' '+d+' more mark'+(d>1?'s':'')+' for '+u.cells[1].textContent+'.'}else t+=' Top grade.';
  res.textContent=t};
 m.addEventListener('input',show);show()}

/* open a question from the link */
function openHash(){var id=location.hash.slice(1),t=id&&$(id);if(t&&t.tagName==='DETAILS'){t.open=true;t.scrollIntoView()}}
addEventListener('hashchange',openHash);openHash();

/* rule search */
var f=$('find');
if(f){var rules=all('.rule'),grps=all('.rgrp'),cnt=$('count');
 var words=function(n){var o=[],w=document.createTreeWalker(n,NodeFilter.SHOW_TEXT),x;while(x=w.nextNode())o.push(x.nodeValue);return o.join(' ')};
 rules.forEach(function(r){r._t=' '+words(r).toLowerCase()});
 var run=function(){var s=f.value.trim().toLowerCase(),n=0,re=new RegExp('[^a-z0-9]'+s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));
  rules.forEach(function(r){var ok=!s||re.test(r._t);r.hidden=!ok;if(ok)n++});
  grps.forEach(function(g){g.hidden=!g.querySelector('.rule:not([hidden])')});
  $('none').hidden=n>0;cnt.textContent=s?n+' rule'+(n===1?'':'s')+' found':rules.length+' rules'};
 f.addEventListener('input',run);
 all('[data-q]').forEach(function(b){b.addEventListener('click',function(){f.value=b.getAttribute('data-q');run();f.scrollIntoView({block:'start'})})});
 var h;try{h=decodeURIComponent(location.hash)}catch(e){h=''}if(h.indexOf('#q=')===0){f.value=h.slice(3);setTimeout(function(){f.scrollIntoView({block:'start'})},50)}
 run()}

/* routines and notices */
var list=$('list');
if(list){var M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
 var D=(window.UPDATES||[]).slice().sort(function(a,b){var x=a.d||'',y=b.d||'';return x<y?1:x>y?-1:0});
 var ok=function(v){return v&&/^(https?:|[^:]*$)/i.test(v)?v:''};
 var go=function(u,t){var a=el('a','',t);a.href=u;a.target='_blank';a.rel='noopener noreferrer';return a};
 D.forEach(function(x){var u=ok(x.u),i=ok(x.i),two=u&&i,r=el(u&&!two?'a':'div','file');
  if(u&&!two){r.href=u;r.target='_blank';r.rel='noopener noreferrer'}
  var l=el('span'),p=String(x.d||'').split('-');l.appendChild(el('b','',x.t||''));l.appendChild(el('small','',p.length===3&&M[p[1]-1]?(+p[2])+' '+M[p[1]-1]+' '+p[0]:''));r.appendChild(l);
  if(two){var g=el('span','links');g.appendChild(go(u,'Page 1'));g.appendChild(go(i,'Page 2'));r.appendChild(g)}
  else if(u)r.appendChild(el('em','','Open \u2192'));list.appendChild(r)});
 $('empty').hidden=D.length>0}
})();

/* nsu-theme-toggle */
(function(){
var K='nsu-theme',d=document.documentElement,bar=document.querySelector('.topline');if(!bar)return;
var ic='<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">';
var moon=ic+'<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
var sun=ic+'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
function saved(){try{return localStorage.getItem(K)==='dark'?'dark':'light'}catch(e){return 'light'}}
function store(t){try{localStorage.setItem(K,t)}catch(e){}}
var b=document.createElement('button');b.type='button';b.className='tbtn';b.id='themebtn';
b.innerHTML='<span class="ti"></span><span class="tl"></span>';
var g=document.createElement('div');g.className='tright';
var nav=bar.querySelector('.pages');if(nav){bar.insertBefore(g,nav);g.appendChild(nav)}else bar.appendChild(g);
g.appendChild(b);
function paint(t){d.setAttribute('data-theme',t);var dark=t==='dark';
 b.setAttribute('aria-pressed',dark?'true':'false');
 b.querySelector('.ti').innerHTML=dark?sun:moon;
 b.querySelector('.tl').textContent=dark?'Light mode':'Dark mode'}
b.addEventListener('click',function(){var t=d.getAttribute('data-theme')==='dark'?'light':'dark';store(t);paint(t)});
paint(saved());
})();
