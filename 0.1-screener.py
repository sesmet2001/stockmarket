import pandas as pd
import sqlite3
import os

URL = "https://stockanalysis.com/fetch/safe-export?cols=marketCap,peRatio,enterpriseValue,peForward,website,interestCoverage,lastSplitDate,zScore,debtFcf,taxRate,taxByRevenue,equity,workingCapital,netWorkingCapital,workingCapitalTurnover,lastSplitType,roic,country,usState,employees,employeesChange,employeesChangePercent,founded,revenue,revenueGrowth,revenueGrowthQ,revenueGrowth3Y,revenueGrowth5Y,revenueGrowthYears,revenueGrowthQuarters,grossProfit,grossProfitGrowth,grossProfitGrowthQ,grossProfitGrowth3Y,grossProfitGrowth5Y,operatingIncome,operatingIncomeGrowth,operatingIncomeGrowthQ,operatingIncomeGrowth3Y,operatingIncomeGrowth5Y,netIncomeGrowth3Y,netIncomeGrowthQ,netIncomeGrowth,netIncome,netIncomeGrowth5Y,netIncomeGrowthYears,netIncomeGrowthQuarters,incomeTax,rndByRevenue,psRatio,pbRatio,evEarnings,evEbit,fcfYield,beta,debtEbitda,debtEquity,quickRatio,currentRatio,inventoryTurnover,assetTurnover,profitPerEmployee,revPerEmployee,eps,epsGrowth,ebit,ebitda,operatingCF,shareBasedComp,sbcByRevenue,epsGrowthQ,epsGrowth3Y,epsGrowth5Y,epsGrowthYears,epsGrowthQuarters,investingCF,financingCF,netCF,capex,fcf,fcfPerShare,fcfGrowth,fcfGrowthQ,fcfGrowth3Y,fcfGrowth5Y,cash,debt,debtGrowth,debtGrowthQoQ,debtGrowth3Y,debtGrowth5Y,adjustedFCF,netCash,netCashGrowth,netCashByMarketCap,assets,liabilities,grossMargin,operatingMargin,pretaxMargin,profitMargin,fcfMargin,ebitdaMargin,ebitMargin,researchAndDevelopment,psForward,pFcfRatio,pegRatio,evSales,evSalesForward,evEbitda,evFcf,earningsYield,fcfEvYield,buybackYield,totalReturn,sharesOut,float,sharesYoY,sharesQoQ,sharesInsiders,sharesInstitutions,roe,roa,roe5y,roa5y,roic5y&type=s"

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
    h = h.replace(' ','_').replace('(','').replace(')','').replace('.','').replace('/','div').capitalize()
    return h

#screener_df = pd.read_csv("screener-stocks.csv")
if os.name == 'nt':
    conn = sqlite3.connect('C:\wamp64\www\html\database\stockradar-lite-tickers.db')
else:
    conn = sqlite3.connect('/var/www/html/database/stockradar-lite-tickers.db')

screener_df = pd.read_csv("C:/Users/idefi/Documents/To backup/Scripts/stockmarket/data/screener-stocks.csv",low_memory=False)

for column in screener_df.columns:
    screener_df.rename(columns={column: rename_header(column)}, inplace=True)

screener_df.to_csv('C:/Users/idefi/Documents/To backup/Scripts/stockmarket/data/screener-stocks-renamed.csv')

#columns = ["rev_growth"]
for column in screener_df.columns:
    print(column)
    if not pd.api.types.is_numeric_dtype(screener_df[column]):
        contains_percent = screener_df[column].str.contains('%').any()
        if contains_percent:
            screener_df[column] = screener_df[column].str.replace('%', '', regex=False)
            screener_df[column] = pd.to_numeric(screener_df[column], errors='coerce')
screener_df.to_sql("screener", conn, if_exists='replace', index=False)

