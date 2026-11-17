import random
import math

from numpy import size

# =========================================================
# PARAMETERS
# =========================================================

POPULATION_SIZE = 10
GENERATIONS = 100

CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.05

CAPACITY = 15


# =========================================================
# ITEM INFORMATION
# =========================================================

ITEMS = {
    '1': {'x': 60, 'y': 200},
    '2': {'x': 23, 'y': 45},
    '3': {'x': 15, 'y': 150},
    '4': {'x': 85, 'y': 90},
    '5': {'x': 71, 'y': 123},
    '6': {'x': 98, 'y': 45},
    '7': {'x': 50, 'y': 220},
    '8': {'x': 20, 'y': 30},
    '9': {'x': 40, 'y': 180},
    '10': {'x': 75, 'y': 155},
    '11': {'x': 82, 'y': 60},
    '12': {'x': 91, 'y': 120},
    '13': {'x': 12, 'y': 210},
    '14': {'x': 37, 'y': 100},
    '15': {'x': 28, 'y': 77},
    '16': {'x': 66, 'y': 89},
    '17': {'x': 55, 'y': 130},
    '18': {'x': 73, 'y': 140},
    '19': {'x': 88, 'y': 33},
    '20': {'x': 42, 'y': 170},
}

ITEM_NAMES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']



# FITNESS FUNCTION

# Calcuate Eucledian distance
def eucledian(x, y):
    return (x-y)**2

def calculate_fitness(chromosome):
   
    cities = []

    for i, bit in enumerate(chromosome):

        if bit == '1':

            item = ITEM_NAMES[i]
            cities.append(ITEMS[item])

    n = size(cities)

    for i in range(0, n - 1):
        dx = eucledian(cities[i]['x'], cities[i+1]['x'])
        dy = eucledian(cities[i]['y'], cities[i+1]['y'])

        fitness = math.sqrt(dx+dy)
    

    return 1/fitness


# 
# INITIAL POPULATION
# 

def generate_population():

    population = []

    for _ in range(POPULATION_SIZE):

        chromosome = ''.join(
            random.choice('01')
            for _ in range(20)
        )

        population.append(chromosome)

    return population


# 
# ROULETTE WHEEL SELECTION
# 

def roulette_selection(population):

    fitness_values = [
        calculate_fitness(chromosome)
        for chromosome in population
    ]

    total_fitness = sum(fitness_values)

    # If every chromosome is invalid
    if total_fitness == 0:
        return random.choice(population)

    return random.choices(
        population,
        weights=fitness_values,
        k=1
    )[0]


# 
# SINGLE-POINT CROSSOVER
# 

def crossover(parent1, parent2):

    if random.random() > CROSSOVER_RATE:
        return parent1, parent2

    point = random.randint(
        1,
        len(parent1) - 1
    )

    child1 = (
        parent1[:point] +
        parent2[point:]
    )

    child2 = (
        parent2[:point] +
        parent1[point:]
    )

    return child1, child2


# 
# MUTATION
# 

def mutation(chromosome):

    chromosome = list(chromosome)

    for i in range(len(chromosome)):

        if random.random() < MUTATION_RATE:

            chromosome[i] = (
                '1'
                if chromosome[i] == '0'
                else '0'
            )

    return ''.join(chromosome)


# 
# DISPLAY POPULATION
# 

def display_population(population, generation):

    print(f"\nGeneration {generation}")


    print(
        "Chromosome | Fitness"
    )

    print("-" * 65)

    for chromosome in population:

        fitness = calculate_fitness(
            chromosome
        )

        print(
            f"{chromosome:^10} | "
            f"{fitness:^7}"
        )


# 
# GENETIC ALGORITHM
# 

def genetic_algorithm():

    population = generate_population()

    best_chromosome = None
    best_fitness = -1

    for generation in range(
        1,
        GENERATIONS + 1
    ):

        display_population(
            population,
            generation
        )

        # 
        # Find best individual
        # 

        generation_best = min(
            population,
            key=lambda chromosome:
                calculate_fitness(chromosome)
        )

        generation_fitness = calculate_fitness(
            generation_best
        )

        if generation_fitness > best_fitness:

            best_fitness = generation_fitness
            best_chromosome = generation_best

        print(
            f"\nBest chromosome: {generation_best}"
        )

        # 
        # Generate next generation
        # 

        new_population = []

        while len(new_population) < POPULATION_SIZE:

            # Roulette-wheel selection
            parent1 = roulette_selection(population)
            parent2 = roulette_selection(population)

            # Crossover
            child1, child2 = crossover(
                parent1,
                parent2
            )

            # Mutation
            child1 = mutation(child1)
            child2 = mutation(child2)

            new_population.append(child1)

            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = new_population

    # 
    # FINAL RESULT
    # 

    final_fitness = (
        calculate_fitness(best_chromosome)
    )


    print("FINAL RESULT:")


    print(
        "Best chromosome :", best_chromosome
    )

    print(
        "Selected items  : ",
        end=""
    )

    selected_items = []

    for i, bit in enumerate(best_chromosome):

        if bit == '1':
            selected_items.append(
                ITEM_NAMES[i]
            )

    print(
        ", ".join(selected_items)
        if selected_items
        else "None"
    )


    print(
        "Fitness         :", final_fitness
    )


if __name__ == "__main__":
    genetic_algorithm()