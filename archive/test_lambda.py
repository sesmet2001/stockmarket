# importing pandas library
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
 
# creating and initializing a nested list
values_list = [[15, 0], [16, 2], [20, 10], [25, 30],
               [35, 50], [40, 45], [41, 25],
               [51, 10], [50, 9]]

def find_crossover(TEMA5, prevTEMA5,SMA50):
    if TEMA5 > SMA50 and prevTEMA5 < SMA50:
        return "bullish crossover"
    elif TEMA5 < SMA50 and prevTEMA5 > SMA50:
        return "bearish crossover"
    return None

# creating a pandas dataframe
df = pd.DataFrame(values_list, columns=['SMA50','TEMA5'])
df['prevTEMA5'] = df['TEMA5'].shift(1)
df.dropna(inplace=True)
df['crossover'] = np.vectorize(find_crossover)(df["TEMA5"],df["prevTEMA5"],df["SMA50"])
print(df)
df.plot.line()
plt.show()
#df['SMAOnTopPrevious'] = df['SMAOnTop'].shift(periods=1, fill_value=False)
#print(df)

#print(type(df.loc[df[df[SMAOnTopPrevious == False]] & df[df['SMAOnTop'] == True]))
# Applying lambda function to find
# the product of 3 columns using
# df.assign()
#df = df.assign(Product=lambda x: (x['Field_1'] * x['Field_2'] * x['Field_3']))
 
# printing dataframe
#df