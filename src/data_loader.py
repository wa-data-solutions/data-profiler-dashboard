import io
import json
from pathlib import Path

import pandas as pd


def carregar_json(uploaded_file):
    """
    Carrega arquivos JSON em diferentes estruturas.

    Suporta:
    - JSON tradicional
    - JSON com lista de registros
    - JSON Lines / NDJSON
    - Arquivos JSON gerados pelo Apache Spark
    """

    conteudo = uploaded_file.getvalue()

    # --------------------------------------------------------
    # JSON LINES / NDJSON
    # --------------------------------------------------------

    try:
        return pd.read_json(
            io.BytesIO(conteudo),
            lines=True
        )

    except ValueError:
        pass

    # --------------------------------------------------------
    # JSON TRADICIONAL
    # --------------------------------------------------------

    try:
        return pd.read_json(
            io.BytesIO(conteudo)
        )

    except ValueError:
        pass

    # --------------------------------------------------------
    # CARREGAMENTO ALTERNATIVO
    # --------------------------------------------------------

    try:

        dados = json.loads(
            conteudo.decode("utf-8")
        )

        if isinstance(dados, list):

            return pd.json_normalize(
                dados
            )

        if isinstance(dados, dict):

            return pd.json_normalize(
                dados
            )

    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        ValueError
    ) as erro:

        raise ValueError(
            "Não foi possível interpretar a estrutura do arquivo JSON."
        ) from erro

    raise ValueError(
        "Estrutura JSON não suportada."
    )


def carregar_excel(uploaded_file):
    """
    Carrega arquivos Excel.

    Lê a primeira planilha do arquivo XLSX.
    """

    return pd.read_excel(
        uploaded_file,
        engine="openpyxl"
    )


def carregar_arquivo(uploaded_file):
    """
    Carrega arquivos enviados pelo usuário.

    Formatos suportados:
    - CSV
    - JSON
    - Parquet
    - XLSX
    """

    extensao = Path(
        uploaded_file.name
    ).suffix.lower()

    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    if extensao == ".csv":

        return pd.read_csv(
            uploaded_file
        )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    elif extensao == ".json":

        return carregar_json(
            uploaded_file
        )

    # --------------------------------------------------------
    # PARQUET
    # --------------------------------------------------------

    elif extensao == ".parquet":

        return pd.read_parquet(
            uploaded_file
        )

    # --------------------------------------------------------
    # EXCEL
    # --------------------------------------------------------

    elif extensao == ".xlsx":

        return carregar_excel(
            uploaded_file
        )

    # --------------------------------------------------------
    # FORMATO NÃO SUPORTADO
    # --------------------------------------------------------

    raise ValueError(
        "Formato não suportado. "
        "Envie um arquivo CSV, JSON, Parquet ou XLSX."
    )