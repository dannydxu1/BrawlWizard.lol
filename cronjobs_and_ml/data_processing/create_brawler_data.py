import pandas as pd
import re
from datetime import datetime
import glob
import os
import argparse


# For new brawlers, they are dropped unless included in one of the classes
# Define brawler classes
formatted_damage_dealer_names = [
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
]

formatted_controller_names = [
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
]

formatted_sniper_names = [
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
]

formatted_thrower_names = [
    "Barley",
    "Dynamike",
    "Grom",
    "Larry & Lawrie",
    "Sprout",
    "Tick",
]

formatted_assasin_names = [
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
]

formatted_tank_names = [
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
]

formatted_support_names = [
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate brawler stats from input file."
    )
    parser.add_argument(
        "input_file",
        type=str,
        nargs="?",
        default=None,
        help="Path to the input CSV file. If not provided, the most recent file in the raw_data folder will be used.",
    )
    return parser.parse_args()


def generate_brawler_stats(input_file, output_file):
    damage_dealers = [element.upper() for element in formatted_damage_dealer_names]
    controllers = [element.upper() for element in formatted_controller_names]
    snipers = [element.upper() for element in formatted_sniper_names]
    throwers = [element.upper() for element in formatted_thrower_names]
    assassins = [element.upper() for element in formatted_assasin_names]
    tanks = [element.upper() for element in formatted_tank_names]
    supports = [element.upper() for element in formatted_support_names]

    df = pd.read_csv(input_file)
    # Convert from wide format to long format
    win_columns = ["winner_1", "winner_2", "winner_3"]
    lose_columns = ["loser_1", "loser_2", "loser_3"]

    winners = df.melt(
        id_vars=["battle_mode", "map_name"],
        value_vars=win_columns,
        var_name="win_column",
        value_name="brawler_id",
    )
    winners["win"] = 1

    losers = df.melt(
        id_vars=["battle_mode", "map_name"],
        value_vars=lose_columns,
        var_name="lose_column",
        value_name="brawler_id",
    )
    losers["win"] = 0

    df_long = pd.concat([winners, losers])

    # Calculate win rate for each brawler
    brawler_stats = (
        df_long.groupby("brawler_id").agg(win_rate=("win", "mean")).reset_index()
    )

    # Calculate usage rate
    total_battles = len(df_long)
    brawler_stats["usage_rate"] = (
        df_long.groupby("brawler_id")["win"].count().values / total_battles
    )

    # Standardize win rate and usage rate
    brawler_stats["standardized_winrate"] = (
        brawler_stats["win_rate"] - brawler_stats["win_rate"].mean()
    ) / brawler_stats["win_rate"].std()
    brawler_stats["standardized_usage_rate"] = (
        brawler_stats["usage_rate"] - brawler_stats["usage_rate"].mean()
    ) / brawler_stats["usage_rate"].std()

    # Calculate composite score
    alpha = 1  # weight for winrate
    beta = 0.01  # weight for usage rate
    brawler_stats["composite_score"] = (
        alpha * brawler_stats["standardized_winrate"]
        + beta * brawler_stats["standardized_usage_rate"]
    )

    # Rank brawlers by composite score
    brawler_stats["rank"] = brawler_stats["composite_score"].rank(ascending=False)

    # Sort by win rate
    brawler_stats = brawler_stats.sort_values("win_rate", ascending=False)

    # Add class column and assign class based on brawler lists
    brawler_stats["class"] = brawler_stats["brawler_id"].apply(
        lambda x: (
            "damage_dealer"
            if x in damage_dealers
            else (
                "controller"
                if x in controllers
                else (
                    "sniper"
                    if x in snipers
                    else (
                        "thrower"
                        if x in throwers
                        else (
                            "assassin"
                            if x in assassins
                            else (
                                "tank"
                                if x in tanks
                                else "support" if x in supports else None
                            )
                        )
                    )
                )
            )
        )
    )

    # Remove rows where class is None
    brawler_stats = brawler_stats.dropna(subset=["class"])

    # Format columns to have a maximum of three decimal places
    brawler_stats["win_rate"] = brawler_stats["win_rate"].round(3)
    brawler_stats["usage_rate"] = brawler_stats["usage_rate"].round(3)
    brawler_stats["standardized_winrate"] = brawler_stats["standardized_winrate"].round(
        3
    )
    brawler_stats["standardized_usage_rate"] = brawler_stats[
        "standardized_usage_rate"
    ].round(3)
    brawler_stats["composite_score"] = brawler_stats["composite_score"].round(3)
    brawler_stats["rank"] = brawler_stats["rank"].round(3)

    # Save the resulting DataFrame to a new CSV file
    brawler_stats.to_csv(output_file, index=False)


def main(input_file):
    if not input_file:
        print("Input file was invalid")
        return
    else:
        print(f'Input: "{input_file}"')
        output_file = f"output/brawler_data.csv"
        print(f'Output: "{output_file}"')
        generate_brawler_stats(input_file, output_file)


def find_most_recent_file(directory):
    files = glob.glob(os.path.join(directory, "*"))
    if not files:
        return None
    most_recent_file = max(files, key=os.path.getctime)
    return most_recent_file


if __name__ == "__main__":
    print(f"> Executing {os.path.basename(__file__)}")
    args = parse_args()
    input_file = args.input_file or find_most_recent_file("raw_data")
    main(input_file)