# Step 0: Weigths
revenue_weight = 1
rev_growth_weight = 1
rev_growth_q_weight = 1
rev_growth_3y_weight = 1
rev_growth_5y_weight = 1
rev_growth_yrs_weight = 1
rev_growth_qtrs_weight = 1
cagr_1y_weight = 1
cagr_3y_weight = 1
cagr_5y_weight = 1
cagr_10y_weight = 1
cagr_15y_weight = 1
cagr_20y_weight = 1
fcf_growth_q_weight = 1
fcf_growth_weight = 1
fcf_growth_3y_weight = 1
fcf_growth_5y_weight = 1
net_income_weight = 1
netinc_growth_q_weight = 1
netinc_growth_weight = 1
netinc_growth_3y_weight = 1
netinc_growth_5y_weight = 1
ebitda_weight = 1
rev_gr_this_q_weight = 1
rev_gr_next_q_weight = 1
rev_gr_this_y_weight = 1	
rev_gr_next_y_weight = 1	
rev_gr_next_5y_weight = 1	
eps_gr_next_y_weight = 1
eps_gr_next_5y_weight = 1	

# Step 1: Normalize the criteria
screener_df["Revenue_rank"] = screener_df["Revenue"].rank(ascending=False) 
screener_df["Rev_growth_rank"] = screener_df["Rev_growth"].rank(ascending=False) 
screener_df["Rev_growth_q_rank"] = screener_df["Rev_growth_q"].rank(ascending=False) 
screener_df["Rev_growth_3y_rank"] = screener_df["Rev_growth_3y"].rank(ascending=False) 
screener_df["Rev_growth_5y_rank"] = screener_df["Rev_growth_5y"].rank(ascending=False) 
screener_df["Rev_growth_yrs_rank"] = screener_df["Rev_growth_yrs"].rank(ascending=False) 
screener_df["Rev_growth_qtrs_rank"] = screener_df["Rev_growth_qtrs"].rank(ascending=False) 
screener_df["Net_income_rank"] = screener_df["Net_income"].rank(ascending=False) 
screener_df["Netinc_growth_q_rank"] = screener_df["Netinc_growth_q"].rank(ascending=False) 
screener_df["Netinc_growth_rank"] = screener_df["Netinc_growth"].rank(ascending=False) 
screener_df["Netinc_growth_3y_rank"] = screener_df["Netinc_growth_3y"].rank(ascending=False) 
screener_df["Netinc_growth_5y_rank"] = screener_df["Netinc_growth_5y"].rank(ascending=False)  
screener_df["Cagr_1y_rank"] = screener_df["Cagr_1y"].rank(ascending=False) 
screener_df["Cagr_3y_rank"] = screener_df["Cagr_3y"].rank(ascending=False)
screener_df["Cagr_5y_rank"] = screener_df["Cagr_5y"].rank(ascending=False)
screener_df["Cagr_10y_rank"] = screener_df["Cagr_10y"].rank(ascending=False)
screener_df["Cagr_15y_rank"] = screener_df["Cagr_15y"].rank(ascending=False)
screener_df["Cagr_20y_rank"] = screener_df["Cagr_20y"].rank(ascending=False)
screener_df["Fcf_growth_q_rank"] = screener_df["Fcf_growth_q"].rank(ascending=False)
screener_df["Fcf_growth_rank"] = screener_df["Fcf_growth"].rank(ascending=False)
screener_df["Fcf_growth_3y_rank"] = screener_df["Fcf_growth_3y"].rank(ascending=False)
screener_df["Fcf_growth_5y_rank"] = screener_df["Fcf_growth_5y"].rank(ascending=False)
screener_df["Ebitda_rank"] = screener_df["Ebitda"].rank(ascending=False)
screener_df["Rev_gr_this_q_rank"] = screener_df["Rev_gr_this_q"].rank(ascending=False)
screener_df["Rev_gr_next_q_rank"] = screener_df["Rev_gr_next_q"].rank(ascending=False)
screener_df["Rev_gr_this_y_rank"] = screener_df["Rev_gr_this_y"].rank(ascending=False)
screener_df["Rev_gr_next_y_rank"] = screener_df["Rev_gr_next_y"].rank(ascending=False)
screener_df["Rev_gr_next_5y_rank"] = screener_df["Rev_gr_next_5y"].rank(ascending=False)
screener_df["Eps_gr_next_y_rank"] = screener_df["Eps_gr_next_y"].rank(ascending=False)
screener_df["Eps_gr_next_5y_rank"] = screener_df["Eps_gr_next_5y"].rank(ascending=False)

