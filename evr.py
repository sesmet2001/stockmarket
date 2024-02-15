import plotly.express as px
import os
import sqlite3
import pandas as pd

DB_PATH = os.getenv('DB_PATH')

conn = sqlite3.connect(DB_PATH + '/database/stockradar-lite-info.db')

# Define your SQL query
query = "SELECT * FROM _yf_info ORDER BY trailingEps DESC LIMIT 1000"

# Execute the query and load the data into a DataFrame
df = pd.read_sql_query(query, conn)

# Create a scatter plot
fig = px.scatter(df, x='enterpriseToRevenue', y='trailingEps',
                 color='sector',  # Color points by the 'species' column
                 hover_data=['shortName', 'enterpriseToRevenue', 'trailingEps'])  

fig.update_layout(
    title="Zoomed View on Specific Range",
    xaxis=dict(range=[-10, 40]),  
    yaxis=dict(range=[0, 40])
)
# Show the plot
fig.show()

# To generate an HTML file
fig.write_html(DB_PATH + "/evr.html")

# Don't forget to close the connection when done
conn.close()