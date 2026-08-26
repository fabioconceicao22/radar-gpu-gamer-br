from __future__ import annotations

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DESEMPENHO = BASE_DIR / "data" / "desempenho_gpus.csv"

COLUNAS_OBRIGATORIAS = {
    "GPU",
    "FPS_1080p",
    "FPS_1440p",
    "FPS_RT_1080p",
    "FPS_RT_1440p",
    "VRAM",
    "Consumo_W",
    "AV1_Encode",
    "Fonte_Benchmark",
    "Fonte_Especificacoes",
    "Benchmark_Atualizado_Em",
}

PESOS = {
    "Gamer 1080p": {
        "Custo-benefício": 0.45,
        "Raster": 0.30,
        "Eficiência": 0.15,
        "VRAM": 0.10,
    },
    "Gamer 1440p": {
        "Custo-benefício": 0.45,
        "Raster": 0.30,
        "VRAM": 0.15,
        "Eficiência": 0.10,
    },
    "Jogos + streaming": {
        "Custo-benefício": 0.35,
        "Raster": 0.25,
        "Ray tracing": 0.15,
        "Eficiência": 0.15,
        "AV1": 0.10,
    },
}


def carregar_base_tecnica(caminho: str | Path = ARQUIVO_DESEMPENHO) -> pd.DataFrame:
    """Carrega benchmarks rastreáveis e falha cedo se a base estiver incompleta."""
    dados = pd.read_csv(caminho)
    faltantes = COLUNAS_OBRIGATORIAS.difference(dados.columns)
    if faltantes:
        raise ValueError(f"Base técnica incompleta: {', '.join(sorted(faltantes))}")
    if dados["GPU"].duplicated().any():
        raise ValueError("A base técnica contém GPUs duplicadas")

    colunas_positivas = [
        "FPS_1080p",
        "FPS_1440p",
        "FPS_RT_1080p",
        "FPS_RT_1440p",
        "VRAM",
        "Consumo_W",
    ]
    if (dados[colunas_positivas] <= 0).any().any():
        raise ValueError("FPS, VRAM e consumo precisam ser maiores que zero")

    dados["AV1_Encode"] = (
        dados["AV1_Encode"].astype(str).str.strip().str.lower().eq("true")
    )
    dados["Benchmark_Atualizado_Em"] = pd.to_datetime(
        dados["Benchmark_Atualizado_Em"], errors="raise"
    )
    return dados


def _normalizar(serie: pd.Series) -> pd.Series:
    maior = float(serie.max())
    if maior <= 0:
        return pd.Series(0.0, index=serie.index)
    return (serie / maior * 100).clip(0, 100)


def adicionar_indice_radar(dados: pd.DataFrame, foco: str) -> pd.DataFrame:
    """Calcula um índice relativo e reproduzível com pesos publicados em PESOS."""
    if foco not in PESOS:
        raise ValueError(f"Perfil desconhecido: {foco}")

    resultado = dados.copy()
    fps_coluna = "FPS_1440p" if foco == "Gamer 1440p" else "FPS_1080p"
    rt_coluna = "FPS_RT_1440p" if foco == "Gamer 1440p" else "FPS_RT_1080p"

    resultado["Componente_Raster"] = _normalizar(resultado[fps_coluna])
    resultado["Componente_Valor"] = _normalizar(
        resultado[fps_coluna] / resultado["Preco_Atual"]
    )
    resultado["Componente_Eficiencia"] = _normalizar(
        resultado[fps_coluna] / resultado["Consumo_W"]
    )
    resultado["Componente_VRAM"] = (resultado["VRAM"] / 12 * 100).clip(upper=100)
    resultado["Componente_RT"] = _normalizar(resultado[rt_coluna])
    resultado["Componente_AV1"] = resultado["AV1_Encode"].map({True: 100.0, False: 0.0})

    componentes = {
        "Custo-benefício": resultado["Componente_Valor"],
        "Raster": resultado["Componente_Raster"],
        "Eficiência": resultado["Componente_Eficiencia"],
        "VRAM": resultado["Componente_VRAM"],
        "Ray tracing": resultado["Componente_RT"],
        "AV1": resultado["Componente_AV1"],
    }
    resultado["Score"] = sum(
        componentes[nome] * peso for nome, peso in PESOS[foco].items()
    ).round(1)
    return resultado


def descrever_metodologia(foco: str) -> str:
    pesos = PESOS[foco]
    return " · ".join(f"{nome}: {peso:.0%}" for nome, peso in pesos.items())

