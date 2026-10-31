import {interpret,CodeError} from './engine.mjs';
const clone=x=>JSON.parse(JSON.stringify(x));
function integer(n,min,max,line=1){if(!Number.isInteger(n)||n<min||n>max)throw new CodeError(`Use um inteiro de ${min} a ${max} neste comando.`,line);return n;}
export function simulate(mission,source,options={}){
 const state={x:mission.start?.[0]||0,y:mission.start?.[1]||0,dir:mission.start?.[2]||0,values:[...(options.values||mission.values||[])],logs:[],output:null,alert:null,total:null,a:options.a??true,b:options.b??false};
 const frames=[];let line=1,variables={},actions=0,metrics={};
 const record=message=>{if(++actions>160)throw new CodeError('Até 160 ações por tentativa. Simplifique o programa.',line);frames.push({line,variables:{...variables},message,state:clone(state)});};
 const front=()=>{const delta=[[0,-1],[1,0],[0,1],[-1,0]][state.dir];return [state.x+delta[0],state.y+delta[1]];};
 const free=()=>{const [x,y]=front();return mission.grid?.[y]?.[x]==='.';};
 const api={registrar:n=>{if(!['number','boolean'].includes(typeof n))throw new CodeError('Registre um número ou valor lógico.',line);state.logs.push(n);state.total=n;record(`Registro: ${n}`);return n;}};
 if(mission.kind==='rover')Object.assign(api,{
  mover:(n=1)=>{integer(n,1,8,line);for(let i=0;i<n;i++){if(!free())throw new CodeError('Há um obstáculo à frente. Verifique o caminho antes de mover.',line);[state.x,state.y]=front();record('O robô avançou uma casa.');}return n;},
  virarDireita:()=>{state.dir=(state.dir+1)%4;record('O robô virou à direita.');return 0;},
  virarEsquerda:()=>{state.dir=(state.dir+3)%4;record('O robô virou à esquerda.');return 0;},
  livre:()=>free()
 });
 if(mission.kind==='sort')Object.assign(api,{tamanho:()=>state.values.length,valor:i=>state.values[integer(i,0,state.values.length-1,line)],trocar:(i,j)=>{integer(i,0,state.values.length-1,line);integer(j,0,state.values.length-1,line);[state.values[i],state.values[j]]=[state.values[j],state.values[i]];record(`Troca entre as posições ${i} e ${j}.`);return 0;}});
 if(mission.kind==='logic')Object.assign(api,{entradaA:()=>state.a,entradaB:()=>state.b,saida:value=>{if(typeof value!=='boolean')throw new CodeError('A saída precisa ser true ou false.',line);state.output=value;record(`Saída ${value?'ligada':'desligada'}.`);return value;}});
 if(mission.kind==='energy')Object.assign(api,{amostras:()=>(options.samples||mission.samples).length,consumo:i=>(options.samples||mission.samples)[integer(i,0,(options.samples||mission.samples).length-1,line)],limite:()=>mission.limit,alertar:value=>{if(typeof value!=='boolean')throw new CodeError('O alerta precisa de uma comparação lógica.',line);state.alert=value;record(`Alerta ${value?'ligado':'desligado'}.`);return value;}});
 frames.push({line:0,variables:{},message:'Estado inicial. Faça uma previsão antes de executar.',state:clone(state)});
 let error=null;
 try{({metrics}=interpret(source,api,(ln,vars)=>{line=ln;variables=vars;}));}catch(e){error={message:e.message,line:e.line||line};}
 let passed=false;
 if(!error){if(mission.kind==='rover'){const goal=options.goal||mission.goalAt;passed=state.x===goal[0]&&state.y===goal[1];}else if(mission.kind==='sort')passed=state.values.every((v,i,a)=>i===0||a[i-1]<=v);else if(mission.kind==='logic')passed=state.output===(state.a||state.b);else{const total=(options.samples||mission.samples).reduce((a,b)=>a+b,0);passed=state.total===total&&state.alert===(total>=mission.limit);}}
 const used=!mission.require||(metrics[mission.require]||0)>0;
 return {frames,state,error,metrics,passed:passed&&used,goalPassed:passed,used,line,variables};
}
export function evaluate(mission,source,options={}){
 const primary=simulate(mission,source,options);const tests=[];
 if(mission.kind==='logic')for(const a of [false,true])for(const b of [false,true]){const r=simulate(mission,source,{a,b});tests.push({label:`A=${Number(a)}, B=${Number(b)} → ${Number(a||b)}`,passed:r.passed});}
 else if(mission.kind==='energy')for(const samples of [[2,3],[3,5,2],[6,5],[]]){const r=simulate(mission,source,{samples});tests.push({label:`Total ${samples.reduce((a,b)=>a+b,0)} / limite ${mission.limit}`,passed:r.passed});}
 else if(mission.kind==='sort')for(const values of [mission.values,mission.alternative]){const r=simulate(mission,source,{values});tests.push({label:`Ordenar [${values.join(', ')}]`,passed:r.passed});}
 else{tests.push({label:'Alcançar a estação sem colisão',passed:primary.goalPassed&&!primary.error});tests.push({label:`Aplicar ${mission.topic.toLowerCase()}`,passed:primary.used&&!primary.error});}
 return {...primary,tests,passed:!primary.error&&tests.every(t=>t.passed)};
}
