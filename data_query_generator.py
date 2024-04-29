import matplotlib.pyplot as plt
import numpy as np
import random, argparse
from queue import Queue
from tqdm import tqdm

# Curves
BEZIER = "bezier"
FMT_SPR = "fermat_spiral"
RND_CRV = "random_curve"
CIRC_ARC = "circ_arc"
CURVE_CHOICES = [BEZIER, FMT_SPR, RND_CRV, CIRC_ARC]

# Distributions
UNIFORM_DIST = "uniform"
CLUSTERED_DIST = "clustered"
RANDOM_DIST = "random"
DIST_CHOICES = [UNIFORM_DIST, CLUSTERED_DIST, RANDOM_DIST]

# Define the parser
parser = argparse.ArgumentParser(description='Quadtree data/query generator')
parser.add_argument('-xl', help="x low coordinate for boundary", type=int, default=-1800)
parser.add_argument('-yl', help="y low coordinate for boundary", type=int, default=-900)
parser.add_argument('-xh', help="x high coordinate for boundary", type=int, default=1800)
parser.add_argument('-yh', help="y high coordinate for boundary", type=int, default=900)
parser.add_argument('-n', help="Number of queries", type=int, default=1000000)
parser.add_argument('-s', help="Sortedness for inserts", type=float, default=0.5)
<<<<<<< HEAD
parser.add_argument('-c', help="Curve type for data", type=str, choices=CURVE_CHOICES, default=BEZIER)
parser.add_argument('-d', help="Distribution type for data", type=str, choices=DIST_CHOICES)
=======
parser.add_argument('-c', help="Curve type for data", type=str, choices=CURVE_CHOICES, default=RND_CRV)
# parser.add_argument('-d', help="Distribution type for data", type=str, choices=DIST_CHOICES, default=CLUSTERED_DIST)
>>>>>>> 89b314dd0adc9fa46924507457496e6d99593ecc

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

QUERY_FILE = "data/insert_s={selectivity}_{suffix}.txt".format(selectivity = args.s, suffix = f"curve={args.c}" if args.c else f"dist={args.d}")

# Functions
def print_parameters():
    print("Input Parameters")
    for action in parser._actions:
        if action.dest != 'help':
            option_strings = ', '.join(action.option_strings)
            print(f"{option_strings} [{action.help}]: {getattr(args, action.dest)}")

def generate_distribution_points(distribution):
    if distribution == UNIFORM_DIST:
        x = np.random.uniform(X_LOW, X_HIGH, NUM_SORTED)
        y = np.random.uniform(Y_LOW, Y_HIGH, NUM_SORTED)

    elif distribution == CLUSTERED_DIST:
        x = np.concatenate([np.random.normal(X_LOW, 30, NUM_SORTED // 2),
                            np.random.normal(X_HIGH, 30, NUM_SORTED // 2)])
        y = np.concatenate([np.random.normal(Y_LOW, 40, NUM_SORTED // 2),
                            np.random.normal(Y_HIGH, 50, NUM_SORTED // 2)])
    return zipper(x, y, NUM_SORTED)

def zipper(x, y, n):
    points = Queue(maxsize=n)
    for xval, yval in zip(x, y):
        points.put((xval, yval))
    return points

def cubic_bezier(t, p0, p1, p2, p3):
    return (1-t)**3 * p0 + 3*(1-t)**2*t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3

def generate_bezier_curve():
    curve_points = Queue(maxsize=NUM_SORTED)
    t_values = np.linspace(0, 1, NUM_SORTED)

    p0 = np.array([X_LOW, Y_LOW])
    p1 = np.array([X_LOW * 0.25, Y_HIGH * 1.5])
    p2 = np.array([X_HIGH * 0.25, Y_LOW * 1.5])
    p3 = np.array([X_HIGH, Y_HIGH])

    for t in t_values:
        x, y = cubic_bezier(t, p0, p1, p2, p3)
        curve_points.put((x, y))
    return curve_points

def generate_fermat_spiral():
    curve_points = Queue(maxsize=NUM_SORTED)
    for i in range(NUM_SORTED):
        theta = 0.1 * i
        r = np.sqrt(theta)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        curve_points.put((x, y))
    return curve_points

def generate_random_curve():
    # Generate theta values
    theta = np.linspace(0, 4 * np.pi, NUM_SORTED)

    # Define parameters for randomness
    a = np.random.uniform(0.5, 2.0)  # amplitude of the sine function
    b = np.random.uniform(0.5, 2.0)  # amplitude of the cosine function
    c = np.random.uniform(0.5, 2.0)  # frequency of the sine function
    d = np.random.uniform(0.5, 2.0)  # frequency of the cosine function

    # Calculate x and y coordinates
    x = X_LOW + (X_HIGH - X_LOW) * ((a * np.sin(c * theta)) / (2 * a))
    y = Y_LOW + (Y_HIGH - Y_LOW) * ((b * np.cos(d * theta)) / (2 * b))

    # Add coordinates to the queue
    return zipper(x, y, NUM_SORTED)

def generate_circular_arc():
    theta = np.linspace(0, np.pi, NUM_SORTED)
    r = np.sqrt((X_HIGH - X_LOW)**2 + (Y_HIGH - Y_LOW)**2) / 2
    x = X_LOW + r * np.cos(theta)
    y = Y_LOW + r * np.sin(theta)
    
    return zipper(x, y, NUM_SORTED)

def write_points_to_query_file(curve_points): 
    index = 1
    with open(QUERY_FILE, 'w') as query_file: #, open(DATA_FILE, 'w') as data_file:
        total_num = 0
        # for _ in tqdm(range(NUM_QUERIES)):
        for _ in (range(NUM_QUERIES)):
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

def plot_points(curve_points:list, curve_type:str):
    curve_x, curve_y = zip(*list(curve_points.queue))
    # Plotting
    # plt.plot(*zip(p0, c0, c1, p1), 'ro-')  # Plot control points and endpoints
    plt.plot(curve_x, curve_y, label='Curve Plot')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f"{curve_type} plot")
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def get_curve_points(curve_type:str):
    if curve_type == BEZIER:
        return generate_bezier_curve()
    elif curve_type == FMT_SPR:
        return generate_fermat_spiral()
    elif curve_type == RND_CRV:
        return generate_random_curve()
    elif curve_type == CIRC_ARC:
        return generate_circular_arc()

# Functions End

# Main start
print_parameters()
<<<<<<< HEAD

if args.d:
    curve_points = generate_distribution_points(args.d)
    plot_points(curve_points, args.d)
else:
    curve_points = get_curve_points(args.c)
    plot_points(curve_points, args.c)
=======
curve_points = get_curve_points(args.c)
# plot_points(curve_points, args.c)
>>>>>>> 89b314dd0adc9fa46924507457496e6d99593ecc
write_points_to_query_file(curve_points)
