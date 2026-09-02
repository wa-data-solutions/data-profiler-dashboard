import streamlit as st
import pandas as pd

from src.data_loader import carregar_arquivo


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Data Profiler",
    page_icon="🔍",
    layout="wide"
)


# ============================================================
# CABEÇALHO
# ============================================================

st.title("🔍 Data Profiler")

st.caption(
    "Dashboard para monitoramento, inspeção e análise técnica "
    "de arquivos de dados."
)


# ============================================================
# UPLOAD DO ARQUIVO
# ============================================================

st.divider()

st.subheader("📁 Upload de Arquivo")

arquivo = st.file_uploader(
    "Selecione um arquivo para análise",
    type=[
        "csv",
        "json",
        "parquet",
        "xlsx"
    ],
    help=(
        "Formatos suportados: "
        "CSV, JSON, Parquet e XLSX."
    )
)


# ============================================================
# VALIDAÇÃO DO UPLOAD
# ============================================================

if arquivo is None:

    st.info(
        "📤 Faça o upload de um arquivo "
        "CSV, JSON, Parquet ou XLSX "
        "para iniciar o Data Profiling."
    )

    st.stop()


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

try:

    df = carregar_arquivo(
        arquivo
    )

except Exception as erro:

    st.error(
        "❌ Não foi possível carregar o arquivo."
    )

    st.error(
        f"Detalhes: {erro}"
    )

    st.stop()


# ============================================================
# INFORMAÇÕES DO ARQUIVO
# ============================================================

st.divider()

st.subheader("📄 Informações do Arquivo")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Nome do Arquivo",
        arquivo.name
    )


with col2:

    formato = arquivo.name.split(
        "."
    )[-1].upper()

    st.metric(
        "Formato",
        formato
    )


with col3:

    tamanho_arquivo_mb = (
        arquivo.size
        / 1024
        / 1024
    )

    st.metric(
        "Tamanho do Arquivo",
        f"{tamanho_arquivo_mb:.2f} MB"
    )


with col4:

    tamanho_memoria_mb = (
        df.memory_usage(
            deep=True
        ).sum()
        / 1024
        / 1024
    )

    st.metric(
        "Tamanho em Memória",
        f"{tamanho_memoria_mb:.2f} MB"
    )


# ============================================================
# VISÃO GERAL DO DATASET
# ============================================================

st.divider()

st.subheader(
    "📊 Visão Geral do Dataset"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total de Registros",
        f"{len(df):,}".replace(
            ",",
            "."
        )
    )


with col2:

    st.metric(
        "Total de Colunas",
        len(df.columns)
    )


with col3:

    total_nulos = int(
        df.isnull().sum().sum()
    )

    st.metric(
        "Valores Nulos",
        f"{total_nulos:,}".replace(
            ",",
            "."
        )
    )


with col4:

    total_duplicados = int(
        df.duplicated().sum()
    )

    st.metric(
        "Registros Duplicados",
        f"{total_duplicados:,}".replace(
            ",",
            "."
        )
    )


# ============================================================
# VISUALIZAÇÃO DOS DADOS
# ============================================================

st.divider()

st.subheader(
    "📋 Visualização dos Dados"
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    height=400
)


# ============================================================
# INFORMAÇÕES TÉCNICAS
# ============================================================

st.divider()

st.subheader(
    "🔍 Informações Técnicas do Dataset"
)

col1, col2 = st.columns(2)


# ============================================================
# TIPOS DE DADOS
# ============================================================

with col1:

    st.markdown(
        "### 🧬 Tipos de Dados"
    )

    tipos_dados = pd.DataFrame({
        "Coluna": df.columns,
        "Tipo de Dado": (
            df.dtypes
            .astype(str)
            .values
        )
    })

    st.dataframe(
        tipos_dados,
        use_container_width=True,
        hide_index=True,
        height=400
    )


# ============================================================
# VALORES NULOS
# ============================================================

with col2:

    st.markdown(
        "### ⚠️ Valores Nulos"
    )

    valores_nulos = (
        df.isnull().sum()
    )

    if len(df) > 0:

        percentual_nulos = (
            valores_nulos
            / len(df)
        ) * 100

    else:

        percentual_nulos = valores_nulos * 0


    nulos = pd.DataFrame({
        "Coluna": valores_nulos.index,
        "Valores Nulos": (
            valores_nulos.values
        ),
        "Percentual (%)": (
            percentual_nulos
            .round(2)
            .values
        )
    })

    st.dataframe(
        nulos,
        use_container_width=True,
        hide_index=True,
        height=400
    )


# ============================================================
# RESUMO ESTATÍSTICO
# ============================================================

st.divider()

st.subheader(
    "📈 Resumo Estatístico"
)

colunas_numericas = (
    df.select_dtypes(
        include="number"
    )
    .columns
    .tolist()
)


if colunas_numericas:

    resumo_estatistico = (
        df[colunas_numericas]
        .describe()
    )

    st.dataframe(
        resumo_estatistico,
        use_container_width=True
    )

else:

    st.info(
        "Nenhuma coluna numérica foi encontrada "
        "para gerar o resumo estatístico."
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Data Profiler | Desenvolvido com Python, "
    "Pandas, PyArrow, OpenPyXL e Streamlit"
)