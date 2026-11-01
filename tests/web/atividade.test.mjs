import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,readdirSync} from 'node:fs';
import {validateLesson,evaluatePractice,gradeQuestions,lessonQuestions} from '../../plataforma/atividade.mjs';
const root=new URL('../../data/',import.meta.url),files=readdirSync(root).filter(f=>/^conteudos-.*\.json$/.test(f));
const lessons=files.flatMap(f=>JSON.parse(readFileSync(new URL(f,root))));
test('todas as 447 unidades têm conteúdo temático próprio',()=>{assert.equal(lessons.length,447);assert.equal(new Set(lessons.map(l=>l.id)).size,447);});
for(const lesson of lessons){
 test(`${lesson.id}: conteúdo, questões, cenários e fontes coerentes`,()=>{assert.deepEqual(validateLesson(lesson),[]);assert.ok(gradeQuestions(lesson.questoes,lesson.questoes.map(q=>q.correta)).every(r=>r.passed));assert.ok(gradeQuestions(lesson.questoes,lesson.questoes.map(q=>(q.correta+1)%q.alternativas.length)).every(r=>!r.passed));assert.equal(lessonQuestions(lesson,1)[0],lesson.questoes[1]);});
 if(lesson.pratica.tipo==='numerica')test(`${lesson.id}: solução passa e esboço constante exige mudança`,()=>{assert.ok(new Set(lesson.pratica.casos.map(c=>JSON.stringify(c.esperado))).size>=2,'Casos devem exigir resultados diferentes');const r=evaluatePractice(lesson.pratica,lesson.pratica.solucao);assert.equal(r.passed,true,JSON.stringify(r.tests.filter(t=>!t.passed)));assert.equal(evaluatePractice(lesson.pratica,'function resolver(a,b){return 0;}').passed,false,'A prática não pode ser aprovada pelo esboço vazio.');});
}
test('executor temático mantém limitação de laços e bloqueia APIs do host',()=>{const p={tipo:'numerica',casos:[{entradas:{a:1,b:2},esperado:3}]};for(const code of ['function resolver(a,b){while(true){}}','function resolver(a,b){return fetch(a);}','function resolver(a,b){return document;}'])assert.equal(evaluatePractice(p,code).passed,false);});
