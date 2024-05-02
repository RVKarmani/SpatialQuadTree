import matplotlib.pyplot as plt
import numpy as np
import random, argparse
# import quads

# tree = quads.QuadTree(
#     (0, 0),  # The center point
#     4000,  # The width
#     2000,  # The height
# )

# Curves
BEZIER = "bezier"
FMT_SPR = "fermat_spiral"
RND_CRV = "random_curve"
CIRC_ARC = "circ_arc"
CURVE_CHOICES = [BEZIER, FMT_SPR, RND_CRV, CIRC_ARC]

# Distributions
UNIFORM_DIST = "uniform"
GAUSSIAN_DIST = "gaussian"
DIST_CHOICES = [UNIFORM_DIST, GAUSSIAN_DIST]

# Define the parser
parser = argparse.ArgumentParser(description="Quadtree data/query generator")
parser.add_argument(
    "-xl", help="x low coordinate for boundary", type=int, default=-1800
)
parser.add_argument("-yl", help="y low coordinate for boundary", type=int, default=-900)
parser.add_argument(
    "-xh", help="x high coordinate for boundary", type=int, default=1800
)
parser.add_argument("-yh", help="y high coordinate for boundary", type=int, default=900)
parser.add_argument("-n", help="Number of queries", type=int, default=10000)
parser.add_argument("-s", help="Sortedness for inserts", type=float, default=0.5)
parser.add_argument(
    "-c", help="Curve type for data", type=str, choices=CURVE_CHOICES, default=FMT_SPR
)
parser.add_argument(
    "-d",
    help="Distribution type for data",
    type=str,
    choices=DIST_CHOICES,
    default=GAUSSIAN_DIST,
)
parser.add_argument(
    "-m", help="Standard deviation for distribution", type=int, default=50
)

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
INSERT_SYMBOL = "i"

QUERY_FILE = f"final_data/insert_n={args.n}_s={args.s}_curve={args.c}_dist={args.d}.txt"


# Functions
def print_parameters():
    print("Input Parameters")
    for action in parser._actions:
        if action.dest != "help":
            option_strings = ", ".join(action.option_strings)
            print(f"{option_strings} [{action.help}]: {getattr(args, action.dest)}")


def cubic_bezier(t, p0, p1, p2, p3):
    return (
        (1 - t) ** 3 * p0
        + 3 * (1 - t) ** 2 * t * p1
        + 3 * (1 - t) * t**2 * p2
        + t**3 * p3
    )


def generate_bezier_curve():
    curve_x = []
    curve_y = []
    dist_x = []
    dist_y = []
    t_values = np.linspace(0, 1, NUM_QUERIES)
    p0 = np.array([X_LOW, Y_LOW])
    p1 = np.array([X_LOW * 0.25, Y_HIGH * 1.5])
    p2 = np.array([X_HIGH * 0.25, Y_LOW * 1.5])
    p3 = np.array([X_HIGH, Y_HIGH])
    index = 0
    with open(QUERY_FILE, "w") as query_file:  # , open(DATA_FILE, 'w') as data_file:
        for _ in range(NUM_QUERIES):
            choice = random.random()
            x, y = cubic_bezier(t_values[index], p0, p1, p2, p3)
            if choice > args.s:  # generate randomly
                xr = None
                yr = None
                if args.d == UNIFORM_DIST:
                    xr = random.uniform(X_LOW, X_HIGH)
                    yr = random.uniform(Y_LOW, Y_HIGH)
                elif args.d == GAUSSIAN_DIST:
                    xr = random.normalvariate(x, (X_HIGH - X_LOW) / int(args.m))
                    yr = random.normalvariate(y, (Y_HIGH - Y_LOW) / int(args.m))
                dist_x.append(xr)
                dist_y.append(yr)
                index = index + 1

                # tree.insert((xr, yr), data="red")
                query_file.write("{} {} {}\n".format(INSERT_SYMBOL, xr, yr))
            else:  # get point on the curve
                curve_x.append(x)
                curve_y.append(y)
                index = index + 1

                # tree.insert((x, y), data="green")
                query_file.write("{} {} {}\n".format(INSERT_SYMBOL, x, y))

    return curve_x, curve_y, dist_x, dist_y


