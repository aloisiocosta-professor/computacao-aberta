export const phases=['off','empty','ready','running','done'];
export const initial=()=>({phase:'off',pc:0,value:0});
export function transition(state,event){
 const s={...state};let message='',accepted=true;
 if(!invariant(s))return{state:initial(),accepted:false,message:'Estado inválido. O computador foi reiniciado.'};
 switch(event){
 case 'POWER_ON':if(s.phase==='off'){Object.assign(s,{phase:'empty',pc:0,value:0});message='Energia ligada. A RAM está vazia.';}else accepted=false;break;
 case 'LOAD':if(s.phase==='empty'){s.phase='ready';message='Três instruções foram copiadas do armazenamento para a RAM.';}else accepted=false;break;
 case 'START':if(s.phase==='ready'){s.phase='running';message='CPU pronta para buscar a primeira instrução.';}else accepted=false;break;
 case 'STEP':if(s.phase==='running'){
  if(s.pc===0){s.value+=2;s.pc=1;message='Instrução 1: acrescentar 2 ao acumulador.';}
  else if(s.pc===1){s.value*=3;s.pc=2;message='Instrução 2: multiplicar o acumulador por 3.';}
  else{s.pc=3;s.phase='done';message='Instrução 3: resultado 6 disponível na memória de saída.';}
 }else accepted=false;break;
 case 'POWER_OFF':if(s.phase!=='off'){Object.assign(s,initial());message='Energia desligada. RAM e estado da CPU foram limpos; o programa no armazenamento permanece.';}else accepted=false;break;
 case 'RESET':if(s.phase==='done'){Object.assign(s,{phase:'ready',pc:0,value:0});message='Programa permanece carregado. Acumulador e contador reiniciados.';}else accepted=false;break;
 default:accepted=false;
 }
 if(!accepted)message={POWER_ON:'O computador já está ligado.',LOAD:'Ligue o computador e carregue somente quando a RAM estiver vazia.',START:'Carregue o programa antes de iniciar.',STEP:'Inicie a execução antes de avançar uma instrução.',POWER_OFF:'O computador já está desligado.',RESET:'Conclua a execução antes de reiniciar o exercício.'}[event]||'Ação não disponível.';
 return {state:accepted?s:{...state},accepted,message};
}
export function invariant(s){return Boolean(s)&&phases.includes(s.phase)&&Number.isInteger(s.pc)&&s.pc>=0&&s.pc<=3&&[0,2,6].includes(s.value)&&(['off','empty','ready'].includes(s.phase)?s.pc===0&&s.value===0:s.phase==='done'?s.pc===3&&s.value===6:s.pc===0&&s.value===0||s.pc===1&&s.value===2||s.pc===2&&s.value===6);}
