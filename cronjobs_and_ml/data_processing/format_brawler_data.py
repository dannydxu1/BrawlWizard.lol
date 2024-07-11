import csv

# Define brawler categories
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
lowercase_brawlers = {brawler.lower(): brawler for brawler in formatted_brawlers}


def process_csv(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in reader:
            brawler_id = row["brawler_id"].lower()
            if brawler_id in lowercase_brawlers:
                if brawler_id == "8-bit":
                    row["brawler_id"] = "8-Bit"
                elif brawler_id == "r-t":
                    row["brawler_id"] = "R-T"
                elif brawler_id == "larry & lawrie":
                    row["brawler_id"] = "Larry & Lawrie"
                else:
                    row["brawler_id"] = brawler_id[0].upper() + brawler_id[1:]
            else:
                print(f"Unknown brawler: {brawler_id}")
            writer.writerow(row)


# Usage
input_file = "output/brawler_data.csv"
output_file = "output/brawler_data_formatted.csv"
process_csv(input_file, output_file)
