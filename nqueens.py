from random import shuffle
from random import randrange
from random import random


def calculate_fitness(desk):
    hit = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if abs(i - j) == abs(desk[i] - desk[j]):
                hit += 1
    return 28 - hit


def visualize(desk):
    visual = [['+' for i in range(8)] for i in range(8)]
    for i in range(8):
        visual[i][desk[i]] = 'Q'
    for i in range(len(visual)):
        visual[i] = ''.join(visual[i])
    return '\n'.join(visual)


class Solver_8_queens:

    def __init__(self, pop_size=100, cross_prob=0.50, mut_prob=0.25):
        self.population = []
        self.fitness = []

        # Генерация исходной случайной популяции.
        for i in range(pop_size):
            desk = list(range(8))
            shuffle(desk)
            self.population.append(desk)
            self.fitness.append(calculate_fitness(desk))

        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def reproduce(self):
        population_old = self.population
        fitness_old = self.fitness
        self.population = []
        self.fitness = []
        while len(self.population) != len(population_old):
            r = randrange(sum(fitness_old))
            summa = 0
            for i in range(len(population_old)):
                if r <= summa:
                    self.population.append(list(population_old[i]))
                    self.fitness.append(fitness_old[i])
                    break
                summa += fitness_old[i]

    def crossingover(self):
        if random() < self.cross_prob:
            p1 = randrange(len(self.population))
            p2 = randrange(len(self.population))
            if p1 != p2:
                k = randrange(len(self.population) - 1) + 1
                slice_1_1 = list(self.population[p1][:k])
                slice_1_2 = list(self.population[p1][k:])
                slice_2_1 = list(self.population[p2][:k])
                slice_2_2 = list(self.population[p2][k:])
                self.population[p1] = slice_1_1 + slice_2_2
                self.population[p2] = slice_2_1 + slice_1_2
                self.fitness[p1] = calculate_fitness(self.population[p1])
                self.fitness[p2] = calculate_fitness(self.population[p2])

    def mutation(self):
        for i in range(len(self.population)):
            if random() < self.mut_prob:
                k1 = randrange(8)
                k2 = randrange(8)
                v1 = self.population[i][k1]
                v2 = self.population[i][k2]
                self.population[i][k1], self.population[i][k2] = v2, v1
                self.fitness[i] = calculate_fitness(self.population[i])

    def get_best_fit(self):
        best_fit = self.fitness[0]
        best_fit_k = 0
        for i in range(1, len(self.population)):
            if self.fitness[i] > best_fit:
                best_fit = self.fitness[i]
                best_fit_k = i
        return best_fit_k, best_fit

    def solve(self, min_fitness=0.98, max_epochs=1000):
        epoch_num = 0
        best_fit_k, best_fit = self.get_best_fit()
        while (max_epochs is None) or (epoch_num < max_epochs):
            if (min_fitness is not None) and (best_fit >= 28 * min_fitness):
                break
            self.reproduce()
            self.crossingover()
            self.mutation()
            best_fit_k, best_fit = self.get_best_fit()
            epoch_num += 1

        # best_fit, epoch_num, visualization
        return best_fit / 28, epoch_num, visualize(self.population[best_fit_k])
