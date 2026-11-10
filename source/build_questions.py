import json,random,collections,re,hashlib,pathlib
ROOT=pathlib.Path(__file__).parent
lessons=json.load(open(ROOT/'lesson_summaries.json',encoding='utf8'))
for lesson in lessons:
 lesson['example']=re.sub(r'^(Ví dụ:\s*){2,}', 'Ví dụ: ', lesson['example'])
SESSION_NAMES={'02':'Nhập môn CNTT và dữ liệu','03':'Hệ điều hành, đường dẫn và tệp tin','05':'Terminal cơ bản','07':'Dòng lệnh nâng cao và script an toàn','09':'Markdown và tài liệu kỹ thuật','11':'Word, Excel và PowerPoint','15':'Phân quyền và Hybrid Workflow','17':'Trình duyệt và DevTools','19':'An toàn thông tin và Secrets','21':'Tìm kiếm và báo lỗi kỹ thuật'}
hints={line.split('|')[0]:line.strip().split('|')[1:] for line in open(ROOT/'hints.txt',encoding='utf8') if line.strip()}
L={(l['session'],l['lesson']):l for l in lessons}
S=collections.defaultdict(list)
for l in lessons:S[l['session']].append(l)

def load_bank(name,typ):
 out=collections.defaultdict(list)
 for no,raw in enumerate(open(ROOT/name,encoding='utf8'),1):
  line=raw.strip('\n')
  if not line or line.startswith('#'):continue
  cols=line.split('\t')
  if len(cols)!=7:raise ValueError((name,no,len(cols),line[:140]))
  sk,q,a,b,c,d,why=cols
  sess,lis=sk.split('-');l=L[(sess,int(lis))]
  out[sess].append({'session':sess,'lesson':l['lesson'],'title':l['title'],'page':l['page'],'type':typ,'question':q,'choices':[a,b,c,d],'answer':0,'explanation':why.strip() + (' Theo phần trọng tâm trong tài liệu: '+l['summary'] if typ=='Vận dụng' else ' Đây là kiến thức mở rộng dựa trên chủ đề '+l['title']+'.')})
 return out
manual=load_bank('manual_bank.txt','Vận dụng')
extended=load_bank('extended_bank.txt','Mở rộng')

def choose_wrong(pool,correct,seed,n=3):
 p=list(dict.fromkeys(str(x).strip() for x in pool if str(x).strip() and str(x).strip()!=correct))
 rng=random.Random(seed)
 rng.shuffle(p)
 if len(p)<n:raise ValueError(('insufficient wrong options',correct,p))
 return p[:n]

def question(l,stem,right,pool,kind,why,serial):
 seed=int(hashlib.sha256(f"{l['session']}-{l['lesson']}-{serial}".encode()).hexdigest()[:12],16)
 return {'session':l['session'],'lesson':l['lesson'],'title':l['title'],'page':l['page'],'type':kind,'question':stem,'choices':[right,*choose_wrong(pool,right,seed)],'answer':0,'explanation':why}

def generate(l):
 session=l['session'];key=f"{session}-{l['lesson']:02d}";H=hints[key];facts=l['bullets'];samples=S[session]
 poolfacts=[f for x in samples if x!=l for f in x['bullets']]
 poolsum=[x['summary'] for x in samples if x!=l]
 if len(poolsum)<3:poolsum += [x['summary'] for x in lessons if x['session']!=session][:3-len(poolsum)]
 poolex=[x['example'] for x in samples if x!=l]
 if len(poolex)<3:poolex += [x['example'] for x in lessons if x['session']!=session][:3-len(poolex)]
 poolnotes=[x['note'] for x in samples if x!=l]
 if len(poolnotes)<3:poolnotes += [x['note'] for x in lessons if x['session']!=session][:3-len(poolnotes)]
 pooltitles=[x['title'] for x in samples if x!=l]
 if len(pooltitles)<3:pooltitles += [x['title'] for x in lessons if x['session']!=session][:3-len(pooltitles)]
 result=[]
 for i,b in enumerate(facts):
  result.append(question(l,f"Theo bài {l['lesson']:02d} – {l['title']}, phát biểu nào giải thích chính xác về «{H[i]}»?",b,poolfacts,'Theo PDF', f"**Ý chính:** {b}\n\n**Vì sao?** Đây là nội dung trọng tâm số {i+1} của bài. {l['summary']}\n\n**Ghi nhớ:** {l['note']}",f'fwd-{i}'))
 result.append(question(l,f"Sau khi học bài «{l['title']}», kết luận bao quát đúng nhất là gì?",l['summary'],poolsum,'Theo PDF',f"**Tóm tắt bài học:** {l['summary']}\n\n**Liên hệ kiến thức:** {facts[0]}\n\n**Lưu ý khi làm bài:** {l['note']}",'summary'))
 result.append(question(l,f"Trong tài liệu, tình huống nào minh họa cụ thể cho bài «{l['title']}»?",l['example'],poolex,'Theo PDF',f"**Ví dụ trong PDF:** {l['example']}\n\n**Cơ sở kiến thức:** {l['summary']}\n\n**Bài học rút ra:** {l['note']}",'example'))
 result.append(question(l,f"Khi ôn bài «{l['title']}», lưu ý nào giúp tránh lỗi hiểu sai thường gặp?",l['note'],poolnotes,'Theo PDF',f"**Điểm cần tránh:** {l['note']}\n\n**Cơ sở để hiểu đúng:** {l['summary']} {facts[min(1,len(facts)-1)]}",'note'))
 for i in range(min(3,len(facts))):
  b=facts[i];wrong=[hint for j,hint in enumerate(H) if j!=i]
  result.append(question(l,f"Đọc mô tả kiến thức sau: «{b}». Mô tả này thuộc nội dung nào của bài «{l['title']}»?",H[i],wrong,'Theo PDF',f"**Đáp án:** {H[i]}.\n\n**Giải thích:** {b}\n\n**Phân biệt:** Các phương án còn lại là nhãn của nội dung trọng tâm khác; cần đối chiếu mô tả kỹ thuật trong câu hỏi, không chọn chỉ vì cùng chủ đề.",f'rev-{i}'))
 result.append(question(l,f"Đoạn tóm tắt «{l['summary']}» được học trong bài nào của cẩm nang?",l['title'],pooltitles,'Theo PDF',f"**Đây là nội dung của bài {l['lesson']:02d}:** {l['title']}.\n\n**Nội dung cốt lõi:** {l['summary']}\n\n**Ví dụ gắn với bài học:** {l['example']}",'reverse-summary'))
 if len(result)<12:
  i=3
  result.append(question(l,f"Cụm nội dung nào khớp với lời giải thích sau trong bài {l['lesson']:02d}? «{facts[i]}»",H[i],[hint for j,hint in enumerate(H) if j!=i],'Theo PDF',f"**Đối chiếu:** {facts[i]}\n\n**Kết luận:** {H[i]}. {l['note']}",'reverse-4'))
 assert len(result)==12,(key,len(result))
 return result

