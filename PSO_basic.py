"""
A basic implementation of Particle Swarm Optimization (PSO) algorithm for optimization problems.
Author: Nithish K Gnani
"""
import numpy as np

# Defining a sample test function
def sample_test_function(params):
    x, y, z = params[0], params[1], params[2]
    return (x-2)**2 + (y+3)**2 + (z-4)**2

# Defining the Rosenbrock function (basic)
def rosenbrock_function(params):
    x, y = params[0], params[1] # x_i, x_{i+1}
    a = 1
    b = 100
    return (a - x)**2 + b * (y - x**2)**2

# Defining the Sphere function
def sphere_function(params):
    return np.sum(params**2)

# Defining the Rosenbrock function in n dimensions
def rosenbrock_function_n(params):
    a = 1
    b = 100
    return np.sum((a - params[:-1])**2 + b * (params[1:] - params[:-1]**2)**2)

# Get user input to choose the test function
print("Choose the test function:")
print("1. Sample Test Function")
print("2. Rosenbrock Function")
print("3. Sphere Function")
print("4. Rosenbrock Function in n dimensions")
choice = int(input("Enter the number of your choice: "))

# Based on the user input for the test function, set the bounds, and number of dimensions
if choice == 1:
    test_function = sample_test_function
    bounds = np.array([[-10, -10, -10], [10, 10, 10]])
    n_dimensions = 3
    print("Test function: Sample Test Function")
    print("Bounds: ", bounds)
    print("Actual solution: [2, -3, 4]")
elif choice == 2:
    test_function = rosenbrock_function
    bounds = np.array([[-5, -5], [5, 5]])
    n_dimensions = 2
    print("Test function: Rosenbrock Function")
    print("Bounds: ", bounds)
    print("Actual solution: [1, 1]")
elif choice == 3:
    test_function = sphere_function
    bounds = np.array([[-5, -5, -5], [5, 5, 5]])
    n_dimensions = 3
    print("Test function: Sphere Function")
    print("Bounds: ", bounds)
    print("Actual solution: [0, 0, 0]")
elif choice == 4:
    test_function = rosenbrock_function_n
    n_dimensions = int(input("Enter the number of dimensions: "))
    bounds = np.array([[-5] * n_dimensions, [5] * n_dimensions])    
    print("Test function: Rosenbrock Function in", n_dimensions, "dimensions")
    print("Bounds: ", bounds)
    print("Actual solution: [1, 1, ..., 1]")
else:
    raise ValueError("Invalid choice")

# Defining parameters: number of particles, maximum iterations, inertia weight, cognitive and social influence coefficients
num_particles = 120 # Number of particles in the swarm
max_iterations = 2000 # Maximum number of iterations for the optimization
wk = 0.5 # wk high: exploration, wk low: exploitation
c1 = 0.8  # Cognitive decision/influence coefficient
c2 = 0.9  # Social decision/influence coefficient
dt = 1 # Time step
c1 = 1.50
c2 = 1.50

# Initialize the particle/agent positions to random and velocities to zero
particlePosk = np.random.uniform(low=bounds[0], high=bounds[1], size=(num_particles, n_dimensions))
vj = np.zeros((num_particles, n_dimensions))

# Initialize the best positions and best costs for each particle
bestPositions = particlePosk.copy()
best_costs = np.array([test_function(p) for p in particlePosk])

# Initialize the global best position and global best cost
glbBest_position = particlePosk[0].copy()
glbBest_cost = best_costs[0]

# List to store the best cost at each iteration for visualization
best_costs_over_time = []

wkMax = 0.9
wkMin = 0.4

# Perform the optimization
for k in range(max_iterations):
    # Linearly interpolate wk from wkMax to wkMin over the iterations
    wk = wkMax - ((wkMax - wkMin) / max_iterations) * k

    # Random numbers between 0 and 1
    r1 = np.random.rand(num_particles, n_dimensions) 
    r2 = np.random.rand(num_particles, n_dimensions)

    # Cognitive influence
    cognitive_influence = c1 * r1 * (bestPositions - particlePosk)
    # Social influence
    social_influence = c2 * r2 * (glbBest_position - particlePosk)

    # Update velocities
    vj = wk * vj + cognitive_influence + social_influence
    
    # Clamp velocities to prevent overshooting
    vj = np.clip(vj, -0.5 * (bounds[1] - bounds[0]), 0.5 * (bounds[1] - bounds[0]))

    # Update the particle positions
    particlePosk += vj * dt

    # Project the particle positions into the bounds
    particlePosk = np.clip(particlePosk, bounds[0], bounds[1])

    # Evaluate the test function
    costs = np.array([test_function(p) for p in particlePosk])

    # Update the best positions and best costs
    is_best = costs < best_costs # boolean array to check if the new cost is better than the best cost
    bestPositions[is_best] = particlePosk[is_best] # Update the best positions
    best_costs[is_best] = costs[is_best] # Update the best costs

    # Update the global best position and global best cost
    glbBest_index = np.argmin(best_costs)
    glbBest_position = bestPositions[glbBest_index].copy()
    glbBest_cost = best_costs[glbBest_index]

    # Store the best cost for visualization
    best_costs_over_time.append(glbBest_cost)

    # Output the cost at regular intervals
    if k % 500 == 0 or k == max_iterations - 1:
        print(f'Iteration {k+1:3d}: Best Cost = {glbBest_cost:.6f}')

# Print final results
print('Global Best Position:', glbBest_position)
print('Global Best Cost:', glbBest_cost)