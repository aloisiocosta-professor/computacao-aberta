/* Interpretador limitado de sintaxe JavaScript. Não usa eval ou Function. */
export class CodeError extends Error {
  constructor(message, line=1) {super(message);this.line=line;}
}
export function tokenize(source) {
  if(source.length>6000) throw new CodeError('Use até 6.000 caracteres por tentativa.');
  const tokens=[]; let i=0,line=1;
  while(i<source.length){
    const c=source[i];
    if(/\s/.test(c)){if(c==='\n')line++;i++;continue;}
    if(source.slice(i,i+2)==='//'){while(i<source.length&&source[i]!=='\n')i++;continue;}
    const match=source.slice(i).match(/^(?:\d+(?:\.\d+)?|[a-zA-Z_$][\w$]*|===|!==|<=|>=|==|!=|\+\+|--|\+=|-=|&&|\|\||[{}();,+\-*/%!=<>])/);
    if(!match) throw new CodeError(`Símbolo não suportado: ${c}. Abra a referência de comandos.`,line);
    tokens.push({v:match[0],line});i+=match[0].length;
    if(tokens.length>2000)throw new CodeError('Programa muito longo para este laboratório.',line);
  }
  tokens.push({v:'EOF',line});return tokens;
}
export function parse(source){
  const ts=tokenize(source);let p=0,depth=0;
  const token=()=>ts[p];
  const eat=(v)=>{const t=ts[p];if(v&&t.v!==v)throw new CodeError(`Esperado “${v}”, encontrado “${t.v}”.`,t.line);p++;return t;};
  const match=v=>token().v===v;
  function name(){const t=eat();if(!/^[a-zA-Z_$][\w$]*$/.test(t.v)||['let','const','function','if','else','for','while','return','true','false','new','this'].includes(t.v))throw new CodeError('Esperado um nome de variável ou função.',t.line);return t.v;}
  const precedence={'||':1,'&&':2,'==':3,'!=':3,'===':3,'!==':3,'<':4,'>':4,'<=':4,'>=':4,'+':5,'-':5,'*':6,'/':6,'%':6};
  function expression(min=0){
    if(++depth>50)throw new CodeError('Expressão muito aninhada.',token().line);
    const t=eat();let a;
    if(t.v==='('){a=expression();eat(')');}
    else if(['!','-','+'].includes(t.v))a={kind:'unary',op:t.v,a:expression(7),line:t.line};
    else if(/^\d/.test(t.v))a={kind:'value',value:Number(t.v),line:t.line};
    else if(['true','false'].includes(t.v))a={kind:'value',value:t.v==='true',line:t.line};
    else if(/^[a-zA-Z_$][\w$]*$/.test(t.v)){
      if(match('(')){eat('(');const args=[];if(!match(')')){do{args.push(expression());if(!match(','))break;eat(',');}while(true);}eat(')');a={kind:'call',name:t.v,args,line:t.line};}
      else a={kind:'name',name:t.v,line:t.line};
    }else throw new CodeError(`Expressão inesperada: ${t.v}.`,t.line);
    while(precedence[token().v]>=min){const op=eat();a={kind:'binary',op:op.v,a,b:expression(precedence[op.v]+1),line:op.line};}
    depth--;return a;
  }
  function simple(){
    const line=token().line;
    if(match('let')||match('const')){const constant=eat().v==='const';const id=name();eat('=');return {kind:'declare',name:id,constant,value:expression(),line};}
    if(/^[a-zA-Z_$]/.test(token().v)&&['=','+=','-=','++','--'].includes(ts[p+1]?.v)){
      const id=name(),op=eat().v;return {kind:'assign',name:id,op,value:['++','--'].includes(op)?{kind:'value',value:1,line}:expression(),line};
    }
    return {kind:'expression',value:expression(),line};
  }
  function statement(){
    if(++depth>50)throw new CodeError('Blocos muito aninhados.',token().line);
    const line=token().line;let node;
    if(match('{')){eat('{');const body=[];while(!match('}')){if(match('EOF'))throw new CodeError('Falta fechar uma chave “}”.',line);body.push(statement());}eat('}');node={kind:'block',body,line};}
    else if(match('for')){eat();eat('(');const init=simple();eat(';');const test=expression();eat(';');const update=simple();eat(')');node={kind:'for',init,test,update,body:statement(),line};}
    else if(match('while')){eat();eat('(');const test=expression();eat(')');node={kind:'while',test,body:statement(),line};}
    else if(match('if')){eat();eat('(');const test=expression();eat(')');const yes=statement();let no=null;if(match('else')){eat();no=statement();}node={kind:'if',test,yes,no,line};}
    else if(match('function')){eat();const id=name();eat('(');const params=[];if(!match(')')){do{params.push(name());if(!match(','))break;eat(',');}while(true);}eat(')');const body=statement();if(body.kind!=='block')throw new CodeError('Uma função precisa de um bloco entre chaves.',line);node={kind:'function',name:id,params,body,line};}
    else if(match('return')){eat();node={kind:'return',value:match(';')?{kind:'value',value:0,line}:expression(),line};eat(';');}
    else if(match(';')){eat();node={kind:'empty',line};}
    else{node=simple();eat(';');}
    depth--;return node;
  }
  const body=[];while(!match('EOF'))body.push(statement());return {kind:'block',body,line:1};
}
class Env {
  constructor(parent=null){this.parent=parent;this.values=new Map();this.constants=new Set();}
  get(name,line){if(this.values.has(name))return this.values.get(name);if(this.parent)return this.parent.get(name,line);throw new CodeError(`“${name}” não foi definido.`,line);}
  declare(name,value,constant,line){if(this.values.has(name))throw new CodeError(`“${name}” já existe neste bloco.`,line);this.values.set(name,value);if(constant)this.constants.add(name);}
  set(name,value,line){if(this.values.has(name)){if(this.constants.has(name))throw new CodeError(`“${name}” é constante.`,line);this.values.set(name,value);}else if(this.parent)this.parent.set(name,value,line);else throw new CodeError(`Declare “${name}” com let antes de usar.`,line);}
  snapshot(){return Object.fromEntries([...this.parent?Object.entries(this.parent.snapshot()):[],...this.values].filter(([,v])=>typeof v==='number'||typeof v==='boolean'));}
}
export function interpret(source,api={},onStep=()=>{}){
  const tree=parse(source),env=new Env();let ops=0,callDepth=0;
  const metrics={loops:0,conditions:0,functionCalls:0,variableReads:0};
  const tick=(n,e)=>{if(++ops>3000)throw new CodeError('Limite de execução. Confira a condição do laço.',n.line);onStep(n.line,e.snapshot());};
  const numeric=(n,line)=>{if(typeof n!=='number'||!Number.isFinite(n)||Math.abs(n)>1e9)throw new CodeError('Use um número finito de até um bilhão.',line);return n;};
  function value(n,e){
    tick(n,e);
    if(n.kind==='value')return n.value;
    if(n.kind==='name'){metrics.variableReads++;return e.get(n.name,n.line);}
    if(n.kind==='unary'){const a=value(n.a,e);return n.op==='!'?!a:n.op==='-'?-numeric(a,n.line):numeric(a,n.line);}
    if(n.kind==='binary'){
      const a=value(n.a,e);if(n.op==='&&')return a&&value(n.b,e);if(n.op==='||')return a||value(n.b,e);const b=value(n.b,e);
      if(['==','==='].includes(n.op))return a===b;if(['!=','!=='].includes(n.op))return a!==b;
      numeric(a,n.line);numeric(b,n.line);
      if(n.op==='<')return a<b;if(n.op==='>')return a>b;if(n.op==='<=')return a<=b;if(n.op==='>=')return a>=b;
      return numeric(n.op==='+'?a+b:n.op==='-'?a-b:n.op==='*'?a*b:n.op==='/'?a/b:a%b,n.line);
    }
    if(n.kind==='call'){
      const args=n.args.map(x=>value(x,e));
      if(Object.hasOwn(api,n.name))return api[n.name](...args);
      const fn=e.get(n.name,n.line);if(!fn||fn.kind!=='function')throw new CodeError(`“${n.name}” não é uma função disponível.`,n.line);
      if(++callDepth>24)throw new CodeError('Muitas chamadas de função. Verifique a recursão.',n.line);
      if(args.length!==fn.params.length)throw new CodeError(`“${n.name}” espera ${fn.params.length} argumentos.`,n.line);
      metrics.functionCalls++;const local=new Env(fn.env);fn.params.forEach((p,i)=>local.declare(p,args[i],false,n.line));const r=exec(fn.body,local);callDepth--;return r?.returned?r.value:0;
    }
    throw new CodeError('Expressão não suportada.',n.line);
  }
  function exec(n,e){
    tick(n,e);
    if(n.kind==='block'){const local=new Env(e);for(const child of n.body){const r=exec(child,local);if(r?.returned)return r;}return;}
    if(n.kind==='declare')e.declare(n.name,value(n.value,e),n.constant,n.line);
    else if(n.kind==='assign'){const b=value(n.value,e);const a=n.op==='='?0:e.get(n.name,n.line);e.set(n.name,n.op==='='?b:n.op==='--'||n.op==='-='?numeric(a,n.line)-numeric(b,n.line):numeric(a,n.line)+numeric(b,n.line),n.line);}
    else if(n.kind==='expression')value(n.value,e);
    else if(n.kind==='function')e.declare(n.name,{...n,env:e},true,n.line);
    else if(n.kind==='return')return {returned:true,value:value(n.value,e)};
    else if(n.kind==='if'){metrics.conditions++;return exec(value(n.test,e)?n.yes:n.no||{kind:'empty',line:n.line},e);}
    else if(n.kind==='for'){const local=new Env(e);exec(n.init,local);while(value(n.test,local)){metrics.loops++;const r=exec(n.body,local);if(r?.returned)return r;exec(n.update,local);}}
    else if(n.kind==='while'){while(value(n.test,e)){metrics.loops++;const r=exec(n.body,e);if(r?.returned)return r;}}
  }
  exec(tree,env);return {metrics,operations:ops};
}
