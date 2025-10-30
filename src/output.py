import csv
from pathlib import Path


def write_output(turni, conteggi, output_dir='.'):
    """Scrive il piano dei turni in `output/turni.csv` (layout verticale)

    Se `pandas` è disponibile salva anche `turni.xlsx` e usa il DataFrame per
    stampare la tabella in console; altrimenti scrive il CSV manualmente e
    stampa la stessa tabella in formato testuale.

    Nota: non vengono creati file di conteggi (CSV/XLSX).
    """
    try:
        import pandas as pd
        pandas_available = True
    except Exception:
        pandas_available = False

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Costruiamo righe utili
    schedule_rows = []
    for giorno, t in turni.items():
        mattina = t.get('mattina') if t.get('mattina') is not None else ''
        pomeriggio = t.get('pomeriggio') if t.get('pomeriggio') is not None else ''
        schedule_rows.append({
            'giorno': str(giorno).capitalize(),
            'mattina': str(mattina),
            'pomeriggio': str(pomeriggio)
        })

    days = [r['giorno'] for r in schedule_rows]
    mattine = [r['mattina'] for r in schedule_rows]
    pomeriggi = [r['pomeriggio'] for r in schedule_rows]

    csv_path = output_dir / 'turni.csv'

    if pandas_available:
        import pandas as pd  # noqa: F401
        df_vert = pd.DataFrame([mattine, pomeriggi], index=['Mattina', 'Pomeriggio'], columns=days)
        xlsx_path = output_dir / 'turni.xlsx'

        df_vert.to_csv(csv_path, encoding='utf-8')
        try:
            df_vert.to_excel(xlsx_path)
        except Exception:
            # se non si può scrivere l'XLSX, ignoriamo l'errore
            pass

        print(f"\nFiles salvati nella cartella: {output_dir}\n- {csv_path.name} (CSV)\n- {xlsx_path.name} (XLSX, se supportato)")
        print("\n⌚ Orario (verticale, come in CSV):")
        print(df_vert.to_string())

        return True

    # fallback senza pandas: scriviamo CSV verticale manualmente e stampiamo solo la tabella
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([''] + days)
        writer.writerow(['Mattina'] + mattine)
        writer.writerow(['Pomeriggio'] + pomeriggi)

    print(f"\nFiles salvati nella cartella: {output_dir}\n- {csv_path.name} (CSV). Per output tabellare e file Excel installa pandas e openpyxl: pip install pandas openpyxl")

    print("\n⌚ Orario (verticale, come in CSV):")
    print('\t' + '\t'.join(days))
    print('Mattina\t' + '\t'.join(mattine))
    print('Pomeriggio\t' + '\t'.join(pomeriggi))

    return True
