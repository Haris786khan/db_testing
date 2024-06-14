
import os
import json
import subprocess
from lxml import etree
import re
import hashlib
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def Plotter():
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
    plt.scatter(data_pca[:, 0], data_pca[:, 1], c='blue', alpha=0.6)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA of JSON Data')
    plt.show()




def start():
                            # Specify the input file path
 input_file_path = '/home/haris/AFLplusplus/plan.txt'  # Replace with the path to your input text file

# Specify the output directory where the XML files will be saved
 output_directory = '/home/haris/output_xml_files'  # Replace with the desired output directory
 
# Ensure the output directory exists, create it if not
 os.makedirs(output_directory, exist_ok=True)

# Define patterns to match the removal sections
 startup_cost_pattern = re.compile(r'<Startup-Cost>.*?\+', re.DOTALL)
 total_cost_pattern = re.compile(r'<Total-Cost>.*?\+', re.DOTALL)
 plan_rows_pattern = re.compile(r'<Plan-Rows>.*?\+', re.DOTALL)

# Define the start and end tags for XML extraction
 start_tag = '<explain xmlns="http://www.postgresql.org/2009/explain">'
 end_tag = '</explain>'

# Define a pattern to match the start and end tags for extraction
 extraction_pattern = re.compile(re.escape(start_tag) + '.*?' + re.escape(end_tag), re.DOTALL)

# Read the contents of the input file
 with open(input_file_path, 'r') as file:
    file_contents = file.read()

# Remove the <Startup-Cost> sections ending with '+' and <Total-Cost> sections ending with '+' and <Plan-Rows> sections ending with '+'
 file_contents = startup_cost_pattern.sub('', file_contents)
 file_contents = total_cost_pattern.sub('', file_contents)
 file_contents = plan_rows_pattern.sub('', file_contents)

# Find all occurrences of the extraction pattern in the modified file contents
 matches = extraction_pattern.findall(file_contents)

# Create a set to track the hashes of the contents of each file to identify duplicates
 unique_files = set()
 file_index = 131

# Process each match and save only unique ones
 for idx, match in enumerate(matches, start=1):

    # Calculate the hash of the current match
    match_hash = hashlib.md5(match.encode()).hexdigest()
    
    # Check if the hash is already in the set of unique files
    if match_hash not in unique_files:
        # Add the hash to the set
        unique_files.add(match_hash)
        
        # Define the output file path
        file_index += 1
        output_file_path = os.path.join(output_directory, f'explain_{file_index}.xml')
        
        # Write the match to the output file
        with open(output_file_path, 'w') as output_file:
            output_file.write(match)
        
        print(f'Saved: {output_file_path}')
    else:
        print(f'Skipped duplicate: explain_{idx}.xml')

 print('Processing completed. Unique XML files have been saved.')
 

       


