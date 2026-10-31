import test from 'node:test';
import assert from 'node:assert/strict';
import {interpret,parse} from '../../plataforma/engine.mjs';
import {missions,byId} from '../../plataforma/missions.mjs';
import {evaluate} from '../../plataforma/simulation.mjs';
const solutions={
 variaveis:'let passos = 3; mover(passos);',
 repeticao:'for(let i=0;i<4;i++){mover();}',
 decisoes:'for(let i=0;i<7;i++){if(livre()){mover();}else{virarDireita();}}',
 funcoes:'function avancar(n){for(let i=0;i<n;i++){mover();}} avancar(3); virarDireita(); avancar(3);',
 ordenacao:'for(let rodada=0;rodada<tamanho();rodada++){for(let i=0;i<tamanho()-1;i++){if(valor(i)>valor(i+1)){trocar(i,i+1);}}}',
 circuito:'let a=entradaA();let b=entradaB();saida(a||b);',
 consumo:'let total=0;for(let i=0;i<amostras();i++){total+=consumo(i);}registrar(total);alertar(total>=limite());'
};
for(const m of missions){
 test(`desafio ${m.id}: solução atende cenários`,()=>{const r=evaluate(m,solutions[m.id]);assert.equal(r.error,null,JSON.stringify(r.error));assert.equal(r.passed,true,JSON.stringify(r.tests));assert.ok(r.frames.length>1);});
 test(`desafio ${m.id}: início exige uma mudança`,()=>assert.equal(evaluate(m,m.starter).passed,false));
}
test('laço infinito é interrompido',()=>{assert.throws(()=>interpret('while(true){}'),/Limite de execução/);});
test('recursão é limitada',()=>{assert.throws(()=>interpret('function f(){f();} f();'),/recursão/);});
test('código longo é rejeitado antes de interpretar',()=>assert.throws(()=>parse(' '.repeat(6001)),/6.000/));
test('DOM e rede não estão no ambiente',()=>{assert.throws(()=>interpret('fetch(1);'),/não foi definido/);assert.throws(()=>interpret('document.body;'),/Símbolo não suportado/);});
test('cadeia constructor/prototype não é acessível',()=>assert.throws(()=>interpret('registrar.constructor(1);'),/Símbolo não suportado/));
test('divisão por zero é rejeitada',()=>assert.throws(()=>interpret('let x=1/0;'),/finito/));
test('const não pode ser reatribuída',()=>assert.throws(()=>interpret('const x=1;x=2;'),/constante/));
test('curto circuito preserva o fluxo',()=>{let calls=0;interpret('if(false && tocar()){tocar();}',{tocar:()=>calls++});assert.equal(calls,0);});
test('função retorna um valor e preserva escopo',()=>{const out=[];interpret('let x=2; function soma(n){let x=3;return n+x;} registrar(soma(x)); registrar(x);',{registrar:n=>out.push(n)});assert.deepEqual(out,[5,2]);});
test('erro de sintaxe preserva número da linha',()=>assert.throws(()=>parse('let x=1;\nlet y=;'),e=>e.line===2));
test('colisão não aprova o desafio e preserva passos anteriores',()=>{const r=evaluate(byId('variaveis'),'let n=8;mover(n);');assert.ok(r.error);assert.equal(r.passed,false);assert.ok(r.frames.length>1);});
test('caso fronteira do consumo detecta > em vez de >=',()=>{const r=evaluate(byId('consumo'),byId('consumo').starter);assert.equal(r.tests[1].passed,false);assert.equal(r.tests[0].passed,true);assert.equal(r.tests[2].passed,true);assert.equal(r.tests[3].passed,true);});
test('não basta escrever a construção sem usá-la',()=>assert.equal(evaluate(byId('repeticao'),'if(false){for(let i=0;i<4;i++){mover();}} mover(4);').passed,false));

test('desafios vinculam unidades reais do currículo',async()=>{const {readFile}=await import('node:fs/promises');const skills=JSON.parse(await readFile(new URL('../../data/habilidades.json',import.meta.url),'utf8'));for(const m of missions)assert.ok(skills.some(h=>h.id===m.unit&&h.disciplina===m.discipline),m.id);});

test('erro de argumento indica a linha do comando',()=>{assert.equal(evaluate(byId('variaveis'),'let n=9;\nmover(n);').error.line,2);});
