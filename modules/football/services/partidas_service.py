from datetime import datetime

from modules.football.models.partida import Partida
from modules.football.providers.api_football import buscar_partidas


def listar_partidas(
    campeonato_id: int,
    temporada: int
) -> list[Partida]:
    """Consulta e transforma partidas em objetos do domínio."""

    dados_api = buscar_partidas(
        campeonato_id=campeonato_id,
        temporada=temporada
    )

    partidas = []

    for item in dados_api:
        fixture = item["fixture"]
        teams = item["teams"]
        goals = item["goals"]

        partida = Partida(
            id=fixture["id"],
            campeonato_id=item["league"]["id"],
            data_hora=datetime.fromisoformat(fixture["date"]),
            mandante=teams["home"]["name"],
            visitante=teams["away"]["name"],
            gols_mandante=goals["home"],
            gols_visitante=goals["away"],
            status=fixture["status"]["short"]
        )

        partidas.append(partida)

    return sorted(
        partidas,
        key=lambda partida: partida.data_hora
    )


if __name__ == "__main__":
    partidas = listar_partidas(71, 2024)

    print(f"Total de partidas: {len(partidas)}")

    for partida in partidas[:5]:
        print(
            f"{partida.mandante} "
            f"{partida.gols_mandante} x "
            f"{partida.gols_visitante} "
            f"{partida.visitante}"
        )
