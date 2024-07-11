import pandas as pd
import json
from collections import defaultdict
import os
import glob
import argparse

"""
Antagony - {Brawler A: {Brawler B, Brawler C, ...}, ...}
    Pick Brawler A to counter enemy Brawler B
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create brawler counters given match and brawler data."
    )
    parser.add_argument(
        "input_file",
        type=str,
        nargs="?",
        default=None,
        help="Path to the input match data CSV file. If not provided, the most recent file in the raw_data folder will be used.",
    )
    return parser.parse_args()


def find_most_recent_file(directory):
    files = glob.glob(os.path.join(directory, "*"))
    if not files:
        return None
    most_recent_file = max(files, key=os.path.getctime)
    return most_recent_file


def process_brawler_data(input_csv_path, output_antagony_json_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path)

    # Initialize dictionary to store antagony data
    antagony_stats = defaultdict(lambda: defaultdict(lambda: {"wins": 0, "total": 0}))

    # Process each row in the DataFrame
    for index, row in df.iterrows():
        winners = [row["winner_1"], row["winner_2"], row["winner_3"]]
        losers = [row["loser_1"], row["loser_2"], row["loser_3"]]

        # Skip rows with NaN values for brawlers
        winners = [brawler for brawler in winners if pd.notna(brawler)]
        losers = [brawler for brawler in losers if pd.notna(brawler)]

        # Update antagony stats
        for winner in winners:
            for loser in losers:
                antagony_stats[winner][loser]["wins"] += 1
                antagony_stats[winner][loser]["total"] += 1
                antagony_stats[loser][winner]["total"] += 1

    # Calculate antagony percentages
    antagony_percentages = defaultdict(dict)

    for brawler, opponents in antagony_stats.items():
        for opponent, stats in opponents.items():
            if stats["total"] > 0:
                antagony_percentage = (stats["wins"] / stats["total"]) * 100
                antagony_percentages[brawler][opponent] = antagony_percentage

    # Prepare JSON data for antagony
    antagony_data = defaultdict(dict)
    for brawler in antagony_percentages:
        antagony = sorted(
            antagony_percentages[brawler].items(), key=lambda x: x[1], reverse=True
        )
        antagony_data[brawler] = [
            {"brawler": opponent, "percentage": percentage}
            for opponent, percentage in antagony
            if opponent != brawler
        ]

    # Save to JSON file
    with open(output_antagony_json_path, "w") as f:
        json.dump(antagony_data, f, indent=4)


if __name__ == "__main__":
    print(f"> Executing {os.path.basename(__file__)}")
    args = parse_args()
    input_file = args.input_file or find_most_recent_file("raw_data")
    if not input_file:
        print("Invalid input file")
    else:
        output_path = "output/brawler_counters.json"
        print(f'Input: "{input_file}"')
        process_brawler_data(input_file, output_path)
        print(f'Output:"{output_path}')
