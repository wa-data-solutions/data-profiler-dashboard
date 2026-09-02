import streamlit as st
import pandas as pd

from src.data_loader import carregar_arquivo


st.set_page_config(
    page_title="Data Profiler",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def formatar_bytes(valor):
    """Converte bytes para uma unidade de tamanho legível."""
    unidades = ["B", "KB", "MB", "GB", "TB"]

    tamanho = float(valor)

    for unidade in unidades:
        if tamanho < 1024:
            return f"{tamanho:.2f} {unidade}"

        tamanho /= 1024

    return f"{tamanho:.2f} PB"


def calcular_memoria_dataframe(df):
    """Calcula o consumo de memória do DataFrame."""
    return df.memory_usage(deep=True).sum()


def gerar_informacoes_tecnicas(df):
    """Gera informações técnicas sobre as colunas do dataset."""

    total_registros = len(df)

    informacoes = pd.DataFrame(
        {
            "Coluna": df.columns,
            "Tipo": [str(tipo) for tipo in df.dtypes],
            "Valores Nulos": df.isna().sum().values,
            "Valores Não Nulos": df.notna().sum().values,
        }
    )

    if total_registros > 0:
        informacoes["% Nulos"] = (
            informacoes["Valores Nulos"] / total_registros * 100
        ).round(2)
    else:
        informacoes["% Nulos"] = 0.0

    return informacoes


st.markdown(
    """
    <style>
        /* =========================================================
           CONFIGURAÇÕES GERAIS
        ========================================================= */

        .block-container {
            max-width: 1450px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        /* =========================================================
           CABEÇALHO
        ========================================================= */

        .hero-container {
            padding: 1.5rem 0 2rem 0;
            border-bottom: 1px solid rgba(128, 128, 128, 0.25);
            margin-bottom: 2.5rem;
        }

        .hero-title {
            font-size: 3.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .hero-description {
            font-size: 1.1rem;
            opacity: 0.75;
            margin: 0;
        }

        /* =========================================================
           TÍTULOS
        ========================================================= */

        .section-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 1.5rem;
            margin-bottom: 1.2rem;
        }

        .section-description {
            font-size: 1rem;
            opacity: 0.75;
            margin-bottom: 1rem;
        }

        /* =========================================================
           MÉTRICAS
        ========================================================= */

        div[data-testid="stMetric"] {
            padding: 1.2rem;
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 14px;
            background-color: rgba(128, 128, 128, 0.05);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.95rem;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }

        /* =========================================================
           TABELAS
        ========================================================= */

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }

        /* =========================================================
           UPLOADER
        ========================================================= */

        [data-testid="stFileUploader"] {
            padding: 1rem;
            border-radius: 14px;
            border: 1px solid rgba(128, 128, 128, 0.2);
        }

        /* =========================================================
           FOOTER
        ========================================================= */

        .custom-footer {
            margin-top: 4rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(128, 128, 128, 0.25);
            text-align: center;
            font-size: 0.9rem;
            opacity: 0.65;
        }

        /* =========================================================
           RESPONSIVIDADE
        ========================================================= */

        @media (max-width: 768px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 2rem;
            }

            .hero-container {
                padding-top: 0.5rem;
                margin-bottom: 1.8rem;
            }

            .hero-title {
                font-size: 2.2rem;
            }

            .hero-description {
                font-size: 0.95rem;
            }

            .section-title {
                font-size: 1.5rem;
            }

            div[data-testid="stMetric"] {
                padding: 0.9rem;
                margin-bottom: 0.5rem;
            }

            div[data-testid="stMetricValue"] {
                font-size: 1.5rem;
            }
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CABEÇALHO
# =========================================================

st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🔎 Data Profiler</div>
        <p class="hero-description">
            Dashboard para monitoramento, inspeção e análise técnica de arquivos de dados.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# UPLOAD
# =========================================================

st.markdown(
    """
    <div class="section-title">📁 Upload de Arquivo</div>
    <div class="section-description">
        Selecione um arquivo para realizar o Data Profiling.
    </div>
    """,
    unsafe_allow_html=True,
)

arquivo = st.file_uploader(
    "Selecione um arquivo",
    type=["csv", "json", "jsonl", "ndjson", "parquet", "xlsx"],
    help="Formatos suportados: CSV, JSON, JSON Lines, NDJSON, Parquet e Excel.",
)


if arquivo is None:

    st.info(
        "📥 Faça o upload de um arquivo CSV, JSON, Parquet ou XLSX para iniciar o Data Profiling."
    )

    st.markdown(
        """
        <div class="custom-footer">
            Data Profiler Dashboard • Desenvolvido com Python e Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


# =========================================================
# CARREGAMENTO DO ARQUIVO
# =========================================================

try:
    with st.spinner("🔄 Carregando e analisando o arquivo..."):
        df = carregar_arquivo(arquivo)

except Exception as erro:

    st.error("❌ Não foi possível carregar o arquivo.")

    with st.expander("Ver detalhes do erro"):
        st.exception(erro)

    st.stop()


# =========================================================
# INFORMAÇÕES DO ARQUIVO
# =========================================================

nome_arquivo = arquivo.name
extensao_arquivo = nome_arquivo.split(".")[-1].upper()
tamanho_arquivo = formatar_bytes(arquivo.size)
tamanho_memoria = formatar_bytes(calcular_memoria_dataframe(df))


st.success(
    f"Arquivo carregado com sucesso: **{nome_arquivo}**"
)


# =========================================================
# VISÃO GERAL
# =========================================================

st.markdown(
    """
    <div class="section-title">📊 Visão Geral</div>
    """,
    unsafe_allow_html=True,
)

total_registros = len(df)
total_colunas = len(df.columns)
total_nulos = int(df.isna().sum().sum())
total_duplicados = int(df.duplicated().sum())


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📄 Registros",
        f"{total_registros:,}".replace(",", "."),
    )

with col2:
    st.metric(
        "🧱 Colunas",
        total_colunas,
    )

with col3:
    st.metric(
        "💾 Arquivo",
        tamanho_arquivo,
    )

with col4:
    st.metric(
        "🧠 Em Memória",
        tamanho_memoria,
    )


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "⚠️ Valores Nulos",
        f"{total_nulos:,}".replace(",", "."),
    )

