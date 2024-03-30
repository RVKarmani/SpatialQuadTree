import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(description='Quadtree data/query generator')
parser.add_argument('-f', help="file name", type=str, default="data/s/insert_s=S.txt")
parser.add_argument('-s', help="sortedness", type=str, default="0.75")
args = parser.parse_args()

if "S" in args.f:
  args.f = args.f.replace("S", args.s)
  title = f"Input Points Visualization, sortedness = {args.s}" 
else:
  title = "Input Points Visualization" 

# File loading
filename = args.f  # Replace with the actual name of your file
with open(filename, 'r') as file:
    data = file.read()
# filename = "dataExample.txt"  # Replace with the actual name of your file
# with open(filename, 'r') as file:
#     data = file.read()

# Parse the data into separate lists for x and y coordinates
lines = data.strip().split("\n")
x = []
y = []
for line in lines:
  parts = line.split()
  x.append(float(parts[1]))
  y.append(float(parts[2]))

# Create the plot
plt.figure(figsize=(8, 6))  # Adjust figure size as desired
plt.scatter(x, y, s=1, marker='.')
plt.xlabel("X-Coordinate")
plt.ylabel("Y-Coordinate")
plt.title(title)
plt.grid(True)

# Show the plot
plt.show()

# plt.savefig(f"images/{title}.png")
