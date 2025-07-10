import pandas as pd

# File paths (change these to your actual file paths)
csv_file = 'merged_players_data.csv'
excel_file = 'SquadPlayerNames_IndianT20League.xlsx'
sheet_name = 'SquadData_AllTeams'

# Load the CSV and Excel "Player Name" columns
csv_df = pd.read_csv(csv_file)
excel_df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Extract 'Player Name' columns and clean them
csv_players = csv_df['Player Name'].dropna().astype(str).str.strip()
excel_players = excel_df['Player Name'].dropna().astype(str).str.strip()

# Get unique names in each
unique_csv = set(csv_players)
unique_excel = set(excel_players)

# Find differences
only_in_csv = unique_csv - unique_excel
only_in_excel = unique_excel - unique_csv

# Output results
print("✅ Players in CSV but not in Excel:")
for name in sorted(only_in_csv):
    print(name)

print("\n✅ Players in Excel but not in CSV:")
i = 0
for name in sorted(only_in_excel):
    i+=1
    print(name)

print(i)
