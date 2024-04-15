import numpy as np
from tslearn.metrics import dtw
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

"""
This file can be used to find similar movement patterns to a target movement pattern.
So given a list of all player movements over a game, we can group each into a np array and track ones with similar patterns using the dtw tool.
Input: target_movement: np array of players' movements from one play
         all_movements: list of np arrays of all players' movements from the every play in the game
Output: A list of np arrays of all the movements that are similar to the target movement
"""
def find_similar_movement_pattern(target_movement, all_movements, k=1):
    distances = [dtw(target_movement, movement) for movement in all_movements]
    indices = np.argsort(distances)[:k]
    similar_movements = [all_movements[i] for i in indices]
    return similar_movements

def generate_movement_pattern(num_frames, num_dimensions):
    # Generate a random initial position
    initial_position = np.random.rand(num_dimensions)
    
    # Generate random deltas for each dimension
    deltas = np.random.uniform(-0.1, 0.1, (num_frames, num_dimensions))
    
    # Generate movement pattern by accumulating deltas
    movement_pattern = np.cumsum(deltas, axis=0) + initial_position
    
    return movement_pattern

target_movement = generate_movement_pattern(10, 2)
all_movements = [generate_movement_pattern(10, 2) for _ in range(15)]

similar_movements = find_similar_movement_pattern(target_movement, all_movements, k=1)

plt.figure(figsize=(10, 5))
for movement in similar_movements:
    plt.plot(movement[:, 0], movement[:, 1], marker='o', label='Similar Movement')

plt.plot(target_movement[:, 0], target_movement[:, 1], marker='o', color='red', label='Target Movement')
plt.legend()
plt.show()
#print("Similar movements shape:", [movement.shape for movement in similar_movements])
#print(f"All movements: {all_movements}")
