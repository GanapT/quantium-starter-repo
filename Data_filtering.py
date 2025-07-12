import pandas as pd
import os
from pathlib import Path


def parse_price(price_str):
    if isinstance(price_str, str):
        return float(price_str.replace('$', ''))
    return float(price_str)


def process_sales_data(input_files, output_file='pink_morsel_sales.csv'):

    all_data = []
    for file_path in input_files:
        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found. Skipping...")
            continue

        df = pd.read_csv(file_path)
        all_data.append(df)

    if not all_data:
        raise FileNotFoundError("No valid input files found!")


    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"\nCombined dataset: {len(combined_df)} total rows")


    unique_products = combined_df['product'].unique()
    print(f"Products found: {list(unique_products)}")


    pink_morsel_df = combined_df[
        combined_df['product'].str.lower() == 'pink morsel'
        ].copy()


    if len(pink_morsel_df) == 0:
        raise ValueError("No Pink Morsel transactions found in the data!")

    initial_count = len(pink_morsel_df)
    pink_morsel_df = pink_morsel_df.dropna(subset=['price', 'quantity', 'date', 'region'])
    final_count = len(pink_morsel_df)


    pink_morsel_df['price_numeric'] = pink_morsel_df['price'].apply(parse_price)
    pink_morsel_df['Sales'] = pink_morsel_df['price_numeric'] * pink_morsel_df['quantity']

    output_df = pink_morsel_df[['Sales', 'date', 'region']].copy()
    output_df.rename(columns={'date': 'Date', 'region': 'Region'}, inplace=True)

    output_df = output_df.sort_values('Date').reset_index(drop=True)


    output_df.to_csv(output_file, index=False)
    return output_df


def main():

    # Define input files
    input_files = [
        'data/daily_sales_data_0.csv',
        'data/daily_sales_data_1.csv',
        'data/daily_sales_data_2.csv'
    ]
    output_file = 'pink_morsel_sales_consolidated.csv'
    processed_data = process_sales_data(input_files, output_file)
    return 0

if __name__ == "__main__":
    exit(main())