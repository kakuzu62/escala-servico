# 📚 GUIA COMPLETO DE INSTALAÇÃO E USO - SISTEMA DE ESCALA DE SERVIÇO

## 🎯 ÍNDICE
1. [Instalação do Git](#instalação-do-git)
2. [Clonar o Repositório](#clonar-o-repositório)
3. [Configurar MySQL](#configurar-mysql)
4. [Configurar Python e Dependências](#configurar-python-e-dependências)
5. [Executar o Programa](#executar-o-programa)
6. [Usar o Sistema](#usar-o-sistema)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 INSTALAÇÃO DO GIT

### Windows
1. Abra o navegador (Chrome, Firefox, Edge, etc.)
2. Acesse: `https://git-scm.com/download/win`
3. Clique em "Click here to download manually" (em azul)
4. Após baixar, abra o arquivo `.exe` que foi baixado
5. Clique em "Next" > "Next" > "Next" até terminar
6. Selecione a opção "Use Git from the Windows Command Prompt" e clique "Next"
7. Clique em "Install" e aguarde a instalação
8. Clique em "Finish"

### Linux (Ubuntu/Debian)
1. Abra o Terminal
2. Digite o comando:
```bash
sudo apt update
sudo apt install git
```
3. Pressione Enter e digite sua senha quando solicitado

### macOS
1. Abra o Terminal
2. Digite o comando:
```bash
brew install git
```
3. Se não tiver Homebrew instalado, acesse: `https://brew.sh` e siga as instruções

---

## 📥 CLONAR O REPOSITÓRIO

### Windows
1. Crie uma pasta chamada "Projetos" no seu Desktop
2. Clique com o botão direito dentro da pasta vazia
3. Selecione "Git Bash Here" (se não aparecer, seu Git não foi instalado corretamente)
4. Uma janela preta aparecerá
5. Digite o comando:
```bash
git clone https://github.com/kakuzu62/escala-servico.git
```
6. Pressione Enter
7. Aguarde a conclusão (verá mensagens na tela)
8. Digite:
```bash
cd escala-servico
```
9. Pressione Enter

### Linux/macOS
1. Abra o Terminal
2. Digite:
```bash
mkdir ~/Projetos
cd ~/Projetos
git clone https://github.com/kakuzu62/escala-servico.git
cd escala-servico
```
3. Pressione Enter após cada comando

---

## 🗄️ CONFIGURAR MYSQL

### Passo 1: Instalar MySQL

#### Windows
1. Acesse: `https://dev.mysql.com/downloads/mysql/`
2. Procure por "MySQL Community Server"
3. Clique no botão verde "Download"
4. Clique em "No thanks, just start my download"
5. Abra o arquivo `.msi` que foi baixado
6. Clique em "Next" > "Accept License" > "Next"
7. Selecione "Server only" e clique "Next"
8. Clique "Next" > "Next" até chegar em "MySQL Server 8.0"
9. Escolha "Standalone MySQL Server / Classic MySQL Server" > "Next"
10. Em "Config Type", deixe "Development Computer" selecionado > "Next"
11. Deixe a porta como `3306` > "Next"
12. Clique "Next" > "Add MySQL Server to Windows Service" > "Next"
13. Em "MySQL Server User Configuration", selecione "Use Legacy Authentication Method" > "Next"
14. Digite uma senha para o usuário root (ex: 123456) > "Next"
15. Clique em "Execute" > "Finish" > "Finish"

#### Linux (Ubuntu/Debian)
1. Abra o Terminal
2. Digite:
```bash
sudo apt update
sudo apt install mysql-server
```
3. Pressione Enter e digite sua senha
4. Quando perguntado "Do you want to continue?", digite `y` e pressione Enter

#### macOS
1. Abra o Terminal
2. Digite:
```bash
brew install mysql
brew services start mysql
```
3. Pressione Enter

### Passo 2: Acessar MySQL e Criar o Banco de Dados

#### Windows
1. Pressione `Windows + R`
2. Digite `cmd` e pressione Enter
3. Digite:
```bash
mysql -u root -p
```
4. Pressione Enter
5. Digite a senha que você definiu (ex: 123456) e pressione Enter
6. O prompt mudará para `mysql>`

#### Linux/macOS
1. Abra o Terminal
2. Digite:
```bash
mysql -u root -p
```
3. Pressione Enter
4. Digite a senha (se não tiver definido, só pressione Enter) e pressione Enter
5. O prompt mudará para `mysql>`

### Passo 3: Executar o Script SQL

1. Você está no prompt `mysql>`
2. Abra o arquivo `database/schema.sql` com um editor de texto (Bloco de Notas, VS Code, etc.)
3. Copie TODO o conteúdo do arquivo
4. Volte para o prompt do MySQL
5. Cole o conteúdo (Ctrl + V ou Cmd + V)
6. Pressione Enter
7. Aguarde a execução (levará alguns segundos)
8. Deve aparecer "Query OK" várias vezes
9. Digite:
```sql
exit
```
10. Pressione Enter para sair do MySQL

### Passo 4: Configurar Credenciais

1. Abra a pasta do projeto com um editor (VS Code recomendado)
2. Procure pela pasta `config`
3. Abra o arquivo `config.ini`
4. Procure pela seção `[DATABASE]`
5. Altere as linhas:
```ini
host = localhost
port = 3306
user = root
password = 123456        <- ALTERE PARA SUA SENHA DO MYSQL
database = escala_servico
```
6. Salve o arquivo (Ctrl + S ou Cmd + S)

---

## 🐍 CONFIGURAR PYTHON E DEPENDÊNCIAS

### Passo 1: Verificar Instalação do Python

#### Windows
1. Pressione `Windows + R`
2. Digite `cmd` e pressione Enter
3. Digite:
```bash
python --version
```
4. Pressione Enter
5. Deve aparecer algo como "Python 3.9.0" ou superior
6. Se aparecer "comando não encontrado", instale Python em: `https://www.python.org/downloads/`

#### Linux/macOS
1. Abra o Terminal
2. Digite:
```bash
python3 --version
```
3. Pressione Enter
4. Deve aparecer a versão do Python

### Passo 2: Criar Ambiente Virtual

#### Windows
1. Abra a pasta do projeto no Command Prompt
2. Navegue para a pasta do projeto:
```bash
cd C:\Users\SeuUsuario\Projetos\escala-servico
```
3. Digite:
```bash
python -m venv venv
```
4. Pressione Enter
5. Aguarde alguns minutos (uma pasta `venv` será criada)

#### Linux/macOS
1. Abra o Terminal
2. Navegue para a pasta do projeto:
```bash
cd ~/Projetos/escala-servico
```
3. Digite:
```bash
python3 -m venv venv
```
4. Pressione Enter
5. Aguarde alguns minutos

### Passo 3: Ativar Ambiente Virtual

#### Windows
1. No Command Prompt (ainda na pasta do projeto), digite:
```bash
venv\Scripts\activate
```
2. Pressione Enter
3. O prompt deve mudar para `(venv) C:\...` (note o "(venv)" no início)

#### Linux/macOS
1. No Terminal (ainda na pasta do projeto), digite:
```bash
source venv/bin/activate
```
2. Pressione Enter
3. O prompt deve mudar para `(venv) user@machine:...` (note o "(venv)" no início)

### Passo 4: Instalar Dependências - SOLUÇÃO PARA O ERRO

⚠️ **SE VOCÊ RECEBEU O ERRO SOBRE "openPyXL" ou "versões yanked":**

Este erro ocorre porque algumas versões antigas dos pacotes foram removidas. Siga estes passos:

#### Solução Rápida (Recomendada):

1. Com o ambiente virtual ativado (veja o "(venv)" no prompt)
2. Digite ESTE comando (para atualizar o pip):
```bash
python -m pip install --upgrade pip
```
3. Pressione Enter e aguarde

4. Agora digite:
```bash
pip install PyQt5==5.15.9 PyQt5-sip==12.13.0 mysql-connector-python==8.2.0 python-dotenv==1.0.0 reportlab==4.0.9 openpyxl==3.14.0 pandas==2.1.3 PyInstaller==6.5.0
```
5. Pressione Enter

6. Aguarde até ver "Successfully installed" com todos os pacotes

#### Se Ainda Não Funcionar:

1. Delete o arquivo `requirements.txt` (se quiser)
2. Digite este comando:
```bash
pip install --no-cache-dir PyQt5 mysql-connector-python pandas reportlab PyInstaller
```
3. Aguarde a instalação

---

## ▶️ EXECUTAR O PROGRAMA

### Windows
1. Abra o Command Prompt na pasta do projeto
2. Certifique-se de que o ambiente virtual está ativado (veja "(venv)" no prompt)
3. Digite:
```bash
python main.py
```
4. Pressione Enter
5. A janela do programa deve aparecer em alguns segundos

### Linux/macOS
1. Abra o Terminal na pasta do projeto
2. Certifique-se de que o ambiente virtual está ativado (veja "(venv)" no prompt)
3. Digite:
```bash
python main.py
```
4. Pressione Enter
5. A janela do programa deve aparecer em alguns segundos

---

## 💻 USAR O SISTEMA

### Primeira Execução - Criar Usuário Admin

#### Opção 1: Via MySQL (Recomendado)
1. Abra o MySQL (conforme instruções acima)
2. Digite:
```sql
INSERT INTO usuarios (nome, email, senha, perfil, ativo) VALUES 
('Administrador', 'admin@escala.com', SHA2('admin123', 256), 'administrador', TRUE);
```
3. Pressione Enter
4. Saia do MySQL digitando `exit`

#### Opção 2: Dentro do Programa
- Será necessário criar opção de cadastro no próximo update

### Login no Sistema

1. A janela do programa abrirá mostrando a tela de Login
2. Digite o email: `admin@escala.com`
3. Digite a senha: `admin123`
4. Clique em "Entrar"
5. Pronto! Você está dentro do sistema

---

## 📖 GUIA DE USO DO SISTEMA

### Aba: Escalas

#### Criar Nova Escala
1. Clique na aba "Escalas"
2. Clique no botão "Criar Nova Escala"
3. Selecione a função no dropdown "Função"
4. Selecione a pessoa no dropdown "Pessoa"
5. Escolha a data no calendário "Data"
6. Clique em "Criar"
7. Mensagem de sucesso deve aparecer

#### Listar e Filtrar Escalas
1. Clique na aba "Escalas"
2. Clique em "Listar Escalas com Filtros"
3. A janela de listagem abrirá
4. Aplique filtros:
   - **Função**: Selecione a função desejada ou deixe "Todas"
   - **Pessoa**: Selecione a pessoa ou deixe "Todas"
   - **Tipo**: Selecione "Preta", "Vermelha" ou "Todas"
   - **Data Início**: Escolha a data inicial
   - **Data Fim**: Escolha a data final
5. Clique em "Filtrar"
6. Os resultados aparecerão na tabela

#### Editar Escala
1. Na janela de listagem, clique em uma linha da tabela para selecioná-la
2. Clique em "Editar"
3. A janela de edição abrirá
4. Altere os dados desejados
5. Clique em "Salvar"
6. A escala será atualizada

#### Deletar Escala
1. Na janela de listagem, clique em uma linha da tabela para selecioná-la
2. Clique em "Deletar"
3. Uma mensagem de confirmação aparecerá
4. Clique em "Sim" para confirmar
5. A escala será deletada

---

### Aba: Funções

#### Criar Nova Função
1. Clique na aba "Funções"
2. Clique em "Criar Nova Função"
3. Digite o nome da função (ex: "Médico", "Enfermeiro", "Técnico")
4. Digite a descrição (opcional)
5. Clique em "Criar"
6. Mensagem de sucesso deve aparecer

---

### Aba: Pessoas

#### Adicionar Nova Pessoa
1. Clique na aba "Pessoas"
2. Clique em "Adicionar Pessoa"
3. Preencha os campos:
   - **Nome**: Nome completo da pessoa
   - **Email**: Email da pessoa (opcional)
   - **Telefone**: Telefone da pessoa (opcional)
   - **Função**: Selecione a função no dropdown
4. Clique em "Adicionar"
5. Mensagem de sucesso deve aparecer

---

### Aba: Relatórios

#### Gerar Relatório
1. Clique na aba "Relatórios"
2. Clique em "Gerar Relatório"
3. Escolha a data desejada no calendário
4. Clique em "Gerar"
5. A tabela será preenchida com as escalas do dia
6. As colunas mostram: Função | Pessoa | Tipo Escala

#### Exportar para PDF
1. Na janela de relatório, após gerar o relatório
2. Clique em "Exportar PDF"
3. Um arquivo PDF será salvo na pasta do projeto
4. Nome do arquivo: `Relatorio_Escala_DD_MM_YYYY.pdf`

---

### Menu: Dashboard (Novo)

#### Acessar Dashboard
1. Clique no menu "Arquivo"
2. Clique em "Dashboard" (se não aparecer, será adicionado em breve)
3. A janela do dashboard abrirá com 5 abas

#### Aba: Estatísticas Gerais
1. Mostra:
   - Total de Funções
   - Total de Pessoas
   - Escalas deste mês
   - Afastamentos ativos

#### Aba: Escalas por Função
1. Tabela com:
   - Nome da Função
   - Total de Escalas
2. Ordenado do maior para o menor

#### Aba: Pessoas
1. Duas sub-abas:
   - **Mais Escalas**: Pessoas com mais escalas atribuídas
   - **Menos Escalas**: Pessoas com menos escalas atribuídas
2. Mostra: Pessoa | Função | Total de Escalas

#### Aba: Afastamentos
1. Duas sub-abas:
   - **Ativos**: Pessoas que estão em afastamento no momento
   - **Próximos**: Afastamentos programados para os próximos 30 dias
2. Mostra: Pessoa | Função | Tipo | Data Início | Data Fim

#### Aba: Folgas
1. Mostra a contagem de folgas de cada pessoa
2. Colunas: Pessoa | Folgas | Ranking
3. Selecione a função no dropdown para filtrar

---

## 🔐 Gerenciar Perfis de Usuários

### Perfis Disponíveis
1. **Administrador**: Acesso total ao sistema
2. **Criador de Escala**: Pode criar e editar escalas
3. **Visualizador**: Apenas leitura de dados

### Criar Novo Usuário (Via MySQL)
1. Abra o MySQL conforme instruções acima
2. Digite:
```sql
INSERT INTO usuarios (nome, email, senha, perfil, ativo) VALUES 
('Seu Nome', 'seu.email@example.com', SHA2('sua_senha', 256), 'criador_escala', TRUE);
```
3. Pressione Enter
4. Troque "criador_escala" pelo perfil desejado
5. Saia digitando `exit`

---

## ⚠️ TROUBLESHOOTING

### ❌ Erro: "ERROR: Ignored the following yanked versions" ou "Could not find a version that satisfies"

**Causa:** Algumas versões dos pacotes foram removidas do PyPI (servidor de pacotes Python)

**Solução:**

1. Com o ambiente virtual ativado, execute:
```bash
python -m pip install --upgrade pip
```

2. Depois execute:
```bash
pip install --no-cache-dir PyQt5 mysql-connector-python pandas reportlab PyInstaller openpyxl python-dotenv
```

3. Se ainda não funcionar, tente instalar cada pacote individualmente:
```bash
pip install PyQt5
pip install mysql-connector-python
pip install pandas
pip install reportlab
pip install PyInstaller
```

---

### ❌ Erro: "Python não foi encontrado"
**Solução:**
1. Reinstale Python: `https://www.python.org/downloads/`
2. Marque a opção "Add Python to PATH" durante a instalação
3. Reinicie o computador

### ❌ Erro: "MySQL não foi encontrado"
**Solução:**
1. Reinstale MySQL conforme instruções acima
2. Certifique-se que o serviço do MySQL está rodando

### ❌ Erro: "Não foi possível conectar ao banco de dados"
**Solução:**
1. Verifique se o MySQL está rodando
2. Verifique os dados em `config/config.ini`
3. Certifique-se que executou o script SQL
4. Tente conectar ao MySQL manualmente para testar

### ❌ Erro ao instalar dependências
**Solução:**
1. Atualize o pip:
```bash
pip install --upgrade pip
```
2. Tente instalar novamente:
```bash
pip install --no-cache-dir -r requirements.txt
```

### ❌ Programa abre mas nada aparece
**Solução:**
1. Verifique se tem um usuário cadastrado no MySQL
2. Verifique se o MySQL está rodando
3. Consulte a aba "Troubleshooting" acima

### ❌ "ModuleNotFoundError: No module named 'PyQt5'"
**Solução:**
1. Certifique-se de que o ambiente virtual está ATIVADO (veja "(venv)" no prompt)
2. Reinstale PyQt5:
```bash
pip install PyQt5 --upgrade --force-reinstall
```

### ❌ "Connection refused" ao conectar ao MySQL
**Solução:**
1. Reinicie o MySQL:
   - **Windows**: Abra "Serviços" (Windows + R > services.msc) e reinicie "MySQL80"
   - **Linux**: `sudo systemctl restart mysql`
   - **macOS**: `brew services restart mysql`

---

## 📞 SUPORTE

Se encontrar problemas:
1. Verifique este guia novamente
2. Procure no Google pelo erro que recebeu
3. Procure no repositório do projeto por issues similares

**Repositório**: `https://github.com/kakuzu62/escala-servico`

---

## ✅ CHECKLIST DE INSTALAÇÃO

- [ ] Git instalado
- [ ] Repositório clonado
- [ ] MySQL instalado
- [ ] Banco de dados criado (schema.sql executado)
- [ ] Arquivo config.ini atualizado com credenciais
- [ ] Python 3.9+ instalado
- [ ] Ambiente virtual criado
- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas SEM ERROS
- [ ] Usuário admin criado
- [ ] Programa executado com sucesso
- [ ] Login realizado com sucesso

Parabéns! 🎉 Seu sistema está pronto para usar!
