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
                                       title="{} most popular stocks on Robinhood on {}".format(num, str(date)))
    return relative_popularity

def get_robinhood_portfolio(num_df, price_df,
                            start=dt.date(2018, 5, 2),
                            end=dt.date(2020, 8, 13)):
    '''
    :param num_df: a dataframe where columns are tickers, indices are dates, and values ore number of shares in portfolio
    :param  price_dir: a dataframe with stock prices, dates in indices, columns being stock indices
    :return: a tuple,
        a DataFrame containing the cap-weights of the portfolio, for each share
        a DataFrame containing the performance of the portfolio, normalized to value 1 at time 0
    '''
    # First, let us make a dataframe with the dollar holdings in each security
    mask_price = (price_df.index > start) & (price_df.index <= end)
    price_df = price_df.loc[mask_price, :]
    dollar_holdings = pd.DataFrame().reindex_like(price_df)
    for ticker in price_df.columns:
        try:
            holdings = num_df.loc[:, ticker]
            price_series = price_df.loc[:, ticker]
            dollar_holding = holdings * price_series.reindex(holdings.index)
            dollar_holdings[ticker] = dollar_holding
        except Exception as e:
            print("Error for {}: {}.".format(ticker, e))
    portfolio_index = dollar_holdings.sum(axis=1)
    portfolio_weights = dollar_holdings.div(portfolio_index, axis=0)
    return dollar_holdings, portfolio_weights

def get_portolio_return(weight_df, ret_df,
                        start=dt.date(2018, 5, 2),
                        end=dt.date(2020, 8, 13)):
    '''
    :param weight_df: values are portfolio weights, indices are dates (rows sum to 1), columns are tickers
    :param ret_df: idem, but values are returns
    :return: a dataframe with the portfolio return for each corresponding date
    '''
    mask_weight = (weight_df.index > start) & (weight_df.index <= end)
    weight_df = weight_df.loc[mask_weight, :]
    mask_ret = (ret_df.index > start) & (ret_df.index <= end)
    ret_df = ret_df.loc[mask_ret, :]
    portfolio_ret = pd.DataFrame().reindex_like(ret_df)
    for ticker in ret_df.columns:
        try:
            weights = weight_df.loc[:, ticker]
            rets = ret_df.loc[:, ticker]
            ret_for_ticker = weights * rets.reindex(weights.index)
            portfolio_ret[ticker] = ret_for_ticker
        except Exception as e:
            print("Error for {}: {}.".format(ticker, e))
    return portfolio_ret.sum(axis=1)