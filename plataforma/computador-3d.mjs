import {initial,transition} from './maquina-computador.mjs';
/*
 * Computador por dentro — figura autoral da Computação Aberta.
 * Engine de projeção / materiais / câmera: Colorfigures, April Zhu, MIT.
 * Não utiliza geometria, texto ou imagens de Field Notes ou statechart-art.
 *
 * MODELO E VERDADE FÍSICA
 * Um gabinete convencional reúne placa-mãe, CPU e dissipador, RAM, armazenamento,
 * fonte e conexões. A posição exata e as dimensões aqui são ilustrativas: não são
 * planta de montagem nem simulação elétrica de uma marca. 1 unidade ≈ 1 cm.
 * Fontes de orientação: Intel, How to Build a Gaming PC; Kingston, Difference
 * Between Memory and Storage. A lista de fontes aparece no texto da figura.
 *
 * PROCESSO DIDÁTICO DECLARADO
 * SSD: conserva o programa [+2, ×3, STORE] enquanto o computador está desligado.
 * POWER_ON: fonte energizada, CPU e RAM voláteis zeradas, sem programa carregado.
 * LOAD: cópia conceitual das três instruções do SSD para a RAM. Não simula boot/OS.
 * START: CPU pronta para executar; valor inicial do acumulador = 0.
 * STEP 1: CPU busca na RAM e soma 2; STEP 2: multiplica por 3; STEP 3: STORE na RAM,
 * exibindo 6. STORE não grava no SSD. POWER_OFF limpa RAM e estado da CPU.
 * O barramento mostrado é uma conexão conceitual; não representa transistores,
 * caches, drivers, DMA, instruções de uma ISA ou ciclo real de clock.
 *
 * PEÇAS, APOIOS E LIMITES (x profundidade; +x frente; y largura; z altura)
 * Estrutura: mesa [0..128,0..104,0..3], pés do gabinete na mesa, piso/base do
 * gabinete [16..66,57..90,5..8], 4 montantes e painéis presos à base.
 * Placa-mãe: [21..61,59..61,18..70], presa a quatro espaçadores nos montantes.
 * CPU/soquete: [36..48,61..65,43..55], montados na placa; dissipador com 5 aletas
 * acima do soquete (em direção a +y); não flutua. RAM: dois DIMMs nos encaixes
 * [51..54,61..66,30..64] e [56..59,61..66,30..64], presos à placa.
 * SSD: [23..40,76..85,21..25] numa bandeja aparafusada à estrutura.
 * Fonte: [20..47,61..81,8..19], apoiada no piso do gabinete.
 * Conexões: conectores de fonte→placa e SSD→placa; pequenos segmentos sobre
 * suportes de piso/parede para ordenação correta; cabo de vídeo do painel traseiro
 * até porta do monitor via a mesa; cabo de teclado da porta USB até o teclado.
 * Monitor: base na mesa, coluna apoiada na base, corpo preso à coluna, tela em
 * +x. Teclado: 36 teclas apoiadas no corpo. Nenhuma peça deriva de assets externos.
 */
