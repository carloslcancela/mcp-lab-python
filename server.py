from mcp.server import MCPServer

from modules.football.tools.partidas import (
    registrar_ferramentas_partidas,
)

mcp = MCPServer("mcp-lab-python")

registrar_ferramentas_partidas(mcp)

if __name__ == "__main__":
    mcp.run()
