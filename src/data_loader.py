import pandas as pd


def carregar_arquivo(arquivo):
    """
    Carrega arquivos CSV, JSON, JSON Lines, NDJSON,
    Parquet ou Excel e retorna um DataFrame Pandas.
    """

    nome_arquivo = arquivo.name.lower()

    # =========================================================
    # CSV
    # =========================================================

    if nome_arquivo.endswith(".csv"):
        return pd.read_csv(arquivo)

    # =========================================================
    # JSON
    # =========================================================

    elif nome_arquivo.endswith(".json"):

        try:
            return pd.read_json(arquivo)

        except ValueError:
            arquivo.seek(0)

            return pd.read_json(
                arquivo,
                lines=True,
            )

    # =========================================================
    # JSON LINES / NDJSON
    # =========================================================

    elif (
        nome_arquivo.endswith(".jsonl")
        or nome_arquivo.endswith(".ndjson")
    ):

        return pd.read_json(
            arquivo,
            lines=True,
        )

    # =========================================================
    # PARQUET
    # =========================================================

    elif nome_arquivo.endswith(".parquet"):

        return pd.read_parquet(
            arquivo,
        )

    # =========================================================
    # EXCEL
    # =========================================================

    elif nome_arquivo.endswith(".xlsx"):

        return pd.read_excel(
            arquivo,
        )

    # =========================================================
    # FORMATO NÃO SUPORTADO
    # =========================================================

    else:

        raise ValueError(
            "Formato de arquivo não suportado."
        )