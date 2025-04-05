import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# Load 20 years of NVDA stock data
stock = "ASML"
data = yf.download(stock, period='20y')

# Calculate 5 technical indicators
data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
data['RSI'] = 100 - (100 / (1 + data['Close'].pct_change().rolling(window=14).apply(lambda x: (x[x > 0].sum() / -x[x < 0].sum()) if -x[x < 0].sum() != 0 else 0)))
data['MACD'] = data['Close'].ewm(span=12).mean() - data['Close'].ewm(span=26).mean()
data['STD_20'] = data['Close'].rolling(window=20).std()

# Drop NaN values
data.dropna(inplace=True)

# Normalize the data
features = ['Close', 'SMA_20', 'EMA_20', 'RSI', 'MACD', 'STD_20']
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[features])

# Sequence preparation
SEQ_LEN = 60
class StockDataset(Dataset):
    def __init__(self, data, seq_len=60):
        self.seq_len = seq_len
        self.data = data

    def __len__(self):
        return len(self.data) - self.seq_len - 7  # for next 7-day prediction

    def __getitem__(self, idx):
        x = self.data[idx:idx+self.seq_len]
        y = self.data[idx+self.seq_len:idx+self.seq_len+7, 0]  # Close price only
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

# Create dataset and dataloader
dataset = StockDataset(data_scaled)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# Transformer Model
class TransformerModel(nn.Module):
    def __init__(self, input_dim, d_model=64, nhead=4, num_layers=2):
        super().__init__()
        self.embedding = nn.Linear(input_dim, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(d_model, 7)  # Predict next 7 days

    def forward(self, x):
        x = self.embedding(x)
        x = x.permute(1, 0, 2)  # Seq_len, batch, features
        x = self.transformer(x)
        x = x[-1]  # Use the last token's output
        return self.fc(x)

model = TransformerModel(input_dim=len(features))
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# Training loop
EPOCHS = 10
for epoch in range(EPOCHS):
    for x_batch, y_batch in dataloader:
        optimizer.zero_grad()
        out = model(x_batch)
        loss = criterion(out, y_batch)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {loss.item():.6f}")

# Predict next 7 days
latest_data = torch.tensor(data_scaled[-SEQ_LEN:], dtype=torch.float32).unsqueeze(0)
with torch.no_grad():
    prediction = model(latest_data).numpy().flatten()

# Inverse scale only Close prices
predicted_prices = scaler.inverse_transform(
    np.concatenate([prediction.reshape(-1, 1), np.zeros((7, len(features)-1))], axis=1)
)[:, 0]

# Plot predictions
plt.figure(figsize=(12, 6))
plt.plot(data.index[-60:], data['Close'][-60:], label='Past 60 Days')
future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=7)
plt.plot(future_dates, predicted_prices, label='Predicted Next 7 Days')
plt.title(stock + ' Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
