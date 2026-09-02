# 🔍 Data Profiler Dashboard

Dashboard interativo desenvolvido em Python para realizar upload, monitoramento, inspeção e análise técnica de arquivos de dados.

O projeto permite carregar diferentes formatos de arquivos e gerar automaticamente informações importantes sobre a estrutura e qualidade do dataset.

## 🚀 Funcionalidades

### 📁 Upload de Arquivos

O Data Profiler suporta os seguintes formatos:

- 📄 CSV
- 📄 JSON
- 📄 JSON Lines / NDJSON
- 📦 Parquet
- 📊 Excel (.xlsx)

### 📊 Visão Geral do Dataset

Após o carregamento do arquivo, o dashboard apresenta:

- Total de registros
- Total de colunas
- Valores nulos
- Registros duplicados
- Tamanho do arquivo
- Tamanho do dataset em memória

### 📋 Visualização dos Dados

Permite visualizar os registros carregados em uma tabela interativa.

### 🔍 Informações Técnicas

O dashboard apresenta:

- Nome das colunas
- Tipos de dados
- Quantidade de valores nulos
- Percentual de valores nulos

### 📈 Resumo Estatístico

Para colunas numéricas, são exibidos:

- Count
- Mean
- Standard Deviation
- Minimum
- 25%
- Median
- 75%
- Maximum

## 🛠️ Tecnologias

- Python
- Pandas
- PyArrow
- OpenPyXL
- Streamlit

## 📂 Estrutura do Projeto

```text
data-profiler-dashboard/
│
├── data/
│   └── processed/
│       └── clientes.parquet
│
├── src/
│   └── data_loader.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore