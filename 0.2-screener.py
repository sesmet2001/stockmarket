import pandas as pd

# Specify the path to your CSV file
#csv_file_path = "C:/Users/idefi/Documents/To-Backup/Scripts/stockmarket/stockanalysis/screener-stocks-2024-11-30.csv"

# Load a few rows and columns from the CSV file
# Use `usecols` to specify which columns you want to include
# Use `nrows` to specify how many rows you want to read
#df = pd.read_csv(csv_file_path, usecols=['Company Name', 'Revenue'], nrows=5)

# Display the resulting DataFrame
#print(df)

#df.to_excel('C:/Users/idefi/Documents/To-Backup/Scripts/stockmarket/stockanalysis/screener-selection.xlsx', index=False)

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "C:/Users/idefi/Documents/To backup/Scripts/Stockmarket/data/screener-stocks.csv"  # Update the path if needed
df = pd.read_csv(file_path)

# Convert relevant growth metrics to numeric values
growth_columns = ['NetInc Growth 5Y', 'Rev. Growth 5Y', 'EPS Growth 5Y']
for col in growth_columns:
    df[col] = df[col].str.replace('%', '', regex=True).astype(float)

# Select the top 5 companies based on Revenue Growth
best_companies = df.nlargest(5, 'Rev. Growth 5Y')

# Plot Revenue Growth Comparison
plt.figure(figsize=(10, 6))
plt.bar(best_companies['Company Name'], best_companies['Rev. Growth 5Y'], color='blue')
plt.xlabel("Company Name")
plt.ylabel("Revenue Growth (5Y) %")
plt.title("Top 5 Companies by Revenue Growth")
plt.xticks(rotation=45, ha='right')
plt.show()

# Plot Net Income Growth Comparison
plt.figure(figsize=(10, 6))
plt.bar(best_companies['Company Name'], best_companies['NetInc Growth 5Y'], color='green')
plt.xlabel("Company Name")
plt.ylabel("Net Income Growth (5Y) %")
plt.title("Top 5 Companies by Net Income Growth")
plt.xticks(rotation=45, ha='right')
plt.show()

# Plot EPS Growth Comparison
plt.figure(figsize=(10, 6))
plt.bar(best_companies['Company Name'], best_companies['EPS Growth 5Y'], color='red')
plt.xlabel("Company Name")
plt.ylabel("EPS Growth (5Y) %")
plt.title("Top 5 Companies by EPS Growth")
plt.xticks(rotation=45, ha='right')
plt.show()
