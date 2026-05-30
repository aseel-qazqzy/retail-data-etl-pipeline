from pathlib import Path
import pandas as pd
import os

BASE_DIR = Path(__file__).resolve().parents[2]
print(BASE_DIR)
files_path = BASE_DIR/ "data"

# Extract function
def extract(store_data, extra_data):
    extra_df = pd.read_parquet(extra_data)
    store_data = pd.read_csv(store_data)
    merged_df = store_data.merge(extra_df, on = "index")
    return merged_df

merged_df = extract(files_path/'raw/grocery_sales.csv', files_path/'raw/extra_data.parquet')

# transform function
def transform(merged_df):
    merged_df.fillna({
        "CPI": merged_df['CPI'].mean(),
        "Unemployment": merged_df['Unemployment'].mean(),
        "Size": merged_df['Size'].mean()
    }, inplace = True
    )
    
    merged_df['Date'] = pd.to_datetime(merged_df['Date'], format = "%Y-%m-%d")
    merged_df['Month'] = merged_df['Date'].dt.month 
    merged_df = merged_df[merged_df['Weekly_Sales']>10000]
    merged_df = merged_df.drop(["index", "Temperature", "Fuel_Price", "MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5", "Type", "Size", "Date"], axis = 1)
    
    return merged_df

def avg_weekly_sales_per_month(clean_data):
    monthly_sales = clean_data[["Month", "Weekly_Sales"]]
    monthly_sales = (
        monthly_sales.groupby("Month")
        .agg(Avg_Sales = ("Weekly_Sales", "mean"))
        .reset_index().round(2)
    )
    return monthly_sales

def load(full_data, full_data_file_path, agg_data, agg_data_file_path):
    full_data.to_csv(full_data_file_path, index = False)
    agg_data.to_csv(agg_data_file_path, index = False)

def validation(file_path):
    if not os.path.exists(file_path):
        raise Exception(f"There is no file at the path {file_path}")
    
def run_pipeline():
    merged_df = extract(files_path/'raw/grocery_sales.csv', files_path/'raw/extra_data.parquet')
    clean_data = transform(merged_df)
    avg_weekly_sales = avg_weekly_sales_per_month(clean_data)
    load(clean_data, files_path/'processed/clean_data.csv', avg_weekly_sales, files_path/'processed/agg_data.csv')

    