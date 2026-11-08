import pytest
import httpx

from modules.football.providers import api_football


def test_buscar_partidas_sucesso(monkeypatch):
    """Verifica a consulta de partidas com resposta válida."""

    monkeypatch.setenv("API_FOOTBALL_KEY", "chave-de-teste")

    def simular_get(url, headers, params, timeout):
        assert url.endswith("/fixtures")
        assert headers["x-apisports-key"] == "chave-de-teste"
        assert params == {"league": 71, "season": 2024}

        return httpx.Response(
            status_code=200,
            json={
                "errors": [],
                "response": [{"fixture": {"id": 123}}]
            },
            request=httpx.Request("GET", url)
        )

    monkeypatch.setattr(api_football.httpx, "get", simular_get)

    resultado = api_football.buscar_partidas(71, 2024)

    assert len(resultado) == 1
    assert resultado[0]["fixture"]["id"] == 123


def test_erro_plano_gratuito(monkeypatch):
    """Verifica se erros de negócio da API são tratados."""

    monkeypatch.setenv("API_FOOTBALL_KEY", "chave-de-teste")

    def simular_get(url, headers, params, timeout):
        return httpx.Response(
            status_code=200,
            json={
                "errors": {
                    "plan": "Free plans do not have access to this season"
                },
                "response": []
            },
            request=httpx.Request("GET", url)
        )

    monkeypatch.setattr(api_football.httpx, "get", simular_get)

    with pytest.raises(RuntimeError, match="Erro retornado pela API"):
        api_football.buscar_partidas(71, 2026)


def test_erro_http(monkeypatch):
    """Verifica o tratamento de erros HTTP."""

    monkeypatch.setenv("API_FOOTBALL_KEY", "chave-de-teste")

    def simular_get(url, headers, params, timeout):
        return httpx.Response(
            status_code=401,
            request=httpx.Request("GET", url)
        )

    monkeypatch.setattr(api_football.httpx, "get", simular_get)

    with pytest.raises(RuntimeError, match="Falha na consulta"):
        api_football.buscar_partidas(71, 2024)


def test_api_key_ausente(monkeypatch):
    """Verifica o comportamento sem credenciais."""

    monkeypatch.delenv("API_FOOTBALL_KEY", raising=False)

    monkeypatch.setattr(
        api_football,
        "load_dotenv",
        lambda: None
    )

    with pytest.raises(ValueError, match="API_FOOTBALL_KEY não configurada"):
        api_football.buscar_partidas(71, 2024)
