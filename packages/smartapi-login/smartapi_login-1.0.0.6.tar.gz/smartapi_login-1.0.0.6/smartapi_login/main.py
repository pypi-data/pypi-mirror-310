# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 11:02:25 2024

@author: Mahesh_Kumar
"""


import subprocess
import sys

# List of libraries to check
required_libraries = [
    'pandas',
    'requests',
    'pytz',
    'pyotp',
]

def install_libraries(libraries):
    """Install libraries using pip if they are not already installed"""
    for library in libraries:
        try:
            __import__(library)
        except ImportError:
            print(f"Library {library} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# Install required libraries
install_libraries(required_libraries)


import pandas as pd
import requests
import time
from datetime import timedelta, date, datetime
from pytz import timezone
from SmartApi import SmartConnect
import pyotp
import json
from cachetools import TTLCache




class SmartAPIHelper:
    _cache = TTLCache(maxsize=20000, ttl=60 * 60)  # Cache 20000 entries for 1 hour

    
    def __init__(self):
        # Initialization code, this can be used to set default values or load from files
        self.api_key_hist = None
        self.api_key_trading = None
        self.uid = None
        self.mpin = None
        self.totp = None
        self.obj=None
        self.obj_trading=None
        self.instrument_df=None
        



    def run(self):
        print("Initializing sessions...")
        self.initialize_sessions()
        print("Fetching data...")
        df = self.get_tradingsymbols()
        print("Processing complete.")


    def login(self, api_key_hist, api_key_trading, uid, mpin, totp):        
        """
        Takes user input for credentials if they are not provided.
        These credentials will not be saved permanently.
        """
        self.api_key_hist = api_key_hist  # Use iloc for position-based access
        self.api_key_trading = api_key_trading
        self.uid = uid
        self.mpin = mpin
        self.totp = totp
        
        print("Login successful! Credentials will not be saved.")
  
    
    def fetch_instrument_df(self):
        
        if self.instrument_df is None:            
            url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
                data = response.json()
                instrument_df = pd.DataFrame(data)
                self.instrument_df=instrument_df
                
               
        
            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve data. Error: {e}")
                return None
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON. Error: {e}")
                return None
        return self.instrument_df
               
        

    def _get_historical_data_session(self):
        if self.obj is None:            
            obj = SmartConnect(api_key=self.api_key_hist)
            data = obj.generateSession(self.uid, self.mpin, pyotp.TOTP(self.totp).now())
            hist_data_refreshToken = data['data']['refreshToken']
            hist_data_feedToken = obj.getfeedToken()
            self.obj=obj
        return self.obj

    def _get_trading_api_session(self):
        if self.obj_trading is None:            
            obj_trading = SmartConnect(api_key=self.api_key_trading)
            trading_data = obj_trading.generateSession(self.uid, self.mpin, pyotp.TOTP(self.totp).now())
            trading_refreshToken = trading_data['data']['refreshToken']
            trading_feedToken = obj_trading.getfeedToken()
            self.obj_trading=obj_trading
        return self.obj_trading

 

    def initialize_sessions(self):
        try:
            obj = self._get_historical_data_session()
            obj_trading = self._get_trading_api_session()
            
            return obj,obj_trading
            
        except Exception as e:
            print("An error occurred during session initialization:", str(e))
        
        pass
        

    def get_ltp(self,symbol):
        try:     
            obj=self._get_historical_data_session()
            Instrument_df=self.fetch_instrument_df()
            token = Instrument_df.loc[Instrument_df['symbol'] == symbol, 'token'].values[0]
            exch_seg = Instrument_df.loc[Instrument_df['symbol'] == symbol, 'exch_seg'].values[0]
            price = obj.ltpData(exch_seg, symbol, token)
            ltp = price['data']['ltp']
            time.sleep(0.5)
            return ltp
            
        except Exception as e:
            print("An error occurred:", str(e))
            return None

        

    def get_ohlc(self, symbol, interval, n):
        obj = self._get_historical_data_session()
        instrument_df = self.fetch_instrument_df()
    
        # token, exch_seg = instrument_df.loc[symbol, ['token', 'exch_seg']]
        token = instrument_df.loc[((instrument_df['symbol'] == symbol), 'token')].values[0]
        exch_seg = instrument_df.loc[(instrument_df['symbol'] == symbol), 'exch_seg'].values[0]

    
        try:
            historic_param = {
                "exchange": exch_seg,
                "symboltoken": token,
                "interval": interval,
                "fromdate": f"{date.today() - timedelta(days=n)} 09:15",
                "todate": f"{date.today() - timedelta(days=0)} 15:30"
            }
    
            col = ['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
            ohlc = obj.getCandleData(historic_param)['data']
            data = pd.DataFrame(ohlc, columns=col, index=None)
            data['timestamp'] = pd.to_datetime(data['timestamp'], format='mixed')
    
            data['symbol'] = symbol
            time.sleep(0.7)
    
            return data
    
        except requests.exceptions.RequestException as e:  # Catch network-related errors
            print(f"Historic API failed: Network issue or bad response - {str(e)}")
            return None  # Or return an error object
    
        except Exception as e:  # Catch other unexpected errors
            print(f"Unexpected error during historical data retrieval: {str(e)}")
            return None  # Or return an error object

   