from csv_read.csv_reader import read_csv
import pathlib
import os
from datetime import datetime
from run_noise_estimate import noise_estimate
from run_descriptive import data_description

def main():
    file_path = pathlib.Path(os.path.dirname(__file__)) / 'data' / 'strasbourg_entzheim.csv'
    data = read_csv(file_path)
    csvkey_list = ['tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wspd', 'wpgt', 'pres', 'tsun']
    for ckey in csvkey_list:
        data_description(data, ckey=ckey)
        noise_estimate(data, key=ckey)


    
    

#Oui, insere la fonction dans main.py mais par

if __name__ == "__main__":
    main()