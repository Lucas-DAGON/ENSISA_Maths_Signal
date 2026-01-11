from csv_read.csv_reader import read_csv
from sumerize_data.data_description import descriptive_stats as ds
import pathlib, os

def data_description(data, ckey='tsun'):
    """Run descriptive statistics for a given key and print/save the summary."""
    p = pathlib.Path(os.path.dirname(__file__)) / 'data' / 'strasbourg_entzheim.csv'
    data = read_csv(p)
    summary = ds(data, key=ckey, show_plots=False, save_csv=f"data_out/summary_{ckey}.csv")
    print(f"Descriptive summary for '{ckey}':")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print('-----------------------------------')
