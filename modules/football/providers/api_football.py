
import os

import httpx
from dotenv import load_dotenv


BASE_URL = "https://v3.football.api-sports.io"


def _get(endpoint: str, params: dict) -> list[dict]:
    """Executa uma requisição GET na API-Football."""

    load_dotenv()

    api_key = os.getenv("API_FOOTBALL_KEY")

    if not api_key:
        raise ValueError("API_FOOTBALL_KEY não configurada.")

    headers = {
        "x-apisports-key": api_key
    }

    try:
        response = httpx.get(
            f"{BASE_URL}/{endpoint.lstrip('/')}",
            headers=headers,
            params=params,
            timeout=15.0
        )

        response.raise_for_status()

    except httpx.HTTPError as erro:
        raise RuntimeError(
            f"Falha na consulta ao endpoint {endpoint}."
        ) from erro

    dados = response.json()

    if dados.get("errors"):
        raise RuntimeError(
            f"Erro retornado pela API: {dados['errors']}"
        )

    return dados.get("response", [])


def buscar_competicoes_brasileiras() -> list[dict]:
    """Busca competições cadastradas no Brasil."""

    return _get(
        endpoint="leagues",
        params={"country": "Brazil"}
    )


def buscar_partidas(
    campeonato_id: int,
    temporada: int
) -> list[dict]:
    """Busca partidas de uma competição em uma temporada."""

    return _get(
        endpoint="fixtures",
        params={
            "league": campeonato_id,
            "season": temporada
        }
    )


if __name__ == "__main__":
    competicoes = buscar_competicoes_brasileiras()

    for item in competicoes:
        liga = item["league"]
        print(f"{liga['name']} | ID: {liga['id']}")
