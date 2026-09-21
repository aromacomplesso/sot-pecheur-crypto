class Alphabet:
    MOD_26 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    MOD_25 = "ABCDEFGHIJKLMNOPQRSTUVXYZ"  # No 'W'

    @classmethod
    def get_alphabet(cls, modulo):
        if modulo == 25:
            return cls.MOD_25
        elif modulo == 26:
            return cls.MOD_26
        else:
            raise ValueError("Modulo must be 25 or 26")

def vigenere_decrypt(ciphertext, key, modulo, mode):
    alphabet = Alphabet.get_alphabet(modulo)
    m = len(alphabet)
    
    char_to_index = {c: i for i, c in enumerate(alphabet)}
    index_to_char = {i: c for i, c in enumerate(alphabet)}
    
    plaintext = []
    key_len = len(key)
    
    for i, c in enumerate(ciphertext):
        if c not in char_to_index:
            plaintext.append(c)  # Keep non-alphabet chars as is
            continue
            
        k_char = key[i % key_len]
        if k_char not in char_to_index:
            raise ValueError(f"Key character {k_char} not in alphabet for modulo {modulo}")
            
        c_idx = char_to_index[c]
        k_idx = char_to_index[k_char]
        
        if mode == 'sub':
            p_idx = (c_idx - k_idx) % m
        elif mode == 'add':
            p_idx = (c_idx + k_idx) % m
        else:
            raise ValueError("Mode must be 'sub' or 'add'")
            
        plaintext.append(index_to_char[p_idx])
        
    return "".join(plaintext)

def text_to_indices(text, modulo):
    alphabet = Alphabet.get_alphabet(modulo)
    char_to_index = {c: i for i, c in enumerate(alphabet)}
    return [char_to_index[c] if c in char_to_index else c for c in text]

def vigenere_decrypt_fast(ciphertext_indices, key_indices, modulo, mode):
    """
    Optimized version that works with lists of integers.
    """
    alphabet = Alphabet.get_alphabet(modulo)
    m = modulo
    index_to_char = {i: c for i, c in enumerate(alphabet)}
    
    plaintext = []
    key_len = len(key_indices)
    
    for i, c_idx in enumerate(ciphertext_indices):
        if isinstance(c_idx, str):
            plaintext.append(c_idx)
            continue
            
        k_idx = key_indices[i % key_len]
        
        if mode == 'sub':
            p_idx = (c_idx - k_idx) % m
        else:
            p_idx = (c_idx + k_idx) % m
            
        plaintext.append(index_to_char[p_idx])
        
    return "".join(plaintext)