def fermat_spiral(theta):
    a = 5  # scaling factor
    return a * np.sqrt(theta)


def generate_fermat_spiral():
    curve_x = []
    curve_y = []
    dist_x = []
    dist_y = []

    theta = np.linspace(0.1, 10 * np.pi, NUM_QUERIES)
    r = np.sqrt(theta)
    x_scaled = 150 * r * np.cos(theta)
    y_scaled = 150 * r * np.sin(theta)

    index = 0
    with open(QUERY_FILE, "w") as query_file:
        for _ in range(NUM_QUERIES):
            choice = random.random()
            x = x_scaled[index]
            y = y_scaled[index]

            if choice > args.s:  # generate randomly
                xr = None
                yr = None
                if args.d == UNIFORM_DIST:
                    xr = random.uniform(X_LOW, X_HIGH)
                    yr = random.uniform(Y_LOW, Y_HIGH)
                elif args.d == GAUSSIAN_DIST:
                    xr = random.normalvariate(x, (X_HIGH - X_LOW) / int(args.m))
                    yr = random.normalvariate(y, (Y_HIGH - Y_LOW) / int(args.m))
                dist_x.append(xr)
                dist_y.append(yr)
                # tree.insert((xr, yr), data="red")
                query_file.write("{} {} {}\n".format(INSERT_SYMBOL, xr, yr))
            else:  # get point on the curve
                curve_x.append(x)
                curve_y.append(y)
                # tree.insert((x, y), data="green")
                query_file.write("{} {} {}\n".format(INSERT_SYMBOL, x, y))
            index = index + 1

    return curve_x, curve_y, dist_x, dist_y


def generate_random_curve():
    # Generate theta values
    theta = np.linspace(0, 4 * np.pi, NUM_QUERIES)
    # Define parameters for randomness
    # a = np.random.uniform(0.5, 2.0)  # amplitude of the sine function
    # b = np.random.uniform(0.5, 2.0)  # amplitude of the cosine function
    # c = np.random.uniform(0.5, 2.0)  # frequency of the sine function
    # d = np.random.uniform(0.5, 2.0)  # frequency of the cosine function
    c = 1
    d = 0.9
    # Calculate x and y coordinates
    x = X_LOW + (X_HIGH - X_LOW) * ((np.sin(c * theta) + 1) / 2)
    y = Y_LOW + (Y_HIGH - Y_LOW) * ((np.cos(d * theta) + 1) / 2)

    # for xl, yl in zip(x, y):
    #     tree.insert((xl, yl), data="green")

    # Add coordinates to the queue
    return x, y


def generate_circular_arc():
    theta = np.linspace(0, np.pi, NUM_SORTED)
    r = np.sqrt((X_HIGH - X_LOW) ** 2 + (Y_HIGH - Y_LOW) ** 2) / 2
    x = X_LOW + r * np.cos(theta)
    y = Y_LOW + r * np.sin(theta)
    # for xl, yl in zip(x, y):
    #     tree.insert((xl, yl), data="green")

    return x, y


def get_curve_points(curve_type: str):
    if curve_type == BEZIER:
        return generate_bezier_curve()
    elif curve_type == FMT_SPR:
        return generate_fermat_spiral()
    # elif curve_type == RND_CRV:
    #     return generate_random_curve()
    # elif curve_type == CIRC_ARC:
    #     return generate_circular_arc()


# Functions End

# Main start

print_parameters()
curve_x, curve_y, dist_x, dist_y = get_curve_points(args.c)

# Plot points
# plt.scatter(curve_x, curve_y, color="green")
# plt.scatter(dist_x, dist_y, color="red")
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.legend()
# plt.grid(True)
# plt.axis("equal")
# plt.show()

# quads.visualize(tree)
