'''
File to test the other files
'''
# Imports
from moment_calculation import *
from dataset import *
from summary_portfolio_stats import *
from coronavirus_data import *
from project_parameter import *

# Directory
try:
    os.chdir(ROOT_DIR)
except:
    pass

# Try stuff
# tickers = get_available_tickers()
# all_robinhood_prices = compile_price_data([t[:-4] for t in tickers], title_ext='all_robinhood_stocks')
# robinhood_popularity = merged_daily_usage_data(tickers)
# robinhood_fb = pd.read_csv("popularity_export/FB.csv")
# robinhood_price = pd.read_csv("stock_dfs/FB.csv")
# time_0_shares = robinhood_popularity.iloc[0, :].fillna(0)
# total_shares = time_0_shares.sum()
# all_robinhood_prices = all_robinhood_prices.fillna(method='ffill')
# all_robinhood_prices.fillna(all_robinhood_prices.mean(), inplace=True)
# robinhood_popularity.fillna(0, inplace=True)
# assert(not robinhood_popularity.isna().any().any())
# assert(not all_robinhood_prices.isna().any().any())
# dol_holdings, robinhood_weights = get_robinhood_portfolio(num_df=robinhood_popularity, price_df=all_robinhood_prices)
# all_stock_returns = get_returns(all_robinhood_prices)
# port_ret = get_portolio_return(robinhood_weights, all_stock_returns)
# # print(port_ret)
# 0