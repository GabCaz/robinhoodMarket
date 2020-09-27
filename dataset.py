''' This file contains functins used to construct the dataset. The only manual step you need to perform is '''
import os
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import pickle

def merged_daily_usage_data(reload=False):
    '''
    :param reload: whether to reload all the data from raw dataframes or use an already saved merged data frame
    :return: a merged dataframe with the daily usage data for all available stocks on Robinhood
    '''

def get_robinhood_portfolio(num_df, price_df, date=dt.datetime.now()):
    '''
    :param date: the date you want to know the portfolio for
    :param num_df: a dataframe where columns are tickers, indices are dates, and values ore number of shares in portfolio
    :param  price_df:  a dataframe where columns are the same tickers, indices are dates, and values ore the prices of shares
    :return:
    '''


def get_price_data(tickers,
                   start=dt.datetime(2018, 1, 1),
                   end=dt.datetime.now(),
                   reload_data=False):
    '''
    Support source: https://pythonprogramming.net/preprocessing-for-machine-learning-python-programming-for-finance/?completed=/stock-price-correlation-table-python-programming-for-finance/
    Save dataframe objects containing the end of day prices for a given set of stock tickers
    :param tickers: a list of strings, corresponding to the tickers we want to save price data for
    :param start: start date we want to have the prices for
    :param end: end date we want to have the returns for
    :param reload_data: whether we want to reload all the data and discard previously downloaded data
    :return: Nothing
    '''
    if not os.path.exists('stock_dfs'):
        os.mkdir('stock_dfs')
        print('Dir for stock dataframes made')
    for ticker in tickers:
        print(ticker)
        if (not os.path.exists('stock_dfs/{}.csv'.format(ticker))) or reload_data:
            try:
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except Exception as e:
                print("Error for {}: {}.".format(ticker, e))
            else:
                print('Already have {}'.format(ticker))

def compile_price_data(tickers):
    '''
    :param tickers: a list of strings, corresponding to the tickers we want to compile price data into a single dataframe for
    After saving the stock price data in directory 'stock_dfs' as above, compile this data into a single dataframe
    '''
    for count, ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df.set_index('Date', inplace=True)
            df.rename(columns={'Adj Close': ticker}, inplace=True)
            df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')
            if count % 10 == 0:
                print(count)
        except Exception as e:
            print("Error for {}: {}.".format(ticker, e))
        print(main_df.head())
        main_df.to_csv('joined_closes.csv')

def get_returns(tickers):
    '''
    :param tickers:
    :return:
    '''
    df = pd.read_csv('joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    ret_df_sp = pd.DataFrame()
    for ticker in tickers:
        ret_df_sp[ticker] = (df[ticker].shift(1) - df[ticker]) / df[ticker]
        ret_df_sp.to_csv('joined_returns.csv')