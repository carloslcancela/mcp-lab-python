from modules.football.models.campeonato import Campeonato
from modules.football.providers.api_football import (
    buscar_competicoes_brasileiras,
)


def listar_campeonatos() -> list[Campeonato]:
    """Retorna os campeonatos brasileiros como objetos do domínio."""

    dados_api = buscar_competicoes_brasileiras()

    campeonatos = []

    for item in dados_api:
        liga = item["league"]
        pais = item["country"]

        campeonato = Campeonato(
            id=liga["id"],
            nome=liga["name"],
            pais=pais["name"],
        )

        campeonatos.append(campeonato)

    return sorted(
        campeonatos,
        key=lambda campeonato: campeonato.nome.casefold()
    )


if __name__ == "__main__":
    campeonatos = listar_campeonatos()

    print(f"Total de campeonatos: {len(campeonatos)}")

    for campeonato in campeonatos[:5]:
        print(
            f"{campeonato.nome} | "
            f"ID: {campeonato.id} | "
            f"País: {campeonato.pais}"
        )
