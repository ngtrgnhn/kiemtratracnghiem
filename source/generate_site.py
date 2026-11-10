import json, pathlib
root=pathlib.Path(__file__).parent
questions=json.loads((root/'questions.json').read_text(encoding='utf8'))
compact=json.dumps(questions,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
html=(root/'site_template.html').read_text(encoding='utf8').replace('__QUIZ_JSON__',compact)
(root/'index.html').write_text(html,encoding='utf8')
print('index.html bytes',len(html.encode('utf8')),'quiz json bytes',len(compact.encode('utf8')))
