import pandas as pd
import numpy as np

def process_series(series):
    series = series.dropna()  # remove NaN values from the current series
    if len(series) < 10:  # if less than 10 data points, return None (will remove this series)
        return None

    moving_averages = series.rolling(window=5).mean()

    # Ignore the last 5 numbers
    max_average = moving_averages.iloc[:-5].max()

    max_average_index = moving_averages[moving_averages == max_average].index[0]

    # If max average is at the end or there are less than 5 numbers after it, return None
    if max_average_index == len(series) - 5 or len(series) - max_average_index - 5 < 5:
        return None

    # Cut the series
    cut_series = series.loc[:max_average_index + 5]

    return cut_series

# Read the Excel file
df = pd.read_excel(f'Table S1_3880_251125.xlsx')

original_column_names = df.columns  # save original column names

# Apply the function to each column
output = df.apply(process_series)

output.columns = original_column_names  # restore original column names

# Drop columns that were removed
output.dropna(axis=1, how='all', inplace=True)

# Write the output to an Excel file
output.to_excel(f'Table S1_3880_251125_cleaned.xlsx')
