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
        lst_beursrally_tickers_all = ["MMM","AALB.AS","ABI.BR","ABT","ABBV","ABN.AS","AC.PA","ACKB.BR","ACOMO.AS","ADBE",\
                                 "AMD","ADYEN.AS","AED.BR","AGN.AS","AGS","AGFB.BR","AD.AS","AF.PA","AI.PA","ABNB",\
                                 "AIR.PA","AKZA.AS","ALFEN.AS","BABA","ALLFG.AS","CDA.PA","GOOGL","ALO.PA","AMZN","AXP",\
                                 "AMG","AMGN","BEL.BR","CACC.PA","MSE.MI","AUEM.L","ANX.PA","JPN.PA","ENER.MI","GOAI.PA",\
                                 "LCWD.MI","APAM","AAPL","ARCAD.AS","MT","ARGX","AKE.PA","ARM","ASC","ASM",\
                                 "ASML","ASRNL.AS","T","ATEB.BR","AVTX","CS.PA","0P00001B46.F","AZE.BR","BSGR.AS","BAMNB.AS",\
                                 "BAR","GOLD","BFIT","BESI.AS","BEKB.BR","BRK.B","BYND","BB","BIIB","BIM.PA",\
                                 "BTLS.BR","BIRK","0P00001BVE.F","0P00001AHF.F","0P00000S1P.F","GOOG","BNP.PA","0P00016F74.F","0P0000YSYV.F","0P00009GVS.F",\
                                 "BA","BOL.PA","BON.PA","BKNG","EN.PA","BPOST.BR","BNB.BR","BREB.BR","AVGO","BRNL.AS",\
                                 "CAP.PA","GOOG","GOOG","CPINV.BR","CCL","CA.PA","CAT","CFEB.BR","CVX","COMB.BR",\
                                 "CSCO","C","CLARI.PA","CMCOM.AS","CMBT.BR","KO","COFB.BR","COIN","CL","COLR.BR",\
                                 "CMCSA","0P00000LM7.F","CRBN.AS","ACA.PA","--------","CTPNV.AS","BN.PA","DSY.PA","DECB.BR","DEME.BR",\
                                 "DIE.BR","0P0000XTFD.F","----------","0P00000HCB.F","DSFIR.AS","-----","EBAY","EBUS.AS","ECONB.BR","EDEN.PA",\
                                 "EKOP.BR","EA","LLY","ELI.BR","ENGI.PA","EL.PA","RF.PA","ECMPA.AS","ERF.PA","ENX.PA",\
                                 "EVS.BR","EXM.BR","EXO.AS","XOM","FAGR.BR","FAST.AS","-------","-------","-------","-------",\
                                 "------","FLOW.AS","FLUX.BR","FFARM.AS","----------","0P0000FTZO.F","----","FUR.AS","0P0000W76V.F","GLPG",\
                                 "GME","GBLB.BR","GE","GEN","GM","GNFT","GILD","GIMB.BR","0P00001D6S.F","----------",\
                                 "GS","0P00000BFO.F","-------","---------","GREEN.BR","HAL.AS","HEIJM.AS","HEIA.AS","------","HD",\
                                 "HOMI.BR","HON","0P0000191J.F","HYL.BR","IBAB.BR","-----------","NK.PA","IMMO.BR","INGA.AS","INPST.AS",\
                                 "INTC","IBM","0P00005Z2C.F","----------","----------","IAEX.AS","---------","---------","IEMM.AS","ITOS",\
                                 "--------","JDEP.AS","JEN.BR","JNJ","JPM","-----","-----","TKWY.AS","KBC.BR","KBCA.BR",\
                                 "KENDR.AS","KER.PA","KIN.BR","LI.PA","KPN.AS","KHC","KWEB","LR.PA","LBTYA","OR.PA",\
                                 "LOTB.BR","LCID","MC.PA","0P0001DFOO.F","MTU.PA","MA","MTLS","MCD","MELE.BR","MRK",\
                                 "META","0P00000HNU.F","ML.PA","MSFT","MSTR","MRNA","MDLZ","MNST","MONT.BR","NFLX",\
                                 "NEM","NEX.PA","NEXTA.BR","NKE","NN.AS","NOK","NCLH","NSI.AS","NVDA","NYXH.BR",\
                                 "OCI.AS","OSPN","ONTEX.BR","ONWD.BR","OPM.PA","ORCL","OBEL.BR","PLTR","PYPL",\
                                 "PEP","RI.PA","PEUG.PA","PFE","PM","PHG","0P00007WAK.F","0P0000HX95.F","0P0000X9NY.F","PINS",\
                                 "PNL.AS","PG","PRX.AS","PROX.BR","PUB.PA","QRF.BR","QCOM","QFG.BR","RAND.AS","RECT.BR",\
                                 "REGN","RELX","RCO.PA","RNO.PA","RET.BR","0P00000C1B.F","0P00000C2K.F","0P0000PU5O.F","0P00000C2O.F","0P0000UVXR.F",\
                                 "ROU.BR","RTX","SK.PA","SAF.PA","SGO.PA","CRM","SAN.PA","SBMO.AS","SLB","SU.PA",\
                                 "0P00001SDO.F","---------","0P0000G13X.F","STX","SCHP.PA","SHEL","SHUR.BR","SIFG.AS","LIGHT.AS","SIP.BR",\
                                 "SLIGR.AS","SMAR.BR","SNAP","GLE.PA","SW.PA","SOF.BR","SOLB.BR","LUV","SBUX","STLA",\
                                 "STM","SYENS.BR","-----","TEP.PA","TSLA","TESB.BR","TEXF.BR","TXN","HO.PA","TINC.BR",\
                                 "TWEKA.AS","TOM2.AS","TTE.PA","TRV","TRI.PA","0P0000Q5N2.F","TUB.BR","UBER","UBI.PA","UCB.BR",\
                                 "UMG.AS","UMI.BR","URW.PA","UL","UNH","VLK.AS","FR.PA","VK.PA","VAN.BR","VUSA.AS",\
                                 "VASTN.AS","VASTB.BR","VIE.PA","VRLA.PA","VZ","VGP.BR","DG.PA","V","VVY.AS","VPK.AS",\
                                 "VRAP.PA","WBA","WMT","DIS","WEB.BR","WDP.BR","MF.PA","WHA.AS","WEHB.BR","WDC",\
                                 "WHATS.BR","BRNT.MI","WCBR.MI","WKL.AS","WLN.PA","XFAB.PA","XIOR.BR"]
        #print(lst_beursrally_tickers_all)
        lst_beursrally_tickers = [item for item in lst_beursrally_tickers_all if "-" not in item]
        #print(lst_beursrally_tickers)

        lst_beursrally_names = []
        # for my_ticker in lst_beursrally_tickers:
        #     my_company = yf.Ticker(my_ticker).info.get("longName", "no name available")
        #    #print(my_company)
        #     lst_beursrally_names.append(my_company)
        # print(lst_beursrally_names)
        lst_beursrally_names = ['3M Company', 'Aalberts N.V.', 'Anheuser-Busch InBev SA/NV', 'Abbott Laboratories', 'AbbVie Inc.', 'ABN AMRO Bank N.V.', 'Accor SA', 'Ackermans & Van Haaren NV', 'Acomo N.V.', 'Adobe Inc.',\
                                'Advanced Micro Devices, Inc.', 'Adyen N.V.', 'Aedifica NV/SA', 'Aegon Ltd.', 'PlayAGS, Inc.', 'Agfa-Gevaert NV', 'Koninklijke Ahold Delhaize N.V.', 'Air France-KLM SA', "L'Air Liquide S.A.", 'Airbnb, Inc.', \
                                'Airbus SE', 'Akzo Nobel N.V.', 'Alfen N.V.', 'Alibaba Group Holding Limited', 'Allfunds Group plc', 'Compagnie des Alpes SA', 'Alphabet Inc.', 'Alstom SA', 'Amazon.com, Inc.', 'American Express Company',\
                                'Affiliated Managers Group, Inc.', 'Amgen Inc.', 'Amundi BEL 20 UCITS ETF Dist', 'Amundi CAC 40 UCITS ETF Acc', 'Amundi EURO STOXX 50 II UCITS ETF Acc', 'Amundi Index Solutions - Amundi MSCI Emerging Markets UCITS ETF-C USD', 'Amundi Index Solutions - Amundi Nasdaq-100 ETF-C EUR', 'Amundi Japan TOPIX II UCITS ETF EUR Dist', 'Amundi MSCI New Energy ESG Screened UCITS ETF Dist', 'Amundi MSCI Robotics & AI ESG Screened UCITS ETF', \
                                'Amundi MSCI World V UCITS ETF', 'Artisan Partners Asset Management Inc.', 'Apple Inc.', 'Arcadis NV', 'ArcelorMittal S.A.', 'argenx SE', 'Arkema S.A.', 'Arm Holdings plc', 'Ardmore Shipping Corporation', 'Avino Silver & Gold Mines Ltd.',\
                                'ASML Holding N.V.', 'ASR Nederland N.V.', 'AT&T Inc.', 'Atenor SA', 'Avalo Therapeutics, Inc.', 'AXA SA', 'AXAWF Switzerland Eq A Cap EUR', 'Azelis Group NV', 'B&S Group S.A.', 'Koninklijke BAM Groep nv', \
                                'GraniteShares Gold Trust', 'Barrick Gold Corporation', 'Global X Health & Wellness ETF', 'BE Semiconductor Industries N.V.', 'NV Bekaert SA', 'Berkshire Hathaway', 'Beyond Meat, Inc.', 'BlackBerry Limited', 'Biogen Inc.', 'bioMérieux S.A.',\
                                'Biotalys NV', 'Birkenstock Holding plc', 'BL-Global Flexible EUR', 'BGF Continental Eurp Flex A2 EUR', 'BGF ESG Multi-Asset A2 EUR', 'Alphabet Inc.', 'BNP Paribas SA', 'BNP Paribas Aqua C C', 'BNP Paribas Disrpt Tech Cl C', 'BNY Mellon Brazil Equity EUR A Acc', \
                                'The Boeing Company', 'Bolloré SE', 'Bonduelle SCA', 'Booking Holdings Inc.', 'Bouygues SA', 'bpost NV/SA', 'Banque nationale de Belgique SA', 'Brederode SA', 'Broadcom Inc.', 'Brunel International N.V.', 'Capgemini SE', 'Alphabet Inc.', 'Alphabet Inc.', 'Care Property Invest NV', 'Carnival Corporation & plc', 'Carrefour SA', 'Caterpillar Inc.', "Compagnie d'Entreprises CFE SA", 'Chevron Corporation', 'Compagnie du Bois Sauvage S.A.',\
                                'Cisco Systems, Inc.', 'Citigroup Inc.', 'Clariane SE', 'CM.com N.V.', 'Cmb.Tech NV', 'The Coca-Cola Company', 'Cofinimmo SA', 'Coinbase Global, Inc.', 'Colgate-Palmolive Company', 'Colruyt Group N.V.', 'Comcast Corporation', 'Comgest Growth Europe EUR Acc', 'Corbion N.V.', 'Crédit Agricole S.A.', 'CTP N.V.', 'Danone S.A.', 'Dassault Systèmes SE', 'Deceuninck NV', 'DEME Group NV', "D'Ieteren Group SA", 'DNCA Invest SRI Europe Growth', 'DPAM B Equities Eur Sust B € Cap', 'DSM-Firmenich AG', 'eBay Inc.', 'Ebusco Holding N.V.', 'Econocom Group SE', 'Edenred SE', 'Ekopak NV', 'Electronic Arts Inc.', \
                                'Eli Lilly and Company', 'Elia Group SA/NV', 'Engie SA', 'EssilorLuxottica Société anonyme', 'Eurazeo SE', 'Eurocommercial Properties N.V.', 'Eurofins Scientific SE', 'Euronext N.V.', 'EVS Broadcast Equipment SA', 'Exmar NV', 'Exor N.V.',\
                                'Exxon Mobil Corporation', 'Fagron NV', 'Fastned B.V.', 'Flow Traders Ltd.', 'Fluxys Belgium SA', 'ForFarmers N.V.', 'Franklin MENA A(acc)EUR', 'Fugro N.V.', 'Fundsmith Equity R EUR Acc', 'Galapagos NV', 'GameStop Corp.', 'Groupe Bruxelles Lambert SA',\
                                'GE Aerospace', 'Gen Digital Inc.', 'General Motors Company', 'Genfit S.A.', 'Gilead Sciences, Inc.', 'Gimv NV', 'Goldman Sachs Europe CORE Equity Portfolio Base Acc EUR', 'The Goldman Sachs Group, Inc.', 'Goldman Sachs Patrimonial Aggressive', \
                                'Greenyard NV', 'HAL Trust', 'Koninklijke Heijmans N.V.', 'Heineken N.V.', 'The Home Depot, Inc.', 'Home Invest Belgium S.A.', 'Honeywell International Inc.', 'HSBC GIF Turkey Equity AC', 'Hyloris Pharmaceuticals SA', 'Ion Beam Applications SA', \
                                'Imerys S.A.', 'Immobel SA', 'ING Groep N.V.', 'InPost S.A.', 'Intel Corporation', 'International Business Machines Corporation', 'Invesco Funds - Invesco Pan European High Income Fund', 'iShares AEX UCITS ETF EUR (Dist)', \
                                'iShares MSCI EM UCITS ETF USD (Dist)', 'iTeos Therapeutics, Inc.', "JDE Peet's N.V.", 'Jensen-Group NV', 'Johnson & Johnson', 'JPMorgan Chase & Co.', 'Just Eat Takeaway.com N.V.', 'KBC Group NV', 'KBC Ancora SA', 'Kendrion N.V.',\
                                'Kering SA', 'Kinepolis Group NV', 'Klépierre SA', 'Koninklijke KPN N.V.', 'The Kraft Heinz Company', 'KraneShares CSI China Internet ETF', 'Legrand SA', 'Liberty Global Ltd.', "L'Oréal S.A.", 'Lotus Bakeries NV', 'Lucid Group, Inc.',\
                                'LVMH Moët Hennessy - Louis Vuitton, Société Européenne', 'M&G (Lux) Japan A EUR Acc', 'Manitou BF SA', 'Mastercard Incorporated', 'Materialise NV', "McDonald's Corporation", 'Melexis NV', 'Merck & Co., Inc.', 'Meta Platforms, Inc.', 'MFS Meridian European Research A1 EUR',\
                                'Compagnie Générale des Établissements Michelin Société en commandite par actions', 'Microsoft Corporation', 'MicroStrategy Incorporated', 'Moderna, Inc.', 'Mondelez International, Inc.', 'Monster Beverage Corporation', 'Montea Comm. VA', 'Netflix, Inc.', 'Newmont Corporation',\
                                'Nexans S.A.', 'Nextensa NV/SA', 'NIKE, Inc.', 'NN Group N.V.', 'Nokia Oyj', 'Norwegian Cruise Line Holdings Ltd.', 'NSI N.V.', 'NVIDIA Corporation', 'Nyxoah S.A.', 'OCI N.V.', 'OneSpan Inc.', 'Ontex Group NV', 'Onward Medical N.V.', 'OPmobility SE', 'Oracle Corporation',\
                                'Orange Belgium S.A.', 'Palantir Technologies Inc.', 'PayPal Holdings, Inc.', 'PepsiCo, Inc.', 'Pernod Ricard SA', 'Peugeot Invest Société anonyme', 'Pfizer Inc.', 'Philip Morris International Inc.', 'Koninklijke Philips N.V.', 'Pictet - Biotech P EUR', 'Pictet-Timber P EUR',\
                                'PIMCO GIS Income Fund E Class EUR (Hedged) Accumulation', 'Pinterest, Inc.', 'PostNL N.V.', 'The Procter & Gamble Company', 'Prosus N.V.', 'Proximus PLC', 'Publicis Groupe S.A.', 'Qrf Comm. VA', 'QUALCOMM Incorporated', 'Quest for Growth NV', 'Randstad N.V.', 'Recticel SA/NV',\
                                'Regeneron Pharmaceuticals, Inc.', 'RELX PLC', 'Rémy Cointreau SA', 'Renault SA', 'Retail Estates N.V.', 'Robeco Emerging Markets Equities D €', 'Robeco Global Consumer Trends D EUR', 'Robeco Indian Equities D €', 'Robeco New World Financials D €',\
                                'Robeco QI Global Conservative Eqs D €', 'Roularta Media Group NV', 'RTX Corporation', 'SEB SA', 'Safran SA', 'Compagnie de Saint-Gobain S.A.', 'Salesforce, Inc.', 'Sanofi', 'SBM Offshore N.V.', 'Schlumberger Limited', 'Schneider Electric S.E.', \
                                'Schroder ISF Emerging Asia A Acc EUR', 'Schroder ISF Greater China A Acc EUR', 'Seagate Technology Holdings plc', 'Séché Environnement SA', 'Shell plc', 'Shurgard Self Storage Ltd', 'Sif Holding N.V.', 'Signify N.V.', 'Sipef NV', 'Sligro Food Group N.V.', \
                                'Smartphoto Group NV', 'Snap Inc.', 'Société Générale Société anonyme', 'Sodexo S.A.', 'Sofina Société Anonyme', 'Solvay SA', 'Southwest Airlines Co.', 'Starbucks Corporation', 'Stellantis N.V.', 'STMicroelectronics N.V.', 'Syensqo SA/NV', 'Teleperformance SE',\
                                'Tesla, Inc.', 'Tessenderlo Group NV', 'Texaf S.A.', 'Texas Instruments Incorporated', 'Thales S.A.', 'TINC NV', 'TKH Group N.V.', 'TomTom N.V.', 'TotalEnergies SE', 'The Travelers Companies, Inc.', 'Trigano S.A.', 'Triodos Impact Mixed Neutral EUR R Acc',\
                                'Financière de Tubize SA', 'Uber Technologies, Inc.', 'Ubisoft Entertainment SA', 'UCB SA', 'Universal Music Group N.V.', 'Umicore SA', 'Unibail-Rodamco-Westfield SE', 'Unilever PLC', 'UnitedHealth Group Incorporated', 'Van Lanschot Kempen NV', 'Valeo SE', \
                                'Vallourec S.A.', 'Van de Velde NV', 'Vanguard S&P 500 UCITS ETF', 'Vastned Retail N.V.', 'Vastned Belgium NV', 'Veolia Environnement SA', 'Verallia Société Anonyme', 'Verizon Communications Inc.', 'VGP NV', 'Vinci SA', 'Visa Inc.', 'Vivoryon Therapeutics N.V.',\
                                'Koninklijke Vopak N.V.', 'Vranken-Pommery Monopole Société Anonyme', 'Walgreens Boots Alliance, Inc.', 'Walmart Inc.', 'The Walt Disney Company', 'Warehouses Estates Belgium S.C.A.', 'Warehouses De Pauw SA', 'Wendel', 'Wereldhave N.V.', 'Wereldhave Belgium',\
                                'Western Digital Corporation', "What's Cooking Group NV/SA", 'WisdomTree Brent Crude Oil', 'WisdomTree Cybersecurity UCITS ETF USD Acc', 'Wolters Kluwer N.V.', 'Worldline SA', 'X-FAB Silicon Foundries SE', 'Xior Student Housing NV']
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