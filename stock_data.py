import yfinance as yf
import requests
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")  
    
    raw_data = data.resample('M').last()  

    graphs = {}

    week_data = data[-7:]  
    graphs['week'] = generate_graph(week_data['Close'], f'{ticker} - Past Week Prices')

    
    month_data = data[-30:]  
    graphs['month'] = generate_graph(month_data['Close'], f'{ticker} - Past Month Prices')

    year_data = data  
    graphs['year'] = generate_graph(year_data['Close'], f'{ticker} - Past Year Prices')

    return raw_data, graphs


def generate_graph(data, title):
    plt.figure(figsize=(10, 5))
    plt.plot(data)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    
    # Save the plot to a string buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return graph_url

def generate_graph(data, title):
    plt.figure(figsize=(10, 5))
    plt.plot(data)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    
    # Show the graph for testing purposes
    plt.show()
    plt.close()
