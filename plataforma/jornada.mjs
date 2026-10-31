import {interpret} from './engine.mjs';
export const steps=['estudo','previsao','codigo','evidencia','revisao'];
export const points={estudo:5,previsao:10,codigo:20,evidencia:5,revisao:10};
export const labels=['Não iniciada','Em exploração','Em prática','Evidência registrada','Retomada feita'];
export const empty=()=>({version:2,records:{},drafts:{},last:null});
export function readState(text,ids){
 const state=empty();try{const s=JSON.parse(text);if(s?.version!==2)return state;for(const id of ids){const r=s.records?.[id];if(r&&typeof r==='object'&&!Array.isArray(r)){state.records[id]={};for(const k of steps)if(r[k]===true)state.records[id][k]=true;for(const k of ['note','source','support','date','due'])if(typeof r[k]==='string')state.records[id][k]=r[k].slice(0,12000);if(Number.isInteger(r.reviewVariant)&&r.reviewVariant>=0&&r.reviewVariant<=1000)state.records[id].reviewVariant=r.reviewVariant;}
 if(typeof s.drafts?.[id]==='string')state.drafts[id]=s.drafts[id].slice(0,6000);}if(ids.includes(s.last))state.last=s.last;}catch{}return state;
}
export function unitPoints(record={}){return steps.reduce((s,k)=>s+(record[k]===true?points[k]:0),0);}
export function summary(units,state){const rs=units.map(u=>state.records[u.id]||{});return {xp:rs.reduce((s,r)=>s+unitPoints(r),0),started:rs.filter(r=>unitPoints(r)>0).length,practiced:rs.filter(r=>r.codigo).length,evidence:rs.filter(r=>r.evidencia).length,reviewed:rs.filter(r=>r.revisao).length,percentage:units.length?Math.round(rs.reduce((s,r)=>s+unitPoints(r),0)/(units.length*50)*100):0};}
export function level(record={}){return record.revisao?4:record.evidencia?3:record.codigo?2:record.estudo||record.previsao?1:0;}
export function dueUnits(units,state,now=new Date()){return units.filter(u=>{const r=state.records[u.id];return r?.codigo&&(!r.revisao||r.due&&new Date(r.due)<=now);});}
export function complete(state,id,step,now=new Date()){
 if(!steps.includes(step))throw Error('Etapa desconhecida');const r=state.records[id]??={};
 if(step==='revisao'&&!r.codigo)return false;
 r[step]=true;r.date=now.toISOString();if(step==='codigo'&&!r.due)r.due=new Date(+now+3*86400000).toISOString();if(step==='revisao')r.due=new Date(+now+7*86400000).toISOString();return true;
}
export function seed(id){return [...id].reduce((s,c)=>((s*31+c.charCodeAt(0))>>>0),0);}
export function caseFor(model,id,variant=0){return model.casos[(seed(id)+variant)%model.casos.length];}
export function expected(id,a,b){
 switch(id){case 'FND':case 'HWD':return a===1&&b===1;case 'MAT':return 2*a+b;case 'PRG':return b+a*(a+1)/2;case 'ALG':return a*(a-1)/2*b;case 'TEO':return(a+b)%2===0;case 'FIS':case 'SIN':return a*b;case 'ELE':case 'SYS':case 'NET':return a/b;case 'SWE':return a>=b&&a<=2*b;case 'DAT':return a>=b;case 'IA':return a/(a+b);case 'HCI':return(a+5)/(b+5);case 'PRO':return a*b/1000;default:throw Error('Modelo desconhecido');}
}
export function same(a,b){return typeof a===typeof b&&(typeof a==='boolean'?a===b:typeof a==='number'&&Number.isFinite(a)&&Math.abs(a-b)<=1e-8*Math.max(1,Math.abs(b)));}
export function question(model,id,variant=0){
 const [a,b]=caseFor(model,id,variant),answer=expected(model.id,a,b);let choices=typeof answer==='boolean'?[true,false]:[answer,answer+1,answer===0?2:-answer,answer+2];
 choices=choices.filter((v,i)=>choices.findIndex(x=>same(v,x))===i);const offset=seed(id+variant)%choices.length;choices=[...choices.slice(offset),...choices.slice(0,offset)];return{a,b,answer,choices};
}
export function evaluateModel(model,source){
 const results=[];
 for(const [a,b] of model.casos){let output,outputs=0,error=null,variables={},trace=[];try{
 interpret(source+`\nsaida(resolver(${a}, ${b}));`,{saida:v=>{outputs++;if(outputs>1)throw Error('Use return em resolver; a saída é registrada pelo laboratório.');output=v;return v;}},(line,vars)=>{variables=vars;if(trace.length<150)trace.push({line,variables:{...vars}});});
 }catch(e){error={message:e.message,line:e.line||1};}
 const target=expected(model.id,a,b);results.push({a,b,output,expected:target,passed:!error&&outputs===1&&same(output,target),error,trace,variables});}
 return{passed:results.every(t=>t.passed),tests:results};
}
export const starter='function resolver(a, b) {\n  // Use as entradas e a regra do modelo.\n  return 0;\n}';
export const solution=m=>`function resolver(a, b) { return ${m.expressao}; }`;

export function hydrateJourney(raw){return {...raw,disciplinas:raw.disciplinas.map(d=>({...d,unidades:d.unidades.map(u=>({...raw.perfis[d.eixo],...u,recursos:u.recursos.map(id=>raw.recursos[id])}))}))};}
