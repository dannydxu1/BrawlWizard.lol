import pandas as pd
import numpy as np
import os
import json
import glob
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create brawler synergies given match and brawler data."
    )
    parser.add_argument(
        "input_file",
        type=str,
        nargs="?",
        default=None,
          help="Path to the input match data CSV file. If not provided, the most recent file in the raw_data folder will be used.",
    )
    return parser.parse_args()


def get_all_brawlers(input_csv_path):
    df = pd.read_csv(input_csv_path)
    brawlers = list(set(df["brawler_id"].tolist()))
    return brawlers


def create_brawler_winrate_dict(input_csv_path):
    df = pd.read_csv(input_csv_path)
    brawler_winrate_dict = dict(zip(df["brawler_id"], df["win_rate"]))
    return brawler_winrate_dict


def find_all_brawler_pairs_synergy(
    input_match_data_csv,
    brawler_data_path="output/brawler_data.csv",
):
    output_path = "output/brawler_synergy.json"
    brawlers = get_all_brawlers(brawler_data_path)
    brawler_winrates = create_brawler_winrate_dict(brawler_data_path)

    brawler_pairs = {
        brawler: {
            inner_s: {"wins": 0, "losses": 0, "winrate": 0, "synergy": 0}
            for inner_s in brawlers
            if inner_s != brawler
        }
        for brawler in brawlers
    }

    df = pd.read_csv(input_match_data_csv)
    for index, row in df.iterrows():
        winners = [row["winner_1"], row["winner_2"], row["winner_3"]]
        losers = [row["loser_1"], row["loser_2"], row["loser_3"]]

        winners = [winner for winner in winners if pd.notna(winner)]
        losers = [loser for loser in losers if pd.notna(loser)]

        if (
            len(winners) != 3
            or len(losers) != 3
            or len(winners) != len(set(winners))
            or len(losers) != len(set(losers))
        ):
            continue

        for primary_idx in range(3):
            for secondary_idx in range(3):
                if primary_idx == secondary_idx:
                    continue
                brawler_pairs[winners[primary_idx]][winners[secondary_idx]]["wins"] += 1
                brawler_pairs[losers[primary_idx]][losers[secondary_idx]]["losses"] += 1

    for brawler, inner_dictionary in brawler_pairs.items():
        for inner_brawler, stats in inner_dictionary.items():
            total_games = stats["wins"] + stats["losses"]
            winrate = (stats["wins"] / total_games) if total_games > 0 else 0
            brawler_pairs[brawler][inner_brawler]["winrate"] = round(winrate, 4)
            synergy_score = (
                0.50
                + winrate
                - (brawler_winrates[brawler] + brawler_winrates[inner_brawler]) / 2
            )
            brawler_pairs[brawler][inner_brawler]["synergy"] = round(synergy_score, 4)

    sorted_inner_brawler_pairs = {
        brawler: dict(
            sorted(
                inner_dict.items(), key=lambda item: item[1]["winrate"], reverse=True
            )
        )
        for brawler, inner_dict in brawler_pairs.items()
    }
    sorted_outer_brawler_pairs = {
        brawler: sorted_inner_brawler_pairs[brawler]
        for brawler in sorted(sorted_inner_brawler_pairs.keys())
    }

    with open(output_path, "w") as f:
        json.dump(sorted_outer_brawler_pairs, f, indent=4)
    print(f'Output:"{output_path}')


def find_brawler_pair_synergy(input_csv_path, brawler_1, brawler_2):
    brawlers = get_all_brawlers()
    if brawler_1 not in brawlers or brawler_2 not in brawlers:
        print("Invalid brawler IDs.")
        return

    df = pd.read_csv(input_csv_path)
    same_team_count = 0
    win_count = 0
    loss_count = 0

    # Process each row in the DataFrame
    for index, row in df.iterrows():
        winners = [row["winner_1"], row["winner_2"], row["winner_3"]]
        losers = [row["loser_1"], row["loser_2"], row["loser_3"]]

        winners = [
            brawler for brawler in winners if pd.notna(brawler)
        ]  # Skip rows with NaN values for brawlers
        losers = [brawler for brawler in losers if pd.notna(brawler)]

        if (
            brawler_1 in winners and brawler_2 in winners
        ):  # Check if on same winning team
            same_team_count += 1
            win_count += 1

        if brawler_1 in losers and brawler_2 in losers:  # Check if on same losing team
            same_team_count += 1
            loss_count += 1

    if same_team_count > 0:
        win_rate = (win_count / same_team_count) * 100
        lose_rate = (loss_count / same_team_count) * 100
    else:
        win_rate = 0
        lose_rate = 0

    return win_rate


def find_most_recent_file(directory):
    print("Finding most recent file")
    files = glob.glob(os.path.join(directory, "*"))
    if not files:
        return None
    most_recent_file = max(files, key=os.path.getctime)
    return most_recent_file


if __name__ == "__main__":
    print(f"> Executing {os.path.basename(__file__)}")
    args = parse_args()
    input_file = args.input_file or find_most_recent_file("raw_data")
    print(f'Input: "{input_file}"')
    if not input_file:
        print("Invalid input file")
    else:
        find_all_brawler_pairs_synergy(input_file)
