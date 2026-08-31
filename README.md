# Dashboard Python com Streamlit e Parquet

Dashboard interativo desenvolvido em Python utilizando Streamlit para visualização e análise de dados armazenados no formato Parquet.

O projeto demonstra a integração entre um processo de ETL e uma camada de visualização de dados, consumindo arquivos gerados pelo pipeline e apresentando informações por meio de uma interface web interativa.

## Tecnologias Utilizadas

* Python
* Streamlit
* Pandas
* PyArrow
* Parquet
* Git
* GitHub

## Estrutura do Projeto

```text
dashboard-python-parquet/
│
├── data/
│   └── processed/
│       └── clientes.parquet
│
├── src/
│   ├── __init__.py
│   └── data_loader.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Funcionalidades

* Leitura de arquivos Parquet
* Visualização dos dados
* Exibição do total de registros
* Exibição do total de colunas
* Informações sobre tipos de dados
* Identificação de valores nulos
* Resumo estatístico de colunas numéricas
* Cache de dados utilizando Streamlit

## Como Executar

Clone o repositório:

```bash
git clone SEU_REPOSITORIO
```

Acesse o diretório:

```bash
cd dashboard-python-parquet
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual.

No Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
streamlit run app.py
```

O dashboard será disponibilizado automaticamente no navegador.

## Arquitetura

```text
Arquivo Excel
      │
      ▼
Pipeline ETL
      │
      ▼
CSV / JSON / PARQUET
                  │
                  ▼
          Dashboard Python
                  │
                  ▼
             STREAMLIT
```

## Formato de Dados

O dashboard utiliza o formato Parquet como fonte de dados.

O Parquet é um formato colunar otimizado para armazenamento e processamento analítico, permitindo melhor desempenho em pipelines de dados e aplicações analíticas.

## Próximas Evoluções

* Filtros interativos
* Gráficos com Plotly
* Seleção dinâmica de colunas
* Indicadores de negócio
* Filtros por período
* Comparação entre datasets
* Paginação
* Integração com banco de dados
* Deploy do dashboard
* Docker
* Integração com Apache Airflow
* Integração com Power BI
