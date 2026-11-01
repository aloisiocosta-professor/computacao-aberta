import {interpret} from './engine.mjs';
export function equivalent(a,b){return typeof a===typeof b&&(typeof b==='boolean'?a===b:typeof b==='number'&&Number.isFinite(a)&&Math.abs(a-b)<=1e-8*Math.max(1,Math.abs(b)));}
export function evaluatePractice(practice,source){
 if(practice.tipo!=='numerica')throw Error('Esta atividade é um jogo de decisões.');
 const tests=practice.casos.map(c=>{const {a,b}=c.entradas;let output,calls=0,line=1,error=null,trace=[];
  try{if(![a,b].every(x=>typeof x==='number'&&Number.isFinite(x)))throw Error('Entradas do cenário inválidas.');
   interpret(source+`\nsaida(resolver(${a},${b}));`,{saida:value=>{calls++;if(calls>1)throw Error('Use return para devolver a resposta; não chame saida diretamente.');output=value;return value;}},(ln,variables)=>{line=ln;if(trace.length<180)trace.push({line:ln,variables:{...variables}});});
  }catch(e){error={message:e.message,line:e.line||line};}
  return {entradas:c.entradas,expected:c.esperado,output,error,trace,passed:!error&&calls===1&&equivalent(output,c.esperado)};
 });return{passed:tests.length>0&&tests.every(t=>t.passed),tests};
}
export function gradeQuestions(questions,answers){return questions.map((q,i)=>({passed:Number.isInteger(answers[i])&&answers[i]===q.correta,feedback:q.feedback[answers[i]]||'Escolha uma alternativa antes de conferir.'}));}
export function lessonQuestions(lesson,variant=0){const n=lesson.questoes.length,offset=variant%n;return [...lesson.questoes.slice(offset),...lesson.questoes.slice(0,offset)];}
export function validateLesson(lesson){
 const errors=[],fail=s=>errors.push(`${lesson?.id||'?'}: ${s}`);
 if(!lesson?.id||!lesson.titulo||typeof lesson.conceito!=='string'||lesson.conceito.length<100)fail('conceito ausente ou insuficiente');
 if(!lesson.exemplo?.enunciado||!lesson.exemplo?.resultado||lesson.exemplo?.passos?.length<3)fail('exemplo sem caso, passos ou resultado');
 if(lesson.visual?.tipo!=='tabela'||!lesson.visual.colunas?.length||!lesson.visual.linhas?.length||!lesson.visual.linhas.every(row=>Array.isArray(row)&&row.length===lesson.visual.colunas.length))fail('representação tabular incoerente');
 const check=(q,field)=>{const options=q.alternativas||q.opcoes;if(!q.enunciado&&!q.situacao)fail(`${field}: falta enunciado`);if(!Array.isArray(options)||options.length<3||new Set(options).size!==options.length)fail(`${field}: alternativas ausentes ou repetidas`);if(!Number.isInteger(q.correta)||q.correta<0||q.correta>=options?.length)fail(`${field}: gabarito inválido`);if(!Array.isArray(q.feedback)||q.feedback.length!==options?.length||q.feedback.some(f=>typeof f!=='string'||f.length<10))fail(`${field}: feedback incompleto`);};
 if(!Array.isArray(lesson.questoes)||lesson.questoes.length<2)fail('menos de duas questões específicas');else lesson.questoes.forEach((q,i)=>check(q,`questão ${i+1}`));
 const p=lesson.pratica;if(p?.tipo==='numerica'){if(p.casos?.length<4||!p.solucao)fail('prática numérica sem casos/solução');if(!p.casos?.every(c=>[c.entradas?.a,c.entradas?.b].every(v=>typeof v==='number'&&Number.isFinite(v))&&['number','boolean'].includes(typeof c.esperado)))fail('casos numéricos inválidos');}
 else if(p?.tipo==='decisao'){if(p.rodadas?.length<2)fail('jogo com menos de duas decisões');else p.rodadas.forEach((q,i)=>check(q,`decisão ${i+1}`));}else fail('tipo de prática desconhecido');
 if(!p?.enunciado||!p?.regra)fail('prática sem tarefa ou regra');
 if(!lesson.projeto?.enunciado||lesson.projeto.criterios?.length<3)fail('projeto incompleto');
 if(!Array.isArray(lesson.fontes)||!lesson.fontes.length||!lesson.fontes.every(f=>/^https:\/\//.test(f.url)&&f.uso&&f.secao&&['PARCIAL','CONFIRMADO'].includes(f.leitura)))fail('fontes/limites incompletos');
 if(lesson.estado_editorial!=='PROPOSTA_AUTORAL'||lesson.validacao_pedagogica!=='NÃO VERIFICADO')fail('não preservar proposta e validação pedagógica');
 return errors;
}
