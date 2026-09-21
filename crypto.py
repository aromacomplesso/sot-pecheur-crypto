# Modulo: crypto.py
# Implementazione dell'Aritmetica Modulare (Modulo 25 e Modulo 26)

ALFABETO_26 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALFABETO_25 = "ABCDEFGHIJKLMNOPQRSTUVXYZ"  # Omissione filologica della "W"

MAPPA_26 = {char: i for i, char in enumerate(ALFABETO_26)}
MAPPA_25 = {char: i for i, char in enumerate(ALFABETO_25)}

def decifra_segmento(testo_cifrato, chiave, modulo=26, modo="sub"):
    """
    Decifra una sequenza mediante aritmetica modulare ciclica.
    Modo 'sub': Decifratura standard di Vigenere -> (Cifrato - Chiave) mod N
    Modo 'add': Operazione additiva inversa     -> (Cifrato + Chiave) mod N
    (Nota: nel cifrario storico di Beaufort reciproco opera come (Chiave - Cifrato) mod N).
    """
    alfabeto = ALFABETO_25 if modulo == 25 else ALFABETO_26
    mappa = MAPPA_25 if modulo == 25 else MAPPA_26
    n = modulo
    len_chiave = len(chiave)
    risultato = []

    for i, char in enumerate(testo_cifrato):
        valore_c = mappa[char]
        valore_k = mappa[chiave[i % len_chiave]]

        if modo == "sub":
            valore_p = (valore_c - valore_k) % n
        else:
            valore_p = (valore_c + valore_k) % n

        risultato.append(alfabeto[valore_p])

    return "".join(risultato)
