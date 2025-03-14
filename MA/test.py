
import concurrent.futures
# from some_ta_module import TA_Handler  # Replace with actual import
import pandas as pd
import time 
from tradingview_ta import TA_Handler, Interval, Exchange
import smtplib
from datetime import datetime
from datetime import datetime
import os
import pywhatkit as kit
import pyautogui
import pyperclip

stock_symbols = [
    "RELIANCE", "HDFCBANK", "ICICIBANK", "ITC", "INFY", "SBIN", "BHARTIARTL", "BAJFINANCE",
    "AXISBANK", "BAJAJFINSV", "NTPC", "TATAMOTORS", "ONGC", "JSWSTEEL", "COALINDIA",
    "WIPRO", "POWERGRID", "ADANIPOWER", "VBL", "DLF", "TATASTEEL", "IOC", "JIOFIN",
    "HINDALCO", "BEL", "HINDZINC", "IRFC", "PFC", "INDUSINDBK", "BANKBARODA", "GODREJCP",
    "RECLTD", "ZOMATO", "TATAPOWER", "GAIL", "PNB", "DABUR", "BPCL", "VEDL", "UNIONBANK",
    "IOB", "CANBK", "IDEA", "JINDALSTEL", "IDBI", "SBICARD", "IRCTC", "CGPOWER", "MOTHERSON",
    "BHEL", "JSWENERGY", "NHPC", "IDFCFIRSTB", "YESBANK", "NMDC", "MUTHOOTFIN", "PATANJALI",
    "HINDPETRO", "INDUSTOWER", "ASHOKLEY", "BANKINDIA", "SUZLON", "SAIL", "UCOBANK", "NYKAA",
    "GMRINFRA", "AWL", "CENTRALBK", "JSWINFRA", "ABCAPITAL", "OIL", "PAYTM", "BANDHANBNK",
    "FEDERALBNK", "RVNL", "KALYANKJIL", "SJVN", "NLCINDIA", "POONAWALLA", "MAHABANK",
    "LICHSGFIN", "BIOCON", "PSB", "IREDA", "EXIDEIND", "MSUMI", "ZEEL", "HINDCOPPER",
    "HUDCO", "IRB", "NATIONALUM", "DEVYANI", "IIFL", "ABFRL", "PEL", "PNBHOUSING", "IDFC",
    "BSOFT", "CDSL", "TRIDENT", "PPLPHARMA", "TTML", "CASTROLIND", "CESC", "RBLBANK",
    "KAYNES", "INOXWIND", "SHYAMMETL", "IRCON", "APTUS", "KIMS", "NSLNISP", "IEX", "NBCC",
    "MANAPPURAM", "HONASA", "WELSPUNLIV", "TRITURBINE", "BLS", "FSL", "HFCL", "SYRMA",
    "EQUITASBNK", "UJJIVANSFB", "CUB", "RAILTEL", "GODREJAGRO", "ALOKINDS", "RTNINDIA",
    "CANFINHOME", "SWSOLAR", "RENUKA", "GRANULES", "JKTYRE", "ENGINERSIN", "ANANTRAJ",
    "JPPOWER", "JMFINANCIL", "PRSMJOHNSN", "NETWORK18", "MMTC", "RPOWER", "RCF", "TV18BRDCST",
    "JUBLPHARMA", "CAMPUS", "RELINFRA", "HOMEFIRST", "ALLCARGO", "EDELWEISS", "MARKSANS",
    "IFCI", "EASEMYTRIP", "ELECTCAST", "FDC", "PGEL", "INFIBEAM", "STLTECH", "NAZARA",
    "PTC", "SOUTHBANK", "PARADEEP", "ORIENTCEM", "RAIN", "RTNPOWER", "LLOYDSENGG", "PATELENG",
    "TI", "JAMNAAUTO", "HCC", "JISLJALEQS", "PAISALO", "TIMETECHNO", "ASHOKA", "BCG",
    "HATHWAY", "BAJAJHIND", "SAKSOFT", "DISHTV", "YATHARTH", "INOXGREEN", "IMAGICAA",
    "SEPC", "SEQUENT", "ISMTLTD", "DEN", "ZAGGLE", "IOLCP", "PFS", "MOREPENLAB",
    "REPCOHOME", "TCNSBRANDS", "DHANI", "CAMLINFINE", "SDBL", "FILATEX", "PCJEWELLER",
    "SADHNANIQ", "GREENPOWER", "MTNL", "SHRIRAMPPS", "SALASAR", "PARACABLES", "JAGRAN",
    "VAKRANGEE", "SUBEXLTD", "GEOJITFSL", "GOKULAGRO", "GOLDIAM", "RAMASTEEL", "UNITECH",
    "BCLIND", "DCW", "GTLINFRA", "SERVOTECH", "HITECH", "SPIC", "MVGJL", "KABRAEXTRU",
    "HARDWYN", "SYNCOMF", "INDORAMA", "REFEX", "BLISSGVS", "JYOTISTRUC", "KOPRAN",
    "GICHSGFIN", "KAMOPAINTS", "SMCGLOBAL", "SNOWMAN", "STEELXIND", "KAMDHENU", "MOTISONS",
    "ZEEMEDIA", "MSPL", "TBZ", "URJA", "MICEL", "ESTER", "NECLIFE", "VIKASLIFE", "FCSSOFT",
    "OSWALGREEN", "AXITA", "CELLECOR", "SBC", "SARVESHWAR", "RADHIKAJWE", "ASMS", "VIKASECO",
    "SAKUMA", "SADBHAV", "ESSENTIA", "PILITA", "KRITIKA", "RAJMET", "INVENTURE", "RHFL",
    "KBCGLOBAL", "VISESHINFO", "FCONSUMER", "TIRUPATIFL", "GTL", "PATINTLOG", "TPHQ",
    "BIOFILCHEM", "SITINET", "GLOBE", "EXCEL", "AJOONI", "SRPL", "GODHA", "GATECH",
    "ANTGRAPHIC", "GAYAPROJ"
]




for i in stock_symbols:
            handler = TA_Handler(
            symbol=i,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY,
        )
            indicators = handler.get_analysis().indicators
            # print(indicators)
            sma10 = indicators['SMA10']
            high_5_percent = sma10 * 1.05  # 5% high
            low_5_percent = sma10 * 0.95   # 5% low

            current_price = indicators['close']
            if current_price > high_5_percent:
                    print(f'high : {i}') 

            if current_price < low_5_percent:
                    print(f'low : {i}')           
            
