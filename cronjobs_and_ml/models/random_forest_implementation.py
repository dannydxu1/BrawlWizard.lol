import pandas as pd
import joblib

# Load the trained model
pipeline = joblib.load("models/random_forest.pkl")
print("Model loaded successfully!")

# Mapping of brawler names to formatted brawler names
formatted_brawlers = [
    "8-Bit",
    "Carl",
    "Chester",
    "Chuck",
    "Clancy",
    "Colette",
    "Colt",
    "Eve",
    "Lola",
    "Nita",
    "Pearl",
    "R-T",
    "Rico",
    "Shelly",
    "Spike",
    "Surge",
    "Tara",
    "Amber",
    "Bo",
    "Jessie",
    "Lou",
    "Charlie",
    "Mr. P",
    "Emz",
    "Otis",
    "Gale",
    "Sandy",
    "Gene",
    "Griff",
    "Squeak",
    "Willow",
    "Penny",
    "Angelo",
    "Bea",
    "Belle",
    "Bonnie",
    "Brock",
    "Janet",
    "Maisie",
    "Mandy",
    "Nani",
    "Piper",
    "Barley",
    "Dynamike",
    "Grom",
    "Larry & Lawrie",
    "Sprout",
    "Tick",
    "Buzz",
    "Cordelius",
    "Crow",
    "Edgar",
    "Fang",
    "Leon",
    "Lily",
    "Melodie",
    "Mico",
    "Mortis",
    "Sam",
    "Stu",
    "Ash",
    "Bibi",
    "Bull",
    "Buster",
    "Darryl",
    "Draco",
    "El Primo",
    "Frank",
    "Hank",
    "Jacky",
    "Meg",
    "Rosa",
    "Berry",
    "Byron",
    "Doug",
    "Gray",
    "Gus",
    "Kit",
    "Max",
    "Pam",
    "Poco",
    "Ruffs",
]

# Create a mapping from lowercase names to formatted names
formatted_brawlers_map = {brawler.lower(): brawler for brawler in formatted_brawlers}


# Function to make predictions based on input
def recommend_brawlers(
    battle_mode,
    map_name,
    winner_1,
    winner_2,
    winner_3,
    loser_1,
    loser_2,
    loser_3,
    top_n=10,
):
    categorical_features = [
        "battle_mode",
        "map_name",
        "winner_1",
        "winner_2",
        "winner_3",
        "loser_1",
        "loser_2",
        "loser_3",
    ]
    input_data = pd.DataFrame(
        [
            [
                battle_mode,
                map_name,
                winner_1,
                winner_2,
                winner_3,
                loser_1,
                loser_2,
                loser_3,
            ]
        ],
        columns=categorical_features,
    )

    # Predict probabilities for each brawler
    probabilities = pipeline.predict_proba(input_data)[0]

    # Get already picked brawlers (case insensitive)
    already_picked = {
        winner_1.lower(),
        winner_2.lower(),
        winner_3.lower(),
        loser_1.lower(),
        loser_2.lower(),
        loser_3.lower(),
    }

    # Get the top N brawlers with the highest probabilities excluding already picked ones
    top_brawlers = []
    for index in probabilities.argsort()[::-1]:
        brawler = pipeline.classes_[index].lower()
        if brawler not in already_picked and brawler in formatted_brawlers_map:
            top_brawlers.append((formatted_brawlers_map[brawler], probabilities[index]))
            if len(top_brawlers) == top_n:
                break

    return top_brawlers


# Example usage of the recommendation function
battle_mode = "knockout"
map_name = "Flaring Phoenix"
winner_1 = ""
winner_2 = "PIPER"
winner_3 = ""
loser_1 = ""
loser_2 = ""
loser_3 = ""

recommended_brawlers = recommend_brawlers(
    battle_mode,
    map_name,
    winner_1,
    winner_2,
    winner_3,
    loser_1,
    loser_2,
    loser_3,
    top_n=10,
)
print(f"Recommended Brawlers: {recommended_brawlers}")


# Function to test custom input
def test_custom_input():
    battle_mode = input("Enter battle mode: ")
    map_name = input("Enter map name: ")
    winner_1 = input("Enter first teammate: ")
    winner_2 = input("Enter second teammate: ")
    winner_3 = input("Enter second teammate: ")
    loser_1 = input("Enter first opponent: ")
    loser_2 = input("Enter second opponent: ")
    loser_3 = input("Enter third opponent: ")
    top_n = int(input("Enter number of top recommendations: "))

    recommended_brawlers = recommend_brawlers(
        battle_mode,
        map_name,
        winner_1,
        winner_2,
        winner_3,
        loser_1,
        loser_2,
        loser_3,
        top_n=top_n,
    )
    print(f"Recommended Brawlers: {recommended_brawlers}")


# Uncomment the line below to test with custom input
# test_custom_input()
