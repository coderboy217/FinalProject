import random
import string
import math
from collections import Counter
from typing import List, Tuple

def generate_initial_population(population_size: int, key_length: int) -> List[str]:
    """
    Generates a list of random strings, each of length key_length.
    """
    return [''.join(random.choices(string.ascii_letters + string.digits, k=key_length)) for _ in range(population_size)]

def get_fitness(key: str) -> float:
    """
    Calculates the fitness of the given key based on its Shannon entropy.
    """
    freqs = Counter(key)
    probs = [float(freqs[c]) / len(key) for c in freqs]
    return -sum(p * math.log(p, 2) for p in probs)

def single_point_crossover(parent1: str, parent2: str) -> Tuple[str, str]:
    """
    Performs a single-point crossover between two parent keys to produce two child keys.
    """
    crossover_point = random.randint(1, len(parent1)-1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(key: str, mutation_rate: float) -> str:
    """
    Performs random mutations on the given key based on the mutation rate.
    """
    key_list = list(key)
    for i in range(len(key_list)):
        if random.random() < mutation_rate:
            key_list[i] = random.choice(string.ascii_letters + string.digits)
    return ''.join(key_list)

def generate_encrypted_key(population_size: int = 100, key_length: int = 32, mutation_rate: float = 0.01,
                           num_generations: int = 1000) -> str:
    """
    Generates an encrypted key using a genetic algorithm.
    """
    population = generate_initial_population(population_size, key_length)
    for generation in range(num_generations):
        # Evaluate fitness of each key
        fitness_scores = [(key, get_fitness(key)) for key in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)

        # Check if we've found a key with maximum fitness
        if fitness_scores[0][1] == 0:
            return fitness_scores[0][0]

        # Select parents for next generation using tournament selection
        parents = []
        for _ in range(population_size // 2):
            tournament = random.sample(fitness_scores, k=5)
            tournament.sort(key=lambda x: x[1], reverse=True)
            parents.extend(tournament[:2])

        # Perform single-point crossover and mutation to create children
        children = []
        for i in range(len(parents) // 2):
            child1, child2 = single_point_crossover(parents[i*2][0], parents[i*2+1][0])
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            children.extend([child1, child2])

        # Replace the old population with the new generation
        population = children

    # Return the key with the highest fitness score
    fitness_scores = [(key, get_fitness(key)) for key in population]
    fitness_scores.sort(key=lambda x: x[1], reverse=True)
    return fitness_scores[0][0]
