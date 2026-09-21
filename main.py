import heapq
import time
from crypto import vigenere_decrypt_fast, text_to_indices, Alphabet
from keys_generator import generate_key_indices, count_keys
from fitness import calculate_fitness
from topology import generate_all_topologies

CIPHERTEXT = "YENSZNUMGLNYYRFVHENMZFZZFDHZVTQHAKXFPKCZPJITSMRYKVSTVOYNKTRRLUVP"

def run_analysis():
    topologies = list(generate_all_topologies(CIPHERTEXT))
    modulos = [25, 26]
    modes = ['sub', 'add']
    
    top_results = [] # max heap (using negative score for heapq? No, python heapq is min-heap, so we keep the top N items. If score is higher than min, we pop and push.)
    MAX_RESULTS = 20
    
    print(f"Starting analysis on {len(topologies)} topologies.")
    
    start_time = time.time()
    
    for topo_name, permuted_text in topologies:
        print(f"\nEvaluating topology: {topo_name} -> {permuted_text}")
        
        for modulo in modulos:
            print(f"  Modulo: {modulo}")
            key_count = count_keys(modulo, min_len=2, max_len=5)
            
            # Pre-translate the permuted ciphertext to indices
            ciphertext_indices = text_to_indices(permuted_text, modulo)
            
            for mode in modes:
                print(f"    Mode: {mode}")
                
                keys_gen = generate_key_indices(modulo, min_len=2, max_len=5)
                
                # To quickly translate key indices back to string for the output
                alphabet = Alphabet.get_alphabet(modulo)
                
                for i, key_indices in enumerate(keys_gen):
                    
                    if i > 0 and i % 2000000 == 0:
                        elapsed = time.time() - start_time
                        print(f"      Processed {i}/{key_count} keys... (Elapsed: {elapsed:.2f}s)")
                        
                    plaintext = vigenere_decrypt_fast(ciphertext_indices, key_indices, modulo, mode)
                    score = calculate_fitness(plaintext)
                    
                    if score > 0:
                        key_str = "".join(alphabet[idx] for idx in key_indices)
                        
                        if len(top_results) < MAX_RESULTS:
                            heapq.heappush(top_results, (score, plaintext, key_str, topo_name, modulo, mode))
                        elif score > top_results[0][0]:
                            heapq.heappushpop(top_results, (score, plaintext, key_str, topo_name, modulo, mode))
                            
    end_time = time.time()
    print(f"\nAnalysis completed in {end_time - start_time:.2f} seconds.")
    print("\n" + "="*50)
    print("--- TOP RESULTS ---")
    print("="*50)
    
    # Sort descending
    sorted_results = sorted(top_results, key=lambda x: x[0], reverse=True)
    for res in sorted_results:
        score, plaintext, key_str, topo_name, modulo, mode = res
        print(f"Score: {score}")
        print(f"Key: {key_str} (Len {len(key_str)}) | Modulo: {modulo} | Mode: {mode} | Topology: {topo_name}")
        print(f"Text: {plaintext}")
        print("-" * 50)

if __name__ == "__main__":
    run_analysis()
