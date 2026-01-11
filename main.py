from csv_read.csv_reader import read_csv
import pathlib
import os
from datetime import datetime
from run_noise_estimate import noise_estimate
from run_descriptive import data_description
import pandas as pd
from plot_data.courbes_des_cycles import plot_annual_cycles

def main():
    file_path = pathlib.Path(os.path.dirname(__file__)) / 'data' / 'strasbourg_entzheim.csv'
    data = read_csv(file_path)
    csvkey_list = ['tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wspd', 'wpgt', 'pres', 'tsun']

    df = pd.read_csv(file_path)
    df["time"] = pd.to_datetime(df["time"])
    df["month"] = df["time"].dt.month
    monthly_cycle = df.groupby("month").mean(numeric_only=True)
    months = range(1, 13)

    # Séparer tsun car manque de variable
    #tsun_monthly = (df.dropna(subset=["tsun"]).groupby("month")["tsun"].sum())
    #tsun_cycle = tsun_monthly.groupby(tsun_monthly.index).mean()


    for ckey in csvkey_list:
        data_description(data, ckey=ckey)
        plot_annual_cycles(ckey, monthly_cycle, months)
        noise_estimate(data, key=ckey)

    

if __name__ == "__main__":
    main()