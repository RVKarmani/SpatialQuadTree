import matplotlib.pyplot as plt

# File loading
filename = "data.txt"  # Replace with the actual name of your file
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
plt.scatter(x, y)
plt.xlabel("X-Coordinate")
plt.ylabel("Y-Coordinate")
plt.title("Input Points Visualization")
plt.grid(True)

# Show the plot
plt.show()
