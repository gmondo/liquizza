#!/usr/bin/env python3
import re, sys

def find_questions(text):
    """
    Restituisce una lista di tuple (num_domanda, start_idx, end_idx).
    """
    headers = list(re.finditer(r'^[ \t]*#\s*Question\s+(\d+)', text, re.MULTILINE))
    sections = []
    for i, m in enumerate(headers):
        num = int(m.group(1))
        start = m.start()
        end = headers[i+1].start() if i+1 < len(headers) else len(text)
        sections.append((num, start, end))
    return sections

def check_section(section_text):
    """
    Divide la sezione in blocchi separati da almeno una riga vuota
    (escludendo l'header) e restituisce il numero di blocchi e i blocchi stessi.
    """
    lines = section_text.splitlines()[1:]      # scarto l'header
    body = "\n".join(lines)
    blocks = re.split(r'\n[ \t]*\n', body)      # split su riga vuota
    blocks = [b for b in blocks if b.strip()]  # tolgo eventuali vuoti residui
    return len(blocks), blocks

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} file.txt")
        sys.exit(2)

    txt = open(sys.argv[1], encoding='utf-8').read()
    questions = find_questions(txt)
    problems = []

    for num, start, end in questions:
        sec = txt[start:end]
        count, blocks = check_section(sec)
        if count != 3:
            problems.append((num, count, blocks))

    if problems:
        print(">>> Errore in queste domande:")
        for num, count, blocks in problems:
            print(f" - Question {num}: trovati {count} blocchi (attesi 3)")
            for i, b in enumerate(blocks, start=1):
                head = b.splitlines()[0]
                print(f"    blocco {i} inizia con: “{head}”")
        sys.exit(1)
    else:
        num_questions = len(questions)
        print(f">>> Tutto OK: trovate {num_questions} sezioni “Question” con 3 blocchi ciascuna.")
        sys.exit(0)

if __name__ == "__main__":
    main()

