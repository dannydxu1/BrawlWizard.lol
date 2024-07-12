import pickle
from collections import defaultdict

# Load the decision tree from a file
with open('decision_treedanny.pkl', 'rb') as f:
    decision_tree = pickle.load(f)

# Function to get the best brawlers with win percentages
def get_best_brawlers(battle_mode, map_name, teammates=None, enemies=None):
    teammates = teammates or []
    enemies = enemies or []

    if battle_mode in decision_tree and map_name in decision_tree[battle_mode]:
        node = decision_tree[battle_mode][map_name]

        # Traverse the tree based on teammates
        for teammate in teammates:
            if teammate in node:
                node = node[teammate]
            else:
                return []

        # Calculate win percentages
        print(node)
        total_wins = sum(node["winners"].values())
        recommendations = []
        for brawler, count in node["winners"].items():
            if brawler not in teammates and brawler not in enemies:
                win_percentage = round((count / total_wins) * 100,2)
                recommendations.append((brawler, win_percentage))

        # Sort recommendations by win percentage and limit to top 5
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:5]
    
    return []

# Example usage
battle_mode = "heist"
map_name = "Safe Zone"
teammates = []
enemies = []

best_brawlers = get_best_brawlers(battle_mode, map_name, teammates, enemies)
print("Top 5 Recommended Brawlers with Win Percentages:", best_brawlers)
