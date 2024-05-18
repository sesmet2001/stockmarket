import pandas as pd
import sqlite3
import os

def format_number(num):
    if num >= 1e9:  # If the number is greater than or equal to 1 billion
        return f"{num / 1e9:.2f}B"
    elif num >= 1e6:  # If the number is greater than or equal to 1 million
        return f"{num / 1e6:.2f}M"
    else:
        return str(num)

def remove_percentage_sign(s):
    return s.replace('%', '')

def rename_header(h):
    h = h.replace(' ','_').replace('(','').replace(')','').replace('.','').replace('/','div').lower()
    return h

#screener_df = pd.read_csv("screener-stocks.csv")
if os.name == 'nt':
    conn = sqlite3.connect('C:\wamp64\www\html\database\stockradar-lite-screener.db')
else:
    conn = sqlite3.connect('/var/www/html/database/stockradar-lite-screener.db')

screener_df = pd.read_csv("data/screener-stocks.csv",low_memory=False)

for column in screener_df.columns:
    screener_df.rename(columns={column: rename_header(column)}, inplace=True)

screener_df.to_csv("data/screener-stocks-renamed.csv")

#columns = ["rev_growth"]
for column in screener_df.columns:
    print(column)
    if not pd.api.types.is_numeric_dtype(screener_df[column]):
        contains_percent = screener_df[column].str.contains('%').any()
        if contains_percent:
            screener_df[column] = screener_df[column].str.replace('%', '', regex=False)
            screener_df[column] = pd.to_numeric(screener_df[column], errors='coerce')
screener_df.to_sql("screener", conn, if_exists='replace', index=False)

#screener_df_cleaned = screener_df.dropna(subset=['Profit Margin'])
#print(screener_df_cleaned['Profit Margin'].dtype)
#screener_df_cleaned['Profit Margin'] = screener_df_cleaned['Profit Margin'].apply(lambda x: remove_percentage_sign(x))
#screener_df_cleaned['Profit Margin'] = screener_df_cleaned['Profit Margin'].astype(float)
#print(screener_df_cleaned.head())
#screener_df_profit_margin = screener_df_cleaned.sort_values("Profit Margin", ascending=False, ignore_index=True).head(1000)[["Symbol","Company Name","Profit Margin","Revenue","Net Income"]]
#screener_df_profit_margin.to_sql('Profit Margin', conn, if_exists='replace', index=False)

conn.close()
