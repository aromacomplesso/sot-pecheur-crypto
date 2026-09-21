FRENCH_WORDS = [
    "LE", "LA", "UN", "ET", "EST", "QUE", "LES", "DES", "QUI", "DANS", "POUR", "UNE",
    "SUR", "PAR", "PAS", "IL", "ELLE", "DU", "AU", "OU", "CE", "SE", "DE", "NE",
    "EN", "ON", "SA", "SON", "SES", "CES", "AUX"
]

CONTEXT_WORDS = [
    "SOT", "PECHEUR", "POISSON", "RHONE", "GRIL", "ARETE", "ANGE", "PEIGNE",
    "RENNES", "CHATEAU", "TRESOR", "GRAAL", "SION", "PRIEURE", "TEMPLE", 
    "DAGOBERT", "MEROVINGIEN", "MARIE", "MADELEINE", "POUSSIN", "TENIERS", 
    "ASMODEE", "BAPHOMET", "SATOR"
]

WORD_WEIGHTS = {}

# Standard words get linear score based on length
for w in FRENCH_WORDS:
    WORD_WEIGHTS[w] = len(w) * 10

# Contextual words get an exponential bonus based on their length to ensure they dominate the score
for w in CONTEXT_WORDS:
    WORD_WEIGHTS[w] = (2 ** len(w)) * 100

# Convert to list of tuples for faster iteration in the hot loop
SCORING_ITEMS = list(WORD_WEIGHTS.items())

def calculate_fitness(text):
    """
    Calculates the fitness score of a given plaintext.
    The score multiplies the occurrences of each word by its weight.
    """
    score = 0
    for word, weight in SCORING_ITEMS:
        c = text.count(word)
        if c > 0:
            score += c * weight
    return score
