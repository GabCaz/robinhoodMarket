''' This file contains functions used to construct the dataset. The only manual step you need to perform is '''
from project_parameter import *
# import pickle

ROOT_DIR = os.path.dirname(os.path.abspath("moment_calculation.py")) # project root directory

def get_available_tickers(path="popularity_export/"):
    '''
    :param path: where you need to put all the Robinhood data files in this directory
    :return: a list with all the available tickers
    '''
    # move to the directory where the files are if you are not there yet
    if os.getcwd()[-15:] != path[-16:-1]:
        os.chdir(ROOT_DIR)
        os.chdir(path)
    files = []
    for file in glob.glob("*.csv"):
        files.append(file)
    os.chdir(ROOT_DIR)
    return files

def merged_daily_usage_data(tickers, reload=False,
                            path="aggregated_daily_data/",
                            file_name='aggregated_daily_robinhood_holdings.csv'):
    '''
    Return a dataframe with concatenated Robinhood popularity data, either from a previously saved csv file in the
    given apath/file_name, or by reconstructing it (if not found or reload=True)
    :param tickers: the tickers of the stocks to aggregate into the dataframe
    :param reload: whether to reload all the data from raw dataframes or use an already saved merged data frame
    :return: a merged dataframe with the daily usage data for all available stocks on Robinhood

    :warning: We recommend not reloading data, as joining all the more than 8000 dataframes together takes a while
    '''
    # move to the folder where you may have constructed the dataset already
    os.chdir(ROOT_DIR)
    if (not os.path.exists(path)):
        os.mkdir(path)
    os.chdir(path)
    # if the file does not already exist or you want to reload it, recreate the file by merging all stock data
    if (not os.path.exists(file_name) or reload):
        data = pd.read_csv(tickers[0])
        data['timestamp'] = pd.to_datetime(data['timestamp']).dt.date
        data = data.drop_duplicates(['timestamp'], keep='last')  # keep EoD data to study macroscopic effects
        data.columns = ['timestamp', tickers[0][:-4]]
        data.set_index(['timestamp'], inplace=True)
        for t in tickers[1:]:
            this_stock = pd.read_csv(t)
            this_stock['timestamp'] = pd.to_datetime(this_stock['timestamp']).dt.date
            this_stock = this_stock.drop_duplicates(['timestamp'],
                                                    keep='last')  # keep EoD data to study macroscopic effects
            this_stock.columns = ['timestamp', t]
            this_stock.set_index(['timestamp'], inplace=True)
            data = data.join(this_stock, how='outer')
    # load and return the merged dataset
    data = pd.read_csv(file_name, parse_dates=True, index_col=['timestamp'])
    data.columns = data.columns.str.replace(".csv", "")
    data.index = [d.date() for d in data.index] # convert to date object
    os.chdir(ROOT_DIR)
    return data

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
    :return: Nothing, just save stock data in dataframes
    '''
    os.chdir(ROOT_DIR)
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

def compile_price_data(tickers, title_ext, path="aggregated_daily_data/", reload=False):
    '''
    :param tickers: a list of strings, corresponding to the tickers we want to compile price data into a single dataframe for
    :param title_ext: add to the title when you want to save the file, so that the file title will be
        joined_closes + title_ext + .csv.
    After saving the stock price data in directory 'stock_dfs' as above, compile this data into a single dataframe
    '''
    os.chdir(ROOT_DIR)
    file_name = path + 'joined_closes' + title_ext + '.csv'
    if (not os.path.exists(path)):
        os.mkdir(path)
    if (not os.path.exists(file_name) or reload):
        main_df = pd.DataFrame()
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
        main_df.to_csv(file_name)
    data = pd.read_csv(file_name, parse_dates=True, index_col=['Date'])
    data.index = [d.date() for d in data.index]  # convert to date object
    return data

def get_returns(price_df):
    '''
    :param price_df: a dataframe with stock prices, dates in indices, columns being stock indices
    :return:
    '''
    ret_df = (price_df / price_df.shift(1)).dropna() - 1
    return ret_df