const pcBounds=[16,66,57,90,5,77];
const pcCaseProfile=rrUV(57,5,90,77,3.4,5);
const pcBoardBounds=boardTop(0,0,128,104,3,5);
const pcDark=matOf('#4b555b'),pcBoardMat=matOf('#6c9f87'),pcChip=matOf('#3f4b54');
const pcCopper=matOf('#cf9b60'),pcCream=matOf('#f7edcf'),pcViolet=matOf('#a99bc1');
const pcPhaseNames={off:'Desligado',empty:'Ligado, RAM vazia',ready:'Programa carregado',running:'Executando',done:'Resultado disponível'};
const pcParts=[
 {at:[42,70,50],text:'CPU',active:s=>s.phase==='running'},
 {at:[53,65,51],text:'RAM',active:s=>['ready','running','done'].includes(s.phase)},
 {at:[31,82,25],text:'ARMAZENAMENTO',active:s=>s.lastEvent==='LOAD'&&s.phase==='ready'},
 {at:[29,70,17],text:'FONTE',active:s=>s.phase!=='off'},
 {at:[29,61,33],text:'PLACA MAE',active:s=>s.phase!=='off'},
 {at:[46,74,26],text:'CONEXOES',active:s=>s.phase==='running'||s.phase==='ready'}
];
const pcEscape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pcCaseCorners=()=>[...on(PX(pcBounds[0]),pcCaseProfile),...on(PX(pcBounds[1]),pcCaseProfile)];
const pcWireBounds=points=>[0,1,2].map(i=>[Math.min(...points.map(p=>p[i]))-.6,Math.max(...points.map(p=>p[i]))+.6]);
function pcWirePieces(parts,points,colour,width=.7){
 for(let i=0;i<points.length-1;i++){
  const segment=[points[i],points[i+1]],ranges=pcWireBounds(segment);
  parts.push({box:[[ranges[0][0],ranges[1][0],ranges[2][0]],[ranges[0][1],ranges[1][1],ranges[2][1]]],svg:rod(segment[0],segment[1],width,matOf(colour),toneI,.55)});
 }
}
function pcAddBox(parts,x0,y0,z0,x1,y1,z1,material,w=.7,shade=toneI){parts.push({box:[[x0,y0,z0],[x1,y1,z1]],svg:box(x0,y0,z0,x1,y1,z1,material,shade,w)});}
function pcPanelText(x,y,z,text,size=3,colour=INK){return facing([1,0,0])?tx(x,y,z,pcEscape(text),size,colour,700):'';}
function pcInside(st){
 const parts=[],powered=st.phase!=='off',cpuActive=st.phase==='running',ramActive=['ready','running','done'].includes(st.phase);
 const boardColour=powered?pcBoardMat:matOf('#7c9183');
 pcAddBox(parts,16,57,5,66,90,8,METAL,1);
 // Vertical chassis uprights: four corner bars secured to the base, not solid walls.
 for(const x of [17,63])for(const y of [58,87])pcAddBox(parts,x,y,8,x+2,y+2,74,METAL,.6);
 // Motherboard on standoffs attached to the far mounting plane.
 for(const x of [23,58])for(const z of [21,66])pcAddBox(parts,x,57.7,z,x+1.6,59,z+1.6,pcCopper,.4);
 pcAddBox(parts,21,59,18,61,61,70,boardColour,.9);
 // Connector traces are split into segments and sorted by their actual bounds.
 for(const x of [28,32,36])pcWirePieces(parts,[[x,61.12,24],[x,61.12,38],[41,61.12,38]],'#c3bc71',.17);
 // CPU socket, die package and cooler: all fixed to the motherboard plane.
 pcAddBox(parts,35,61,42,49,62.2,56,METAL,.65);
 pcAddBox(parts,36.7,62.2,43.7,47.3,64.8,54.3,cpuActive?matOf('#efb757'):pcChip,.8);
 for(let z=44;z<=54;z+=2.5)pcAddBox(parts,35.4,64.8,z,48.6,71,z+1.05,METAL,.45);
 pcAddBox(parts,39,71,46,45,72,52,cpuActive?matOf('#d6b567'):pcDark,.5);
 // DIMMs extend out of their sockets. Contact strips meet the slots on the board.
 for(const x of [51,56]){
  pcAddBox(parts,x-.6,61,29,x+3.6,62.1,65,pcDark,.55);
  pcAddBox(parts,x,62.1,30,x+3,65.3,64,ramActive?matOf('#b9c69c'):pcBoardMat,.7);
  for(let z=33;z<=58;z+=8)pcAddBox(parts,x+.3,65.3,z,x+2.7,66,z+5,pcChip,.35);
  pcAddBox(parts,x-.5,62,28,x+3.5,65,29.3,pcCream,.4);
  pcAddBox(parts,x-.5,62,64.7,x+3.5,65,66,pcCream,.4);
 }
 // PSU rests on case floor; its terminal block faces toward the motherboard.
 pcAddBox(parts,20,61,8,47,81,19,pcDark,.9);
 pcAddBox(parts,45,62,13,48.2,67,17,pcCream,.45);
 for(let x=24;x<=39;x+=3)pcAddBox(parts,x,68,19.05,x+.7,77,19.35,METAL,.25);
 // SSD and tray: its three small program marks remain even when power is off.
 pcAddBox(parts,21,74,19,42,87,21,METAL,.55);
 pcAddBox(parts,23,76,21,40,85,25,pcViolet,.75);
 for(let x=26;x<=35;x+=4)pcAddBox(parts,x,78,25.05,x+2,82.5,25.25,pcCream,.3);
 pcAddBox(parts,39.4,76.8,21.6,41,80.6,23.8,pcCopper,.4);
 // Solid cable connectors are fixed to the SSD, motherboard and PSU respectively.
 pcAddBox(parts,43,61,23,48,63.2,27,pcCopper,.45);
 pcAddBox(parts,46,61,31,50,63,35,pcCream,.45);
 pcWirePieces(parts,[[40.5,78.3,23],[44,78.3,23],[46,74,23],[46,63,25]],st.lastEvent==='LOAD'&&st.phase==='ready'?'#f0b342':'#9c75b2',.65);
 pcWirePieces(parts,[[48,64,15],[50,64,15],[50,62,24],[48,62,33]],powered?'#c7884d':'#958478',.7);
 // Case exhaust fan: bracket and four spokes. No continuously moving decoration.
 pcAddBox(parts,18,70,57,20,84,71,pcDark,.6);
 const fanCenter=[20.15,77,64];
 parts.push({box:[[20,70.5,57.5],[21.1,83.5,70.5]],svg:cylX(20,21,77,64,5.5,METAL,toneI,.6,20)});
 for(const [dy,dz] of [[-4,0],[4,0],[0,-4],[0,4]]){
  const end=[21.15,77+dy,64+dz],ranges=pcWireBounds([fanCenter,end]);
  parts.push({box:[[ranges[0][0],ranges[1][0],ranges[2][0]],[ranges[0][1],ranges[1][1],ranges[2][1]]],svg:rod(fanCenter,end,.55,pcDark,toneI,.35)});
 }
 return byDepth(parts);
}
function pcCase(st,m){
 const x0=pcBounds[0],x1=pcBounds[1];
 let body=extrude(pcCaseProfile,x0,x1,m,tone);
 if(facing([1,0,0]))body+=shape(on(PX(x1),pcCaseProfile),tone([1,0,0],m),1.4);
 if(facing([-1,0,0]))body+=shape(on(PX(x0),pcCaseProfile),tone([-1,0,0],m),1.4);
 body+=hullInk(pcCaseCorners(),2.8);
 if(facing([0,1,0])){
  body+=shape(on(PY(90.12),rrUV(23,13,58,69,2.5,4)),mix(tone([0,1,0],m),'#ffffff',.08),.9);
  for(const x of [25,55])for(const z of [16,66])body+=shape(on(PY(90.2),ellUV(x,z,.8,.8,8)),METAL.m,.3);
  body+=txY(41,90.25,39,'ABERTA',4.8,mix(tone([0,1,0],m),'#000000',.25),700);
 }
 // Real rear plane: ports, vent and electrical connector, visible only from behind.
 if(facing([-1,0,0])){
  body+=shape(on(PX(15.8),rectUV(61,21,69,44)),METAL.m,.7);
  for(const z of [25,31,37])body+=shape(on(PX(15.7),rectUV(62,z,67,z+2.1)),pcDark.m,.4);
  body+=shape(on(PX(15.8),rectUV(75,10,85,16)),pcDark.m,.65);
  for(let z=53;z<=68;z+=3)body+=line([[15.72,72,z],[15.72,84,z]],.8);
 }
 return body;
}
function pcFront(st){
 const parts=[],powered=st.phase!=='off';
 // Mounted front panel follows depth ordering relative to the body when turned away.
 const panel=[67,60,12,67.7,86,68];
 pcAddBox(parts,...panel,pcCream,.8);
 let power=cylX(67.8,69.1,74,61,2.9,powered?matOf('#9fbe89'):pcDark,toneI,.7,20);
 power+=pcPanelText(69.2,74,60.2,powered?'I':'O',2.7,powered?'#314d35':'#f1e8d0');
 parts.push({box:[[67.8,70.9,57.9],[69.2,77.1,64.1]],svg:act('power',power)});
 if(facing([1,0,0])){
  parts.push({box:[[67.75,63,45],[68.1,83,55]],svg:shape(on(PX(67.8),rectUV(63,46,83,55)),'#273e3b',.7)+pcPanelText(67.94,73,49,st.phase==='off'?'OFF':st.phase==='done'?'RAM 6':st.phase==='running'?'CPU '+st.value:'ON',2.8,'#c8e3ae')});
  for(const y of [66,77])parts.push({box:[[67.8,y,36],[68.1,y+6,38]],svg:shape(on(PX(67.9),rectUV(y,36,y+6,38)),pcDark.m,.5)});
  parts.push({box:[[67.8,64,20],[68.1,82,30]],svg:pcPanelText(67.95,73,26,'COMPUTACAO',2.1)+pcPanelText(67.95,73,22,'ABERTA',2.7)});
 }
 return byDepth(parts);
}
function pcMonitor(st){
 const parts=[],powered=st.phase!=='off';
 pcAddBox(parts,75,16,3,94,42,6,pcDark,1);
 pcAddBox(parts,81,26,6,85,32,33,METAL,.75);
 pcAddBox(parts,80,5,31,87,53,69,pcDark,1.3);
 if(facing([1,0,0])){
  let screen=shape(on(PX(87.13),rectUV(8,34,50,66)),powered?'#d9e7d0':'#364848',.8);
  if(powered){
   screen+=pcPanelText(87.18,29,60,'PROGRAMA',3.3,'#405c4f');
   screen+=pcPanelText(87.18,29,49,st.phase==='done'?'6':st.phase==='running'?String(st.value):st.phase==='ready'?'PRONTO':'CARREGAR',st.phase==='done'||st.phase==='running'?9:3.3,'#345e4c');
   screen+=pcPanelText(87.18,29,39,st.phase==='done'?'SAIDA NA RAM':st.phase==='running'?'CPU / RAM':'0 + 2; x 3; STORE',2.25,'#58735e');
  }
  parts.push({box:[[87.1,8,34],[87.2,50,66]],svg:screen});
 }
 if(facing([-1,0,0]))parts.push({box:[[79.8,22,48],[80,37,58]],svg:shape(on(PX(79.9),rrUV(22,48,37,58,1)),METAL.m,.6)});
 return byDepth(parts);
}
function pcKeyboard(){
 const parts=[];
 pcAddBox(parts,103,8,3.1,122,53,6.5,pcCream,1.1);
 for(let row=0;row<4;row++)for(let col=0;col<9;col++)pcAddBox(parts,105+row*3.7,10+col*4.6,6.5,107.7+row*3.7,13.5+col*4.6,7.4,pcViolet,.3);
 return byDepth(parts);
}
function pcScene(st,m){
 const sceneParts=[],k=ease(st.xr||0);
 let svg=board(0,0,128,104,3,5,WOOD);
 svg+=castShadow([...pcCaseCorners(),[80,5,69],[87,53,69],[122,53,7]],3,pcBoardBounds);
 // Feet touch the board and support the chassis.
 for(const x of [20,58])for(const y of [61,83])pcAddBox(sceneParts,x,y,3,x+5,y+5,5,pcDark,.7);
 const shell=pcCase(st,m);
 let caseView=k>0?xrGhost(shell,'',k,pcCaseProfile,16,66,m)+`<g opacity="${f(k)}">${pcInside(st)}</g>`:shell;
 // Surface pieces are opaque and sorted together with the chassis as separate bodies.
 caseView=byDepth([
  {box:[[16,57,5],[66,90,77]],svg:caseView},
  {box:[[67,60,12],[69.2,86,68]],svg:pcFront(st)}
 ]);
 sceneParts.push({box:[[16,57,5],[69.2,90,77]],svg:caseView});
 sceneParts.push({box:[[75,5,3],[94,53,69]],svg:pcMonitor(st)});
 sceneParts.push({box:[[103,8,3.1],[122,53,7.4]],svg:pcKeyboard()});
 // Cables remain along the rear panel and on the board, with anchored endpoints.
 pcWirePieces(sceneParts,[[15.5,64,30],[12,64,30],[12,54,30],[12,54,4],[71,54,4],[78,50,4],[78,49,38],[80,49,38]],'#667c8d',.65);
 pcWirePieces(sceneParts,[[15.5,66,25],[11,66,25],[11,48,25],[11,48,4],[97,48,4],[102,48,5.2],[103,48,5.2]],'#9a8b6c',.55);
 pcWirePieces(sceneParts,[[15.5,80,13],[10,80,13],[10,95,13],[10,99,3.7],[5,99,3.7]],'#59626a',.8);
 svg+=byDepth(sceneParts);
 if(k>.6)svg+=xrCallouts(pcParts.map(p=>({at:p.at,text:p.text,on:p.active(st)})),pcBounds);
 else if(facing([1,0,0]))svg+=tag([69.2,74,61],12,-14,'ENERGIA',st.phase!=='off');
 return svg;
}
let pcLastMessage='Comece por Ligar. O programa permanece no armazenamento; CPU e RAM estão vazias.';
let pcAccepted=true;
function pcSend(st,event,ui){
 const result=transition({phase:st.phase,pc:st.pc,value:st.value},event);
 if(result.accepted){Object.assign(st,result.state);st.lastEvent=event;}
 pcLastMessage=result.message;pcAccepted=result.accepted;
 ui.render();
}
const pcUI=mountFigure({
 fig:'CA-01',title:'Computador por dentro',turn:'full',size:[128,104,82],palette:'mint',
 state:{...initial(),xr:0,xrT:0,lastEvent:null},scene:pcScene,
 readout:st=>`${pcPhaseNames[st.phase]} | instrucoes ${st.pc}/3 | acumulador ${st.value}`,
 stats:st=>[
  {label:'Estado',value:pcPhaseNames[st.phase],small:true},
  {label:'Instrucoes executadas',value:`${st.pc} / 3`,small:true},
  {label:'Acumulador da CPU',value:String(st.value),small:true}
 ],
 buttons:[
  {label:'1. Ligar',onClick:(st,ui)=>pcSend(st,'POWER_ON',ui)},
  {label:'2. Carregar programa',onClick:(st,ui)=>pcSend(st,'LOAD',ui)},
  {label:'3. Iniciar execucao',onClick:(st,ui)=>pcSend(st,'START',ui)},
  {label:'4. Executar um passo',onClick:(st,ui)=>pcSend(st,'STEP',ui)},
  {label:'5. Desligar',onClick:(st,ui)=>pcSend(st,'POWER_OFF',ui)},
  {label:'Reexecutar programa',onClick:(st,ui)=>pcSend(st,'RESET',ui)}
 ],
 acts:{power:(st,_el,ui)=>pcSend(st,st.phase==='off'?'POWER_ON':'POWER_OFF',ui)}
});
xrMount(()=>pcUI,()=> '');
// Keep all process actions as native buttons. The power shape is an optional
// pointer duplicate of the same action; no essential operation depends on it.
document.body.classList.add('computer-lesson');
const pcHeader=document.querySelector('header');
pcHeader.innerHTML='<h1 id="computer-heading" tabindex="-1">Computador por dentro</h1><nav aria-label="Navegação da figura"><a href="./">← Voltar à jornada</a></nav>';
const pcMain=document.createElement('main');pcMain.id='computer-main';
const pcIntro=document.createElement('div');pcIntro.className='intro';
pcIntro.innerHTML='<p><strong>Um programa, três instruções.</strong> Gire o computador, abra a vista interna e acompanhe a passagem do armazenamento para a RAM e a execução pela CPU. Use os botões na ordem indicada; ações fora de ordem explicam o que falta.</p><p>Arraste para girar, use as setas do teclado ou os controles de vista. O zoom altera apenas a visualização.</p>';
pcMain.append(pcIntro);
const pcStage=document.querySelector('.stage');
const pcViewSet=document.querySelector('.vset');
pcStage.insertBefore(pcViewSet,document.getElementById('fig'));
pcMain.append(pcStage,document.getElementById('readout'),document.querySelector('.mcap'),document.querySelector('.controls'));
pcMain.insertAdjacentHTML('beforeend',`
 <div class="machine-status" id="machine-feedback" role="status" aria-live="polite" aria-atomic="true"><strong>O que está acontecendo</strong><span id="machine-message"></span></div>
 <ol class="state-path" aria-label="Estados do programa">
  <li data-phase="off">Desligado<small>Sem estado volátil</small></li>
  <li data-phase="empty">Ligado<small>RAM vazia</small></li>
  <li data-phase="ready">Carregado<small>Programa na RAM</small></li>
  <li data-phase="running">Execução<small>CPU busca as instruções</small></li>
  <li data-phase="done">Resultado<small>6 na saída em RAM</small></li>
 </ol>
 <div class="lesson-columns">
  <section class="lesson-panel" aria-labelledby="program-title"><h2 id="program-title">O pequeno programa</h2>
   <table><caption>Acumulador começa em 0. Cada passo executa uma instrução do modelo.</caption><thead><tr><th scope="col">Passo</th><th scope="col">Instrução</th><th scope="col">Efeito</th></tr></thead><tbody>
    <tr data-instruction="0"><th scope="row">1</th><td><code>ADD 2</code></td><td>0 + 2 = 2 na CPU</td></tr>
    <tr data-instruction="1"><th scope="row">2</th><td><code>MUL 3</code></td><td>2 × 3 = 6 na CPU</td></tr>
    <tr data-instruction="2"><th scope="row">3</th><td><code>STORE</code></td><td>6 copiado para a saída em RAM</td></tr>
   </tbody></table>
   <p id="memory-description"></p>
  </section>
  <section class="lesson-panel" aria-labelledby="parts-title"><h2 id="parts-title">Peças e funções</h2>
   <p>Na vista interna, os rótulos identificam as peças. A lista continua disponível sem depender da imagem.</p>
   <ul class="part-list"><li>CPU: executa as instruções e mantém o acumulador.</li><li>RAM: guarda o programa carregado e a saída temporária.</li><li>Armazenamento: conserva o programa ao desligar.</li><li>Placa-mãe e conexões: interligam os componentes.</li><li>Fonte: fornece energia ao conjunto.</li><li>Monitor e teclado: saída e entrada representadas.</li></ul>
   <ol id="mobile-part-labels" class="part-list" aria-label="Correspondência dos rótulos numerados" hidden></ol>
  </section>
 </div>
 <details><summary>O que este modelo explica — e seus limites</summary>
  <p>Esta é uma representação autoral simplificada de um computador convencional, sem vínculo com um fabricante. A disposição das peças é ilustrativa. O exercício representa carregar instruções, executar operações e perder o estado volátil ao desligar; ele não simula inicialização real, sistema operacional, circuitos eletrônicos, caches, ciclo de clock ou o conjunto de instruções de uma CPU comercial.</p>
  <p>O programa de três instruções permanece conceitualmente no armazenamento. O comando <code>STORE</code> deste modelo escreve a saída em RAM; ele não salva o resultado no SSD. Desligar limpa o programa carregado, o acumulador e a saída em RAM. Reexecutar preserva o programa carregado, reiniciando contador e acumulador.</p>
  <p>Não há gravação de progresso, conta, coleta de dados ou serviço de IA. Os controles de cor, zoom, rótulos e câmera só modificam a apresentação. A máquina de estados do exercício limita as ações válidas.</p>
  <p class="sources">Orientação sobre componentes e memória: <a href="https://www.intel.com/content/www/us/en/gaming/resources/how-to-build-a-gaming-pc.html" target="_blank" rel="noopener">Intel — componentes de um PC</a>; <a href="https://www.kingston.com/en/blog/pc-performance/difference-between-memory-storage" target="_blank" rel="noopener">Kingston — memória e armazenamento</a>. Consulta parcial em 01/11/2026; não são instruções de montagem nem validação do modelo.</p>
 </details>
`);
document.body.insertBefore(pcMain,document.querySelector('footer'));
const pcFooter=document.querySelector('footer');
pcFooter.innerHTML='Figura autoral da Computação Aberta · Engine MIT de <a href="https://april-zhu.com/colorfigures" target="_blank" rel="noopener">Colorfigures / April Zhu ↗</a> · <a href="./vendor/colorfigures/LICENSE">Licença do engine</a>';
const pcSVG=document.getElementById('fig');pcSVG.setAttribute('aria-describedby','memory-description');
const pcLabelsControl=document.getElementById('lblctl');pcLabelsControl.hidden=true;
document.getElementById('xrb').textContent='Ver interior';
document.getElementById('lblb').textContent='Rótulos';
document.getElementById('vreset').textContent='Vista inicial';
document.getElementById('vspin').textContent='Rotação automática';
document.querySelector('label[for="wb"]').textContent='Traço ilustrado';
for(const label of document.querySelectorAll('.controls .ctl > label')){
 if(label.textContent==='Colour')label.textContent='Cor do gabinete';
 if(label.textContent==='View')label.textContent='Vista';
}
for(const b of document.querySelectorAll('#pals button'))b.setAttribute('aria-label','Cor do gabinete: '+({mustard:'amarelo',tomato:'vermelho',mint:'verde',cobalt:'azul',blush:'rosa'}[b.title]||b.title));
const pcZoomControl=document.createElement('div');pcZoomControl.className='ctl';
pcZoomControl.innerHTML='<label for="computer-zoom">Zoom da figura</label><input id="computer-zoom" type="range" min="75" max="160" step="5" value="100" aria-valuetext="100 por cento">';
document.querySelector('.controls').append(pcZoomControl);
const pcBaseView=pcSVG.getAttribute('viewBox').split(/\s+/).map(Number);
document.getElementById('computer-zoom').addEventListener('input',e=>{
 const scale=Number(e.target.value)/100,[x,y,w,h]=pcBaseView,nw=w/scale,nh=h/scale;
 pcSVG.setAttribute('viewBox',`${x+(w-nw)/2} ${y+(h-nh)/2} ${nw} ${nh}`);
 e.target.setAttribute('aria-valuetext',`${e.target.value} por cento`);pcUI.render();
});
// The standalone vendor engine is used without the single-file builder. Supply
// the engine's documented phone badge hook and a matching text legend here.
window.LBL_U=()=>matchMedia('(max-width:560px)').matches?pcSVG.viewBox.baseVal.width/Math.max(1,pcSVG.getBoundingClientRect().width):0;
const pcRenderBase=pcUI.render;
const pcLabelButton=document.getElementById('lblb'),pcToggleLabels=pcLabelButton.onclick;
pcLabelButton.onclick=()=>{pcToggleLabels();pcUI.render();};
pcUI.render=()=>{
 pcRenderBase();const st=pcUI.st;
 const message=document.getElementById('machine-message');if(message.textContent!==pcLastMessage)message.textContent=pcLastMessage;
 document.getElementById('machine-feedback').dataset.accepted=String(pcAccepted);
 for(const li of document.querySelectorAll('[data-phase]')){if(li.dataset.phase===st.phase)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current');}
 for(const tr of document.querySelectorAll('[data-instruction]'))tr.dataset.active=String(st.phase==='running'&&Number(tr.dataset.instruction)===st.pc||st.phase==='done'&&Number(tr.dataset.instruction)===2);
 const memText=st.phase==='off'?'Desligado: RAM e CPU vazias. O armazenamento conserva as três instruções.':st.phase==='empty'?'Ligado: a RAM está vazia. Carregue o programa para continuar.':st.phase==='done'?'Programa carregado na RAM. Saída em RAM: 6. Acumulador da CPU: 6.':`Programa carregado na RAM. Saída ainda não armazenada: 0. Acumulador da CPU: ${st.value}.`;
 const memory=document.getElementById('memory-description');if(memory.textContent!==memText)memory.textContent=memText;
 pcSVG.setAttribute('aria-label',`Computador didático 3D. Estado: ${pcPhaseNames[st.phase]}. Instruções executadas: ${st.pc} de 3. Acumulador: ${st.value}.`);
 const mobileLegend=document.getElementById('mobile-part-labels');
 mobileLegend.hidden=!(matchMedia('(max-width:560px)').matches&&st.xr>.6&&!document.documentElement.classList.contains('nolabels'));
 if(!mobileLegend.hidden){const tags=[...pcSVG.querySelectorAll('.tag[data-n]')].map(t=>({n:Number(t.dataset.n),text:t.dataset.t,on:t.classList.contains('on')})).sort((a,b)=>a.n-b.n);mobileLegend.innerHTML=tags.map(t=>`<li value="${t.n}" data-active="${t.on}">${pcEscape(t.text)}</li>`).join('');}
};
if(matchMedia('(prefers-reduced-motion:reduce)').matches){
 document.getElementById('xrb').onclick=()=>{const st=pcUI.st;st.xrT=st.xrT?0:1;st.xr=st.xrT;document.getElementById('xrb').setAttribute('aria-pressed',String(Boolean(st.xrT)));pcUI.render();};
 document.getElementById('vreset').onclick=()=>{setCam(YAW0,PITCH0);pcUI.render();};
 const turnButton=document.getElementById('vspin');turnButton.textContent='Girar 30 graus';turnButton.removeAttribute('aria-pressed');turnButton.onclick=()=>{setCam(YAW+30,PITCH);pcUI.render();};
 addEventListener('keydown',e=>{const delta={ArrowLeft:[-15,0],ArrowRight:[15,0],ArrowUp:[0,8],ArrowDown:[0,-8]}[e.key];if(!delta||/input|textarea|select/i.test(e.target.tagName))return;e.preventDefault();e.stopImmediatePropagation();setCam(YAW+delta[0],PITCH+delta[1]);pcUI.render();},{capture:true});
}
addEventListener('resize',()=>pcUI.render());
pcUI.render();
