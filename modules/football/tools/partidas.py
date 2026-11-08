from mcp.server import MCPServer

from modules.football.services.partidas_service import listar_partidas


def registrar_ferramentas_partidas(mcp: MCPServer) -> None:
    """Registra as ferramentas MCP relacionadas a partidas."""

    @mcp.tool()
    def consultar_jogos(
        campeonato_id: int,
        temporada: int,
        limite: int = 5
    ) -> dict:
        """Consulta jogos e placares de um campeonato em uma temporada.

        Args:
            campeonato_id: Identificador do campeonato na API.
            temporada: Ano da temporada, por exemplo 2024.
            limite: Quantidade máxima de partidas retornadas (1 a 20).
        """

        if not 1 <= limite <= 20:
            raise ValueError("O limite deve estar entre 1 e 20.")

        partidas = listar_partidas(
            campeonato_id=campeonato_id,
            temporada=temporada
        )

        resultado = []

        for partida in partidas[:limite]:
            resultado.append({
                "data": partida.data_hora.isoformat(),
                "mandante": partida.mandante,
                "visitante": partida.visitante,
                "gols_mandante": partida.gols_mandante,
                "gols_visitante": partida.gols_visitante,
                "status": partida.status
            })

        return {
            "total_partidas": len(partidas),
            "partidas": resultado
        }
