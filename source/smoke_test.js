// Tiny DOM stand-in for functional smoke tests in an environment where browser navigation is admin-blocked.
const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const data=JSON.parse(html.match(/<script id="quiz-json" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const js=html.match(/<script>\s*([\s\S]*?)\s*<\/script>/)[1];
const store={};
const sessionStore={};
function makeStorage(data){return {get length(){return Object.keys(data).length},key(i){return Object.keys(data)[i]||null},getItem(k){return Object.prototype.hasOwnProperty.call(data,k)?data[k]:null},setItem(k,v){data[k]=String(v)},removeItem(k){delete data[k]},clear(){for(const k of Object.keys(data))delete data[k]}}}
const localStorage=makeStorage(store), sessionStorage=makeStorage(sessionStore);
function runApp(){
 class Element{
  constructor(tag='div'){this.tagName=tag.toUpperCase();this.children=[];this.listeners={};this.className='';this.disabled=false;this.innerHTML='';this._text='';this.value='all';this.style={};this.classList={add:(...cs)=>{for(const c of cs)if(!this.className.split(' ').includes(c))this.className+=(this.className?' ':'')+c},remove:(c)=>{this.className=this.className.split(' ').filter(v=>v!==c).join(' ')},toggle:(c,force)=>{this.classList[force?'add':'remove'](c)}}}
  set textContent(v){this._text=String(v)}get textContent(){return this._text}
  replaceChildren(...v){this.children=v}
  appendChild(el){this.children.push(el)}append(...els){this.children.push(...els)}
  setAttribute(k,v){this[k]=v}addEventListener(k,cb){this.listeners[k]=cb}
  click(){if(this.disabled)return;this.listeners.click?.()}
  add(option){this.children.push(option)}
  scrollIntoView(){}
 }
 const all={};const el=id=>all[id]??(all[id]=new Element());
 el('quiz-json').textContent=JSON.stringify(data);
 const document={getElementById:el,createElement:t=>new Element(t),addEventListener(){},activeElement:{tagName:'BODY'}};
 class Option {constructor(text,value){this.text=text;this.value=value}}
 const ctx={document,window:{innerWidth:1440,scrollTo(){},addEventListener(){},localStorage,sessionStorage},navigator:{},location:{protocol:'file:'},localStorage,sessionStorage,console,Option,confirm:()=>true,setTimeout:(cb)=>cb(),clearTimeout:()=>{}};
 vm.createContext(ctx);vm.runInContext(js,ctx,{timeout:2500});return {all,el,ctx}
}
function test(){let app=runApp(),el=app.el;
 const assert=(ok,m)=>{if(!ok)throw new Error(m)};
 localStorage.setItem('external-app-key','KEEP_ME');
 localStorage.setItem('itquiz_47_lessons_600_v2','OLD_PROGRESS');
 sessionStorage.setItem('itquiz_47_lessons_600_v1','OLDER_PROGRESS');
 assert(el('session-list').children.length===10,'sessions not loaded');
 assert(el('number-grid').children.length===60,'palette not loaded');
 assert(el('check').disabled===true,'check should be disabled at start');
 assert(el('question-text').textContent.length>15,'missing question');
 el('options').children[0].click();assert(el('check').disabled===false,'answer selection did not unlock completion');
 el('check').click();assert(el('explanation').innerHTML.includes('Đáp án đúng:'),'missing detailed feedback');
 assert(el('done-count').textContent==='1/60','session grade did not update');
 el('next').click();assert(JSON.parse(localStorage.getItem('itquiz_47_lessons_600_v3')).current==='02-002','next failed');
 app=runApp();el=app.el;
 assert(el('done-count').textContent==='1/60','persist failed');
 el('session-list').children[6].click();assert(el('session-eyebrow').textContent==='SESSION 15 / 10','session switching failed');
 assert(el('number-grid').children.length===60,'wrong question count Session15');
 el('lesson-select').listeners.change({target:{value:'2'}});assert(el('number-grid').children.length===20,'lesson filter failed');
 // Select but do not submit an answer in another session, then reset everything.
 el('options').children[1].click();
 assert(Object.keys(JSON.parse(localStorage.getItem('itquiz_47_lessons_600_v3')).picks).length>=2,'missing ungraded selection');
 el('reset-all').click();assert(el('done-count').textContent==='0/60','reset failed');
 assert(el('session-eyebrow').textContent==='SESSION 02 / 10','reset did not return to first session');
 assert(el('all-progress').textContent==='0/600 câu đã làm','all-session counter not reset');
 assert(el('correct-count').textContent==='0','correct-count not reset');
 assert(el('accuracy').textContent==='—','accuracy not reset');
 assert(el('progress-percent').textContent==='0%','progress bar not reset');
 assert(!el('explanation').className.includes('good')&&!el('explanation').className.includes('bad'),'explanation not reset');
 assert(el('number-grid').children.length===60,'lesson filter not reset');
 assert(el('check').disabled===true,'answer not reset');
 assert(localStorage.getItem('itquiz_47_lessons_600_v3')===null,'saved progress not deleted');
 assert(localStorage.getItem('itquiz_47_lessons_600_v2')===null,'old progress not deleted');
 assert(sessionStorage.getItem('itquiz_47_lessons_600_v1')===null,'session progress not deleted');
 assert(localStorage.getItem('external-app-key')==='KEEP_ME','unrelated storage deleted');
 app=runApp();el=app.el;
 assert(el('all-progress').textContent==='0/600 câu đã làm','progress reappeared after relaunch');
 assert(el('check').disabled,'old answer reappeared after relaunch');
 for(let i=0;i<10;i++){el('session-list').children[i].click();assert(el('done-count').textContent==='0/60','session '+i+' still has progress')}
 assert(el('question-text').textContent.length>15,'question missing after reset');
 console.log('SMOKE TEST SUCCESS: 600 questions, 10 sessions, select, grade, explanation, navigate, persistent state, lesson filter, reset.');
}
console.log('Question bank',data.questions.length,'per session:',Object.fromEntries(Object.keys(data.sessions).map(s=>[s,data.questions.filter(q=>q.session===s).length])));
test();
