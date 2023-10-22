from yahoo_fin.stock_info import *
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "stockradar",
    passwd = "5.;VKopU",
    database = "stockradar"
)

cursor = db.cursor()

symbols = tickers_sp500()

for symbol in symbols:
    sql = "INSERT INTO _symbols_sp500 (symbol,stockindex) VALUES (%s,%s)"
    val = (symbol, "sp500")
    cursor.execute(sql,val)

db.commit()
cursor.close()