auto={(l['session'],l['lesson']):generate(l) for l in lessons}
quiz=[]
for sess,ls in S.items():
 # Make every lesson and every original chapter represented. Prioritize authored and genuine expansion.
 base=[q for q in manual[sess]]+extended[sess]
 remaining=60-len(base)
 if remaining<0:raise ValueError(('too many authored',sess))
 count={l['lesson']:0 for l in ls}
 # round robin across lessons, take front question types first, preserving coverage.
 while remaining:
  advanced=False
  for l in ls:
   if not remaining:break
   idx=count[l['lesson']]
   if idx>=12:continue
   base.append(auto[(sess,l['lesson'])][idx])
   count[l['lesson']]+=1;remaining-=1;advanced=True
  if not advanced:raise ValueError(('cannot reach 60',sess,count))
 # Sort by lesson (not by type), preserving auto+manual+expanded interleaving with stable seeded shuffle.
 for l in ls:
  pool=[x for x in base if x['lesson']==l['lesson']]
  random.Random(int(sess)*100+l['lesson']).shuffle(pool)
  quiz.extend(pool)

# stable per-session ids/answer shuffle, with fair A/B/C/D distribution
seen=set()
for sess in SESSION_NAMES:
 qs=[x for x in quiz if x['session']==sess]
 for i,q in enumerate(qs,1):
  q['id']=f'{sess}-{i:03d}'
  norm=re.sub(r'\s+',' ',q['question']).casefold().strip()
  if norm in seen:raise ValueError(('duplicate stem',q['question']))
  seen.add(norm)
  if len(q['choices'])!=4 or len(set(q['choices']))!=4:raise ValueError(('bad choices',q['id']))
  seed=int(hashlib.sha256(q['id'].encode()).hexdigest()[:12],16)
  shuffled=q['choices'][:]
  random.Random(seed).shuffle(shuffled)
  q['answer']=shuffled.index(q['choices'][0]);q['choices']=shuffled
  assert q['question'].strip() and q['explanation'].strip()
quiz.sort(key=lambda q:(int(q['session']),int(q['id'].split('-')[1])))
counts=collections.Counter(x['session'] for x in quiz)
bytype=collections.Counter(x['type'] for x in quiz)
assert len(quiz)==600 and all(counts[s]==60 for s in SESSION_NAMES),counts
assert len(set((q['session'],q['lesson']) for q in quiz))==47
output={'version':3,'title':'Luyện trắc nghiệm CNTT • 10 Session','source':'Cẩm nang ôn thi cuối học phần, 47 bài, 198 trang, biên soạn 10/11/2026','sessions':SESSION_NAMES,'lessons':[{k:l[k] for k in ('session','lesson','title','page')} for l in lessons],'questions':quiz}
with open(ROOT/'questions.json','w',encoding='utf8') as f:json.dump(output,f,ensure_ascii=False,indent=1)
print('OK',len(quiz),dict(counts),'type',dict(bytype));
for sess in SESSION_NAMES:
 per=collections.Counter(q['lesson'] for q in quiz if q['session']==sess)
 print(sess,'lessons',dict(per))
print('sample:',json.dumps(quiz[0],ensure_ascii=False,indent=2)[:1600]);
