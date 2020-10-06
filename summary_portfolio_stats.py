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
    mask = (price_df.index > start) & (price_df.index <= end)
    price_df = price_df.loc[mask, :]
    dollar_holdings = pd.DataFrame().reindex_like(price_df)
    for ticker in price_df.columns:
        try:
            holdings = num_df.loc[:, ticker]
            price_series = price_df.loc[:, ticker]
            dollar_holding = holdings * price_series.reindex(holdings.index)
            dollar_holdings[ticker] = dollar_holding
        # if dollar_holdings.empty:
        #     dollar_holdings = dollar_holding
        # else:
        #     dollar_holdings = dollar_holdings.join(dollar_holdings, how='outer')
        except Exception as e:
            print("Error for {}: {}.".format(ticker, e))
    portfolio_index = dollar_holdings.sum(axis=1)
    portfolio_weights = dollar_holdings.div(portfolio_index, axis=0)
    return dollar_holdings, portfolio_weights

# main
# tickers = get_available_tickers()
# all_robinhood_prices = compile_price_data([t[:-4] for t in tickers], title_ext='all_robinhood_stocks')
# robinhood_popularity = merged_daily_usage_data(tickers)
# time_0_shares = robinhood_popularity.iloc[0, :].fillna(0)
# total_shares = time_0_shares.sum()
# missing_nb = 0
# missing_shares = []
# for i in range(len(time_0_shares)):
#     ticker = time_0_shares.index[i]
#     if (not ticker in all_robinhood_prices.columns):
#         missing_nb += time_0_shares.iloc[i]
#         missing_shares.append(ticker)
# print("We have data for {} % of the shares.".format(100 - 100 * missing_nb / total_shares))
# print('The missing shares are {}.'.format(missing_shares))
# all_robinhood_prices = all_robinhood_prices.fillna(method='ffill')
# all_robinhood_prices.fillna(all_robinhood_prices.mean(), inplace=True)
# robinhood_popularity.fillna(0, inplace=True)
# assert(not robinhood_popularity.isna().any().any())
# assert(not all_robinhood_prices.isna().any().any())
# dol_holdings, robinhood_weights = get_robinhood_portfolio(num_df=robinhood_popularity, price_df=all_robinhood_prices)
# print(robinhood_weights)