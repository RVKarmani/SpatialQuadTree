import matplotlib.pyplot as plt
import numpy as np
import random, argparse
from queue import Queue

from tqdm import tqdm

# Define the parser
parser = argparse.ArgumentParser(description='Quadtree data/query generator')

parser.add_argument('-xl', help="x low coordinate for boundary", type=int, default=-180)
parser.add_argument('-yl', help="y low coordinate for boundary", type=int, default=-90)
parser.add_argument('-xh', help="x high coordinate for boundary", type=int, default=180)
parser.add_argument('-yh', help="y high coordinate for boundary", type=int, default=90)

parser.add_argument('-n', help="Number of queries", type=int, default=100000)
parser.add_argument('-s', help="Sortedness for inserts", type=float, default=0.5)

args = parser.parse_args()

# Boundary
X_LOW = args.xl
Y_LOW = args.yl
X_HIGH = args.xh
Y_HIGH = args.yh

# Number of points
NUM_QUERIES = args.n
NUM_SORTED = int(args.s * NUM_QUERIES)
NUM_RANDOM = int(NUM_QUERIES - NUM_SORTED)
INSERT_SYMBOL = 'i'

print("Input Parameters")
for action in parser._actions:
    if action.dest != 'help':
        option_strings = ', '.join(action.option_strings)
        print(f"{option_strings} [{action.help}]: {getattr(args, action.dest)}")

FILE_SUFFIX = f"n-{NUM_QUERIES}_s-{args.s}_xl-{args.xl}_yl-{args.yl}_xh-{args.xh}_yh-{args.yh}"
# QUERY_FILE = f"insert.txt"
# QUERY_FILE = f"queries-{FILE_SUFFIX}.txt"
# DATA_FILE = f"data-{FILE_SUFFIX}.txt"

QUERY_FILE = f"insert_s={args.s}.txt"

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
t_values = np.linspace(0, 1, NUM_SORTED)
curve_points = Queue(maxsize=NUM_SORTED)

for t in t_values:
    curve_points.put(bezier_curve(p0, p1, c0, c1, t))

print("Generating queries for quadtree")

# index = 1

with open(QUERY_FILE, 'w') as query_file: #, open(DATA_FILE, 'w') as data_file:
    total_num = 0
    for _ in tqdm(range(NUM_QUERIES)):
        choice = random.random()
        if choice > args.s: # generate randomly
            query_file.write("{} {} {}\n".format(INSERT_SYMBOL, random.uniform(X_LOW, X_HIGH), random.uniform(Y_LOW, Y_HIGH)))

            # data_file.write("{} {} {}\n".format(index, random.uniform(X_LOW, X_HIGH), random.uniform(Y_LOW, Y_HIGH)))
            # index = index + 1
        else: # get point on the curve
            sorted_coord = curve_points.get()
            query_file.write("{} {} {}\n".format(INSERT_SYMBOL, sorted_coord[0], sorted_coord[1]))
            
            # data_file.write("{} {} {}\n".format(index, sorted_coord[0], sorted_coord[1]))
            # index = index + 1

# curve_x, curve_y = zip(*curve_points)
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
