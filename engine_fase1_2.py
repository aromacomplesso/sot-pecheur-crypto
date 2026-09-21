# Modulo: engine_fase1_2.py
# Estrazione perimetrale e calcolo dell'Indice di Coincidenza (IC)

from collections import Counter

# Stringa lineare pura dei 64 caratteri della cornice
CORNER_64 = (
    "YENSZNUMGLNYYRFVHENMZFZZFDHZVTQHAKXFPKCZ"
    "PJITSMRYKVSTVOYNKTRRLUVP"
)

def calcola_indice_coincidenza(testo):
    """
    Calcola l'Indice di Coincidenza di Friedman su una stringa.
    Rapporto tra la somma delle combinazioni di lettere identiche
    e il totale delle coppie estraibili: N * (N - 1).
    """
    n = len(testo)
    if n <= 1:
        return 0.0

    conteggi = Counter(testo)
    somma_coppie = sum(f * (f - 1) for f in conteggi.values())
    totale_coppie = n * (n - 1)

    return somma_coppie / totale_coppie

if __name__ == "__main__":
    ic = calcola_indice_coincidenza(CORNER_64)
    print(f"Lunghezza stringa: {len(CORNER_64)} caratteri")
    print(f"Indice di Coincidenza calcolato: {ic:.4f}")
    # Output effettivo: Indice di Coincidenza calcolato: 0.0417 (168 coppie / 4032)
    # Il valore è coerente con la soglia teorica dei testi cifrati (circa 0.040)
    # e marcatamente distante dal francese in chiaro (circa 0.078).
