# Modulo: main.py
# Orchestrazione della setacciatura massiva e salvataggio dei profili ottimali

import heapq
from itertools import product
from crypto import decifra_segmento, ALFABETO_25, ALFABETO_26
from fitness import calcola_fitness

CAPACITA_HEAP = 20

def esegui_scansione(stringhe_topologiche):
    """
    Scansiona lo spazio di ricerca su moduli 25 e 26, chiavi da 2 a 5 lettere,
    modalità add e sub, mantenendo i migliori 20 risultati in un min-heap.
    """
    migliori_risultati = []  # Struttura min-heap: (fitness, dati_risultato)

    for nome_topo, testo_cifrato in stringhe_topologiche.items():
        for modulo in [25, 26]:
            alfabeto = ALFABETO_25 if modulo == 25 else ALFABETO_26

            # Generazione iterativa delle chiavi per lunghezze da 2 a 5
            for lun in range(2, 6):
                for chiave_tuple in product(alfabeto, repeat=lun):
                    chiave = "".join(chiave_tuple)

                    for modo in ["sub", "add"]:
                        decifrato = decifra_segmento(testo_cifrato, chiave, modulo, modo)
                        score = calcola_fitness(decifrato)

                        # Gestione della coda di priorità
                        if len(migliori_risultati) < CAPACITA_HEAP:
                            heapq.heappush(migliori_risultati, (score, chiave, modulo, modo, nome_topo, decifrato))
                        elif score > migliori_risultati[0][0]:
                            heapq.heapreplace(migliori_risultati, (score, chiave, modulo, modo, nome_topo, decifrato))

    return sorted(migliori_risultati, key=lambda x: x[0], reverse=True)
