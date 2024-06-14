import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Step 1: Read and Prepare Data
data_directory = '/home/haris/vector3'  # Specify the directory containing the JSON files
json_files = [os.path.join(data_directory, f) for f in os.listdir(data_directory) if f.endswith('.json')]

data_list = []
keys_set = set()

# Read each JSON file and collect data
for file in json_files:
    with open(file, 'r') as f:
        json_data = json.load(f)
        # Collect all keys from all JSON files
        keys_set.update(json_data.keys())
        # Convert values to a list
        data_list.append(json_data)

# Convert data to a numpy array
keys_list = list(keys_set)
data_matrix = np.zeros((len(data_list), len(keys_list)))

original_vector_count = data_matrix.shape[0]
# Fill the data matrix
for i, json_data in enumerate(data_list):
    for j, key in enumerate(keys_list):
        data_matrix[i, j] = json_data.get(key, 0)  # Use 0 for missing keys

# Step 1.1: Remove duplicate vectors
# Convert the numpy array to a list of tuples
data_tuples = [tuple(row) for row in data_matrix]

# Convert the list of tuples to a set to remove duplicates
unique_data_set = set(data_tuples)

# Convert the set back to a list of tuples
unique_data_list = list(unique_data_set)
unique_vector_count = len(unique_data_set)
print(f'Number of original vectors: {original_vector_count}')
print(f'Number of unique vectors: {unique_vector_count}')
# Convert the list of tuples back to a numpy array
data_matrix_unique = np.array(unique_data_list)

# Step 2: Standardize the data
scaler = StandardScaler()
data_standardized = scaler.fit_transform(data_matrix_unique)

# Step 3: Perform PCA
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_standardized)

# Step 4: Visualize the results
plt.figure(figsize=(8, 6))
plt.scatter(data_pca[:, 0], data_pca[:, 1], c='red', alpha=0.6)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of JSON Data')
plt.show()
