import matplotlib.pyplot as plt
from argparse import ArgumentParser
import os
import glob
import json
import numpy as np
import pandas as pd
import re


def get_s_list(file_path):

    if "bezier" in file_path:
        suffix = "bezier"
    elif "spiral" in file_path:
        suffix = "fermat_spiral"
    else:
        raise

    # Compile a regular expression to capture the 's' value from each command line
    s_value_pattern = re.compile(rf'insert_s=(\d+\.\d+)_curve={suffix}.txt')

    # List to store the extracted 's' values
    extracted_s_values = []

    # Open and read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Search for the pattern in each line
            search_result = s_value_pattern.search(line)
            if search_result:
                # If a match is found, add the 's' value to the list
                extracted_s_values.append(float(search_result.group(1)))

    # Print all the extracted 's' values
    print(extracted_s_values)
    return extracted_s_values


def get_results(graph):

    ss = get_s_list(f"test_{graph}.sh")
    # print(ss)

    with open(f"data/result_{graph}.json", "r") as f:
        results = json.load(f)

    prepare_results = []

    for s, res in zip(ss, results):
        res["s"] = s
        for k, v in res.items():
            if 'time' in k and k != "Index creation time":
                time = v
                break
        else:
            print(res)
            raise "No time"
        res["time"] = time
        prepare_results.append(res)

    results = prepare_results
    return results


def get_mode_name(res):

    mode_id = res["Mode"]
    # modes = {
    #     0: "naive",
    #     1: "leaf_or_parent",
    #     2: "cache",
    # }

    if mode_id == 0:
        mode = "naive"
    elif mode_id == 1:
        level = res['Level of Parent stored']
        if level == 0:
            mode = "leaf"
        else:
            mode = f"parent(level={level})"
    elif mode_id == 2:
        mode = "cache(size=3)"
    else:
        raise

    return mode


def draw_time_mode_s(all_results):
    # Number of rows is the number of sets of results
    num_rows = len(all_results)
    
    # Create a large figure to accommodate all subplots
    fig, axes = plt.subplots(num_rows, 3, figsize=(16, 10 * num_rows))
    
    # Iterate through each set of results
    for idx, (graph_name, results) in enumerate(all_results.items()):
        # Prepare a dictionary to hold the data for each mode, and for each variable
        mode_data = {}
        
        # Process each result
        for res in results:
            s = res['s']
            mode = get_mode_name(res)
            time = res['time']
            hit_rate = res.get("Hit rate", 0)  # Using .get to provide a default value if key is missing
            height = res["height"]
            
            # If the mode is not yet in the dictionary, add it
            if mode not in mode_data:
                mode_data[mode] = {'s': [], 'time': [], 'hit_rate': [], 'height': []}
            
            # Append the 's', 'time', 'hit_rate', and 'height' to the appropriate lists in the dictionary
            mode_data[mode]['s'].append(s)
            mode_data[mode]['time'].append(time)
            mode_data[mode]['hit_rate'].append(hit_rate)
            mode_data[mode]['height'].append(height)

        # Define axes for each row
        if num_rows > 1:
            ax1, ax2, ax3 = axes[idx]
        else:
            ax1, ax2, ax3 = axes

        # Plot time vs s
        for mode, data in mode_data.items():
            ax1.plot(data['s'], data['time'], label=mode)
        ax1.set_title(f'Time vs. s ({graph_name})')
        ax1.set_xlabel('s value')
        ax1.set_ylabel('Time')
        ax1.legend()

        # Plot hit rate vs s
        for mode, data in mode_data.items():
            ax2.plot(data['s'], data['hit_rate'], label=mode)
        ax2.set_title(f'Hit Rate vs. s ({graph_name})')
        ax2.set_xlabel('s value')
        ax2.set_ylabel('Hit Rate')
        ax2.legend()

        # Plot height vs s
        for mode, data in mode_data.items():
            ax3.plot(data['s'], data['height'], label=mode)
        ax3.set_title(f'Height vs. s ({graph_name})')
        ax3.set_xlabel('s value')
        ax3.set_ylabel('Height')
        ax3.legend()

    # Adjust layout and display the plot
    plt.tight_layout()
    # plt.show()
    graph_names = list(all_results.keys())
    plt.savefig(f"images/results_time_hitRate_height__{graph_names}.png")


def draw_level_hit_rate(graph="level_spiral"):
    with open(f"data/result_{graph}.json", "r") as f:
        results = json.load(f)

    prepare_results = []

    for res in results:
        for k, v in res.items():
            if 'time' in k and k != "Index creation time":
                time = v
                break
        else:
            print(res)
            raise "No time"
        res["time"] = time
        prepare_results.append(res)

    results = prepare_results

    hit_rates = [res["Hit rate"] for res in results]
    levels = [res["Level of Parent stored"] for res in results]

    # Creating the plot
    plt.figure(figsize=(10, 5))
    plt.plot(levels, hit_rates, marker='o')
    plt.title('Hit Rate by Level of Parent Stored')
    plt.xlabel('Level of Parent Stored')
    plt.ylabel('Hit Rate')
    plt.grid(True)
    plt.show()
        



def main():
        
    # # graph_names = ["bezier", "spiral"]
    # graph_names = ["bezier"]
    # all_results = {graph_name: get_results(graph_name) for graph_name in graph_names}

    # draw_time_mode_s(all_results)


    spiral_level = draw_level_hit_rate()
    


if __name__ == "__main__":
    main()

