# tutor.py
from dataclasses import dataclass

@dataclass(frozen=True, eq=True)  # Make the class immutable and provide equality comparison
class Borsista:
    nome: str
    cognome: str
    ore_totali: float  # Changed to float since we have decimal values in main.py
    laureando: bool = False

    def __str__(self):
        return f"{self.nome} {self.cognome}"
    
    def __hash__(self):
        # Create a hash based on the immutable attributes that make each borsista unique
        return hash((self.nome, self.cognome))
    
    def get_ore_con_turni(self, num_turni):
        """Calculate total hours including assigned shifts"""
        return self.ore_totali + (num_turni * 4)  # 4 hours per shift
