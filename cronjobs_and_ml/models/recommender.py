import csv
import pickle
import os
# Function to read data from CSV file
def read_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entry = {
                "battle_mode": row["battle_mode"],
                "map_name": row["map_name"],
                "winners": [row["winner_1"], row["winner_2"], row["winner_3"]],
                "losers": [row["loser_1"], row["loser_2"], row["loser_3"]],
            }
            data.append(entry)
    return data

# Read data from the provided CSV file path
file_path = 'raw_data/dannybattle.csv'
data = read_csv(file_path)

# Initialize the decision tree as a regular dictionary
decision_tree = {}

# Build the decision tree
for entry in data:
    battle_mode = entry["battle_mode"]
    map_name = entry["map_name"]
    winners = entry["winners"]
    losers = entry["losers"]

    if battle_mode not in decision_tree:
        decision_tree[battle_mode] = {}
    if map_name not in decision_tree[battle_mode]:
        decision_tree[battle_mode][map_name] = {}

    for winner in winners:
        if winner not in decision_tree[battle_mode][map_name]:
            decision_tree[battle_mode][map_name][winner] = {"winners": {}, "losers": {}}
        
        # Increment the winner count
        if winner not in decision_tree[battle_mode][map_name][winner]["winners"]:
            decision_tree[battle_mode][map_name][winner]["winners"][winner] = 0
        decision_tree[battle_mode][map_name][winner]["winners"][winner] += 1
        
        for w in winners:
            if w != winner:
                if w not in decision_tree[battle_mode][map_name][winner]["winners"]:
                    decision_tree[battle_mode][map_name][winner]["winners"][w] = 0
                decision_tree[battle_mode][map_name][winner]["winners"][w] += 1
        
        for l in losers:
            if l not in decision_tree[battle_mode][map_name][winner]["losers"]:
                decision_tree[battle_mode][map_name][winner]["losers"][l] = 0
            decision_tree[battle_mode][map_name][winner]["losers"][l] += 1

# Save the decision tree to a file
with open('decision_treedanny.pkl', 'wb') as f:
    pickle.dump(decision_tree, f)
