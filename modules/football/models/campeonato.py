from dataclasses import dataclass


@dataclass(frozen=True)
class Campeonato:
    id: int
    nome: str
    pais: str
