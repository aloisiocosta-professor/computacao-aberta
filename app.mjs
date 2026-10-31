import {missions,byId} from './missions.mjs';
import {evaluate,simulate} from './simulation.mjs';
const $=id=>document.getElementById(id);
const SOURCE='https://github.com/aloisiocosta-professor/computacao-aberta/blob/feature/plataforma-visual/';
const KEY='computacao-aberta-lab-v1';
let saved={drafts:{},progress:{},reflections:{},assisted:{},selected:missions[0].id};
try{const data=JSON.parse(localStorage.getItem(KEY)||'null');if(data&&typeof data==='object')for(const k of Object.keys(saved))if(Object.hasOwn(data,k)&&typeof data[k]===typeof saved[k]&&(typeof saved[k]!=='object'||data[k]&&!Array.isArray(data[k])))saved[k]=data[k];}catch{}
let mission=byId(saved.selected),result=null,frame=0,timer=null,variant=false,a=true,b=false,catalog=[];
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function save(){try{localStorage.setItem(KEY,JSON.stringify(saved));}catch{$('reflection-status').textContent='Armazenamento indisponível. Exporte o registro para preservá-lo.';}}
function halt(){if(timer)clearInterval(timer);timer=null;$('play').textContent='▶';$('play').setAttribute('aria-label','Reproduzir execução');}
function nav(){
 $('mission-list').innerHTML=missions.map((m,i)=>`<button type="button" data-mission="${m.id}" class="${saved.progress[m.id]?.passed?'done':''}" ${m.id===mission.id?'aria-current="step"':''} title="${escape(m.title)}"><span class="mission-bullet">${saved.progress[m.id]?.passed?'✓':String(i+1).padStart(2,'0')}</span>${escape(m.topic)}</button>`).join('');
 const n=missions.filter(m=>saved.progress[m.id]?.passed).length;$('path-count').textContent=`${n} / ${missions.length}`;$('completed-count').textContent=`${n} de ${missions.length}`;
}
function draft(){return saved.drafts[mission.id]??mission.starter;}
function gutter(){const lines=$('code').value.split('\n').length;$('gutter').textContent=Array.from({length:Math.max(lines,10)},(_,i)=>i+1).join('\n');const line=$('code').value.slice(0,$('code').selectionStart).split('\n').length;$('cursor-line').textContent=`linha ${line}`;}
function load(id){
 halt();mission=byId(id);document.title=mission.title+' · Computação Aberta';saved.selected=mission.id;save();result=null;frame=0;variant=false;
 $('mission-title').textContent=mission.title;$('mission-number').textContent=`MISSÃO ${String(missions.indexOf(mission)+1).padStart(2,'0')} · ${mission.discipline}`;$('mission-time').textContent=mission.minutes;$('mission-goal').textContent=mission.goal;$('prediction').textContent=mission.predict;$('crumb-topic').textContent=mission.topic;$('concept').textContent=mission.concept;$('transfer').textContent=mission.transfer;$('code').value=draft();$('reflection').value=saved.reflections[mission.id]||'';$('reflection-status').textContent='';$('hint-content').hidden=true;$('hint-content').textContent='';$('feedback').textContent='Faça uma previsão. Depois execute o programa e compare o resultado.';$('feedback-badge').textContent='Sua próxima descoberta';$('feedback-badge').className='neutral-badge';$('test-results').replaceChildren();$('scenario').hidden=!mission.variantGoal&&mission.kind!=='sort';$('scenario').textContent='Outro cenário ↻';$('source-lesson').href=SOURCE+`unidades/por-disciplina/${mission.discipline.toLowerCase()}.md`;
 $('continue').textContent=missions.indexOf(mission)===missions.length-1?'Voltar ao início →':'Próximo desafio →';$('sim-mode').textContent={rover:'ROVER LAB',sort:'ALGORITMOS',logic:'LÓGICA DIGITAL',energy:'DADOS E DECISÕES'}[mission.kind];
 nav();gutter();render();
}
function options(){return {a,b,...(variant?mission.kind==='sort'?{values:mission.alternative}:{goal:mission.variantGoal}:{})};}
function current(){if(result)return result.frames[frame];return simulate(mission,'',options()).frames[0];}
function rover(state){
 const grid=mission.grid,w=grid[0].length,h=grid.length,s=42,ox=35,oy=24;const goal=variant?mission.variantGoal:mission.goalAt;let shapes='';
 grid.forEach((row,y)=>[...row].forEach((c,x)=>{const xx=ox+x*s,yy=oy+y*s;shapes+=`<rect x="${xx}" y="${yy}" width="39" height="39" rx="5" fill="${c==='#'?'#193b45':'#2c4d56'}" stroke="${c==='#'?'#20434e':'#41616a'}" stroke-width=".8"/>`;if(c==='#'&&(x+y)%3===0)shapes+=`<path d="M${xx+10} ${yy+24}l8 -9 9 9" fill="none" stroke="#2a4c56" stroke-width="2"/>`;}));
 const history=result?result.frames.slice(0,frame+1):[];
 history.forEach(f=>{shapes+=`<circle cx="${ox+f.state.x*s+19.5}" cy="${oy+f.state.y*s+19.5}" r="3" fill="#8ac6ab" opacity=".3"/>`;});
 const gx=ox+goal[0]*s+19.5,gy=oy+goal[1]*s+19.5;
 shapes+=`<rect x="${gx-16}" y="${gy-16}" width="32" height="32" rx="7" fill="#3d6759" stroke="#b6e4a2" stroke-width="1.4"/><path d="M${gx-6} ${gy}l4 4 9 -9" stroke="#ccedb8" stroke-width="2.5" fill="none"/>`;
 const x=ox+state.x*s+19.5,y=oy+state.y*s+19.5;
 shapes+=`<g transform="translate(${x},${y}) rotate(${state.dir*90})"><rect x="-15" y="-10" width="6" height="20" rx="2" fill="#709ba4"/><rect x="9" y="-10" width="6" height="20" rx="2" fill="#709ba4"/><rect x="-11" y="-12" width="22" height="25" rx="6" fill="#e5f0df"/><rect x="-8" y="-8" width="16" height="9" rx="3" fill="#193d47"/><circle cx="-4" cy="-4" r="2" fill="#9cdebe"/><circle cx="4" cy="-4" r="2" fill="#9cdebe"/><path d="M-4 -17h8l-4 -5z" fill="#d9edaa"/><rect x="-4" y="5" width="8" height="3" rx="1" fill="#7eb29a"/></g>`;
 for(let c=0;c<w;c++)shapes+=`<text x="${ox+c*s+19.5}" y="${oy+h*s+13}" text-anchor="middle" fill="#73969f" font-size="9">${c}</text>`;
 for(let r=0;r<h;r++)shapes+=`<text x="${ox-15}" y="${oy+r*s+23}" text-anchor="middle" fill="#73969f" font-size="9">${r}</text>`;
 const description=`Robô na coluna ${state.x}, linha ${state.y}, voltado para ${['norte','leste','sul','oeste'][state.dir]}. Estação na coluna ${goal[0]}, linha ${goal[1]}.`;
 $('scene').innerHTML=`<svg role="img" aria-label="${description}" viewBox="0 0 ${w*s+70} ${h*s+61}">${shapes}</svg>`;$('scene-legend').innerHTML=`<span><i class="legend-square"></i> Estação</span><span><i class="legend-square obstacle"></i> Obstáculo</span><span>Coluna ${state.x} · linha ${state.y} · ${['N','L','S','O'][state.dir]}</span>`;
}
function sorting(state){
 const arr=state.values,max=Math.max(...arr,1),width=320,base=232;let shapes=`<path d="M28 ${base+1}h264" stroke="#53747a"/>`;
 arr.forEach((v,i)=>{const h=v/max*140,x=40+i*64;shapes+=`<rect x="${x}" y="${base-h}" width="43" height="${h}" rx="5" fill="${i%2?'#91c9bb':'#c2dda1'}"/><text x="${x+21}" y="${base-h-12}" text-anchor="middle" fill="#e2efe1" font-size="17">${v}</text><text x="${x+21}" y="${base+21}" text-anchor="middle" fill="#8bb0b7" font-size="10">${i}</text>`;});
 $('scene').innerHTML=`<svg viewBox="0 0 ${width} 290" role="img" aria-label="Valores nas barras: ${arr.join(', ')}. As posições começam em zero."><text x="160" y="35" text-anchor="middle" fill="#aac8c8" font-size="11">UM ALGORITMO, CADA TROCA VISÍVEL</text>${shapes}</svg>`;$('scene-legend').textContent=`Posições 0 a ${arr.length-1} · valores atuais: [${arr.join(', ')}]`;
}
function logic(state){
 const on=state.output===true;const color=on?'#c9e89e':'#4c6b74';
 const tests=[[0,0],[0,1],[1,0],[1,1]];const rows=tests.map(([x,y])=>`<tr><td>${x}</td><td>${y}</td><td>${x||y}</td></tr>`).join('');
 $('scene').innerHTML=`<div class="logic-wrap"><div class="toggle-inputs"><button id="input-a" aria-pressed="${a}">A ${a?'ligada':'desligada'}</button><button id="input-b" aria-pressed="${b}">B ${b?'ligada':'desligada'}</button></div><svg viewBox="0 0 320 105" role="img" aria-label="Entrada A ${Number(a)}, B ${Number(b)}. Saída ${state.output===null?'não definida':Number(on)}."><path d="M42 32h77M42 75h77M200 53h56" stroke="#73988f" stroke-width="3" fill="none"/><circle cx="42" cy="32" r="8" fill="${a?'#c6e69d':'#4c6b74'}"/><circle cx="42" cy="75" r="8" fill="${b?'#c6e69d':'#4c6b74'}"/><rect x="118" y="16" width="83" height="74" rx="17" fill="#28515a" stroke="#83b5a0"/><text x="160" y="60" font-size="16" text-anchor="middle" fill="#d0e4c9">seu código</text><circle cx="264" cy="53" r="16" fill="${color}" stroke="#a1bdb1"/><path d="M256 77h16" stroke="#97b9ac" stroke-width="3"/></svg><table class="truth-table"><caption>Tabela-verdade esperada</caption><thead><tr><th scope="col">A</th><th scope="col">B</th><th scope="col">Saída</th></tr></thead><tbody>${rows}</tbody></table></div>`;
 $('input-a').onclick=()=>{a=!a;rerenderInputs();};$('input-b').onclick=()=>{b=!b;rerenderInputs();};$('scene-legend').textContent='Altere as entradas para experimentar. A tabela mostra o resultado esperado.';
}
function energy(state){
 const values=mission.samples;const max=Math.max(...values);let shapes='';values.forEach((v,i)=>{const h=v/max*74;shapes+=`<rect x="${66+i*67}" y="${90-h}" width="38" height="${h}" rx="4" fill="#84bfae"/><text x="${85+i*67}" y="106" fill="#bfd8d6" text-anchor="middle" font-size="11">${v}</text>`;});
 $('scene').innerHTML=`<div class="logic-wrap"><p class="energy-title">AMOSTRAS FICTÍCIAS DE CONSUMO</p><svg viewBox="0 0 320 115" role="img" aria-label="Amostras ${values.join(', ')}">${shapes}</svg><div class="energy-value">${state.total===null?'—':state.total} <span>/ limite ${mission.limit}</span></div><div class="energy-alert ${state.alert?'on':''}">${state.alert===null?'Aguardando decisão':state.alert?'● Alerta ligado':'○ Alerta desligado'}</div></div>`;$('scene-legend').textContent='Teste também os casos abaixo, igual e acima do limite.';
}
function render(){
 const f=current();if(mission.kind==='rover')rover(f.state);else if(mission.kind==='sort')sorting(f.state);else if(mission.kind==='logic')logic(f.state);else energy(f.state);
 $('scrub').max=String((result?.frames.length||1)-1);$('scrub').value=String(frame);$('scrub').disabled=!result||result.frames.length<2;
 $('step-label').textContent=result?`Passo ${frame} de ${result.frames.length-1}`:'Pronto para experimentar';$('trace-message').textContent=f.message+(f.line?` · linha ${f.line}`:'');
 $('memory').replaceChildren();const pairs=Object.entries(f.variables);if(!pairs.length){const p=document.createElement('p');p.className='empty-note';p.textContent='Os valores aparecem ao avançar pela execução.';$('memory').append(p);}else{
 const table=document.createElement('table');table.className='memory-table';table.innerHTML='<caption class="sr-only">Variáveis neste passo</caption>';for(const [name,val] of pairs){const tr=document.createElement('tr'),th=document.createElement('th'),td=document.createElement('td');th.scope='row';th.textContent=name;td.textContent=String(val);tr.append(th,td);table.append(tr);}$('memory').append(table);
 }
 for(const id of ['first','previous','next','play'])$(id).disabled=!result||result.frames.length<2||(id==='previous'||id==='first'?frame===0:id==='next'?frame===result.frames.length-1:false);
}
function rerenderInputs(){halt();if(result){result=evaluate(mission,$('code').value,options());frame=result.frames.length-1;showFeedback(false);}render();}
function showFeedback(record=true){
 const r=result;let message;
 if(r.error)message=`Linha ${r.error.line}: ${r.error.message}`;
 else if(r.passed)message='Seu programa passou nos casos desta missão. Agora percorra os passos e explique por que funcionou.';
 else if(r.goalPassed&&!r.used)message=`Você alcançou o objetivo. Agora aplique ${mission.topic.toLowerCase()} para praticar a habilidade proposta.`;
 else message=mission.kind==='rover'?'Ainda não chegou à estação. Compare a posição final com a meta e ajuste uma parte do código.':'Alguns casos ainda não passaram. Observe os resultados e teste uma hipótese por vez.';
 $('feedback').textContent=message;$('feedback-badge').textContent=r.error?'Revise e experimente':r.passed?'Casos aprovados':'Continue investigando';$('feedback-badge').className=`neutral-badge ${r.passed?'success':'failure'}`;
 $('test-results').replaceChildren();for(const t of r.tests){const li=document.createElement('li');li.className=t.passed?'pass':'fail';li.textContent=`${t.passed?'✓':'○'} ${t.label}`;$('test-results').append(li);}
 if(record){const old=saved.progress[mission.id]||{};saved.progress[mission.id]={passed:Boolean(old.passed||r.passed),latestPassed:r.passed,attempts:(old.attempts||0)+1,assisted:Boolean(saved.assisted[mission.id]),scenario:variant?'alternativo':'inicial',tests:r.tests,date:new Date().toISOString()};save();nav();}
}
function play(){if(!result||result.frames.length<2)return;if(timer){halt();return;}if(frame>=result.frames.length-1)frame=0;$('play').textContent='Ⅱ';$('play').setAttribute('aria-label','Pausar execução');timer=setInterval(()=>{frame++;render();if(frame>=result.frames.length-1)halt();},350);}
function run(){halt();saved.drafts[mission.id]=$('code').value;save();result=evaluate(mission,$('code').value,options());frame=0;render();showFeedback();if(matchMedia('(prefers-reduced-motion: reduce)').matches){frame=result.frames.length-1;render();}else play();}
$('run').onclick=run;$('play').onclick=play;$('first').onclick=()=>{halt();frame=0;render();};$('previous').onclick=()=>{halt();frame=Math.max(0,frame-1);render();};$('next').onclick=()=>{halt();frame=Math.min(result.frames.length-1,frame+1);render();};$('scrub').oninput=()=>{halt();frame=Number($('scrub').value);render();};
$('mission-list').onclick=e=>{const button=e.target.closest('[data-mission]');if(button)load(button.dataset.mission);};
$('code').oninput=()=>{saved.drafts[mission.id]=$('code').value;save();gutter();};$('code').addEventListener('keyup',gutter);$('code').addEventListener('click',gutter);$('code').onscroll=()=>{$('gutter').scrollTop=$('code').scrollTop;};$('code').onkeydown=e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();run();}};
$('reset-code').onclick=()=>{saved.drafts[mission.id]=mission.starter;save();load(mission.id);};
$('hint').onclick=()=>{saved.assisted[mission.id]=true;save();$('hint-content').textContent=mission.hint;$('hint-content').hidden=false;};
$('scenario').onclick=()=>{halt();variant=!variant;result=null;frame=0;$('scenario').textContent=variant?'Cenário inicial ↻':'Outro cenário ↻';$('feedback').textContent='Cenário alterado. Faça uma nova previsão e execute o código.';$('test-results').replaceChildren();$('feedback-badge').textContent='Novo cenário';$('feedback-badge').className='neutral-badge';render();};
$('continue').onclick=()=>{load(missions[(missions.indexOf(mission)+1)%missions.length].id);$('mission-title').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'center'});};
$('save-reflection').onclick=()=>{saved.reflections[mission.id]=$('reflection').value;save();$('reflection-status').textContent='Explicação guardada neste navegador.';};
for(const [button,dialog] of [['catalog-open','catalog-dialog'],['mobile-catalog','catalog-dialog'],['guide-open','guide-dialog'],['mobile-guide','guide-dialog'],['references-open','about-dialog']])$(button).onclick=()=>{if(dialog==='guide-dialog'){saved.assisted[mission.id]=true;save();}$(dialog).showModal();};
document.querySelectorAll('.close-dialog').forEach(b=>b.onclick=()=>b.closest('dialog').close());
$('clear-progress').onclick=()=>{if(confirm('Apagar os códigos, explicações e registros salvos neste navegador? Exporte antes se quiser guardar uma cópia.')){saved={drafts:{},progress:{},reflections:{},assisted:{},selected:mission.id};save();load(mission.id);}};
$('export-progress').onclick=()=>{const record={type:'registro_local_simulador',version:1,date:new Date().toISOString(),limite:'Evidência dos casos deste simulador. Não certifica domínio, autoria ou aprendizagem independente.',...saved};const url=URL.createObjectURL(new Blob([JSON.stringify(record,null,2)],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download='computacao-aberta-meu-registro.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
$('read-mission').onclick=()=>{if(!('speechSynthesis'in window)){$('feedback').textContent='Leitura em voz alta indisponível neste navegador. As instruções completas estão acima.';return;}speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(mission.title+'. '+mission.goal+'. '+mission.predict);utterance.lang='pt-BR';speechSynthesis.speak(utterance);};
function searchCatalog(){const query=$('catalog-search').value.toLocaleLowerCase('pt-BR');const rows=catalog.filter(x=>`${x.id} ${x.nome} ${x.eixo} ${x.unidades.map(u=>u.titulo).join(' ')}`.toLocaleLowerCase('pt-BR').includes(query));$('catalog-count').textContent=`${rows.length} disciplinas encontradas`;$('catalog-results').innerHTML=rows.map(s=>`<details><summary>${escape(s.id)} · ${escape(s.nome)}<small>${escape(s.eixo)} · ${s.unidades.length} unidades</small></summary><ul>${s.unidades.map(u=>`<li>${escape(u.titulo)} <span class="state-tag">${escape(u.estado)}</span></li>`).join('')}</ul><a href="${SOURCE}unidades/por-disciplina/${s.id.toLowerCase()}.md" target="_blank" rel="noopener">Abrir unidades e fontes ↗</a></details>`).join('');}
$('catalog-search').oninput=searchCatalog;
fetch('./catalogo.json').then(r=>{if(!r.ok)throw Error('Catálogo indisponível');return r.json();}).then(data=>{catalog=data;searchCatalog();}).catch(()=>{$('catalog-count').textContent='Não foi possível carregar o catálogo. Consulte as disciplinas no GitHub.';});
fetch('./release.json').then(r=>r.json()).then(r=>{$('build-label').textContent=`v${r.version} · ${r.commit.slice(0,7)}`;}).catch(()=>{});
load(mission.id);
