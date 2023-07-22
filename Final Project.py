#FINAL PROJECT
#Social Network Analysis
#ARMIN ZAKARIAN
#Importing Libraries

import random
import matplotlib.pyplot as plt
import numpy as np

# Genetic Algorithm Class
class GeneticAlgorithm:
    def __init__(self, nodes, edges, weights, k, population_size=50, generations=100, mutation_rate=0.1):
        self.nodes = nodes
        self.edges = edges
        self.weights = weights
        self.k = k
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    #  Linear Threshold Model
    def calculate_influence(self, seed_set):
        activated_nodes = set(seed_set)
        new_activated = set()

        while new_activated:
            for activated_node in new_activated:
                for neighbor in self.edges[activated_node]:
                    if neighbor not in activated_nodes:
                        # tolid astane
                        threshold = np.random.normal(0.5, 0.1)
                        weight_sum = sum(self.weights[neighbor][activated_neighbor] for activated_neighbor in activated_nodes)

                        if weight_sum >= threshold:
                            activated_nodes.add(neighbor)

            new_activated = activated_nodes - new_activated

        return len(activated_nodes)

    # initial population seed_set
    def initial_population(self):
        population = []
        for _ in range(self.population_size):
            candidate = random.sample(self.nodes, self.k)
            population.append(candidate)

        return population

    # fitness def
    def fitness(self, candidate):
        return self.calculate_influence(candidate)

    # Parents selection for new generation
    def select_parents(self, population):
        parents = []
        fitness_values = [self.fitness(candidate) for candidate in population]
        total_fitness = sum(fitness_values)
        probabilities = [fitness / total_fitness for fitness in fitness_values]

        for _ in range(2):
            parent = random.choices(population, probabilities)[0]
            parents.append(parent)

        return parents

    # Crossover def Parents
    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, self.k - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    # Mutate def
    def mutate(self, candidate):
        for i in range(self.k):
            if random.random() < self.mutation_rate:
                candidate[i] = random.choice(self.nodes)

    # Optimization def for seed set
    def optimize(self):
        population = self.initial_population()

        for _ in range(self.generations):
            new_population = []

            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)

            population = new_population

        # Select the Best seed set
        return max(population, key=self.fitness)

# Example for seed set
nodes = ['A', 'B', 'C', 'D']
edges = {'A': ['B', 'C'], 'B': ['C', 'D'], 'C': ['D'], 'D': []}
weights = {'A': {'B': 0.6, 'C': 0.8}, 'B': {'C': 0.4, 'D': 0.5}, 'C': {'D': 0.7}, 'D': {}}
k = 2

# Sample for GENETIC ALGORITHM
genetic = GeneticAlgorithm(nodes, edges, weights, k)
seed_set = genetic.optimize()
print(seed_set)