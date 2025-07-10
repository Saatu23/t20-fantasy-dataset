import pandas as pd

# Load all datasets
file1 = r"filtered_ipl_training_data.csv"
file2 = r"2024_filtered_ipl_training_data.csv"
file3 = r"consistency_in_players_name.csv"
file4 = r"2025_filtered_ipl_training_data.csv"

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)
df4 = pd.read_csv(file4)

# Standardize player names for consistency
# for df in [df1, df2, df3]:
#     df["Player"] = df["Player"].str.strip().str.lower()

# Select relevant columns
df2 = df2[['Player', 'Total fantasy points', 'Fantasy points per match', 
           'Chennai', 'Delhi', 'Mumbai', 'Kolkata', 'Bengaluru', 'Hyderabad', 
           'Ahmedabad', 'Jaipur', 'Mohali', 'Lucknow', 'Dharamsala', 'Guwahati', 
           'Indore', 'Visakhapatnam', 
           'Chennai_matches', 'Delhi_matches', 'Mumbai_matches', 'Kolkata_matches', 
           'Bengaluru_matches', 'Hyderabad_matches', 'Ahmedabad_matches', 'Jaipur_matches', 
           'Mohali_matches', 'Lucknow_matches', 'Dharamsala_matches', 'Guwahati_matches', 
           'Indore_matches', 'Visakhapatnam_matches',
           'Chennai_avg_fantasy', 'Delhi_avg_fantasy', 'Mumbai_avg_fantasy', 'Kolkata_avg_fantasy', 
           'Bengaluru_avg_fantasy', 'Hyderabad_avg_fantasy', 'Ahmedabad_avg_fantasy', 'Jaipur_avg_fantasy', 
           'Mohali_avg_fantasy', 'Lucknow_avg_fantasy', 'Dharamsala_avg_fantasy', 'Guwahati_avg_fantasy', 
           'Indore_avg_fantasy', 'Visakhapatnam_avg_fantasy']]

df3 = df3[['Player', 'Credits', 'Player Type', 'Player Name', 'Team']]
df4 = df4[['Player', 'Total current fantasy points', 'Current Fantasy points per match']]

# Merge df3 first (to add its columns after Player)
merged_df = pd.merge(df1, df3, on='Player', how='left')

# Merge df2 next (so fantasy points are added at the end)
merged_df = pd.merge(merged_df, df2, on='Player', how='left')

merged_df = pd.merge(merged_df, df4, on='Player', how='left')  # Merge df4 last

# Reorder columns: df3 columns after Player, Fantasy columns at the end
core_columns = ['Player', 'Credits', 'Player Type', 'Player Name', 'Team']
fantasy_columns = ['Total fantasy points', 'Fantasy points per match']
current_fantasy_columns = ['Total current fantasy points', 'Current Fantasy points per match']
remaining_columns = [col for col in merged_df.columns if col not in core_columns + fantasy_columns + current_fantasy_columns + ['Player']]

final_order = core_columns + remaining_columns + fantasy_columns + current_fantasy_columns
merged_df = merged_df[final_order]

# Save final merged dataset
merged_df.to_csv("merged_players_data.csv", index=False)

print("Merge completed! Columns are correctly ordered.")

