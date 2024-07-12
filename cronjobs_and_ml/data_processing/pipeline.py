import subprocess
import os
import sys
import re


def run_subprocess(script, *args):
    result = subprocess.run(
        [sys.executable, script] + list(args),
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"Error running {script}: {result.stderr}")
        sys.exit(1)
    return result


def main(num_battles=1000, player_tag="#PLYYP2RRQ"):
    fetch_data_script = "data_fetching/get_battle_logs.py"
    result = run_subprocess(fetch_data_script, player_tag, str(num_battles))

    match = re.search(r'Output: "(.*?)"', result.stdout)
    if match:
        match_data_file = match.group(1)
        stats_scripts = [
            "create_brawler_synergy.py",
            "create_brawler_counters.py",
            "create_map_brawler_winrates.py",
        ]

        # Run create_brawler_data.py
        relative_path = "data_processing/" + "create_brawler_data.py"
        result = run_subprocess(relative_path, match_data_file)

        match = re.search(r'Output: "(.*?)"', result.stdout)
        if match:
            brawler_data_file = match.group(1)

            # Run format_brawler_data.py
            relative_path = "data_processing/" + "format_brawler_data.py"
            result = run_subprocess(relative_path, brawler_data_file)
    
            match = re.search(r'Output: "(.*?)"', result.stdout)
            if match:
                formatted_brawler_data_file = match.group(1)

                # Run stats scripts with the formatted brawler data file
                for script in stats_scripts:
                    relative_path = "data_processing/" + script
                    run_subprocess(relative_path, match_data_file)
            else:
                print(
                    "Could not find the output file in the script output of format_brawler_data.py."
                )
                sys.exit(1)
        else:
            print(
                "Could not find the output file in the script output of create_brawler_data.py."
            )
            sys.exit(1)
    else:
        print(
            "Could not find the output file in the script output of get_battle_logs.py."
        )
        sys.exit(1)


if __name__ == "__main__":
    print(f"> Executing {os.path.basename(__file__)}")
    if len(sys.argv) != 3:
        print("Default usage: python pipeline.py <num_battles> <player_tag>")
        print(
            "Input parameters not passed in, using default values (1000 battles, player tag #PLYYP2RRQ)"
        )
        main()
    else:
        num_battles = int(sys.argv[1])
        player_tag = sys.argv[2]
        main(num_battles, player_tag)
