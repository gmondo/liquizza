import random
import os
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
    domande = []
    return domande

def leggi_domande_da_file(nome_file):
    domande = []
    if nome_file.endswith(".csv"):
        domande = elabora_contenuto_csv(nome_file)
    else:
        domande = elabora_contenuto_txt(nome_file)
    return domande
    with open(nome_file, "r") as file:
        righe = file.readlines()
        for riga in righe:
            elementi = riga.strip().split(";")
            domanda = elementi[0]
            risposte = elementi[1:-1]
            risposte_corrette = elementi[-1]
            domande.append({
                "domanda": domanda,
                "risposte": risposte,
                "risposte_corrette": risposte_corrette
            })
    return domande

def scegli_file_da_lista(files):
    print("Scegli un file:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    scelta = input("Inserisci il numero del file da caricare: ")
    return files[int(scelta) - 1]

def main():
    directory = os.getcwd() 
    files_csv = [file for file in os.listdir(directory) \
            if file.endswith(".csv") or file.endswith(".txt")]
    
    if not files_csv:
        print(f"Nessun file .csv o .txt trovato nella directory {directory}.")
        return
    
    nome_file = scegli_file_da_lista(files_csv)  # Scegli il file da caricare
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
