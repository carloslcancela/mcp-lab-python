from modules.football.services import partidas_service


def test_listar_partidas(monkeypatch):
    """Verifica a transformação de dados da API em objetos Partida."""

    resposta_simulada = [
        {
            "fixture": {
                "id": 123,
                "date": "2024-04-13T21:30:00+00:00",
                "status": {"short": "FT"}
            },
            "league": {"id": 71},
            "teams": {
                "home": {"name": "Internacional"},
                "away": {"name": "Bahia"}
            },
            "goals": {
                "home": 2,
                "away": 1
            }
        }
    ]

    def buscar_partidas_simulado(campeonato_id, temporada):
        assert campeonato_id == 71
        assert temporada == 2024
        return resposta_simulada

    monkeypatch.setattr(
        partidas_service,
        "buscar_partidas",
        buscar_partidas_simulado
    )

    resultado = partidas_service.listar_partidas(71, 2024)

    assert len(resultado) == 1
    assert resultado[0].id == 123
    assert resultado[0].mandante == "Internacional"
    assert resultado[0].visitante == "Bahia"
    assert resultado[0].gols_mandante == 2
    assert resultado[0].gols_visitante == 1
    assert resultado[0].status == "FT"
