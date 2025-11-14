# Sistema de Controle e Gerenciamento de Obras

Aplicação em Python desenvolvida para cadastro, acompanhamento e análise de obras civis, como parte da disciplina **Programação para Ciência de Dados**.

**Curso:** MBA Ciência de Dados – UNIFOR  
**Instrutor:** Cássio Pinheiro  
**Aluno:** Thierry Pereira Canoco – Matrícula 2527390  
**Data de Entrega:** 14/11/2025  
**Repositório GitHub:** https://github.com/tcanoco/projeto_05_controle_obras_engenharia

---

# 1. Objetivo do Projeto

O objetivo do projeto é desenvolver um **Sistema de Controle de Obras**, executado totalmente em console e integrando os conteúdos estudados ao longo da disciplina.

## ✔ Módulo 1 – Estruturas Python
- Listas  
- Dicionários  
- Funções  
- Laços e condicionais  
- Manipulação de datas  
- Menu interativo  

## ✔ Módulo 2 – Análise de Dados
- Persistência de dados em CSV  
- DataFrames com Pandas  

## ✔ Módulo 3 – Visualização
- Gráficos gerenciais com Matplotlib  

## 🎯 O sistema permite:
- Controle de progresso físico  
- Controle de custos realizados  
- Cálculo de desvio orçamentário  
- Cálculo de atraso  
- Relatórios completos  
- Visualizações gráficas para análise  

---

# 2. Requirements

O arquivo `requirements.txt` contém todas as dependências necessárias.

### 📦 Instalação das dependências
```bash
pip install -r requirements.txt
📋 Conteúdo do arquivo
ini
Copiar código
asttokens==3.0.0
comm==0.2.3
contourpy==1.3.3
cycler==0.12.1
debugpy==1.8.17
decorator==5.2.1
executing==2.2.1
fonttools==4.60.1
ipykernel==7.1.0
ipython==9.7.0
ipython_pygments_lexers==1.1.1
jedi==0.19.2
jupyter_client==8.6.3
jupyter_core==5.9.1
kiwisolver==1.4.9
matplotlib==3.10.7
matplotlib-inline==0.2.1
nest-asyncio==1.6.0
numpy==2.3.4
packaging==25.0
pandas==2.3.3
parso==0.8.5
pexpect==4.9.0
pillow==12.0.0
platformdirs==4.5.0
prompt_toolkit==3.0.52
psutil==7.1.3
ptyprocess==0.7.0
pure_eval==0.2.3
Pygments==2.19.2
pyparsing==3.2.5
python-dateutil==2.9.0.post0
pytz==2025.2
pyzmq==27.1.0
seaborn==0.13.2
six==1.17.0
stack-data==0.6.3
tornado==6.5.2
traitlets==5.14.3
tzdata==2025.2
wcwidth==0.2.14
3. Diagrama de Contexto (C4 – Nível 1)
mermaid
Copiar código
C4Context
    title Diagrama de Contexto do Sistema de Obras

    Person(gestor, "Gestor de Obras", "Usuário responsável por cadastrar, atualizar e analisar obras")
    System(sistema, "Sistema de Controle de Obras (Python)", "Aplicação de console para acompanhamento de obras")

    Boundary(storage, "Armazenamento") {
        SystemDb(csv1, "obras.csv", "Armazena dados das obras")
        SystemDb(csv2, "etapas.csv", "Armazena dados das etapas")
    }

    Rel(gestor, sistema, "Entrada de dados, consultas e geração de relatórios")
    Rel(sistema, csv1, "Lê e escreve dados das obras", "Pandas")
    Rel(sistema, csv2, "Lê e escreve dados das etapas", "Pandas")
4. Funcionalidades Implementadas
Funcionalidade	Descrição	Módulo
Cadastro de Obras	Criação do registro principal	Módulo 1
Cadastro de Etapas	Insere etapas com custo orçado	Módulo 1
Atualização de Progresso	Ajusta porcentagem concluída e status	Módulo 1
Registro de Custos	Define custo realizado	Módulo 1
Cálculo de Métricas	Progresso, custo, desvio, atraso	Módulo 1
Persistência em CSV	Lê e salva dados usando Pandas	Módulo 2
DataFrame Resumo	Tabela gerencial das obras	Módulo 2
Relatórios em Console	Relatórios individuais e gerais	Módulo 1
Gráficos	Progresso, custo e atraso	Módulo 3
Menu Completo	Sistema interativo no terminal	Módulo 1

5. Estrutura dos Dados
Obras
python
Copiar código
obras = {
    "OBR001": {
        "codigo": "OBR001",
        "nome": "Edifício Residencial",
        "localizacao": "Fortaleza, CE",
        "tipo": "Residencial",
        "data_inicio": "2024-01-15",
        "data_prevista": "2024-12-15",
        "orcamento": 5000000.0,
        "responsavel": "Eng João Silva",
        "status": "Planejamento"
    }
}
Etapas
python
Copiar código
etapas = [
    {
        "obra_codigo": "OBR001",
        "nome": "Fundação",
        "custo_orcado": 450000.0,
        "custo_realizado": 0.0,
        "percentual_conclusao": 0.0,
        "status": "Pendente",
        "data_conclusao": ""
    }
]
6. Fluxo do Sistema
Cadastrar obra

Cadastrar etapas

Atualizar progresso e custos

Exibir relatórios

Gerar DataFrame

Gerar gráficos

Dados salvos automaticamente

7. Menu da Aplicação
Copiar código
1 cadastrar obra
2 cadastrar etapa
3 atualizar progresso
4 registrar custo
5 relatório obra
6 relatório geral
7 dataframe
8 gráficos
9 sair
Submenu de gráficos
Copiar código
1 progresso
2 custo
3 atraso
8. Gráficos Gerados (Matplotlib)
✔ Progresso das Obras
Comparação do percentual de avanço.

✔ Custo Realizado
Mostra quanto já foi gasto por obra.

✔ Atraso
Comparação dos dias de atraso.

9. Persistência
Arquivos gerados automaticamente:

Copiar código
obras.csv
etapas.csv
Podem ser usados no Excel ou Pandas.

10. Como Executar
Instalar dependências
bash
Copiar código
pip install -r requirements.txt
Executar o sistema
bash
Copiar código
python sistema_obras.py
powershell
Copiar código
FIM DO README