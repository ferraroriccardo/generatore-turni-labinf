# generatore-turni-labinf

Generatore di turni per i borsisti del laboratorio (labinf).

## Panoramica

Questo repository contiene uno script semplice per assegnare turni a borsisti. Le informazioni principali (elenco persone, ore da svolgere, disponibilità mattino/pomeriggio) sono gestite da `main.py`.

## Uso — istruzioni rapide

1) Aggiorna le persone e le ore in `main.py`

- Apri `main.py` e individua la struttura dati che contiene le persone (da riga 7 a 14). Per ogni persona specifica il totale di ore già svolte, secondo il foglio excel con il conteggio di ore

2) Aggiorna le disponibilità (`dizMattine` e `dizPomeriggi`)

- Sempre in `main.py` trova i dizionari `dizMattine` e `dizPomeriggi` e aggiorna le liste di disponibilità per ciascuna persona.
- Assicurati che i nomi usati come chiavi corrispondano esattamente ai nomi definiti nella struttura persone (sono variabili e non stringhe).

3) Esegui il programma

- Dalla cartella del repository, lancia lo script con PowerShell:

```powershell
python .\main.py
```

Il programma stamperà i turni generati

### Dove viene salvato l'output

Oltre alla stampa a video, il programma salva il calendario dei turni in formato CSV nella cartella `output/` (creata automaticamente se non esiste). Il file si chiama:

- `output/turni.csv` — contiene la tabella dei turni in layout verticale (colonne = giorni; righe = Mattina, Pomeriggio).

Se `pandas` e `openpyxl` sono installati, il programma prova anche a scrivere `output/turni.xlsx` e l'output su terminale sarà formattato.

## Metodo di assegnazione delle priorità

L'algoritmo di assegnazione dei turni segue una logica semplice e prevedibile per garantire equità e rispetto delle disponibilità:

1) Un turno a testa secondo le disponibilità

- Prima di tutto si assegna a ciascuna persona al massimo un turno, compatibilmente con le sue disponibilità (mattina/pomeriggio). In questo modo tutti ricevono almeno un turno se possibile.

2) Chi ha più ore da recuperare

- Dopo la prima assegnazione, si calcola per ogni persona la differenza tra le ore totali previste e le ore già assegnate (deficit di ore).
- Si ordinano le persone in ordine decrescente di deficit (chi ha il deficit maggiore — cioè ha molte ore in meno rispetto al previsto — ha priorità) e si assegnano i turni rimanenti seguendo questo ordine, sempre rispettando le disponibilità.

3) Priorità per i laureandi

- Dopo aver gestito il deficit orario, se rimangono turni non assegnati o in caso di parità/necessità di scelta tra persone con deficit simile, i laureandi (studenti in fase di laurea) vengono considerati con priorità superiore.
- Se tra più laureandi c'è ancora necessità di scegliere, si può applicare un ulteriore criterio (ad es. chi ha meno turni già assegnati, o ordine alfabetico) — l'implementazione di tie-breaker è opzionale e configurabile.



### Esempio (pseudocodice)

- In pseudocodice il flusso principale può essere rappresentato così:

```text
assegna_un_turno_a_testa(secondo_disponibilita)
calcola_deficit_per_ogni_persona()
ordina_per_deficit_decrescente()
assegna_turni_rimanenti_ristretti_alla_disponibilita()
se_turni_rimangono: assegna_a_laureandi_con_priorita()
```

Questa spiegazione può essere trasferita direttamente nel codice come commento o come docstring per rendere l'intenzione facilmente leggibile da chi mantiene il progetto.