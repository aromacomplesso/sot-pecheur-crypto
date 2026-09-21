# Modulo: fitness.py
# Funzione di plausibilità linguistica con ponderazione esponenziale

# Bigrammi a frequenza dominante nel francese classico (incluso "AN")
BIGRAMMI_FRANCESI = {
    "ES", "EN", "OU", "DE", "TE", "ON", "SE", "LA", "LE", "RE",
    "ME", "ER", "NE", "QU", "IT", "UR", "IS", "TI", "ST", "NT", "AN"
}

# Lessico contestuale del crittogramma e del patrimonio storico
PAROLE_CHIAVE_CONTESTUALI = [
    "CHATEAU", "ASMODEE", "PECHEUR", "POUSSIN", "PRIEURE",
    "RENNES", "RHONE", "POISSON", "GRIL", "ARETE", "PEIGNE"
]

def calcola_fitness(testo):
    """
    Assegna un punteggio numerico oggettivo al testo decifrato.
    Combina la morbidezza fonetica dei bigrammi con il balzo
    esponenziale associato a parole compiute: (2 elevato a L) · 100.
    """
    punteggio = 0.0

    # Livello 1: Riconoscimento dei bigrammi con regolarizzazione additiva
    for i in range(len(testo) - 1):
        coppia = testo[i:i+2]
        if coppia in BIGRAMMI_FRANCESI:
            punteggio += 10.0
        else:
            punteggio += 0.05  # Costante infinitesima di smoothing di Laplace

    # Livello 2: Riconoscimento lessicale con crescita esponenziale
    for parola in PAROLE_CHIAVE_CONTESTUALI:
        if parola in testo:
            lunghezza = len(parola)
            punteggio += (2 ** lunghezza) * 100

    return punteggio
