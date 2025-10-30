# main.py

from src.borsista import Borsista
from src.generatore_di_turni_labinf import assegna_turni
from src.output import write_output

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

# ---------------------- OUTPUT ----------------------
# Ora tutta la logica di presentazione/salvataggio dell'output è delegata a
# `output.write_output`. Qui chiamiamo semplicemente la funzione che crea le
# tabelle (CSV/XLSX quando possibile) e stampa una versione leggibile in console.
write_output(turni, conteggi, output_dir='output')
