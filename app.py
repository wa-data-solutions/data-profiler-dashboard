import streamlit as st
import pandas as pd

from src.data_loader import carregar_dados


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Dashboard de Dados",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# TÍTULO
# ============================================================

st.title("📊 Dashboard de Dados")
st.caption("Dashboard desenvolvido em Python + Streamlit consumindo dados em formato Parquet")


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

@st.cache_data
def carregar_dataframe():
    return carregar_dados()


try:
    df = carregar_dataframe()

except FileNotFoundError as erro:
    st.error("❌ Não foi possível localizar o arquivo Parquet.")
    st.code(str(erro))
    st.stop()

except Exception as erro:
    st.error("❌ Ocorreu um erro ao carregar os dados.")
    st.exception(erro)
    st.stop()


# ============================================================
# MÉTRICAS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total de Registros",
        f"{len(df):,}".replace(",", ".")
    )

with col2:
    st.metric(
        "Total de Colunas",
        len(df.columns)
    )

with col3:
    tamanho_mb = df.memory_usage(deep=True).sum() / 1024 / 1024

    st.metric(
        "Tamanho em Memória",
        f"{tamanho_mb:.2f} MB"
    )


# ============================================================
# VISUALIZAÇÃO DOS DADOS
# ============================================================

st.divider()

st.subheader("📋 Visualização dos Dados")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# ESTRUTURA DOS DADOS
# ============================================================

st.divider()

st.subheader("🔍 Informações do Dataset")

col1, col2 = st.columns(2)


with col1:

    st.markdown("### Tipos de Dados")

    tipos_dados = pd.DataFrame({
        "Coluna": df.columns,
        "Tipo": df.dtypes.astype(str)
    })

    st.dataframe(
        tipos_dados,
        use_container_width=True,
        hide_index=True
    )


with col2:

    st.markdown("### Valores Nulos")

    valores_nulos = df.isnull().sum()

    nulos = pd.DataFrame({
        "Coluna": valores_nulos.index,
        "Valores Nulos": valores_nulos.values
    })

    st.dataframe(
        nulos,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# RESUMO ESTATÍSTICO
# ============================================================

st.divider()

st.subheader("📈 Resumo Estatístico")

colunas_numericas = df.select_dtypes(include="number").columns.tolist()

if colunas_numericas:

    st.dataframe(
        df[colunas_numericas].describe(),
        use_container_width=True
    )

else:

    st.info(
        "Nenhuma coluna numérica encontrada para gerar o resumo estatístico."
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Projeto desenvolvido com Python, Pandas, PyArrow e Streamlit | "
    "Fonte de dados: arquivo Parquet"
)