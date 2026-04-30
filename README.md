# 🤖 Automação de Busca de Vagas com Python

> Script Python que automatiza a busca de vagas de emprego em portais e APIs públicas, com filtros personalizados por localidade, modelo de trabalho, PCD e banco de talentos.

---

## 💡 Por que criei isso?

Procurar emprego é cansativo. Entrar em 10 sites diferentes, filtrar manualmente, copiar vaga por vaga... perda de tempo e energia.

Como analista de dados em transição para Engenharia de Dados e IA, decidi usar o que sei fazer — **automatizar**.

Este script faz em segundos o que eu levava horas fazendo manualmente:

- 🔍 Busca vagas em múltiplos portais ao mesmo tempo
- 📍 Filtra por modelo de trabalho (Remoto — Brasil todo, ou Híbrido apenas em Brasília-DF)
- ♿ Identifica vagas PCD e bancos de talentos automaticamente
- 💾 Exporta tudo organizado em Excel com abas separadas

---

## 🎯 Foco das buscas

| Área | Termos |
|------|--------|
| Visualização | Power BI, Dashboard, Relatórios |
| Dados | Analista de Dados, Engenharia de Dados |
| BI | Business Intelligence, Analista BI |
| Inclusão | Vagas PCD, Banco de Talentos |

---

## ⚙️ Funcionalidades

- 🔍 **Busca simultânea** por múltiplos termos
- 📅 **Filtro por data** — apenas vagas da última semana
- 📍 **Filtro de localidade** — Remoto (Brasil todo) ou Híbrido apenas em Brasília-DF
- ♿ **Detecção automática** de vagas PCD
- 🗂️ **Detecção de banco de talentos**
- 📊 **Tabela organizada** no terminal
- 💾 **Exportação para Excel** com abas separadas e nome com data automática
- 🔗 **Links diretos** para candidatura

---

## 🛠️ Tecnologias usadas

```
Python 3.x
├── requests     → chamadas HTTP para as APIs
├── pandas       → organização dos dados em tabela
├── tabulate     → exibição formatada no terminal
└── openpyxl     → exportação para Excel
```

---

## 📁 Estrutura do projeto

```
automacao-busca-vagas/
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .gitignore
├── 📂 src/
│   └── 📄 busca_vagas.py
└── 📂 output/
    └── vagas_dados_YYYY-MM-DD.xlsx  ← gerado automaticamente
```

---

## 🚀 Como usar

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/automacao-busca-vagas.git
cd automacao-busca-vagas
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Configure suas credenciais**

Crie uma conta gratuita em [developer.adzuna.com](https://developer.adzuna.com) e substitua no topo do script `src/busca_vagas.py`:

```python
APP_ID  = "seu_app_id"
APP_KEY = "seu_app_key"
```

**4. Execute**
```bash
python src/busca_vagas.py
```

---

## 📊 Exemplo de saída

```
======================================================================
🤖 AUTOMAÇÃO DE BUSCA DE VAGAS — Analista de BI
======================================================================
📅 Filtro: vagas dos últimos 7 dias
📍 Filtro: Remoto (Brasil todo) ou Híbrido apenas em Brasília-DF
🔍 Termos: Power BI, dashboard analista dados, Business Intelligence...
======================================================================

✅ 18 vagas encontradas!

💼 VAGAS ABERTAS (15):
+----------------------------------+------------------+------------+----------------+------------+
| Vaga                             | Empresa          | Salário    | Modelo         | Aberta em  |
+==================================+==================+============+================+============+
| Analista de Dados Sênior         | Nubank           | A combinar | 🌐 Remoto      | 28/04/2026 |
| Analista Power BI PL             | Bradesco         | A combinar | 🌐 Remoto      | 27/04/2026 |
| Engenheiro de Dados JR           | iFood            | A combinar | 🌐 Remoto      | 29/04/2026 |
+----------------------------------+------------------+------------+----------------+------------+

♿ VAGAS PCD (2): ...
🗂️ BANCO DE TALENTOS (1): ...

💾 Excel salvo em: 'output/vagas_dados_2026-04-30.xlsx'
```

---

## 📁 Estrutura do Excel exportado

```
vagas_dados_YYYY-MM-DD.xlsx
├── 📋 Todas as Vagas
├── 💼 Vagas Abertas
├── ♿ PCD
└── 🗂️ Banco de Talentos
```

---

## 🗺️ Próximos passos

- [ ] Agendamento automático diário com `schedule`
- [ ] Notificação por e-mail ou WhatsApp quando aparecer vaga nova
- [ ] Integração com a API da Gupy
- [ ] Dashboard em Power BI com histórico de vagas
- [ ] Análise de palavras-chave mais pedidas nas vagas

---

## 👨‍💻 Autor

**Rodrigo Salgado**  
Analista de Power BI | Especialista em BI & Dashboards | Em transição para Engenheiro de Dados & IA

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/seu-perfil)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/seu-usuario)

---

> 💬 *"Automatizei a busca de emprego porque um bom analista de dados não faz manualmente o que pode ser automatizado."*
