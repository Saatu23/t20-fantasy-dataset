# 📊 T20 Fantasy Dataset

[![Made with Python](https://img.shields.io/badge/Built%20with-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Data Source](https://img.shields.io/badge/Data%20source-Custom%20Parsed-blue)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](./LICENSE)

> A highly detailed dataset containing T20 cricket player statistics, fantasy performance history, and venue-specific metrics.  
> Built entirely by parsing **ball-by-ball commentary JSONs**, this dataset powers my [IPL Fantasy Predictor](https://github.com/Saatu23/ipl-fantasy-predictor).

---

### 📦 Dataset Files

- `merged_players_data.csv` – Primary dataset with all player stats and fantasy data
- `venues.csv` – Maps `match_number` to the match `venue` for use in modeling

---

### 🧠 Features Breakdown

#### 🏏 **Basic Player Info**
| Column            | Description                      |
|------------------|----------------------------------|
| Player            | Player short name (ID)           |
| Player Name       | Full name                        |
| Team              | Franchise name                   |
| Player Type       | `WK`, `BAT`, `ALL`, or `BOWL`    |
| Credits           | Fantasy league credit value      |

#### 📊 **Batting Stats**
- Matches Played, Runs, Balls Faced
- Fours, Sixes, Dot Balls
- 25+/50+/75+/100+ scores
- Runs in Powerplay, Middle Overs, Death Overs
- Batting Average, Strike Rate

#### 🏏 **Bowling Stats**
- Wickets, LBW/Bowled Wickets
- Balls Bowled, Dot Balls Bowled
- Runs Conceded, Economy
- 3+/4+/5+ Wicket hauls
- Balls Bowled in Powerplay / Death
- Bowling Average, Bowling Strike Rate

#### 🧤 **Fielding Stats**
- Catches, Stumpings, Run-Outs
- Per Match: Catches/Stumpings/Run-Outs

#### 📈 **Fantasy Performance**
- Total Fantasy Points, Fantasy Points per Match
- Total Current Fantasy Points (latest season)
- Current Fantasy Points per Match

#### 🏟️ **Venue-Specific Metrics**
- Columns like:
  - `Mumbai`, `Chennai`, `Kolkata`, ... (fantasy points at venue)
  - `Mumbai_matches`, `Kolkata_matches`, ... (match count at venue)
  - `Mumbai_avg_fantasy`, `Chennai_avg_fantasy`, etc.

---

### 📊 Sample Schema (Partial)

| Player Name | Team | Player Type | Runs | Wickets | Fantasy points per match | Mumbai_avg_fantasy | ... |
|-------------|------|--------------|------|---------|----------------------------|---------------------|-----|
| R Sharma    | MI   | BAT          | 5523 | 2       | 48.2                       | 52.7                | ... |

---

### 📂 Use Cases

✅ Model training for fantasy point prediction  
✅ Form-based team selection  
✅ Venue-aware player analysis  
✅ Fantasy strategy optimization  
✅ Custom cricket dashboards

---

### 🛠 Built Using

- Python (pandas, NumPy)
- Raw JSON parsing from IPL ball-by-ball commentary
- Custom mapping and aggregation logic
- Manual validation for role, credit, and match mappings

---

### 🧪 Sample Usage (Python)

```python
import pandas as pd

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/Saatu23/t20-fantasy-dataset/main/merged_players_data.csv")

# Example: Top 5 all-rounders by Fantasy Points per Match
top_all = df[df["Player Type"] == "ALL"].sort_values("Fantasy points per match", ascending=False).head()
print(top_all[["Player Name", "Fantasy points per match"]])
```
### 🙋‍♂️ Author

**Satyam Kumar Mishra**  
📧 satyammishra20102004@gmail.com  
🔗 [GitHub](https://github.com/Saatu23)
