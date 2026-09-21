def linear_topology(text):
    return [text]

def get_perimeter_points(width, height):
    """
    Returns the coordinates of the perimeter of a width x height grid,
    read clockwise starting from top-left (0,0).
    """
    points = []
    for c in range(width): points.append((0, c))
    for r in range(1, height - 1): points.append((r, width - 1))
    for c in range(width - 1, -1, -1): points.append((height - 1, c))
    for r in range(height - 2, 0, -1): points.append((r, 0))
    return points

def perimeter_topologies(text, width=22, height=12):
    """
    Given a text of length matching the perimeter, maps characters to perimeter
    coordinates and reads them back in various geometric orders.
    """
    points = get_perimeter_points(width, height)
    if len(text) != len(points):
        return []
        
    point_to_char = {points[i]: text[i] for i in range(len(text))}
    
    topologies = []
    
    # 1. Vertical columns (left to right, top to bottom)
    pts_vertical = sorted(points, key=lambda p: (p[1], p[0]))
    topologies.append("".join(point_to_char[p] for p in pts_vertical))
    
    # 2. Vertical columns (right to left)
    pts_vertical_rev = sorted(points, key=lambda p: (-p[1], p[0]))
    topologies.append("".join(point_to_char[p] for p in pts_vertical_rev))
    
    # 3. Diagonal (top-left to bottom-right axes)
    pts_diag1 = sorted(points, key=lambda p: (p[0] - p[1], p[0]))
    topologies.append("".join(point_to_char[p] for p in pts_diag1))
    
    # 4. Diagonal (top-right to bottom-left axes)
    pts_diag2 = sorted(points, key=lambda p: (p[0] + p[1], p[0]))
    topologies.append("".join(point_to_char[p] for p in pts_diag2))
    
    return topologies

def _is_valid_knight_move(r, c, visited):
    return 0 <= r < 8 and 0 <= c < 8 and (r, c) not in visited

def _get_knight_moves(r, c):
    moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]
    return [(r + dr, c + dc) for dr, dc in moves]

def warnsdorff_tour(start_r, start_c):
    """
    Generates a Knight's Tour on 8x8 using Warnsdorff's heuristic.
    """
    path = [(start_r, start_c)]
    visited = set(path)
    
    for _ in range(63):
        curr_r, curr_c = path[-1]
        next_moves = []
        for nr, nc in _get_knight_moves(curr_r, curr_c):
            if _is_valid_knight_move(nr, nc, visited):
                # Count onward moves
                onward_count = sum(1 for nnr, nnc in _get_knight_moves(nr, nc) if _is_valid_knight_move(nnr, nnc, visited))
                next_moves.append((onward_count, (nr, nc)))
        
        if not next_moves:
            return None # Dead end
            
        # Sort by onward count (Warnsdorff's rule: pick minimum)
        next_moves.sort(key=lambda x: x[0])
        best_move = next_moves[0][1]
        path.append(best_move)
        visited.add(best_move)
        
    return path

def knight_topologies(text):
    """
    Reads the 8x8 text along various knight's tours.
    Text is assumed to be laid out linearly row by row.
    """
    if len(text) != 64:
        return []
        
    topologies = []
    
    # Generate some tours from different corners
    starts = [(0,0), (0,7), (7,0), (7,7), (3,3), (4,4)]
    
    for sr, sc in starts:
        tour = warnsdorff_tour(sr, sc)
        if tour and len(tour) == 64:
            # Map tour coordinates to linear text index (row * 8 + col)
            permuted = "".join(text[r * 8 + c] for r, c in tour)
            topologies.append(permuted)
            
    # Include a hardcoded Euler-like magic tour pattern if desired, 
    # but Warnsdorff from corners covers the requested "historical" feel.
    
    return topologies

def generate_all_topologies(text):
    """
    Yields pairs of (topology_name, permuted_text)
    """
    yield ("Linear", text)
    
    perims = perimeter_topologies(text, width=22, height=12)
    for i, t in enumerate(perims):
        yield (f"Perimeter_22x12_Variant_{i+1}", t)
        
    knights = knight_topologies(text)
    for i, t in enumerate(knights):
        yield (f"Knight_Tour_Variant_{i+1}", t)
