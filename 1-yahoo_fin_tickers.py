import sqlite3
import yahoo_fin.stock_info as si
import yfinance as yf
import pandas as pd
import sqlite3
import os

def main():
    try:
        #  Define variables
        DB_PATH = os.getenv('DB_PATH')
        conn_tickers = sqlite3.connect(DB_PATH + "/database/stockradar-lite-tickers.db")
        pd.set_option('display.max_columns', None)

        # Screener tickers
        conn_screener = sqlite3.connect(DB_PATH + "/database/stockradar-lite-screener.db")
        pd_screener_tickers = pd.read_sql_query("SELECT symbol,company_name FROM screener", conn_screener)
        lst_screener_tickers = pd_screener_tickers['symbol'].tolist()
        pd_screener_tickers.rename(columns={'symbol': 'Ticker'}, inplace=True)
        pd_screener_tickers.rename(columns={'company_name': 'Company'}, inplace=True)
        pd_screener_tickers.set_index(['Ticker'])
        print("screener tickers done")

        # Dow Jones tickers
        pd_dow_tickers_full = si.tickers_dow(include_company_data = True)
        pd_dow_tickers = pd_dow_tickers_full[['Symbol','Company']]
        lst_dow_tickers = pd_dow_tickers['Symbol']
        pd_dow_tickers.rename(columns={'Symbol': 'Ticker'}, inplace=True)
        pd_dow_tickers.set_index(['Ticker'])
        print("dow tickers done")

        # SP500 tickers
        #pd_sp500_tickers_full = si.tickers_sp500(include_company_data = True)
        #pd_sp500_tickers = pd_sp500_tickers_full[['Symbol','Security']]
        lst_sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        dict_sp500_tickers = {
            "Ticker": lst_sp500_tickers.Symbol,
            "Company": lst_sp500_tickers.Security
        }
        lst_sp500_tickers = lst_sp500_tickers['Symbol']
        pd_sp500_tickers = pd.DataFrame.from_dict(dict_sp500_tickers) 
        pd_sp500_tickers.set_index(['Ticker'])
        print("sp500 tickers done")

        # Nasdaq tickers
        pd_nasdaq_tickers_full = si.tickers_nasdaq(include_company_data = True)
        pd_nasdaq_tickers = pd_nasdaq_tickers_full[['Symbol','Security Name']]
        lst_nasdaq_tickers = pd_nasdaq_tickers['Symbol']
        pd_nasdaq_tickers.rename(columns={'Symbol': 'Ticker'}, inplace=True)
        pd_nasdaq_tickers.rename(columns={'Security Name': 'Company'}, inplace=True)
        pd_nasdaq_tickers.set_index(['Ticker'])
        pd_nasdaq_tickers.drop(index=pd_nasdaq_tickers.index[-1],axis=0,inplace=True)
        print("nasdaq tickers done")

        # Beursrally tickers
        lst_beursrally_tickers = ["MMM","AALB.AS","ABI.BR","ABT","ABBV","ABN.AS","AC.PA","ACKB.BR","ACOMO.AS","ADBE",\
                                 "AMD","ADYEN.AS","AED.BR","AGN.AS","AGS","AGFB.BR","AD.AS","AF.PA","AI.PA","ABNB",\
                                 "AIR.PA","AKZA.AS","ALFEN.AS","BABA","ALLFG.AS","CDA.PA","GOOGL","ALO.PA","AMZN","AXP",\
                                 "AMG","AMGN","BEL.BR","CACC.PA","MSE.MI","AUEM.L","ANX.PA","JPN.PA","ENER.MI","GOAI.PA",\
                                 "LCWD.MI","APAM","AAPL","ARCAD.AS","MT","ARGX","AKE.PA","ARM","ASC","ASM",\
                                 "ASML","ASRNL.AS","T","ATEB.BR","AVTX","CS.PA","0P00001B46.F","AZE.BR","BSGR.AS","BAMNB.AS",\
                                 "BAR","GOLD","BFIT","BESI.AS","BEKB.BR","BRK.B","BYND","BB","BIIB","BIM.PA",\
                                 "BTLS.BR","BIRK","0P00001BVE.F","0P00001AHF.F","0P00000S1P.F","GOOG","BNP.PA","0P00016F74.F","0P0000YSYV.F","0P00009GVS.F",\
                                 "BA","BOL.PA","BON.PA","BKNG","EN.PA","BPOST.BR","BNB.BR","BREB.BR","AVGO","BRNL.AS",\
                                 "CAP.PA","GOOG","GOOG","CPINV.BR","CCL","CA.PA","CAT","CFEB.BR","CVX","COMB.BR",\
                                 "CSCO","C","CLARI.PA","CMCOM.AS","CMBT.BR","KO","COFB.BR","COIN","CL","COLR.BR"]
        #lst_beursrally_names = []
        #for my_ticker in lst_beursrally_tickers:
        #    my_company = yf.Ticker(my_ticker).info.get("longName", "Company name not available")
        #    print(my_company)
        #    lst_beursrally_names.append(my_company)
        #print(lst_beursrally_names)
        lst_beursrally_names = ['3M Company', 'Aalberts N.V.', 'Anheuser-Busch InBev SA/NV', 'Abbott Laboratories', 'AbbVie Inc.', 'ABN AMRO Bank N.V.', 'Accor SA', 'Ackermans & Van Haaren NV', 'Acomo N.V.', 'Adobe Inc.',\
                                'Advanced Micro Devices, Inc.', 'Adyen N.V.', 'Aedifica NV/SA', 'Aegon Ltd.', 'PlayAGS, Inc.', 'Agfa-Gevaert NV', 'Koninklijke Ahold Delhaize N.V.', 'Air France-KLM SA', "L'Air Liquide S.A.", 'Airbnb, Inc.', \
                                'Airbus SE', 'Akzo Nobel N.V.', 'Alfen N.V.', 'Alibaba Group Holding Limited', 'Allfunds Group plc', 'Compagnie des Alpes SA', 'Alphabet Inc.', 'Alstom SA', 'Amazon.com, Inc.', 'American Express Company',\
                                'Affiliated Managers Group, Inc.', 'Amgen Inc.', 'Amundi BEL 20 UCITS ETF Dist', 'Amundi CAC 40 UCITS ETF Acc', 'Amundi EURO STOXX 50 II UCITS ETF Acc', 'Amundi Index Solutions - Amundi MSCI Emerging Markets UCITS ETF-C USD', 'Amundi Index Solutions - Amundi Nasdaq-100 ETF-C EUR', 'Amundi Japan TOPIX II UCITS ETF EUR Dist', 'Amundi MSCI New Energy ESG Screened UCITS ETF Dist', 'Amundi MSCI Robotics & AI ESG Screened UCITS ETF', \
                                'Amundi MSCI World V UCITS ETF', 'Artisan Partners Asset Management Inc.', 'Apple Inc.', 'Arcadis NV', 'ArcelorMittal S.A.', 'argenx SE', 'Arkema S.A.', 'Arm Holdings plc', 'Ardmore Shipping Corporation', 'Avino Silver & Gold Mines Ltd.',\
                                'ASML Holding N.V.', 'ASR Nederland N.V.', 'AT&T Inc.', 'Atenor SA', 'Avalo Therapeutics, Inc.', 'AXA SA', 'AXAWF Switzerland Eq A Cap EUR', 'Azelis Group NV', 'B&S Group S.A.', 'Koninklijke BAM Groep nv', \
                                'GraniteShares Gold Trust', 'Barrick Gold Corporation', 'Global X Health & Wellness ETF', 'BE Semiconductor Industries N.V.', 'NV Bekaert SA', 'Berkshire Hathaway', 'Beyond Meat, Inc.', 'BlackBerry Limited', 'Biogen Inc.', 'bioMérieux S.A.',\
                                'Biotalys NV', 'Birkenstock Holding plc', 'BL-Global Flexible EUR', 'BGF Continental Eurp Flex A2 EUR', 'BGF ESG Multi-Asset A2 EUR', 'Alphabet Inc.', 'BNP Paribas SA', 'BNP Paribas Aqua C C', 'BNP Paribas Disrpt Tech Cl C', 'BNY Mellon Brazil Equity EUR A Acc', \
                                'The Boeing Company', 'Bolloré SE', 'Bonduelle SCA', 'Booking Holdings Inc.', 'Bouygues SA', 'bpost NV/SA', 'Banque nationale de Belgique SA', 'Brederode SA', 'Broadcom Inc.', 'Brunel International N.V.', 'Capgemini SE', 'Alphabet Inc.', 'Alphabet Inc.', 'Care Property Invest NV', 'Carnival Corporation & plc', 'Carrefour SA', 'Caterpillar Inc.', "Compagnie d'Entreprises CFE SA", 'Chevron Corporation', 'Compagnie du Bois Sauvage S.A.',\
                                'Cisco Systems, Inc.', 'Citigroup Inc.', 'Clariane SE', 'CM.com N.V.', 'Cmb.Tech NV', 'The Coca-Cola Company', 'Cofinimmo SA', 'Coinbase Global, Inc.', 'Colgate-Palmolive Company', 'Colruyt Group N.V.']
        dict_beursrally_tickers = {
            "Ticker": lst_beursrally_tickers,
            "Company": lst_beursrally_names
        }
        pd_beursrally_tickers = pd.DataFrame.from_dict(dict_beursrally_tickers) 
        pd_beursrally_tickers.set_index(['Ticker'])
        print("beursrally tickers done")

        # Precious metals
        dict_precious_metals_tickers = {
            "Ticker": [ "GC=F","SI=F","PA=F","PL=F" ],
            "Company":  [ "Gold","Silver","Palladium","Platinum" ]
        }
        pd_precious_metals_tickers =  pd.DataFrame.from_dict(dict_precious_metals_tickers) 
        lst_precious_metals_tickers = pd_precious_metals_tickers['Ticker'] 
        pd_precious_metals_tickers.set_index(['Ticker'])
        print("precious metals tickers done")

        # Exchange rates
        dict_exchange_rates_tickers = {
            "Ticker": [ "EURUSD=X","EURJPY=X","EURRUB=X" ],
            "Company": [ "US Dollar", "Japanese Yen", "Russian Rouble"]
        }
        pd_exchange_rates_tickers = pd.DataFrame.from_dict(dict_exchange_rates_tickers)  
        lst_exchange_rates_tickers = pd_exchange_rates_tickers['Ticker']
        pd_exchange_rates_tickers.set_index(['Ticker'])
        print(pd_exchange_rates_tickers)
        print("exchange rates tickers done")       

        # Oil
        dict_oil_tickers = {
            "Ticker": [ "CL=F" ],
            "Company": [ "Crude oil" ]
        }
        pd_oil_tickers = pd.DataFrame.from_dict(dict_oil_tickers)
        lst_oil_tickers = pd_oil_tickers['Ticker']
        pd_oil_tickers.set_index(['Ticker'])
        print(pd_oil_tickers)
        print("oil tickers done")    

        # Crypto
        dict_crypto_tickers = {
            "Ticker": ["BTC-USD","ETH-USD","BNB-USD","XRP-USD","SOL-USD","ADA-USD","DOGE-USD","LINK-USD","DOT-USD","SHIB-USD"],
            "Company": [ "Bitcoin","Ethereum","Binance Coin","Ripple","Solana","Cardano","Dogecoin","Chainlink","Polkadot","Shibu Inu"]
        }
        pd_crypto_tickers = pd.DataFrame.from_dict(dict_crypto_tickers)  
        lst_crypto_tickers = pd_crypto_tickers['Ticker']
        pd_crypto_tickers.set_index(['Ticker'])
        print(pd_crypto_tickers)
        print("crypto tickers done")    

        # Other tickers
        dict_other_tickers = {
            "Ticker": [ "VUSA.AS" ],
            "Company": [ "Vanguard S&P 500 UCITS ETF" ]
        }
        pd_other_tickers = pd.DataFrame.from_dict(dict_other_tickers)  
        lst_other_tickers = pd_other_tickers['Ticker']
        pd_other_tickers.set_index(['Ticker'])
        print("other tickers done")


        # Concat and remove duplicates
        print("before concat")
        pd_all_tickers = pd.concat([pd_screener_tickers, pd_dow_tickers, pd_sp500_tickers, pd_nasdaq_tickers, pd_beursrally_tickers, pd_precious_metals_tickers, pd_exchange_rates_tickers, pd_oil_tickers, pd_crypto_tickers, pd_other_tickers])
        print("after concat")
        pd_all_tickers = pd_all_tickers.drop_duplicates(subset='Ticker')
        pd_alltemp_tickers = pd_all_tickers[pd_all_tickers['Ticker'] != 'BRK.B']
        pd_final_tickers = pd_alltemp_tickers[pd_alltemp_tickers['Ticker'] != 'BF.B']

        print(pd_final_tickers)

        # Mark tickers
        pd_final_tickers = pd_final_tickers.copy()
        print("before loop")
        for index, row in pd_final_tickers.iterrows():
            #print("loop")
            for my_ticker in lst_screener_tickers:
                #print("loop")
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "Screener"] = 1
            for my_ticker in lst_dow_tickers:
                #print("loop dow")
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "Dow"] = 1
            for my_ticker in lst_sp500_tickers:
                #print("loop sp500")
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "SP500"] = 1
            for my_ticker in lst_nasdaq_tickers:
                #print("loop nasdaq")
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "Nasdaq"] = 1
            for my_ticker in lst_beursrally_tickers:
                #print("loop beursrally " + my_ticker)
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "Beursrally"] = 1
            for my_ticker in lst_precious_metals_tickers:
                #print("loop metals)")
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "PreciousMetals"] = 1
            for my_ticker in lst_exchange_rates_tickers:
                #print("loop exhchange")
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "ExchangeRates"] = 1
            for my_ticker in lst_oil_tickers:
                #print("loop oil")
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "Oil"] = 1
            for my_ticker in lst_crypto_tickers:
                #print("loop crypto")
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "Crypto"] = 1
            for my_ticker in lst_other_tickers:
                #print("loop other")
                if my_ticker == row['Ticker']:
                    pd_final_tickers.loc[pd_final_tickers['Ticker'] == my_ticker, "Other"] = 1

        pd_final_tickers.to_sql('_yahoo_fin_tickers', con=conn_tickers, if_exists='replace')
        conn_tickers.close()
        print("all done")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()