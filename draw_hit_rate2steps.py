import os
import matplotlib.pyplot as plt
import numpy as np


def parse_filename(filename):
    # Extract method and level from the filename
    parts = filename.split('_')
    method = parts[2]  # e.g., 'method=2'
    level = parts[-1].split('.')[0]  # e.g., 'level=0'
    return method, level

def process_directory(base_directory):
    data = []  # List to store all data

    # List all directories in the base directory
    directories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]

    # Process each directory
    for directory in directories:
        # Extract 's' value from the directory name
        s = directory.split('=')[-1]
        dir_path = os.path.join(base_directory, directory)

        # List all text files in the current directory
        files = [f for f in os.listdir(dir_path) if f.endswith('.txt')]

        for file in files:
            # Parse 'method' and 'level' from the filename
            parts = file.replace('.txt', '').split('_')
            # print(parts)
            method = parts[3].split('=')[-1]
            level = parts[4].split('=')[-1]

            # Read the hit rate from the file
            filepath = os.path.join(dir_path, file)

            hit_rates = []
            with open(filepath, 'r') as f:
                for line in f:
                    hit_rate = float(line.strip())  # Convert line to float and remove any trailing newline characters
                    hit_rates.append(hit_rate)

            # Store the extracted data
            data.append({
                's': float(s),
                'method': f"method={method}_level={level}",
                'hit_rates': hit_rates
            })

    return data


def plot_hit_rates(data):
    # 为每个s值和每个method生成子图
    fig1, axes1 = plt.subplots(nrows=len(set(d['s'] for d in data)), figsize=(10, 8))
    fig2, axes2 = plt.subplots(nrows=len(set(d['method'] for d in data)), figsize=(10, 8))

    # 子图索引
    s_index = {s: idx for idx, s in enumerate(sorted(set(d['s'] for d in data)))}
    method_index = {method: idx for idx, method in enumerate(sorted(set(d['method'] for d in data)))}

    # 绘制每个数据点
    for d in data:
        steps = np.linspace(1, len(d['hit_rates']), 100, endpoint=True, dtype=int) - 1
        sampled_hit_rates = [d['hit_rates'][i] for i in steps]

        # 绘制基于s的图
        ax1 = axes1[s_index[d['s']]]
        ax1.plot(steps, sampled_hit_rates, label=d["method"])
        ax1.set_title(f's = {d["s"]}')
        ax1.set_xlabel('Step')
        ax1.set_ylabel('Hit Rate')
        ax1.legend(loc="right")

        # 绘制基于method的图
        ax2 = axes2[method_index[d['method']]]
        ax2.plot(steps, sampled_hit_rates, label=f"s={d['s']}")
        ax2.set_title(f'Method = {d["method"]}')
        ax2.set_xlabel('Step')
        ax2.set_ylabel('Hit Rate')
        ax2.legend(loc="right")

    fig1.tight_layout()
    fig2.tight_layout()
    # plt.show()

    fig1.savefig('logs/hit_rate_compare_sortedness.png')  # 保存基于 s 分组的图
    fig2.savefig('logs/hit_rate_compare_methods.png')  # 保存基于 method 分组的图


def main():
    # Assuming 'logs' is the top-level directory containing all subdirectories
    base_directory = 'logs'
    all_data = process_directory(base_directory)

    # # Print the collected data
    # for item in all_data:
    #     print(item)
    #     quit()

    plot_hit_rates(all_data)


if __name__ == "__main__":
    main()
   