from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Partida:
    id: int
    campeonato_id: int
    data_hora: datetime

    mandante: str
    visitante: str

    gols_mandante: int | None
    gols_visitante: int | None

    status: str
