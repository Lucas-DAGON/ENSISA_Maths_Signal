from csv_read.csv_reader import read_csv
import signal_filter.signal_filter as sf
import pathlib
import os

monday = 0
tuesday = 1
wednesday = 2
thursday = 3
friday = 4
saturday = 5
sunday = 6

def main():
    file_path = pathlib.Path(os.path.dirname(__file__)) / 'data' / 'strasbourg_entzheim.csv'
    data = read_csv(file_path)
    # Example usage of the signal_filter functions
    year = '2023'
    test_2023 = sf.get_data_per_day_of_week(data, monday)
    avg_value = sf.get_average_value(test_2023, 'tmax')
    print(f"Average tmax on Mondays in {year}: {avg_value}")
    




if __name__ == "__main__":
    main()