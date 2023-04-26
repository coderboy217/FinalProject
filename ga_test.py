from ga import GeneticAlgorithm

# Define target string and GA parameters
target = "Hello, world!"
mutation_rate = 0.01
population_size = 100

# Initialize GeneticAlgorithm object
ga_obj = GeneticAlgorithm(target, mutation_rate, population_size)

# Test fitness() method with example chromosome
chromosome = "0100100001100101011011000110110001101111001000000111011101101111011100100110110001100100"
fitness_score = ga_obj.fitness(chromosome)
print(f"Fitness of example chromosome '{chromosome}': {fitness_score}")