def convert2vector(plan_json_path,i):
    '''The function uses the tree2vec model to convert the plan.json file to a vector.json file. The function takes the path to the plan.json file as input and returns the path to the vector.json file.'''
    main = r"/home/haris/Downloads/tree2vec/main.py"
    out = os.path.join("/home/haris/vector3/vector"+ str( 600 + i)+".json")
    try:
        p = subprocess.Popen(
            ["python3", main, "-i", plan_json_path, "-o", out],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stderr = p.communicate()[0]
        if stderr:
            print(stderr)
    except Exception as e:
        print(f"Error : {e}")

def find_child(arr, index):
    temp = []
    for i in range(len(arr)):
        if arr[i]["parent"] == index:
            temp.append(i)
    return temp

def func(
    arr, index
):  ### converts into ast of type parent(type)-child(value) structure
    lst = find_child(arr, index)
    temp = {
        "type": arr[index].get("type", "unknown"),
        "strategy": arr[index].get("Strategy", "unknown"),
        "partial-mode": arr[index].get("Partial-Mode","unknown"),
        "parallel-aware": arr[index].get("Parallel-Aware", "unknown"),
        "cost": {
            #"startup": arr[index].get("Startup-Cost", "unknown"),
            "#total": arr[index].get("Total-Cost", "unknown"),
        },
        

        #"rows": arr[index].get("Plan-Rows", "unknown"),
        "width": arr[index].get("Plan-Width", "unknown"),
        "children": []
    }
    
    for child_index in lst:
        child_ast = func(arr, child_index)
        temp["children"].append(child_ast)
        
    return temp

def depth(node):  #### returns depth of any node
    d = 0
    """Why is this a while loop?"""
    while node is not None:
        d += 1
        node = node.getparent()  ######## etree function
    return d

def helper(fname):
    xml = etree.parse(plan_path)
    root = xml.getroot()
    print(root.tag)
    head=""
    
    for plan_node in root.iter("{http://www.postgresql.org/2009/explain}Plan"):
        head = plan_node.find("{http://www.postgresql.org/2009/explain}Node-Type").text
        partial_mode =plan_node.find("{http://www.postgresql.org/2009/explain}Partial-Mode")
        if(partial_mode!=None and partial_mode.text=="Partial"):
            head="Partial " + head
        if(partial_mode!=None and partial_mode.text=="Finalize"):
            head="Finalize " + head

        break
    # Initialize the AST-like list of dictionaries
    ast = []
    
    # Initialize the current node index and parent index
    curr = 0
    ast.append({
        "index": curr,
        "type":head ,
        "depth": 0,
        "parent": -1
    })
    f=0
    
    
    # Add the root node to the AST list
    
    # Iterate over the <Plan> elements in the XML file
    for plan_node in root.iter("{http://www.postgresql.org/2009/explain}Plan"):
        if(f==0):
            f=1
            continue
        
        # Extract relevant attributes from the plan node
        
        node_type = plan_node.find("{http://www.postgresql.org/2009/explain}Node-Type").text
        strategy = plan_node.find("{http://www.postgresql.org/2009/explain}Strategy")
        partial_mode =plan_node.find("{http://www.postgresql.org/2009/explain}Partial-Mode")
        parallel_aware=plan_node.find("{http://www.postgresql.org/2009/explain}Parallel-Aware").text
        #startup_cost = plan_node.find("{http://www.postgresql.org/2009/explain}Startup-Cost").text
        
        #total_cost = plan_node.find("{http://www.postgresql.org/2009/explain}Total-Cost").text
        #plan_rows = plan_node.find("{http://www.postgresql.org/2009/explain}Plan-Rows").text
        plan_width = plan_node.find("{http://www.postgresql.org/2009/explain}Plan-Width").text
        if(parallel_aware=="true"):
            node_type="Parallel " + node_type
        if(partial_mode!=None and partial_mode.text=="Partial"):
            node_type="Partial " + node_type
        if(partial_mode!=None and partial_mode.text=="Finalize"):
            node_type="Finalize " + node_type
        
        # Determine the parent node based on depth and previous nodes in the AST
        parent = -1
        depths = depth(plan_node)
        
        for i in range(curr, -1, -1):
            if ast[i]["depth"] < depths:
                parent = i
                break
        
        # Increment the current node index
        curr += 1
        
        
        # Create a dictionary representing the current node
        data = {
            "index": curr,
            "type": node_type,
            "partial-mode":partial_mode ,
            "parallel-aware": parallel_aware,
            "strategy": strategy,
            #"startup_cost": startup_cost,
            
            #"total_cost": total_cost,
            #"rows": plan_rows,
            "width": plan_width,
            "depth": depths,
            "parent": parent
        }
        
        
        # Append the dictionary to the AST-like list of dictionaries
        ast.append(data)
    
    
    # Return the AST-like list of dictionaries
    return ast

def check_and_remove_invalid_xml(file_path):
    try:
        # Attempt to parse the XML file
        ET.parse(file_path)
        return True
    except ET.ParseError:
        # If a parse error occurs, the file is invalid
        
        # Remove the invalid file
        os.remove(file_path)
        print(f"Removed invalid XML file: {file_path}")
        return False
def convert2ast(plan_path,i):
     
    xml = etree.parse(plan_path)
    lookup = helper(plan_path)
    
    tree = [func(lookup, 0)]
    with open(
      
        os.path.join("/home/haris/plan/plan"+str(i)+".json"),"w") as file:
        json.dump(tree, file)
    '''return os.path.join("your/path/to/dump/parsed/json/plan.json") '''
    return os.path.join("/home/haris/plan/plan"+str(i)+".json")
start()
folder_path="/home/haris/output_xml_files"
i=0
for file_name in os.listdir(folder_path):
 plan_path = os.path.join(folder_path, file_name)
 with open(plan_path, 'r') as file:
        content = file.read()

    # Define the string to find
 query_plan_string = "QUERY PLAN"

    # Find the index of the query_plan_string
 index = content.find(query_plan_string)
 if(content.count('<Query>')==2):
            first_query_index = content.find('<Query>')
            second_query_index = content.find('<Query>', first_query_index + len('<Query>'))
            content = content[:first_query_index] + content[second_query_index:]
            
            with open(plan_path, 'w') as file:
                file.write(content)
            
    
 if index != -1:
        print(plan_path)
        # Calculate the start of the content to keep (after "  QUERY PLAN   ")
        start_of_remaining_content = index + len(query_plan_string)
        
        # Keep only the content after "  QUERY PLAN   "
        remaining_content = content[start_of_remaining_content:]
        
        
        # Write the remaining content back to the file
        
        
        start_tag = '<explain xmlns="http://www.postgresql.org/2009/explain">'
        end_tag = '</explain>'
        start_pos = remaining_content.find(start_tag)
        end_pos = remaining_content.find(end_tag)
        end_pos += len(end_tag)
        extracted_content = remaining_content[start_pos:end_pos]
        
        
        with open(plan_path,'w') as file:
            file.write(extracted_content)
        
#  with open(plan_path,'r') as file:
#     content=file.read()
# #  modified=content.replace("       QUERY PLAN ",'')
# #  pattern = r'--+'
# #  #modu=modified.replace("--------------------------------------------------------------------------------------------","")
 
# #  index=modified.find("</explain>")
# #  modifie = modified[:index + len("</explain>")]
# #  result = re.sub(pattern, '', modifie)
# #  result=result.replace(" List of languages",'')
# #  result=result.replace(" List of Relations",'')
# #  result=result.replace(" Access privileges",'')
#     start_tag = '<explain xmlns="http://www.postgresql.org/2009/explain">'
#     end_tag = '</explain>'
    
#     # Find the positions of the starting and ending tags
#     start_pos = content.find(start_tag)
#     end_pos = content.find(end_tag)
    
#     # Check if both tags are found and in the correct order
#     if start_pos != -1 and end_pos != -1 and end_pos > start_pos:
#         # Add the length of the end tag to the end position
#         end_pos += len(end_tag)
        
#         # Extract the content between the starting and ending tags (including the tags)
#         extracted_content = content[start_pos:end_pos]

 
 
#  with open(plan_path,'w') as file:
#      file.write(extracted_content)
 if(check_and_remove_invalid_xml(plan_path)==True):
  plan_json_path = convert2ast(plan_path,i)
  convert2vector(plan_json_path,i)
  i=i+1
  print("created")
Plotter()




