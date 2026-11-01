export const title='Computador didático: um programa de três instruções';
export const state=v=>({off:'Desligado',empty:'Ligado, RAM vazia',ready:'Programa na RAM',running:`Executando: etapa ${v.pc+1}, valor ${v.value}`,done:'Resultado 6 na RAM'})[v.phase];
export const step=action=>({PowerOn:'você liga',Load:'você carrega o programa',Start:'você inicia',Add:'somar 2',Multiply:'multiplicar por 3',Store:'armazenar resultado',PowerOff:'você desliga',Reset:'você reinicia o exercício'})[action]||action;
export const group=v=>v.phase;
export const colors={off:'tan',empty:'yellow',ready:'blue',running:'teal',done:'teal'};
