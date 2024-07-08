import csv


def read_first_column(file_path):
    first_column_items = []

    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            first_column_items.append(
                row[0]
            )  # Append the first column item to the list

    return first_column_items


# Example usage
file_path = "brawler_data.csv"  # Replace with your CSV file path
first_column_items = read_first_column(file_path)
print(first_column_items)
