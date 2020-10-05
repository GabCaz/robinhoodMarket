'''
This file allows to get summary statistics about the Robinhood portfolio and market portfolio. For example, it allows to
see what are the most popular shares on Robinhood at any given moment, and to see what is the cap-weighted
'''
from dataset import *
from project_parameter import *

def most_popular_stocks(robinhood_popularity, date=dt.date(2020, 8, 13), make_plot=True,
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
        relative_popularity[:num][::-1].plot(kind='barh', figsize=(num / 2, num * 2 / 3), colormap=cmap,
                                       title="{} most popular stocks on Robinhood on {}".format(num, str(date)[:-9]))
    return relative_popularity

def get_robinhood_portfolio(num_df, price_dir='stock_dfs',
                            start=dt.date(2018, 1, 1),
                            end=dt.date(2020, 8, 13)):
    '''
    :param date: the date you want to know the portfolio for. By default the last date data is available for
    :param num_df: a dataframe where columns are tickers, indices are dates, and values ore number of shares in portfolio
    :param  price_dir: a directory where, for each ticker in the columns of num_df, there exists a file named <TICKER>.csv,
        which contains price data corresponding to that ticker
    :return: a tuple,
        a DataFrame containing the cap-weights of the portfolio, for each share
        a DataFrame containing the performance of the portfolio, normalized to value 1 at time 0
    '''
    for ticker in num_df.index:
        pass