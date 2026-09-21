# Decodifica Crittografica del «Sot Pêcheur» (Rennes-le-Château)

Questo repository contiene l'architettura software e gli script in linguaggio Python utilizzati per l'analisi statistica, geometrica e algebrica del crittogramma perimetrale del **«Sot Pêcheur»**, associato alla vicenda storica di **Rennes-le-Château**.

Il codice costituisce il corredo tecnico e metodologico del capitolo di saggistica storico-scientifica:
> *«La Nuova Frontiera della Cerca: Come l'Intelligenza Artificiale ha interpretato l'enigma del Sot Pêcheur»*

---

## Struttura del Software

L'ecosistema opera secondo una pipeline modulare sequenziale:

1. **`engine_fase1_2.py`**:
   - Estrazione della sequenza perimetrale di 64 caratteri dalla griglia rettangolare 22x12.
   - Calcolo dell'Indice di Coincidenza (IC) di William Friedman ($IC \approx 0{,}0417$), a riprova della natura polialfabetica del testo cifrato.

2. **`topology.py`**:
   - Modellazione della scacchiera ortogonale 8x8 e della griglia perimetrale rettangolare 22x12.
   - Implementazione dell'algoritmo euristico di Warnsdorff (1823) per la generazione deterministica del Salto del Cavallo (*Knight's Tour*) e percorsi perimetrali geometrici.

3. **`crypto.py`**:
   - Motore algebrico modulare ciclico.
   - Supporto simultaneo per **Modulo 25** (filologia ottocentesca francese con omissione filologica della lettera *W*) e **Modulo 26** (moderno).
   - Modalità di decifrazione sottrattiva (Vigenère) e additiva/reciproca (Beaufort).

4. **`fitness.py`**:
   - Funzione di valutazione statistica e plausibilità lessicale.
   - Livello 1: Riconoscimento lineare delle particelle grammaticali e parole comuni del francese (`lunghezza × 10`).
   - Livello 2: Ponderazione esponenziale per lessemi contestuali legati a Rennes-le-Château (`(2^L) × 100`).

5. **`keys_generator.py`**:
   - Generatore combinatorio efficiente degli indici numerici delle chiavi alfabetiche (da 2 a 5 caratteri) per Modulo 25 e 26.

6. **`main.py`**:
   - Orchestratore della setacciatura combinatoria (fino a 495 milioni di combinazioni).
   - Gestione della memoria tramite coda di priorità *min-heap* (`heapq`) per il salvataggio dei migliori 20 risultati.

---

## Requisiti ed Esecuzione

Il codice è scritto in puro **Python 3** standard (senza dipendenze esterne obbligatorie).

```bash
# Esecuzione del calcolo dell'Indice di Coincidenza
python3 engine_fase1_2.py

# Test dei singoli moduli
python3 crypto.py
python3 topology.py
```

---

## Licenza e Replicabilità

Codice pubblicato a scopo di verifica scientifica, trasparenza metodologica e riproducibilità della ricerca storiografica.
