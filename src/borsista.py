from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class Borsista:
    nome: str
    cognome: str
    ore_totali: float
    laureando: bool = False

    def __str__(self):
        return f"{self.nome} {self.cognome}"
    
    def __hash__(self):
        return hash((self.nome, self.cognome))
    
    def get_ore_con_turni(self, num_turni):
        """Calculate total hours including assigned shifts"""
        return self.ore_totali + (num_turni * 4)  # 4 hours per shift
