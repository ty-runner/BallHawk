import numpy as np
from tslearn.metrics import dtw
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

"""
This script is used to find similar movement patterns to a target movement pattern.

Given a list of all player movements over a game, we can group each into a numpy array 
and track ones with similar patterns using the DTW tool.

Functions:
    find_similar_movement_pattern(target_movement, all_movements, k=1):
        Finds and returns the k most similar movement patterns to the target movement.
    
    generate_movement_pattern(num_frames, num_dimensions):
        Generates a random movement pattern with a specified number of frames and dimensions.

Examples:
    # Generate a target movement pattern and a list of movements
    target_movement = generate_movement_pattern(10, 2)
    all_movements = [generate_movement_pattern(10, 2) for _ in range(15)]
    
    # Find the most similar movement pattern
    similar_movements = find_similar_movement_pattern(target_movement, all_movements, k=1)
    
    # Plot the target movement and similar movements
    plt.figure(figsize=(10, 5))
    for movement in similar_movements:
        plt.plot(movement[:, 0], movement[:, 1], marker='o', label='Similar Movement')
    plt.plot(target_movement[:, 0], target_movement[:, 1], marker='o', color='red', label='Target Movement')
    plt.legend()
    plt.show()
"""

def find_similar_movement_pattern(target_movement: np.ndarray, all_movements: list, k: int = 1) -> list:
    """
    Find the k most similar movement patterns to the target movement.

    Args:
        target_movement (np.ndarray): A numpy array of the target movement pattern.
        all_movements (list): A list of numpy arrays representing all movements.
        k (int): The number of similar movements to find.

    Returns:
        list: A list of numpy arrays of the k most similar movements.
    """
    distances = [dtw(target_movement, movement) for movement in all_movements]
    indices = np.argsort(distances)[:k]
    similar_movements = [all_movements[i] for i in indices]
    return similar_movements

def generate_movement_pattern(num_frames: int, num_dimensions: int) -> np.ndarray:
    """
    Generate a random movement pattern.

    Args:
        num_frames (int): The number of frames in the movement pattern.
        num_dimensions (int): The number of dimensions in the movement pattern.

    Returns:
        np.ndarray: A numpy array representing the generated movement pattern.
    """
    initial_position = np.random.rand(num_dimensions)
    deltas = np.random.uniform(-0.1, 0.1, (num_frames, num_dimensions))
    movement_pattern = np.cumsum(deltas, axis=0) + initial_position
    return movement_pattern

# Generate a target movement pattern and a list of movements
target_movement = generate_movement_pattern(10, 2)
all_movements = [generate_movement_pattern(10, 2) for _ in range(15)]

# Find the most similar movement pattern
similar_movements = find_similar_movement_pattern(target_movement, all_movements, k=1)

# Plot the target movement and similar movements
plt.figure(figsize=(10, 5))
for movement in similar_movements:
    plt.plot(movement[:, 0], movement[:, 1], marker='o', label='Similar Movement')

plt.plot(target_movement[:, 0], target_movement[:, 1], marker='o', color='red', label='Target Movement')
plt.legend()
plt.show()