with col6:
    st.metric(
        "🔁 Duplicados",
        f"{total_duplicados:,}".replace(",", "."),
    )

with col7:
    st.metric(
        "📦 Formato",
        extensao_arquivo,
    )

with col8:
    percentual_nulos = (
        total_nulos / (total_registros * total_colunas) * 100
        if total_registros > 0 and total_colunas > 0
        else 0
    )

    st.metric(
        "📉 % Nulos",
        f"{percentual_nulos:.2f}%",
    )


st.divider()


# =========================================================
# VISUALIZAÇÃO DOS DADOS
# =========================================================

st.markdown(
    """
    <div class="section-title">📋 Visualização dos Dados</div>
    <div class="section-description">
        Pré-visualização dos dados carregados no Data Profiler.
    </div>
    """,
    unsafe_allow_html=True,
)

quantidade_preview = st.selectbox(
    "Quantidade de registros para visualização",
    options=[10, 25, 50, 100],
    index=0,
)

st.dataframe(
    df.head(quantidade_preview),
    use_container_width=True,
    hide_index=False,
)


st.divider()


# =========================================================
# INFORMAÇÕES TÉCNICAS
# =========================================================

st.markdown(
    """
    <div class="section-title">🧬 Informações Técnicas do Dataset</div>
    <div class="section-description">
        Estrutura, tipos de dados e informações sobre valores ausentes.
    </div>
    """,
    unsafe_allow_html=True,
)

informacoes = gerar_informacoes_tecnicas(df)

col_esquerda, col_direita = st.columns(2)

with col_esquerda:

    st.subheader("Tipos de Dados")

    tipos_dados = pd.DataFrame(
        {
            "Coluna": df.columns,
            "Tipo": [str(tipo) for tipo in df.dtypes],
        }
    )

    st.dataframe(
        tipos_dados,
        use_container_width=True,
        hide_index=True,
    )


with col_direita:

    st.subheader("Valores Nulos")

    valores_nulos = pd.DataFrame(
        {
            "Coluna": df.columns,
            "Valores Nulos": df.isna().sum().values,
            "% Nulos": (
                (df.isna().sum() / len(df) * 100).round(2).values
                if len(df) > 0
                else [0] * len(df.columns)
            ),
        }
    )

    st.dataframe(
        valores_nulos,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# =========================================================
# DETALHAMENTO DAS COLUNAS
# =========================================================

st.markdown(
    """
    <div class="section-title">🔍 Detalhamento das Colunas</div>
    """,
    unsafe_allow_html=True,
)

st.dataframe(
    informacoes,
    use_container_width=True,
    hide_index=True,
)


st.divider()


# =========================================================
# RESUMO ESTATÍSTICO
# =========================================================

st.markdown(
    """
    <div class="section-title">📈 Resumo Estatístico</div>
    <div class="section-description">
        Estatísticas descritivas das colunas numéricas do dataset.
    </div>
    """,
    unsafe_allow_html=True,
)


colunas_numericas = df.select_dtypes(
    include=["number"]
).columns


if len(colunas_numericas) > 0:

    resumo_estatistico = (
        df[colunas_numericas]
        .describe()
        .round(2)
    )

    st.dataframe(
        resumo_estatistico,
        use_container_width=True,
    )

else:

    st.info(
        "ℹ️ Nenhuma coluna numérica foi encontrada para gerar o resumo estatístico."
    )


# =========================================================
# INFORMAÇÕES DO ARQUIVO
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-title">ℹ️ Informações do Arquivo</div>
    """,
    unsafe_allow_html=True,
)

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.caption("Nome do Arquivo")
    st.code(nome_arquivo)

with col_info2:
    st.caption("Formato")
    st.code(extensao_arquivo)

with col_info3:
    st.caption("Tamanho Original")
    st.code(tamanho_arquivo)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="custom-footer">
        Data Profiler Dashboard • Python • Pandas • Streamlit
        <br>
        Desenvolvido por Wendril Araujo Ferreira
    </div>
    """,
    unsafe_allow_html=True,
)