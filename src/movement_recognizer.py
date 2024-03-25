import numpy as np
from tslearn.metrics import dtw
from sklearn.neighbors import NearestNeighbors

def find_similar_movement_pattern(target_movement, all_movements, k=1):
    distances = [dtw(target_movement, movement) for movement in all_movements]
    indices = np.argsort(distances)[:k]
    similar_movements = [all_movements[i] for i in indices]
    return similar_movements

# Example usage:
target_movement = np.array([[x1, y1], [x2, y2], [x3, y3]])  # Your target movement
all_movements = [...]  # List of numpy arrays representing all movements

similar_movements = find_similar_movement_pattern(target_movement, all_movements, k=5)
print("Similar movements found:", similar_movements)
