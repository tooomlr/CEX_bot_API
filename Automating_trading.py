
import os
from binance.client import Client
import requests
import json
import sqlite3


api_key = ""
api_secret = ""


# SQLite database connection
conn = sqlite3.connect('trading.db')
c = conn.cursor()

#Get a list of all available cryptocurrencies.
def ListPair():
    client = Client(api_key, api_secret)
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
        print(s['symbol'])

ListPair()
#Create a function to display the 'ask' or bid price of an asset.

#def getDepth():
    
#Get order book for an asset
def getOrderBook():
    client = Client(api_key, api_secret)
    depth = client.get_order_book(symbol='BTCUSDT')
    print (depth)
getOrderBook()


#Create a function to read agregated trading data (candles)
def refreshDataCandle(pair='BTCUSD', duration='5m'):
    client = Client(api_key, api_secret)
    candles = client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_5MINUTE)
    print(candles)
c.execute('''CREATE TABLE IF NOT EXISTS candles (
                    id INTEGER PRIMARY KEY,
                    date INTEGER,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume REAL)''')
conn.commit()
conn.close()
refreshDataCandle()

#Create a sqlite table to store said data

#Store candlModify function to update when new candle data is available

#Create a function to extract all available trade database

def refreshData(pair='BTCUSD'):

    c.execute('''CREATE TABLE IF NOT EXISTS trades (pair text, timestamp integer, price real, amount real)''')
    client = Client(api_key, api_secret)

    all_trades = client.get_historical_trades(pair)

    for trade in all_trades:
        c.execute('''INSERT INTO trades (pair, timestamp, price, amount) VALUES (?,?,?,?)''', (pair, trade['timestamp'], trade['price'], trade['amount']))
    
    conn.commit()
    conn.close()
    
#Create an order
def createOrder(api_key, secret_key, direction, price, amount, pair='BTCUSD', order_type='LimitOrder'):
    client = Client(api_key, api_secret)
    response = client.create_order(direction, price, amount, pair, order_type)
    
    return response
createOrder()
#Cancel an order
def cancelOrder(api_key, secret_key, uuid):
    
    client = Client(api_key, secret_key)
    response = client.cancel_order(uuid)
    return response
cancelOrder()
    