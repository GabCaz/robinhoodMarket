'''
This file allows to get summary statistics about the Robinhood portfolio and market portfolio. For example, it allows to
see what are the most popular shares on Robinhood at any given moment, and to see what is the cap-weighted
'''
from dataset import *
import matplotlib.pyplot as plt

def most_popular_stocks(robinhood_popularity, date=dt.datetime(2020, 8, 13), make_plot=True,
                        num=15):
    '''
    :param robinhood_popularity: a dataframe with shares held by users
    :param date: by default the last date where Robinhood data is available
    :param num: the number of most widely owned stocks to plot
    :return: A series with  the weights corresponding to the most popular shares on Robinhood, by number of users who
    detain them, for the given date
    '''
    shares_held = robinhood_popularity.loc[date, :].sort_values(ascending=False).dropna()
    relative_popularity = shares_held / shares_held.sum()
    if make_plot:
        relative_popularity[:num][::-1].plot(kind='barh', figsize=(num / 2, num * 2 / 3),
                                       title="{} most popular stocks on Robinhood on {}".format(num, str(date.date)[:-9]))
    return relative_popularity



def get_robinhood_portfolio(num_df, price_df, date=dt.datetime(2020, 8, 13)):
    '''
    :param date: the date you want to know the portfolio for. By default the last date data is available for
    :param num_df: a dataframe where columns are tickers, indices are dates, and values ore number of shares in portfolio
    :param  price_df:  a dataframe where columns are the same tickers, indices are dates, and values ore the prices of shares
    :return:
    '''
