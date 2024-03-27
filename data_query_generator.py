import matplotlib.pyplot as plt
import numpy as np
import random

# Boundary
X_LOW = -180
Y_LOW = -90
X_HIGH = 180
Y_HIGH = 90

# Endpoints
p0 = (random.uniform(X_LOW, X_LOW + 5), random.uniform(Y_LOW, Y_LOW + 5))
p1 = (random.uniform(X_HIGH - 5, X_HIGH), random.uniform(Y_HIGH - 5, Y_HIGH))

# Control points
c0 = (-1 * p0[0] / random.randint(2, 4) , p0[1] / random.randint(2, 4))
c1 = (-1 * p1[0] / random.randint(2, 4) , p1[1] / random.randint(2, 4))

# p0 = (-170, -80)
# p1 = (170, 80)
# c0 = (90, -45)
# c1 = (-90, 45)

def bezier_curve(p0, p1, c0, c1, t):
    # Bezier curve equation
    x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * c0[0] + 3 * (1 - t) * t**2 * c1[0] + t**3 * p1[0]
    y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * c0[1] + 3 * (1 - t) * t**2 * c1[1] + t**3 * p1[1]
    return x, y

# Random control points within a certain range
# control_range = 3  # Adjust this as needed
# c0 = np.array(p0) + np.random.uniform(-control_range, control_range, size=2)
# c1 = np.array(p1) + np.random.uniform(-control_range, control_range, size=2)

# Generate points on the curve
# Number of points
t_values = np.linspace(0, 1, 150)
curve_points = [bezier_curve(p0, p1, c0, c1, t) for t in t_values]

print("Generating data for quadtree")
with open('data.txt', 'w') as f:
    # Use first 100 values for building the path, rest for queries
    for idx, coordinate in enumerate(curve_points[:100]):
        f.write("{} {} {}\n".format(idx + 1, coordinate[0], coordinate[1]))
        print(f"{idx + 1} - {coordinate}")

print("Generating queries for quadtree")
query_choices = ['i', 'p']

with open('queries.txt', 'w') as f:
    # Use first 100 values for building the path, rest for queries
    for coordinate in curve_points[100:]:
        f.write("{} {} {}\n".format(random.choice(query_choices), coordinate[0], coordinate[1]))
            
curve_x, curve_y = zip(*curve_points)
# print(f"Curve X: {curve_x}")
# print(f"\nCurve Y: {curve_y}")
# # Plotting
# plt.plot(*zip(p0, c0, c1, p1), 'ro-')  # Plot control points and endpoints
# plt.plot(curve_x, curve_y, label='Bezier Curve')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Bezier Curve between two fixed points with random control points')
# plt.legend()
# plt.grid(True)
# plt.axis('equal')
# plt.show()
