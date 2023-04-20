import pandas as pd
from deap import base, creator, tools, algorithms
import random

# Load the bug data into a pandas dataframe
bugs = pd.read_csv('bugs.csv')

# Define the genetic algorithm parameters
POPULATION_SIZE = 100
P_CROSSOVER = 0.9
P_MUTATION = 0.1
MAX_GENERATIONS = 50
HALL_OF_FAME_SIZE = 10

# Define the evaluation function that calculates the CII
def evaluateCII(individual):
    assignee_param_bugs = bugs.groupby(['Assignee', 'Type', 'Component', 'Priority', 'Severity', 'Classification'])['Bug ID'].count().reset_index()
    assignee_param_bugs = assignee_param_bugs.pivot_table(index=['Assignee', 'Type', 'Component', 'Priority', 'Severity', 'Classification'], columns='Bug ID', values='Bug ID').reset_index()
    assignee_param_bugs = assignee_param_bugs.fillna(0)
    assignee_param_bugs.columns.name = None
    assignee_param_bugs['expertise_score'] = individual[0]
    assignee_param_bugs['trust_factor'] = individual[1]
    assignee_param_bugs['cii'] = assignee_param_bugs['expertise_score'] * assignee_param_bugs['trust_factor']
    corr_matrix = assignee_param_bugs[['Assignee', 'cii']].groupby('Assignee').corr(method='pearson')
    corr_matrix = corr_matrix.unstack(level=0).fillna(0)
    cii = corr_matrix.sum().sum()
    return (cii,)

# Create the fitness function and the individual class
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Create the toolbox with the genetic operators
toolbox = base.Toolbox()
toolbox.register("expertise_score", random.uniform, 0, 1)
toolbox.register("trust_factor", random.uniform, 0, 1)
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.expertise_score, toolbox.trust_factor), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluateCII)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Create the hall of fame and the statistics object
hof = tools.HallOfFame(HALL_OF_FAME_SIZE)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("max", max)

# Run the genetic algorithm
population = toolbox.population(n=POPULATION_SIZE)
algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION, ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

# Print the best individual found
best = hof.items[0]
print("Best individual = ", best)
