import os
import re
from collections import Counter
import numpy as np

# Directory containing the txt files
directory = '/home/haris/query_results'

# List to store all the execution times
execution_times = []

# Regular expression to match 'Execution Time: ' followed by a number and ' ms'
execution_time_pattern = re.compile(r'Execution Time: (\d+\.\d+) ms')

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            content = file.read()
            match = execution_time_pattern.search(content)
            if match:
                execution_time = float(match.group(1))
                execution_times.append(execution_time)

# Convert to numpy array for statistical calculations
execution_times_np = np.array(execution_times)

# Calculate the mean
mean_execution_time = np.mean(execution_times_np)

# Calculate the mode
mode_execution_time = Counter(execution_times).most_common(1)[0][0]

# Calculate the variance
variance_execution_time = np.var(execution_times_np)

# Calculate the max and min
max_execution_time = np.max(execution_times_np)
min_execution_time = np.min(execution_times_np)

# Print results
print(f"Execution Times: {execution_times}")
print(f"Mean Execution Time: {mean_execution_time} ms")
print(f"Mode Execution Time: {mode_execution_time} ms")
print(f"Variance of Execution Times: {variance_execution_time} ms^2")
print(f"Max Execution Time: {max_execution_time} ms")
print(f"Min Execution Time: {min_execution_time} ms")

