import pandas as pd
import numpy as np
from functools import partial
from scipy.spatial.distance import cdist
import random

# Load input data from CSV file
df = pd.read_csv('bug_data.csv')

# Define weight values for each feature
weights = {
    'type': 0.2,
    'resolution': 0.1,
    'priority': 0.2,
    'severity': 0.2,
    'last_login': 0.1,
    'classification': 0.1,
    'knowledge': 0.1
}

# Create a dictionary to map values to integer IDs
value_map = {}

# Define function to encode categorical values as integers
def encode_categorical(column):
    unique_values = column.unique()
    for i, value in enumerate(unique_values):
        value_map[value] = i
    return column.apply(lambda x: value_map[x])

# Encode categorical columns as integers
df['type'] = encode_categorical(df['type'])
df['resolution'] = encode_categorical(df['resolution'])
df['assignee'] = encode_categorical(df['assignee'])
df['priority'] = encode_categorical(df['priority'])
df['severity'] = encode_categorical(df['severity'])
df['classification'] = encode_categorical(df['classification'])

# Define a function to calculate the distance between two bugs
def bug_distance(x1, x2):
    weights_array = np.array(list(weights.values()))
    x1_values = np.array(x1[1:])
    x2_values = np.array(x2[1:])
    categorical_indices = np.where(weights_array < 1)[0]
    categorical_weights = weights_array[categorical_indices]
    categorical_weights /= categorical_weights.sum()
    categorical_distances = cdist(x1_values[categorical_indices].reshape(1, -1),
                                   x2_values[categorical_indices].reshape(1, -1),
                                   metric='hamming')[0]
    numerical_indices = np.where(weights_array == 1)[0]
    numerical_weights = weights_array[numerical_indices]
    numerical_distances = cdist(x1_values[numerical_indices].reshape(1, -1),
                                x2_values[numerical_indices].reshape(1, -1))[0]
    distance = np.dot(categorical_distances, categorical_weights) + \
               np.dot(numerical_distances, numerical_weights)
    return distance

# Define a function to calculate the fitness of a community
def community_fitness(community, distances):
    n_bugs = len(community)
    community_distances = np.zeros((n_bugs, n_bugs))
    for i in range(n_bugs):
        for j in range(i+1, n_bugs):
            community_distances[i][j] = community_distances[j][i] = distances[community[i], community[j]]
    intra_community_distance = community_distances.sum() / (n_bugs * (n_bugs - 1) / 2)
    inter_community_distance = distances[np.ix_(community, community)].mean()
    fitness = intra_community_distance / inter_community_distance
    return fitness

# Define a function to initialize the population
def initialize_population(n_bugs, pop_size):
    population = []
    for i in range(pop_size):
        community = random.sample(range(n_bugs), int(n_bugs/pop_size))
        population.append(community)
    return population

def selection(population):
    pop_scores = []
    for i in range(len(population)):
        score = fitness(population[i])
        pop_scores.append((i, score))
    pop_scores.sort(key=lambda x: x[1], reverse=True)
    mating_pool = []
    for i in range(int(len(population)/2)):
        parent1_index = pop_scores[i][0]
        parent2_index = pop_scores[i+1][0]
        mating_pool.append(population[parent1_index])
        mating_pool.append(population[parent2_index])
    return mating_pool

def crossover(mating_pool):
    children = []
    for i in range(0, len(mating_pool), 2):
        parent1 = mating_pool[i]
        parent2 = mating_pool[i+1]
        child1 = parent1[:4] + parent2[4:]
        child2 = parent2[:4] + parent1[4:]
        children.append(child1)
        children.append(child2)
    return children

def mutation(children, mutation_rate):
    for i in range(len(children)):
        if random.random() < mutation_rate:
            j = random.randint(4, len(children[i])-1)
            if j == 4:
                children[i][j] = random.choice(priority_levels)
            elif j == 5:
                children[i][j] = random.choice(severities)
            elif j == 6:
                children[i][j] = random.choice(last_login_times)
            elif j == 7:
                children[i][j] = random.choice(bug_classifications)
            elif j == 8:
                children[i][j] = round(random.uniform(0, 1), 2)
    return children

def genetic_algorithm(population, mutation_rate, generations):
    best_individual = None
    for i in range(generations):
        mating_pool = selection(population)
        children = crossover(mating_pool)
        population = mutation(children, mutation_rate)
        best_individual = population[0]
        print("Generation: {}, Best Score: {}".format(i+1, fitness(best_individual)))
    return best_individual

# Example usage
if __name__ == "__main__":
    # Read in bug data from CSV file
    df = pd.read_csv("bug_data.csv")
    # Convert categorical variables to lists
    types = list(df["type"])
    resolution_status = list(df["resolution_status"])
    assignees = list(df["assignee"])
    priorities = list(df["priority"])
    severities = list(df["severity"])
    last_login_times = list(df["last_login_time"])
    bug_classifications = list(df["bug_classification"])
    developer_knowledge = list(df["developer_knowledge"])
    # Set up initial population
    population = []
    for i in range(100):
        individual = [random.choice(types), random.choice(resolution_status), random.choice(assignees), 
                      random.choice(priorities), random.choice(severities), random.choice(last_login_times), 
                      random.choice(bug_classifications), round(random.uniform(0, 1), 2)]
        population.append(individual)
    # Run genetic algorithm
    best_individual = genetic_algorithm(population, mutation_rate=0.1, generations=10)
    print("Best individual: ", best_individual)
