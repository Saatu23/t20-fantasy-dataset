import subprocess

# Define the script file paths
script1 = "extracting_data.py"
script2 = "recent_fantasy_points.py"
script3 = "current_2025_form.py"
script4 = "merging_with_consistent_names.py"

# Run Script 1
print("Running Script 1: Extracting 2021-present data...")
subprocess.run(["python", script1], check=True)

# Run Script 2
print("Running Script 2: Extracting 2024-present data with fantasy points...")
subprocess.run(["python", script2], check=True)

# Run Script 3
print("Running Script 3: Extracting 2025-present data with fantasy points...")
subprocess.run(["python", script3], check=True)

# Run Script 4
print("Running Script 4: Merging datasets...")
subprocess.run(["python", script4], check=True)

print("All scripts executed successfully!")
