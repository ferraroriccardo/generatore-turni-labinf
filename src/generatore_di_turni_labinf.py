import random
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional

GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì"]

def get_ore_totali(persona, conteggio_turni: Dict) -> float:
    """Calcola le ore totali di una persona considerando i turni assegnati."""
    return persona.get_ore_con_turni(conteggio_turni[persona])

def get_ore_min_max(persone: Set, conteggio_turni: Dict) -> Tuple[float, float]:
    """Calcola il minimo e massimo delle ore totali tra tutte le persone."""
    if not persone:
        return 0, 0
    ore_per_persona = [get_ore_totali(p, conteggio_turni) for p in persone]
    return min(ore_per_persona), max(ore_per_persona)

def check_ore_differenza(persone: Set, conteggio_turni: Dict, max_ore_differenza: float) -> bool:
    """Verifica se la differenza di ore è accettabile."""
    ore_min, ore_max = get_ore_min_max(persone, conteggio_turni)
    return (ore_max - ore_min) <= max_ore_differenza

def score_secondo_turno(persona, laureandi: List, conteggio_turni: Dict, 
                       persone: Set, max_ore_differenza: float) -> float:
    """Calcola il punteggio per l'assegnazione del secondo turno.
    Punteggio più basso = priorità più alta."""
    ore_min, _ = get_ore_min_max(persone, conteggio_turni)
    ore_persona = get_ore_totali(persona, conteggio_turni)
    
    # Punteggio base basato sulle ore
    score = ore_persona - ore_min
    
    # Se la differenza ore è maggiore del max, dai priorità assoluta a chi ha meno ore
    if score > max_ore_differenza:
        return score
    
    # Altrimenti considera prima il fatto di essere laureando
    if persona in laureandi:
        score -= 1000  # Bonus significativo per i laureandi
        
    return score

def get_tutte_le_persone(dizMattine: Dict, dizPomeriggi: Dict) -> Set:
    """Raccoglie tutte le persone disponibili nella settimana."""
    persone = set()
    for giorno in GIORNI:
        persone.update(dizMattine.get(giorno, []))
        persone.update(dizPomeriggi.get(giorno, []))
    return persone

def get_laureandi(persone: Set) -> List:
    """Identifica i laureandi tra le persone disponibili."""
    return [p for p in persone if p.laureando]

