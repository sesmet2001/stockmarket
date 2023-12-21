import yfinance as yf
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

# Define a list of S&P 500 stock symbols
sp500_symbols = ['AAPL', 'MSFT', 'GOOGL']  # Add more symbols

# Download historical stock data
data = yf.download(sp500_symbols, start='2022-01-01', end='2022-12-31', progress=False)

# Extract adjusted closing prices
closing_prices = data['Adj Close']

# Calculate daily returns
returns = closing_prices.pct_change().dropna()

# Calculate correlation matrix
correlation_matrix = returns.corr()

# Perform hierarchical clustering
linkage_matrix = sch.linkage(correlation_matrix, method='ward')

# Plot the dendrogram to visualize clusters
dendrogram = sch.dendrogram(linkage_matrix, labels=correlation_matrix.columns)
plt.xlabel('Stocks')
plt.ylabel('Correlation Distance')
plt.title('Hierarchical Clustering of S&P 500 Stocks')
plt.show()

# Determine the number of clusters (groups) based on the dendrogram structure
num_clusters = 3  # Adjust as needed

# Use a clustering algorithm (e.g., K-Means) to assign stocks to groups
from sklearn.cluster import AgglomerativeClustering

cluster_model = AgglomerativeClustering(n_clusters=num_clusters)
clusters = cluster_model.fit_predict(correlation_matrix)

# Print the stocks in each cluster
for cluster_num in range(num_clusters):
    stocks_in_cluster = correlation_matrix.columns[clusters == cluster_num]
    print(f'Cluster {cluster_num + 1}: {stocks_in_cluster.tolist()}')
