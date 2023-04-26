import random
import string
import math

class GeneticAlgorithm:
    def __init__(self, target_string, mutation_rate, population_size):
        self.target = target_string
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.population = []
        self.fitness_scores = []
        self.generation = 0

        # Initialize population with binary strings of correct length
        for i in range(population_size):
            key = ''.join(random.choice('01') for _ in range(len(target_string)))
            self.population.append(key)

    def fitness(self, key):
        fitness = 0
        for i in range(len(key)):
            # Calculate frequency of each character in the key
            char_count = key.count(key[i])
            char_freq = char_count / len(key)

            # Calculate the entropy for the character frequency
            if char_freq != 0:
                fitness += char_freq * math.log2(char_freq)

        # Take the negative of the entropy to get a fitness score
        return -fitness

    def calculate_fitness(self):
        self.fitness_scores = []
        for key in self.population:
            self.fitness_scores.append(self.fitness(key))

    def selection(self):
        # Select parents using tournament selection
        parents = []
        for i in range(2):
            tournament = random.sample(range(self.population_size), 3)
            parent_index = tournament[0]
            for j in tournament[1:]:
                if self.fitness_scores[j] > self.fitness_scores[parent_index]:
                    parent_index = j
            parents.append(self.population[parent_index])

        return parents

    def crossover(self, parent1, parent2):
        # Perform single point crossover at a valid binary digit boundary
        gene_length = len(parent1) // 2
        crossover_point = gene_length * random.randint(1, len(parent1) // gene_length - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        return child1, child2

    def mutation(self, key):
        # Mutate each binary digit with probability mutation_rate
        mutated_key = ""
        for digit in key:
            if random.random() < self.mutation_rate:
                mutated_key += '0' if digit == '1' else '1'
            else:
                mutated_key += digit

        return mutated_key

    def evolve(self):
        self.calculate_fitness()

        # Select parents and generate offspring
        new_population = []
        for i in range(self.population_size):
            parent1, parent2 = self.selection()
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)
            new_population.append(child1)
            new_population.append(child2)

        # Replace old population with new population
        self.population = new_population
        self.generation += 1

    def get_best_key(self):
        # Get the best key from the current population
        best_index = self.fitness_scores.index(max(self.fitness_scores))
        return self.population[best_index]
