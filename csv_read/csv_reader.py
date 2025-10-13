import csv
if __name__ == "__main__":
    import pathlib
    import os

def read_csv(file_path) -> list[dict]:
    """Reads a CSV file and returns its contents as a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
    

if __name__ == "__main__":
    # Example usage
    file_path = pathlib.Path(os.path.dirname(__file__)).parent / 'data' / 'strasbourg_entzheim.csv'
    data = read_csv(file_path)
    for row in data:
        print(row)