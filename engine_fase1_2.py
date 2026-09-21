import collections
import math
import json

# ==========================================
# CONSTANTS & INPUTS
# ==========================================
Testo_Centrale_Raw = """YENSZNUMGLNYYRFVHENMZF PSOT+PECHEUR+A+L'EMBZ VOUCHURE DU RHONE, SONZ UPOISSON+SUR+LE GRIL+F LDEUX + FOIS RETOURNAUD RN MALIN SURVINTET+ XH RXV+FOIS+LE GOUTA.CUZ TIT, IL+NE+LUI + RESTA + QV KUE L'ARETE.UN+ANGE + T NVEILLAITET+EN+FIT+UQ YNPEIGNE D'OR.BS.CURH OVTSVKYRMS TIJ PZCKP FX KA"""
Cornice_Esterna = """YENSZNUMGLNYYRFVHENMZFZZFDHZVTQHAKXFPKCZPJITSMRYKVSTVOYNKTRRLUVP"""
ALF_26 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALF_25 = "ABCDEFGHIJKLMNOPQRSTUVXYZ" # W omitted

# French scoring data
# Most common French bigrams
FRENCH_BIGRAMS = ["ES", "EN", "OU", "DE", "NT", "TE", "ON", "SE", "LA", "LE", "RE", "ME", "ER", "NE", "QU", "IT", "UR", "IS", "TI", "ST"]
# Common French words + words from the fable
FRENCH_WORDS = {"LE", "LA", "LES", "DE", "DES", "UN", "UNE", "ET", "EST", "EN", "QUE", "QUI", "DANS", "POUR", "IL", "NE", "LUI", "RESTA", "SOT", "PECHEUR", "ANGE", "FOIS", "DEUX", "TROIS", "SUR", "GRIL", "MALIN", "PEIGNE", "OR", "ARETE", "RHONE", "SON", "POISSON", "VEILLAIT", "FIT"}

# ==========================================
# PHASE 1: SCORING ENGINE
# ==========================================
def calculate_ic(text):
    text = "".join([c for c in text if c.isalpha()])
    N = len(text)
    if N <= 1: return 0
    freqs = collections.Counter(text)
    ic = sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1))
    return ic

def score_french(text):
    text = "".join([c for c in text if c.isalpha()])
    score = 0
    
    # Bigram score
    for i in range(len(text)-1):
        bg = text[i:i+2]
        if bg in FRENCH_BIGRAMS:
            score += 2
            
    # Word score (simplified sliding window)
    for w in FRENCH_WORDS:
        if w in text:
            score += len(w) * 3
            
    return score

def fitness(text):
    ic = calculate_ic(text)
    sc = score_french(text)
    return {"ic": round(ic, 4), "score": sc, "text": text}

# ==========================================
# PHASE 2: TOPOLOGY EXPLORATION
# ==========================================
def warnsdorff_tours():
    """Generates 64 Knight's tours, one from each starting square using Warnsdorff's heuristic."""
    moves = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]
    
    def is_valid(x, y, board):
        return 0 <= x < 8 and 0 <= y < 8 and board[y][x] == -1
        
    def get_degree(x, y, board):
        count = 0
        for dx, dy in moves:
            if is_valid(x+dx, y+dy, board):
                count += 1
        return count

    tours = []
    
    for start_y in range(8):
        for start_x in range(8):
            board = [[-1 for _ in range(8)] for _ in range(8)]
            curr_x, curr_y = start_x, start_y
            board[curr_y][curr_x] = 0
            path = [(curr_x, curr_y)]
            
            for step in range(1, 64):
                next_moves = []
                for dx, dy in moves:
                    nx, ny = curr_x + dx, curr_y + dy
                    if is_valid(nx, ny, board):
                        next_moves.append((get_degree(nx, ny, board), nx, ny))
                
                if not next_moves:
                    break # Dead end
                    
                # Sort by Warnsdorff's rule (minimum degree first)
                next_moves.sort(key=lambda x: x[0])
                _, curr_x, curr_y = next_moves[0]
                board[curr_y][curr_x] = step
                path.append((curr_x, curr_y))
                
            if len(path) == 64:
                tours.append(path)
                
    return tours

def extract_paths(cornice):
    """Extracts strings from the 64-char cornice using different topological paths."""
    grid = [list(cornice[i*8:(i+1)*8]) for i in range(8)]
    paths = {}
    
    # Linear Forward & Reverse
    paths["Linear_FWD"] = cornice
    paths["Linear_REV"] = cornice[::-1]
    
    # Boustrophedon (Snake)
    snake = ""
    for i in range(8):
        if i % 2 == 0:
            snake += "".join(grid[i])
        else:
            snake += "".join(grid[i][::-1])
    paths["Boustrophedon"] = snake
    
    # Spiral (clockwise from top-left)
    spiral = ""
    top, bottom, left, right = 0, 7, 0, 7
    dir = 0
    while top <= bottom and left <= right:
        if dir == 0:
            for i in range(left, right + 1): spiral += grid[top][i]
            top += 1
        elif dir == 1:
            for i in range(top, bottom + 1): spiral += grid[i][right]
            right -= 1
        elif dir == 2:
            for i in range(right, left - 1, -1): spiral += grid[bottom][i]
            bottom -= 1
        elif dir == 3:
            for i in range(bottom, top - 1, -1): spiral += grid[i][left]
            left += 1
        dir = (dir + 1) % 4
    paths["Spiral_CW"] = spiral
    
    # Rotations
    rot90 = ""
    for c in range(8):
        for r in range(7, -1, -1):
            rot90 += grid[r][c]
    paths["Rot90"] = rot90
    
    # Knight's Tours
    tours = warnsdorff_tours()
    for idx, tour in enumerate(tours):
        kt_str = "".join(grid[y][x] for x, y in tour)
        paths[f"KnightTour_{idx}"] = kt_str
        
    return paths

if __name__ == "__main__":
    print("Running Phase 1 & 2 Engine...")
    print(f"Cornice length: {len(Cornice_Esterna)}")
    
    # Test scoring on Cornice
    base_score = fitness(Cornice_Esterna)
    print(f"Base Cornice Fitness: {base_score}")
    
    # Extract topologies
    paths = extract_paths(Cornice_Esterna)
    print(f"Generated {len(paths)} topological paths (including Knight's Tours).")
    
    # Output some paths
    print("\\nSample Topologies:")
    print(f"Boustrophedon: {paths['Boustrophedon'][:20]}...")
    print(f"Spiral_CW:     {paths['Spiral_CW'][:20]}...")
    print(f"KnightTour_0:  {paths['KnightTour_0'][:20]}...")
    print(f"KnightTour_10: {paths['KnightTour_10'][:20]}...")
    
    print("\\nPhase 1 & 2 Completed Successfully. Ready for Phase 3 (Brute Force Vigenere).")
