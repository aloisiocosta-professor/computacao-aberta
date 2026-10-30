# Publicação e continuidade

Nome provisório: computacao-aberta. Destino pretendido: perfil aloisiocosta-professor, repositório público novo. A conexão GitHub consultada não expôs operação para criar repositórios; nenhum repositório remoto foi criado, nem credencial foi lida. Não houve push, merge, tag, release ou execução remota.

O pacote contém os arquivos, histórico Git local e um git bundle. Para publicar, criar um repositório vazio com o nome escolhido e sem inicializar README/licença. Depois, no diretório do projeto, adicionar o remote confirmado e enviar main/develop. Não inserir tokens nos arquivos ou no histórico.

Exemplo de comandos após confirmar a URL do repositório vazio:

```bash
git remote add origin URL_CONFIRMADA_DO_REPOSITORIO
git push -u origin main
git push -u origin develop
```

Uma alternativa é usar o navegador com uma sessão GitHub já autenticada, mediante autorização para essa alternativa. A restrição é de capacidade da conexão atual, não de autorização para preparar este projeto.

CI: o workflow incluído valida estrutura local, sem instalar dependências nem baixar livros. A execução remota permanece pendente. Custos, quotas e políticas da conta devem ser conhecidos antes de habilitar serviços adicionais; nenhum serviço pago foi ativado.
