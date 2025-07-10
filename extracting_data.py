import json
import pandas as pd
import os

# Paths to required files
base_folder = ""
json_folder = os.path.join(base_folder, "ipl_json")
output_file = os.path.join(base_folder, "filtered_ipl_training_data.csv")

print("Processing all JSON files...")

# Initialize match_data list
match_data = []

player_stats = {}

# Process the selected JSON file
for json_file in os.listdir(json_folder):
    if json_file.endswith(".json"):
        file_path = os.path.join(json_folder, json_file)
        with open(file_path, "r") as file:
            match = json.load(file)

            players_played_in_match = set()
            player_match_runs = {}
            player_match_wickets = {}

            def initialize_player(player_name):
                if player_name not in player_stats:
                    player_stats[player_name] = {}

                player_stats[player_name] = {
                    **{
                        "Player": player_name,
                        "Matches Played": 0,

                        # Batting stats
                        "Runs": 0, "Balls Faced": 0, "Fours": 0, "Sixes": 0, "Dot Balls": 0,
                        "25+ Scores": 0, "50+ Scores": 0, "75+ Scores": 0, "100+ Scores": 0,
                        "Runs in Powerplay": 0, "Runs in Middle Overs": 0, "Runs in Death Overs": 0,
                        "Batting Average": 0, "Strike Rate": 0,

                        # Bowling stats
                        "Wickets": 0, "LBW/Bowled Wickets": 0, "Runs Conceded": 0, "Balls Bowled": 0,
                        "Dot Balls Bowled": 0, "3+ Wickets": 0, "4+ Wickets": 0, "5+ Wickets": 0, "economy": 0,
                        "Balls Bowled in Powerplay": 0, "Balls Bowled in Death Overs": 0,
                        "Bowling Average": 0, "Bowling Strike Rate": 0,

                        # Fielding stats
                        "Catches": 0, "Stumpings": 0, "Run-Outs": 0
                    },
                    **player_stats[player_name]
                }

            # Extract innings data
            for innings in match["innings"]:
                for over in innings["overs"]:
                    over_number = over["over"]
                    for delivery in over["deliveries"]:
                        batter = delivery["batter"]
                        bowler = delivery["bowler"]
                        total_runs = delivery["runs"]["total"]
                        runs_scored = delivery["runs"]["batter"]

                        initialize_player(batter)

                        if batter not in players_played_in_match:
                            player_stats[batter]["Matches Played"] += 1
                            players_played_in_match.add(batter)

                        player_stats[batter]["Runs"] += runs_scored
                        player_stats[batter]["Balls Faced"] += 1

                        if runs_scored == 4:
                            player_stats[batter]["Fours"] += 1
                        if runs_scored == 6:
                            player_stats[batter]["Sixes"] += 1
                        if runs_scored == 0:
                            player_stats[batter]["Dot Balls"] += 1

                        if 1 <= over_number <= 6:
                            player_stats[batter]["Runs in Powerplay"] += runs_scored
                        elif 7 <= over_number <= 15:
                            player_stats[batter]["Runs in Middle Overs"] += runs_scored
                        elif 16 <= over_number <= 20:
                            player_stats[batter]["Runs in Death Overs"] += runs_scored

                        player_match_runs[batter] = player_match_runs.get(batter, 0) + runs_scored

                        initialize_player(bowler)

                        if bowler not in players_played_in_match:
                            player_stats[bowler]["Matches Played"] += 1
                            players_played_in_match.add(bowler)

                        player_stats[bowler]["Runs Conceded"] += total_runs
                        player_stats[bowler]["Balls Bowled"] += 1
                        if total_runs == 0:
                            player_stats[bowler]["Dot Balls Bowled"] += 1
                        if "wickets" in delivery and delivery["wickets"]:
                            for wicket in delivery["wickets"]:
                                if wicket["kind"] != "run out":
                                    if wicket["kind"] in ["bowled", "lbw"]:
                                        player_stats[bowler]["LBW/Bowled Wickets"] += 1
                                    player_stats[bowler]["Wickets"] += 1
                                    player_match_wickets[bowler] = player_match_wickets.get(bowler, 0) + 1

                        if 1 <= over_number <= 6:
                            player_stats[bowler]["Balls Bowled in Powerplay"] += 1
                        elif 16 <= over_number <= 20:
                            player_stats[bowler]["Balls Bowled in Death Overs"] += 1

                        for wicket in delivery.get("wickets", []):
                            for fielder in wicket.get("fielders", []):
                                fielder = fielder.get("name", "") if isinstance(fielder, dict) else fielder

                                initialize_player(fielder)

                                if fielder not in players_played_in_match:
                                    player_stats[fielder]["Matches Played"] += 1
                                    players_played_in_match.add(fielder)

                                if wicket["kind"] == "caught":
                                    player_stats[fielder]["Catches"] += 1
                                elif wicket["kind"] == "stumped":
                                    player_stats[fielder]["Stumpings"] += 1
                                elif wicket["kind"] == "run out":
                                    player_stats[fielder]["Run-Outs"] += 1

            # --- Milestone calculation after match ---
            for player in players_played_in_match:
                runs = player_match_runs.get(player, 0)
                wickets = player_match_wickets.get(player, 0)

                if runs >= 100:
                    player_stats[player]["100+ Scores"] += 1
                elif runs >= 75:
                    player_stats[player]["75+ Scores"] += 1
                elif runs >= 50:
                    player_stats[player]["50+ Scores"] += 1
                elif runs >= 25:
                    player_stats[player]["25+ Scores"] += 1

                if wickets >= 5:
                    player_stats[player]["5+ Wickets"] += 1
                elif wickets >= 4:
                    player_stats[player]["4+ Wickets"] += 1
                elif wickets >= 3:
                    player_stats[player]["3+ Wickets"] += 1

