# Modulo: topology.py
# Risoluzione del Cammino del Cavallo tramite l'algoritmo di Warnsdorff (1823)

# Lista ordinata delle 8 mosse legali a "L" del cavallo
# L'ordine vettoriale garantisce uno spareggio deterministico e coerente
MOSSE_CAVALLO = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def mossa_valida(r, c, visitate):
    """Verifica se la casella (r, c) risiede nella scacchiera e non è stata visitata."""
    return 0 <= r < 8 and 0 <= c < 8 and not visitate[r][c]

def calcola_grado(r, c, visitate):
    """Calcola i gradi di libertà residui (uscite future) dalla casella (r, c)."""
    grado = 0
    for dr, dc in MOSSE_CAVALLO:
        if mossa_valida(r + dr, c + dc, visitate):
            grado += 1
    return grado

def esegui_warnsdorff(riga_inizio, colonna_inizio, matrice_8x8):
    """Genera una sequenza lineare di 64 lettere partendo da una coordinata iniziale."""
    visitate = [[False for _ in range(8)] for _ in range(8)]
    r, c = riga_inizio, colonna_inizio
    percorso = [matrice_8x8[r][c]]
    visitate[r][c] = True

    for _ in range(63):
        candidati = []
        for dr, dc in MOSSE_CAVALLO:
            nr, nc = r + dr, c + dc
            if mossa_valida(nr, nc, visitate):
                grado = calcola_grado(nr, nc, visitate)
                candidati.append((grado, nr, nc))

        if not candidati:
            break

        # Regola di Warnsdorff: ordina per grado minimo (spareggio su ordine di lista)
        candidati.sort(key=lambda x: x[0])
        _, r, c = candidati[0]
        visitate[r][c] = True
        percorso.append(matrice_8x8[r][c])

    return "".join(percorso)
