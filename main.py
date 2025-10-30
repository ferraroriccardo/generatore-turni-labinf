# main.py

from borsista import Borsista
from generatore_di_turni_labinf import assegna_turni

# ---------------------- DEFINIZIONE PERSONE ----------------------
digre = Borsista("Matteo", "Di Gregorio", 37, laureando=True)
matteo = Borsista("Matteo", "De Cataldo", 20.5, laureando=False)
riccardo = Borsista("Riccardo", "Ferraro", 31.5, laureando=False)
samuele = Borsista("Samuele", "Gentile", 26, laureando=False)
gabriele = Borsista("Gabriele", "Giustizieri", 24, laureando=False)
mauricio = Borsista("Mauricio", "Revelo", 24.5, laureando=False)
andrea = Borsista("Andrea", "Romano", 28.5, laureando=False)
sesgiog = Borsista("Sergio", "Princivalle", 30, laureando=True)

# ---------------------- DISPONIBILITÀ SETTIMANALI ----------------------
dizMattine = {
    "lunedì": [andrea],
    "martedì": [gabriele, sesgiog, riccardo, digre],
    "mercoledì": [gabriele, sesgiog],
    "giovedì": [gabriele, samuele, matteo, sesgiog, mauricio],
    "venerdì": [samuele, matteo, mauricio]
}

dizPomeriggi = {
    "lunedì": [mauricio, digre],
    "martedì": [andrea, matteo],
    "mercoledì": [samuele, matteo, digre],
    "giovedì": [gabriele, samuele, riccardo, digre],
    "venerdì": [digre, matteo]
}

# ---------------------- PARAMETRI DI GENERAZIONE ----------------------
MAX_ORE_DIFFERENZA = 30  # massima differenza di ore consentita tra borsisti

# ---------------------- GENERAZIONE TURNI ----------------------
turni, conteggi = assegna_turni(dizMattine, dizPomeriggi, max_ore_differenza=MAX_ORE_DIFFERENZA)

# ---------------------- STAMPA RISULTATI ----------------------
print("\n📅 ASSEGNAZIONE TURNI:")
for giorno, t in turni.items():
    mattina = t['mattina']
    pomeriggio = t['pomeriggio']
    print(f"{giorno.capitalize()}: mattina = {mattina}, pomeriggio = {pomeriggio}")

print("\n📊 Totale turni per persona:")
for persona, n_turni in conteggi.items():
    status = "🎓" if persona.laureando else ""
    print(f"{persona}: {n_turni} turni {status}")
