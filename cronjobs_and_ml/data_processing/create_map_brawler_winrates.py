import pandas as pd
import json
from collections import defaultdict
import os
import glob
import argparse

"""
Map Brawler Winrates - {Map Name: [{Brawler: Winrate, Ranking}, ...], ...}
    Brawler winrates on each map
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a JSON file with the best brawler rankings on each map given match data."
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


def process_map_brawler_data(input_csv_path, output_json_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path)

    # Initialize dictionaries to store data
    map_brawler_stats = defaultdict(
        lambda: defaultdict(lambda: {"wins": 0, "losses": 0})
    )

    # Process each row in the DataFrame
    for index, row in df.iterrows():
        map_name = row["map_name"]

        winners = [row["winner_1"], row["winner_2"], row["winner_3"]]
        losers = [row["loser_1"], row["loser_2"], row["loser_3"]]

        # Skip rows with NaN values for brawlers
        winners = [brawler for brawler in winners if pd.notna(brawler)]
        losers = [brawler for brawler in losers if pd.notna(brawler)]

        for brawler in winners:
            map_brawler_stats[map_name][brawler]["wins"] += 1

        for brawler in losers:
            map_brawler_stats[map_name][brawler]["losses"] += 1

    # Calculate win rates and prepare data for JSON
    map_brawler_winrates = defaultdict(list)

    for map_name, brawlers in map_brawler_stats.items():
        for brawler, stats in brawlers.items():
            total_games = stats["wins"] + stats["losses"]
            winrate = (stats["wins"] / total_games) * 100 if total_games > 0 else 0
            map_brawler_winrates[map_name].append(
                {
                    "brawler": brawler,
                    "winrate": winrate,
                    "ranking": None,  # Placeholder for ranking
                }
            )

    # Rank brawlers by winrate on each map
    for map_name, brawlers in map_brawler_winrates.items():
        brawlers.sort(key=lambda x: x["winrate"], reverse=True)
        for rank, brawler in enumerate(brawlers, start=1):
            brawler["ranking"] = rank

    # Convert the dictionary to JSON and save to file
    with open(output_json_path, "w") as f:
        json.dump(map_brawler_winrates, f, indent=4)


if __name__ == "__main__":
    print(f"> Executing {os.path.basename(__file__)}")
    args = parse_args()
    input_file = args.input_file or find_most_recent_file("raw_data")
    if not input_file:
        print("Invalid input file")
    else:
        print(f'Input:"{input_file}')
        output_path = "output/brawler_map_winrates.json"
        process_map_brawler_data(input_file, output_path)
        print(f'Output:"{output_path}')
