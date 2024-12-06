import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class ModelNetwork(nn.Module):
    def __init__(self, *, input_dim, hidden_layers, output_dim):
        """ Initialize the simple neural network.
        
        Parameters:
        - input_dim: Dimension of the input features.
        - hidden_layers: List of integers representing the number of neurons in each hidden layer.
        - output_dim: Dimension of the output (number of classes).
        """
        super(ModelNetwork, self).__init__()
        layers = []
        prev_dim = input_dim
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            prev_dim = hidden_dim
        layers.append(nn.Linear(prev_dim, output_dim))
        layers.append(nn.Softmax(dim=1))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        """ Forward pass through the network.
        
        Parameters:
        - x: Input tensor.
        
        Returns:
        - Output tensor.
        """
        return self.model(x)


class EvolutionarySearcher:
    def __init__(self, input_dim, output_dim, population_size=10, mutation_rate=0.1, crossover_rate=0.7, generations=50):
        """ Initialize the evolutionary search algorithm.
        
        Parameters:
        - input_dim: Dimension of the input features.
        - output_dim: Dimension of the output (number of classes).
        - population_size: Number of individuals in the population.
        - mutation_rate: Probability of mutation.
        - crossover_rate: Probability of crossover.
        - generations: Number of generations to evolve.
        """
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.population = self._initialize_population()

    def _initialize_population(self):
        """ Initialize the population with random architectures.
        
        Returns:
        - List of dictionaries representing the architectures.
        """
        population = []
        for _ in range(self.population_size):
            hidden_layers = [random.randint(16, 128) for _ in range(random.randint(1, 3))]
            population.append({'hidden_layers': hidden_layers})
        return population

    def _mutate(self, individual):
        """ Mutate an individual's architecture.
        
        Parameters:
        - individual: Dictionary representing the architecture.
        
        Returns:
        - Mutated architecture.
        """
        if random.random() < self.mutation_rate:
            index = random.randint(0, len(individual['hidden_layers']) - 1)
            individual['hidden_layers'][index] = random.randint(16, 128)
        return individual

    def _crossover(self, parent1, parent2):
        """ Perform crossover between two parents.
        
        Parameters:
        - parent1: First parent's architecture.
        - parent2: Second parent's architecture.
        
        Returns:
        - Child architecture.
        """
        if random.random() < self.crossover_rate:
            min_layer_dim =  min(len(parent1['hidden_layers']), len(parent2['hidden_layers']))
            split_point = random.randint(1, min_layer_dim)
            child_hidden_layers = parent1['hidden_layers'][:split_point] + parent2['hidden_layers'][split_point:]
            return {'hidden_layers': child_hidden_layers}
        else:
            return parent1

    def _evaluate_fitness(self, individual, X_train, y_train, X_val, y_val):
        """ Evaluate the fitness of an individual's architecture.
        
        Parameters:
        - individual: Dictionary representing the architecture.
        - X_train: Training data.
        - y_train: Training labels.
        - X_val: Validation data.
        - y_val: Validation labels.
        
        Returns:
        - Fitness score (accuracy on validation set).
        """
        model = ModelNetwork(input_dim=self.input_dim, hidden_layers=individual['hidden_layers'], output_dim=self.output_dim)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        # Train the model
        for _ in range(10):
            optimizer.zero_grad()
            outputs = model(X_train)
            loss = criterion(outputs, y_train)
            loss.backward()
            optimizer.step()

        # Evaluate on validation set
        with torch.no_grad():
            outputs = model(X_val)
            _, predicted = torch.max(outputs.data, 1)
            accuracy = (predicted == y_val).sum().item() / y_val.size(0)
        return accuracy

    def search(self, train_features, train_targets, validate_features, validate_targets, verbose=False):
        """ Perform the evolutionary search.
        
        Parameters:
        - train_features: Training data.
        - train_targets: Training labels.
        - validate_features: Validation data.
        - validate_targets: Validation labels.
        - verbose: Whether to output logs during the search.
        
        Returns:
        - Best architecture found.
        """
        x_train = torch.tensor(train_features, dtype=torch.float32)
        y_train = torch.tensor(train_targets, dtype=torch.long)
        x_val = torch.tensor(validate_features, dtype=torch.float32)
        y_val = torch.tensor(validate_targets, dtype=torch.long)

        for generation in range(self.generations):
            # Evaluate fitness
            fitness_scores = [self._evaluate_fitness(individual, x_train, y_train, x_val, y_val) for individual in self.population]
            best_index = np.argmax(fitness_scores)
            best_individual = self.population[best_index]
            if verbose:
                print(f"Generation {generation}, Best Fitness: {fitness_scores[best_index]:.4f}")

            # Select parents
            parents = [self.population[i] for i in np.argsort(fitness_scores)[-self.population_size//2:]]

            # Create new population
            new_population = [best_individual]  # Keep the best individual
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(parents, 2)
                child = self._crossover(parent1, parent2)
                child = self._mutate(child)
                new_population.append(child)

            self.population = new_population

        if verbose:
            print("best architecture Found:", best_individual)
        return best_individual
