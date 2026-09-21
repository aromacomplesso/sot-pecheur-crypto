import itertools
from crypto import Alphabet

def generate_keys(modulo, min_len=2, max_len=5):
    """
    Generator yielding all possible keys from length min_len to max_len
    as strings.
    """
    alphabet = Alphabet.get_alphabet(modulo)
    for length in range(min_len, max_len + 1):
        for key_tuple in itertools.product(alphabet, repeat=length):
            yield "".join(key_tuple)

def generate_key_indices(modulo, min_len=2, max_len=5):
    """
    Generator yielding keys as tuples of integers for faster arithmetic.
    """
    alphabet = Alphabet.get_alphabet(modulo)
    m = len(alphabet)
    for length in range(min_len, max_len + 1):
        for key_tuple in itertools.product(range(m), repeat=length):
            yield key_tuple

def count_keys(modulo, min_len=2, max_len=5):
    alphabet = Alphabet.get_alphabet(modulo)
    m = len(alphabet)
    return sum(m ** length for length in range(min_len, max_len + 1))
