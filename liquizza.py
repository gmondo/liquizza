import random
import os
import sys
import time

def elabora_contenuto_csv(nome_file):
    domande = []
    with open(nome_file, "r") as file:
        righe = file.readlines()
        for riga in righe:
            riga = riga.strip()
            if not riga or riga.startswith('#'):
                continue
            elementi = riga.split('|')
            domanda = elementi[0]
            num_risposte_errate = int(elementi[1])
            risposte = elementi[2:]
    
            # Tutte le risposte sono corrette, tranne le prime num_risposte_errate
            domande.append({
                "domanda": domanda,
                "num_risposte_errate": num_risposte_errate,
                "risposte": risposte
            })
    return domande

def elabora_contenuto_txt(nome_file):
    with open(nome_file, 'r', encoding='utf-8') as file:
        righe = file.readlines()

    domande_e_risposte = []
    stato = 'domanda'
    domanda = []
    risposte_errate = []
    risposte_corrette = []
    testo_corrente = None
    prev_righe_vuote = 0

    def aggiungi_domanda():
        """Aggiunge la domanda corrente alla lista finale, se valida."""
        if domanda:
            domande_e_risposte.append({
                'domanda': ' '.join(domanda),
                'num_risposte_errate': len(risposte_errate),
                'risposte': risposte_errate + risposte_corrette,
            })

    for riga in righe:
        print(stato, riga)
        riga = riga.rstrip()  # Rimuove spazi e newline finali
        if riga.lstrip().startswith('#'):  # Ignora commenti
            continue

        if riga.strip() == '':  # Riga vuota
            prev_righe_vuote += 1
            if prev_righe_vuote > 1:
                continue

            # Cambia stato in base al contesto
            if stato == 'domanda':
                stato = 'risposte_errate'
            elif stato == 'risposte_errate':
                if testo_corrente:
                    risposte_errate.append(testo_corrente.rstrip())
                testo_corrente = None
                stato = 'risposte_corrette'
            elif stato == 'risposte_corrette':
                if testo_corrente:
                    risposte_corrette.append(testo_corrente.rstrip())
                testo_corrente = None
                aggiungi_domanda()
                stato = 'domanda'
                domanda = []
                risposte_errate = []
                risposte_corrette = []
            continue

        prev_righe_vuote = 0

        if stato == 'domanda':
            domanda.append(riga+'\n')
            continue

        if stato in ['risposte_errate', 'risposte_corrette']:
            # Se la riga è indentata, è una continuazione della risposta corrente
            if riga[0].isspace():
                if testo_corrente:
                    testo_corrente += '\n' + riga.rstrip()
                continue

            # Salva la risposta corrente e inizia una nuova
            if testo_corrente:
                if stato == 'risposte_errate':
                    risposte_errate.append(testo_corrente.rstrip())
                elif stato == 'risposte_corrette':
                    risposte_corrette.append(testo_corrente.rstrip())
            testo_corrente = riga

    # Salva l'ultima risposta e domanda, se presenti
    if testo_corrente:
        if stato == 'risposte_errate':
            risposte_errate.append(testo_corrente.rstrip())
        elif stato == 'risposte_corrette':
            risposte_corrette.append(testo_corrente.rstrip())
    aggiungi_domanda()

    return domande_e_risposte

def leggi_domande_da_file(nome_file):
    domande = []
    if nome_file.endswith(".csv"):
        domande = elabora_contenuto_csv(nome_file)
    else:
        domande = elabora_contenuto_txt(nome_file)
    print(domande)
    return domande

def scegli_file_da_lista(files):
    print("Scegli un file:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    scelta = input("Inserisci il numero del file da caricare: ")
    return files[int(scelta) - 1]

def main():
    if len(sys.argv) > 1:
        nome_file = sys.argv[1]
    else:
        directory = os.getcwd() 
        file_choices = [file for file in os.listdir(directory) \
            if file.endswith(".csv") or file.endswith(".txt")]
    
        if not file_choices:
            print(f"No supported file in {directory}.")
            return
    
        nome_file = scegli_file_da_lista(file_choices)

    domande = leggi_domande_da_file(nome_file)
    random.shuffle(domande)  # Mischia l'ordine delle domande

    start_time = time.time()
    numero_domande = len(domande)
    
    for numero, domanda in enumerate(domande, start=1):
        while True:
            print(f"{numero}/{numero_domande}: {domanda['domanda']}")
            # crea un array di indici di tutte le risposte
            indici_iniziali = list(range(len(domanda['risposte'])))

            # mescola gli indici tenendo traccia della posizione iniziale
            random.shuffle(indici_iniziali)
            risposte_mischiate = [None] * len(domanda['risposte'])
            for i, indice in enumerate(indici_iniziali):
                risposte_mischiate[i] = domanda['risposte'][indice]
        
            # sono corrette le risposte oltre quelle errate
            risposta_corretta = []
            for i, pos_iniziale in enumerate(indici_iniziali):
                if pos_iniziale + 1 > domanda['num_risposte_errate']:
                    risposta_corretta.append(i+1)

            # stampa risposte mescolate e chiedi risposta
            for i, risposta in enumerate(risposte_mischiate, start=1):
                print(f"{i}. {risposta}")
        
            if len(domanda['risposte']) - domanda['num_risposte_errate'] == 1:
                risposte_utente = input("Inserisci il numero della risposta corretta: ")
            else:
                risposte_utente = input("Inserisci il numero delle risposte corrette separate da spazi: ")
            risposte_utente = list(map(int, risposte_utente.split()))
            
            if risposte_utente == risposta_corretta:
                print("Corretto!\n")
                break
            else:
                print("Risposta sbagliata. Riprova.\n")
    
    tempo_medio_risposta = (time.time() - start_time) / numero_domande
    print(f"Tempo medio di risposta: {tempo_medio_risposta:.2f} secondi")

if __name__ == "__main__":
    main()
