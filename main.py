import re
import os
import time
from functools import wraps
from numpy.core.numeric import NaN, count_nonzero

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def check_time(function):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = function(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f'Tempo decorrido na função <{function.__name__}> : {round(time_elapsed, 3)} segundos')
        return result
    return wrapper


@check_time
def read_rain_file(file_path: str) -> pd.DataFrame:
    with open(file_path, 'r') as f:
        raw_file = f.readlines()

    list_dados = [line.split() for line in raw_file]
    float_raw_lines = [list(map(float, raw_line)) for raw_line in list_dados]
    return pd.DataFrame(float_raw_lines, columns=['lat', 'long', 'data_value'])

@check_time
def read_contour_file(file_path: str) -> pd.DataFrame:
    line_split_comp = re.compile(r'\s*,')

    with open(file_path, 'r') as f:
        raw_file = f.readlines()

    l_raw_lines = [line_split_comp.split(raw_file_line.strip()) for raw_file_line in raw_file]
    l_raw_lines = list(filter(lambda item: bool(item[0]), l_raw_lines))
    float_raw_lines = [list(map(float, raw_line))[:2] for raw_line in l_raw_lines]
    header_line = float_raw_lines.pop(0)
    assert len(float_raw_lines) == int(header_line[0])
    return pd.DataFrame(float_raw_lines, columns=['lat', 'long'])

@check_time
def apply_contour(contour_df: pd.DataFrame, rain_df: pd.DataFrame) -> pd.DataFrame:
    
    max_lat  = max(contour_df['lat'])
    min_lat  = min(contour_df['lat'])
    max_long = max(contour_df['long'])
    min_long = min(contour_df['long'])

    drop_list = []

    for row_index in range(len(rain_df['lat'])):
        if (rain_df['lat'][row_index] > max_lat or rain_df['lat'][row_index] < min_lat) or (rain_df['long'][row_index] > max_long or rain_df['long'][row_index] < min_long):
            drop_list.append(row_index)

    rain_croped = rain_df.drop(rain_df.index[drop_list])

    return rain_croped
    

@check_time
def main() -> None:
    contour_df: pd.DataFrame = read_contour_file('PSATCMG_CAMARGOS.bln')

    for file in os.listdir('forecast_files'):
        rain_df: pd.DataFrame = read_rain_file('forecast_files/'+file)
        rain_crop_df: pd.DataFrame = apply_contour(contour_df, rain_df)

        with open('forecast_files_crop/'+file, "w+") as cropped_file:
            cropped_file.write(rain_crop_df.to_string(header=False, index=False, col_space=5))

if __name__ == '__main__':
    main()