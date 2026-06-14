# Sistema de Escala de Serviço

Sistema Desktop para gerenciamento de escalas de serviço com contagem de folgas automática.

## 📋 Características

- ✅ Gerenciamento de funções (expansível)
- ✅ Escalas Preta (seg-sex) e Vermelha (fins de semana + feriados)
- ✅ Contagem automática de folgas
- ✅ Algoritmo inteligente de priorização
- ✅ Gestão de afastamentos (férias, licença, missão, etc.)
- ✅ Sistema de perfis e permissões
- ✅ Relatórios em formato de tabela
- ✅ Banco de dados MySQL

## 🛠️ Instalação

### Pré-requisitos
- Python 3.9+
- MySQL 5.7+
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/kakuzu62/escala-servico.git
cd escala-servico
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
   - **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   - **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure o banco de dados:
   - Edite `config/config.ini` com suas credenciais MySQL
   - Execute o script SQL em `database/schema.sql`

6. Execute o programa:
```bash
python main.py
```

## 📦 Dependências

Ver arquivo `requirements.txt`

## 🏗️ Estrutura do Projeto

```
escala-servico/
├── config/              # Configurações do projeto
├── database/            # Scripts SQL
├── models/              # Modelos de dados
├── controllers/         # Lógica de negócio
├── services/            # Serviços auxiliares
├── ui/                  # Interface gráfica
├── main.py              # Arquivo principal
└── requirements.txt     # Dependências
```

## 🔐 Segurança

- Senhas são armazenadas com hash SHA-256
- Controle de acesso baseado em perfis
- Validação de entrada em todos os formulários

## 📝 Licença

MIT

## 👤 Autor

kakuzu62
