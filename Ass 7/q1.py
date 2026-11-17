import random


# PARAMETERS

POPULATION_SIZE = 6
GENERATIONS = 10
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.05

# FITNESS FUNCTION

def fitness(chromosome):
    """
    Convert 4-bit chromosome to integer x
    and calculate f(x) = 15x - x^2.
    """

    x = int(chromosome, 2)

    return 15 * x - x * x


# INITIAL POPULATION

def generate_population():
    """
    Generate a random population of 4-bit chromosomes.
    """

    population = []

    for _ in range(POPULATION_SIZE):
        chromosome = ''.join(
            random.choice('01')
            for _ in range(4)
        )

        population.append(chromosome)

    return population


# ROULETTE WHEEL SELECTION

def roulette_selection(population):
    """
    Select one chromosome using roulette-wheel selection.
    """

    fitness_values = [
        fitness(chromosome)
        for chromosome in population
    ]

    total_fitness = sum(fitness_values)

    # If all fitness values are zero
    if total_fitness == 0:
        return random.choice(population)

    probabilities = [
        value / total_fitness
        for value in fitness_values
    ]

    return random.choices(
        population,
        weights=probabilities,
        k=1
    )[0]


# SINGLE-POINT CROSSOVER

def crossover(parent1, parent2):
    """
    Perform single-point crossover.
    """

    if random.random() > CROSSOVER_RATE:
        return parent1, parent2

    # Crossover point between 1 and length-1
    point = random.randint(1, len(parent1) - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


# MUTATION

def mutation(chromosome):
    """
    Mutate each bit with a small probability.
    """

    chromosome = list(chromosome)

    for i in range(len(chromosome)):

        if random.random() < MUTATION_RATE:

            chromosome[i] = (
                '1'
                if chromosome[i] == '0'
                else '0'
            )

    return ''.join(chromosome)


# DISPLAY POPULATION

def display_population(population, generation):

    print(f"\nGeneration {generation}")
    print("-" * 45)
    print("Chromosome | x  | Fitness")
    print("-" * 45)

    for chromosome in population:

        x = int(chromosome, 2)
        fit = fitness(chromosome)

        print(
            f"{chromosome:^10} | "
            f"{x:^2} | "
            f"{fit:^7}"
        )


# GENETIC ALGORITHM

def genetic_algorithm():

    population = generate_population()

    best_chromosome = None
    best_fitness = float('-inf')

    for generation in range(1, GENERATIONS + 1):

        display_population(population, generation)

        # Find best individual in current generation

        generation_best = max(
            population,
            key=fitness
        )

        generation_best_fitness = fitness(
            generation_best
        )

        if generation_best_fitness > best_fitness:

            best_fitness = generation_best_fitness
            best_chromosome = generation_best

        print(
            f"\nBest: {generation_best} "
            f"(x={int(generation_best, 2)}, "
            f"fitness={generation_best_fitness})"
        )

        # Create next generation

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

    # FINAL RESULT

    print("\n" + "=" * 50)
    print("FINAL RESULT")
    print("=" * 50)

    x = int(best_chromosome, 2)

    print("Best chromosome :", best_chromosome)
    print("Best x          :", x)
    print("Maximum fitness :", best_fitness)


# MAIN

if __name__ == "__main__":
    genetic_algorithm()