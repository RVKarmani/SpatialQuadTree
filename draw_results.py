import matplotlib.pyplot as plt
from argparse import ArgumentParser
import os
import json
import numpy as np


def get_parser():
    parser = ArgumentParser()
    parser.add_argument("--task", type=str, default="t", choices=["m", "h", "t"], help="tree map, hitting rate, time")
    
    return parser



def draw_ht2num():
    """
    hitting rate to the number of data   

    Parameters:
    - hitting_rate: list
    - random_rate: list
    """
    print("Drawing hitting to random rate...")
    
    hitting_rate = []
    random_rate = []


def draw_t2r():
    """
    time to the random rate of data

    Parameters:
    - t_naive: list
    - t_bulk: list
    - random_rate: list
    """
    print("Drawing time to random rate...")

    with open("data/result.json", "r") as f:
        results = json.load(f)

    s2t_naive = {}
    s2t_bulk = {}

    for result in results:
        try:
            s2t_bulk[float(result["s"])] = float(result["Bulk Insert time"])
        except KeyError:
            s2t_naive[float(result["s"])] = float(result["Naive Insert time"])  

    print(s2t_bulk)
    print(s2t_naive)

    # Sorting keys for consistent plotting
    keys_sorted = sorted(s2t_naive.keys())

    # Extracting values in the sorted order of keys
    naive_times = [s2t_naive[key] for key in keys_sorted]
    bulk_times = [s2t_bulk[key] for key in keys_sorted]

    # Defining the x-axis for the plot
    x = np.arange(len(keys_sorted))

    # Plotting both sets of times
    width = 0.35  # Width of the bars
    plt.bar(x - width/2, naive_times, width, label='Naive Insert Time')
    plt.bar(x + width/2, bulk_times, width, label='Bulk Insert Time')

    # Adding labels and title
    plt.xlabel('Random Generated Points Rate')
    plt.ylabel('Time / $\mu$s')
    plt.title('Comparison of Naive and Bulk Insert Times')
    plt.xticks(x, labels=[str(key) for key in keys_sorted])
    plt.legend()

    # Displaying the plot
    plt.show()


def draw_tree():
    print("Drawing the tree map...")

    for datafile in os.listdir("data/s"):
        if not datafile.startswith("insert"):
            continue
        print(datafile)


def main():
    args = get_parser().parse_args()
    if args.task == "m":
        draw_tree()
    elif args.task == "h":
        draw_ht2num()
    elif args.task == "t":
        draw_t2r()


if __name__ == "__main__":
    main()
