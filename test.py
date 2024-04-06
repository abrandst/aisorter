import os
import subprocess

# Define the directories
source_dir = "mail"
result_dir = "result"

# Create the result directory if it doesn't exist
os.makedirs(result_dir, exist_ok=True)

# List all files in the source directory
for filename in os.listdir(source_dir):
    # Construct the full path for the source and result files
    source_file = os.path.join(source_dir, filename)
    result_file = os.path.join(result_dir, filename)
    
    # Call cat.py with the source file and capture the output
    output = subprocess.check_output(['python', 'cat.py', source_file], text=True)

    # Write the output to the result file
    with open(result_file, 'w') as f:
        f.write(output)

print("Processing complete.")
