from yahoo_fin.stock_info import *
from collections import Counter

# db = mysql.connect(
#     host = "localhost",
#     user = "stockradar",
#     passwd = "5.;VKopU",
#     database = "stockradar"
# )

# cursor = db.cursor()

tickers_nasdaq = tickers_nasdaq()
print(len(tickers_nasdaq))

tickers_dow = tickers_dow()
print(tickers_dow)


tickers_ftse100 = tickers_ftse100()
print(tickers_ftse100)

tickers_ftse250 = tickers_ftse250()
print(tickers_ftse250)

tickers_ibovespa = tickers_ibovespa()
print(len(tickers_ibovespa))

tickers_nifty50 = tickers_nifty50()
print(tickers_nifty50)

tickers_niftybank = tickers_niftybank()
print(tickers_niftybank)

diff_list = list((Counter(tickers_nifty50) - Counter(tickers_niftybank)).elements())

print("Result of list subtraction : ",len(diff_list))

tickers_other = tickers_other()
print(tickers_other.index("ALNOV.PA"))

# for symbol in symbols:
#     #sql = "INSERT INTO _symbols_nasdaq (symbol,stockindex) VALUES (%s,%s)"
#     val = (symbol, "nasdaq")
#     cursor.execute(sql,val)

# db.commit()
# cursor.close()