# Compute additional statistics
for player in player_stats:
    stats = player_stats[player]
    matches = stats["Matches Played"]
    if matches > 0:
        stats["Catches per Match"] = round(stats["Catches"] / matches, 3)
        stats["Stumpings per Match"] = round(stats["Stumpings"] / matches, 3)
        stats["Run-Outs per Match"] = round(stats["Run-Outs"] / matches, 3)
        stats["Catches per Match"] = round(stats["Catches"] / matches, 3)
        stats["Strike Rate"] = round((stats["Runs"] / stats["Balls Faced"]) * 100, 2) if stats["Balls Faced"] > 0 else 0
        stats["Batting Average"] = round(stats["Runs"] / matches, 2) if matches > 0 else 0
        stats["Bowling Average"] = round(stats["Runs Conceded"] / stats["Wickets"], 2) if stats["Wickets"] > 0 else 0
        stats["Bowling Strike Rate"] = round(stats["Balls Bowled"] / stats["Wickets"], 2) if stats["Wickets"] > 0 else 0
        stats["25+ runs per Match"] = round(stats["25+ Scores"] / matches, 3)
        stats["50+ runs per Match"] = round(stats["50+ Scores"] / matches, 3)
        stats["75+ runs per Match"] = round(stats["75+ Scores"] / matches, 3)
        stats["100+ runs per Match"] = round(stats["100+ Scores"] / matches, 3)
        stats["3+ wickets per Match"] = round(stats["3+ Wickets"] / matches, 3)
        stats["4+ wickets per Match"] = round(stats["4+ Wickets"] / matches, 3)
        stats["5+ wickets per Match"] = round(stats["5+ Wickets"] / matches, 3)
        if stats["Balls Bowled"]:
            stats["economy"] = round((stats["Runs Conceded"]*6) / stats["Balls Bowled"], 2)

# Convert to Pandas DataFrame
df = pd.DataFrame(player_stats.values())

# Save final dataset
df.to_csv(output_file, index=False)

print(f"Filtered IPL data saved to {output_file}")