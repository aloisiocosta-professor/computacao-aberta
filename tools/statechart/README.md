# Statechart local

Scripts oficiais de https://github.com/cursor/plugins/tree/main/pstack/skills/statechart, commit ae5650febf4320793844c12c4adaa937f417f8da. Licença MIT, Lauren Tan (2026), preservada em LICENSE. Não há serviço externo nem skill global statechart instalada.

Requer Node 24 com TypeScript nativo e Java >=11. O CLI oficial aceita JAVA e TLA2TOOLS para usar instalações existentes. TLC v1.7.4, arquivo oficial https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar, SHA256 936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88.

```sh
TLA2TOOLS=/caminho/tla2tools.jar JAVA=/usr/bin/java tools/statechart/scripts/statechart models/Computador.tla --view models/view.mjs --out /tmp/computador-verificado
```

A saída precisa ser uma pasta nova. Resultado desta execução em docs/statecharts/: 7 estados, 13 transições, TypeOK, VolatileReset, ResultOK, ExecutionOK e ausência de deadlock. Não é uma prova de hardware real nem de toda a plataforma. Runtime separado em plataforma/maquina-computador.mjs e testes exploram todos os estados/eventos, inclusive eventos inválidos.