# Step 2: Combine ranks (e.g., weighted sum or simple sum)
screener_df["Total_Rank"] = \
    revenue_weight * screener_df["Revenue_rank"] + \
    rev_growth_weight * screener_df["Rev_growth_rank"] + \
    rev_growth_q_weight * screener_df["Rev_growth_q_rank"] + \
    rev_growth_3y_weight * screener_df["Rev_growth_3y_rank"] + \
    rev_growth_5y_weight * screener_df["Rev_growth_5y_rank"] + \
    rev_growth_yrs_weight * screener_df["Rev_growth_yrs_rank"] + \
    rev_growth_qtrs_weight * screener_df["Rev_growth_qtrs_rank"] + \
    cagr_1y_weight * screener_df["Cagr_1y_rank"] + \
    cagr_3y_weight * screener_df["Cagr_3y_rank"] + \
    cagr_5y_weight * screener_df["Cagr_5y_rank"] + \
    cagr_10y_weight * screener_df["Cagr_10y_rank"] + \
    cagr_15y_weight * screener_df["Cagr_15y_rank"] + \
    cagr_20y_weight * screener_df["Cagr_20y_rank"] + \
    fcf_growth_q_weight * screener_df["Fcf_growth_q_rank"] + \
    fcf_growth_weight * screener_df["Fcf_growth_rank"] + \
    fcf_growth_3y_weight * screener_df["Fcf_growth_3y_rank"] + \
    fcf_growth_5y_weight * screener_df["Fcf_growth_5y_rank"] + \
    net_income_weight * screener_df["Net_income_rank"] + \
    netinc_growth_q_weight * screener_df["Netinc_growth_q_rank"] + \
    netinc_growth_weight * screener_df["Netinc_growth_rank"] + \
    netinc_growth_3y_weight * screener_df["Netinc_growth_3y_rank"] + \
    netinc_growth_5y_weight * screener_df["Netinc_growth_5y_rank"] + \
    ebitda_weight * screener_df["Ebitda_rank"] + \
    rev_gr_this_q_weight * screener_df["Rev_gr_this_q_rank"] + \
    rev_gr_next_q_weight * screener_df["Rev_gr_next_q_rank"] + \
    rev_gr_this_y_weight * screener_df["Rev_gr_this_y_rank"] + \
    rev_gr_next_y_weight * screener_df["Rev_gr_next_y_rank"] + \
    rev_gr_next_5y_weight * screener_df["Rev_gr_next_5y_rank"] + \
    eps_gr_next_y_weight * screener_df["Eps_gr_next_y_rank"] + \
    eps_gr_next_5y_weight * screener_df["Eps_gr_next_5y_rank"]

# Step 3: Final ranking
screener_df["Final_Rank"] = screener_df["Total_Rank"].rank(ascending=True)  # Lower total rank = Higher priority

print("\nRanked DataFrame:")
print(screener_df.sort_values(by="Final_Rank").head(50)["Company_name"])

#screener_df_cleaned = screener_df.dropna(subset=['Profit Margin'])
#print(screener_df_cleaned['Profit Margin'].dtype)
#screener_df_cleaned['Profit Margin'] = screener_df_cleaned['Profit Margin'].apply(lambda x: remove_percentage_sign(x))
#screener_df_cleaned['Profit Margin'] = screener_df_cleaned['Profit Margin'].astype(float)
#print(screener_df_cleaned.head())
#screener_df_profit_margin = screener_df_cleaned.sort_values("Profit Margin", ascending=False, ignore_index=True).head(1000)[["Symbol","Company Name","Profit Margin","Revenue","Net Income"]]
#screener_df_profit_margin.to_sql('Profit Margin', conn, if_exists='replace', index=False)

conn.close()
