from pathlib import Path
import re
root=Path(__file__).parent
p=root/'site_template.html'
s=p.read_text(encoding='utf-8')
# Prioritize answering: session title then quiz, and put metrics/overview after the quiz.
a=s.index('    <div class="hero">')
b=s.index('    <article class="question-card"',a)
c=s.index('    <section class="navigator"',b)
pre=s[a:b]
article=s[b:c]
hm=re.search(r'    <div class="hero">(.*?)\n    </div>\n    <div class="progress-wrapper">',pre,re.S)
assert hm, 'hero markup not found'
hero_contents=hm.group(1)
stat_re=re.search(r'\n      (<div class="stat-grid">[^\n]+)',hero_contents,re.S)
assert stat_re, 'stat block missing'
stat=stat_re.group(1)
header=hero_contents[:stat_re.start()]
progress=re.search(r'    <div class="progress-wrapper">[^\n]+\n',pre,re.S)
assert progress
banner=re.search(r'    <div id="finished-banner"[^\n]+\n',pre,re.S)
assert banner
s=s[:a]+'    <div class="hero">'+header+'\n    </div>\n'+article+'    <section class="quiz-metrics" aria-label="Thống kê luyện tập">\n      '+stat+'\n'+progress.group(0)+banner.group(0)+'    </section>\n'+s[c:]
# Consolidate header spacing, make question clearly first content on desktop/mobile.
s=s.replace('    @keyframes enter{', '''    /* Question-first layout: statistics and full navigation follow the quiz. */
    .hero{margin-bottom:12px;align-items:center}
    .hero h1{font-size:clamp(19px,2.1vw,25px)}
    .hero-description{margin-top:3px;font-size:12px}
    .quiz-metrics{margin-top:14px}
    .quiz-metrics .stat-grid{margin-bottom:12px}
    .quiz-metrics .stat{flex:1;min-width:90px}
    .quiz-metrics .progress-wrapper{margin-bottom:12px}
    .question-card{scroll-margin-top:14px}
    @media(max-width:820px){.hero{gap:3px}.hero h1{font-size:20px}.hero-description{display:none}.question-card{padding:19px 16px}.quiz-metrics .stat-grid{gap:7px}}
    @keyframes enter{''')
# Store state only under a dedicated key and clear every app-owned save on reset, never unrelated localStorage.
s=s.replace("  let state={session:'02',current:'02-001',picks:{},graded:{}};",'''  const freshState=()=>({session:sessions[0],current:bySession[sessions[0]][0].id,picks:{},graded:{}});
  let state=freshState();''')
s=s.replace("  function save(){try{localStorage.setItem(storageKey,JSON.stringify(state))}catch(err){}}",'''  function save(){try{localStorage.setItem(storageKey,JSON.stringify(state))}catch(err){}}
  function clearAppProgress(){
    // Delete all historical IT Quiz progress keys, including old versions,
    // but NEVER clear unrelated websites/apps' storage.
    let ok=true;
    for(const storageName of ['localStorage','sessionStorage']){
      try{
        const storage=window[storageName];
        const owned=[];
        for(let i=0;i<storage.length;i++){
          const key=storage.key(i);
          if(key&&(key===storageKey||key.startsWith('itquiz_47_lessons_600_')))owned.push(key);
        }
        // The current key may not be enumerable in some embedded browsers.
        if(!owned.includes(storageKey))owned.push(storageKey);
        for(const key of owned)storage.removeItem(key);
      }catch(err){ok=false;console.warn('Không thể xóa tiến độ trong '+storageName,err)}
    }
    return ok;
  }
  function resetQuiz(scroll=true){
    state=freshState();
    selectedLesson='all';
    const storageCleared=clearAppProgress();
    renderLessonOptions();
    render();
    showToast(storageCleared?'Đã xóa toàn bộ đáp án và kết quả của 600 câu.':'Đã đặt lại giao diện; trình duyệt không cho phép xóa tiến độ đã lưu.');
    if(scroll)$('question-card').scrollIntoView({behavior:'smooth',block:'start'});
  }''')
old="  $('reset-all').addEventListener('click',()=>{if(!confirm('Làm lại toàn bộ 600 câu ở cả 10 session? Tất cả đáp án, kết quả và tiến độ sẽ bị xóa.'))return;state={session:'02',current:'02-001',picks:{},graded:{}};selectedLesson='all';save();renderLessonOptions();render();showToast('Đã đặt lại toàn bộ 600 câu.');window.scrollTo({top:0,behavior:'smooth'})});"
assert old in s
s=s.replace(old,"  $('reset-all').addEventListener('click',()=>{if(!confirm('Làm lại toàn bộ 600 câu ở cả 10 session? Tất cả đáp án, kết quả và tiến độ sẽ bị xóa vĩnh viễn trên thiết bị này.'))return;resetQuiz(true)});")
s=s.replace("  load();if(!bySession[state.session])",'''  // When another open tab resets the quiz, refresh this tab's UI as well.
  window.addEventListener('storage',e=>{if(e.key===storageKey&&e.newValue===null)resetQuiz(false)});
  load();if(!bySession[state.session])''')
p.write_text(s,encoding='utf-8')
print('Patched',p)
