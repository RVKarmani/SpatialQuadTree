import matplotlib.pyplot as plt
from argparse import ArgumentParser
import os
import glob
import json
import numpy as np
import pandas as pd


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

        if float(result["s"]) == 1:
            continue

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
    plt.xlabel('Sortedness')
    plt.ylabel('Time / $\mu$s')
    plt.title('Comparison of Naive and Bulk Insert Times')
    plt.xticks(x, labels=[str(key) for key in keys_sorted])
    plt.legend()

    # Displaying the plot
    # plt.show()
    plt.savefig("images/t2randomRate.png")


def draw_tree():
    print("Drawing the tree map...")

    # Getting all the CSV files in the 'tree' directory
    files = glob.glob('tree/*.csv')

    for file_path in files:
        # Extracting the file name to use as part of the chart's title
        file_name = os.path.basename(file_path)
        title_part = file_name.split('.')[0]  # Assuming the file name format is "tree_lll.csv", removing the extension
        title_part = title_part.replace('tree_', '')  # Removing the prefix "tree_", leaving "lll"

        # Reading the CSV file
        df = pd.read_csv(file_path, header=None, names=['xmin', 'ymin', 'xmax', 'ymax'])

        # Plotting each boundary box
        for _, row in df.iterrows():
            plt.plot([row['xmin'], row['xmax'], row['xmax'], row['xmin'], row['xmin']],
                    [row['ymin'], row['ymin'], row['ymax'], row['ymax'], row['ymin']], 'k-')

        # Setting the chart title to "QuadTree_lll" and axis labels
        plt.title(f'QuadTree_{title_part}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.axis('equal')
        
        # Displaying the chart
        # plt.show()
        plt.savefig(f'images/QuadTree_{title_part}.png')

        # Clearing the current figure for the next file
        plt.clf()


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