def assegna_turni(dizMattine, dizPomeriggi, max_turni=2, max_ore_differenza=30):
    giorni = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì"]
    turni_finali = {g: {"mattina": None, "pomeriggio": None} for g in giorni}
    conteggio_turni = defaultdict(int)

    # Raccogli tutte le persone disponibili nella settimana
    tutte_le_persone = set()
    for giorno in giorni:
        tutte_le_persone.update(dizMattine.get(giorno, []))
        tutte_le_persone.update(dizPomeriggi.get(giorno, []))

    # Crea lista laureandi
    laureandi = [p for p in tutte_le_persone if p.laureando]

    def get_ore_totali(persona):
        return persona.get_ore_con_turni(conteggio_turni[persona])

    def get_ore_min_max():
        """Ritorna il minimo e massimo delle ore totali tra tutte le persone"""
        if not tutte_le_persone:
            return 0, 0
        ore_per_persona = [get_ore_totali(p) for p in tutte_le_persone]
        return min(ore_per_persona), max(ore_per_persona)

    def check_ore_differenza():
        """Verifica se la differenza di ore è accettabile"""
        ore_min, ore_max = get_ore_min_max()
        return (ore_max - ore_min) <= max_ore_differenza

    def score_secondo_turno(persona):
        """Calcola il punteggio per l'assegnazione del secondo turno.
        Punteggio più basso = priorità più alta"""
        ore_min, _ = get_ore_min_max()
        ore_persona = get_ore_totali(persona)
        
        # Punteggio base basato sulle ore (0 per chi ha ore minime, cresce con la differenza)
        score = ore_persona - ore_min
        
        # Se la differenza ore è maggiore del max, dai priorità assoluta a chi ha meno ore
        if score > max_ore_differenza:
            return score
        
        # Altrimenti considera prima il fatto di essere laureando
        if persona.laureando:
            score -= 1000  # Bonus significativo per i laureandi
            
        return score

    # Prima fase: assicurati che tutti abbiano almeno un turno
    persone_senza_turni = tutte_le_persone.copy()
    
    for giorno in giorni:
        disponibili_mattina = dizMattine.get(giorno, [])
        disponibili_pomeriggio = dizPomeriggi.get(giorno, [])

        candidato_mattina = None
        candidato_pomeriggio = None

        # --- SCELTA MATTINA ---
        if disponibili_mattina:
            # Prima assegna a chi non ha ancora turni
            disponibili_senza_turni = [p for p in disponibili_mattina if p in persone_senza_turni]
            if disponibili_senza_turni:
                candidato_mattina = min(disponibili_senza_turni, key=get_ore_totali)
            else:
                # Se tutti hanno già un turno, usa i criteri standard
                sotto_limite = [p for p in disponibili_mattina if conteggio_turni[p] < max_turni]
                if sotto_limite:
                    # Per il secondo turno, usa il punteggio che considera sia ore che laureando
                    candidato_mattina = min(sotto_limite, key=lambda p: (
                        0 if p in persone_senza_turni else score_secondo_turno(p)
                    ))
                else:
                    candidato_mattina = min(disponibili_mattina, key=lambda p: (
                        0 if p in persone_senza_turni else get_ore_totali(p)
                    ))
            
            conteggio_turni[candidato_mattina] += 1
            persone_senza_turni.discard(candidato_mattina)  # Rimuovi dalla lista chi ha ottenuto un turno

        # --- SCELTA POMERIGGIO ---
        disponibili_pomeriggio = [p for p in disponibili_pomeriggio if p != candidato_mattina]
        if disponibili_pomeriggio:
            # Prima assegna a chi non ha ancora turni
            disponibili_senza_turni = [p for p in disponibili_pomeriggio if p in persone_senza_turni]
            if disponibili_senza_turni:
                candidato_pomeriggio = min(disponibili_senza_turni, key=get_ore_totali)
            else:
                # Se tutti hanno già un turno, usa i criteri per il secondo turno
                sotto_limite = [p for p in disponibili_pomeriggio if conteggio_turni[p] < max_turni]
                if sotto_limite:
                    candidato_pomeriggio = min(sotto_limite, key=score_secondo_turno)
                else:
                    candidato_pomeriggio = min(disponibili_pomeriggio, key=get_ore_totali)
            
            conteggio_turni[candidato_pomeriggio] += 1
            persone_senza_turni.discard(candidato_pomeriggio)
        else:
            # --- PIANO B INTELLIGENTE ---
            if candidato_mattina:
                conteggio_turni[candidato_mattina] -= 1  # rollback

            best_pair = (None, None)
            max_coperti = -1
            best_score = float("inf")

            for matt in disponibili_mattina or [None]:
                for pom in disponibili_pomeriggio or [None]:
                    if matt and pom and matt == pom:
                        continue
                    coperti = int(matt is not None) + int(pom is not None)
                    
                    # Calcola il punteggio considerando entrambe le persone
                    score = 0
                    if matt:
                        score += (0 if matt in persone_senza_turni else score_secondo_turno(matt))
                    if pom:
                        score += (0 if pom in persone_senza_turni else score_secondo_turno(pom))
                    
                    # Penalizza fortemente se lasciamo qualcuno senza turni
                    if matt and matt in persone_senza_turni:
                        score -= 2000
                    if pom and pom in persone_senza_turni:
                        score -= 2000
                    
                    # Verifica validità
                    valid_matt = (matt is None) or (conteggio_turni[matt] < max_turni)
                    valid_pom = (pom is None) or (conteggio_turni[pom] < max_turni)
                    
                    if not (valid_matt and valid_pom):
                        continue
                        
                    if coperti > max_coperti or (coperti == max_coperti and score < best_score):
                        best_pair, max_coperti, best_score = (matt, pom), coperti, score

            candidato_mattina, candidato_pomeriggio = best_pair
            if candidato_mattina:
                conteggio_turni[candidato_mattina] += 1
                persone_senza_turni.discard(candidato_mattina)
            if candidato_pomeriggio:
                conteggio_turni[candidato_pomeriggio] += 1
                persone_senza_turni.discard(candidato_pomeriggio)

        turni_finali[giorno]["mattina"] = candidato_mattina or "NESSUNO DISPONIBILE"
        turni_finali[giorno]["pomeriggio"] = candidato_pomeriggio or "NESSUNO DISPONIBILE"

    return turni_finali, dict(conteggio_turni)
