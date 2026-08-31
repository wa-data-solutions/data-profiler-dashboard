from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "clientes.parquet"


def carregar_dados():
    """
    Carrega os dados do arquivo Parquet.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo Parquet não encontrado: {DATA_PATH}"
        )

    return pd.read_parquet(DATA_PATH)