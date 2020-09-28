'''
Util functions to calculate moments through the program
'''
from project_parameter import *

def get_realized_daily_vol(returns, make_pct=True):
    '''
    :param returns: 1D np array of doubles, corresponding to financial returns
    :param log_ret: True iif the returns given are log-returns (True by default, since ABM model models log prices)
    :return: the squared returns
    '''
    returns = returns.copy()
    if make_pct:
        returns *= 100
    return np.sqrt((returns) ** 2)

def get_acvs(returns, lags=[1, 5, 50]):
    '''
    :param returns: 1D array
    :param lags: list of integers for which we want to compute the autocovariance
    :param log_ret: True iif the returns given are log-returns (True by default, since ABM model models log prices)
    :return: the corresponding autocovariances in a dict, where the key is the lag, and the value is the acv
    '''
    returns = returns.copy()
    acf_func = acf(returns, unbiased=True, nlags=max(lags), fft=False)
    return dict(zip(lags, acf_func[lags]))

def get_conditional_vol(returns, p=1, o=1, q=1, update_freq=5, make_pct=True):
    '''
    :param returns: 1D np array of doubles
    :param p: Lag order of the symmetric innovation
    :param o: Lag order of the asymmetric innovation
    :param q: Lag order of lagged volatility or equivalent
    :param update_freq: Frequency of iteration updates. Output is generated every update_freq iterations.
    :return: Estimated conditional volatility (nobs element array)
    '''
    returns = returns.copy()
    if make_pct:
        returns *= 100
    gjr_model = arch_model(returns, p=p, o=o, q=q)
    res = gjr_model.fit(update_freq=update_freq, disp='off')
    return res.conditional_volatility

def hill_estimator(returns, perc=0.95, make_pct=True):
    '''
    :param returns: 1D np array of doubles
    :param perc: a double strictly between 0 and 1, corresponding to the percentile of the Hill estimator we are
            trying to use, e.g. for 95%, we are going to estimate the size of the 95% tails
    :param make_pct: if you want to multiply the returns given by 100
    :return: the Hill estimator for that given threshold
    '''
    returns = returns.copy()
    if make_pct:
        returns *= 100
    abs_returns = np.abs(returns).squeeze()
    sorted_abs_returns = np.sort(abs_returns)[::-1] # sorting in descending order
    k = int((1.0 - perc) * len(sorted_abs_returns))  # position of the perc-percentile (eg 95%-percentile) largest abs return
    returns_in_tail = sorted_abs_returns[:k] - sorted_abs_returns[k] # subtracting the perc-percentile largest abs return
    gamma = np.mean(returns_in_tail)
    hill_estimator = 1.0 / gamma
    return hill_estimator

def plot_vol(return_df, popularity_df, make_pct=True):
    '''
    :param returns: 1D np array of doubles
    :param make_pct:
    '''
    dates = return_df.index
    fig, axes = plt.subplots(nrows=popularity_df.shape[1], ncols=1, figsize=(10, 5 * popularity_df.shape[1]))
    for i, ticker in enumerate(return_df.columns):
        # get returns and popularity numbers for the dates we have available
        popularity_numbers = popularity_df[ticker][dates].values
        ret_data = return_df[ticker][dates].values

        # plot volatility data on the left axis
        axes[i].plot(dates, get_realized_daily_vol(ret_data, make_pct=make_pct),
                     label='Realized Volatility', color=cmap(5), alpha=0.3)
        axes[i].set_ylabel('Volatility')
        axes[i].plot(dates, get_conditional_vol(ret_data, make_pct=make_pct), label='Conditional Volatility',
                     color=cmap(1))
        axes[i].yaxis.label.set_color(cmap(1))
        axes[i].legend(loc='upper left')
        axes[i].grid(False)

        # plot popularity numbers on the right axis
        right_axis = axes[i].twinx()
        right_axis.plot(dates, popularity_numbers, label='Users holding', color=cmap(0))
        right_axis.set_ylabel('Number of users holding')
        right_axis.yaxis.label.set_color(cmap(0))
        right_axis.legend(loc='upper right')
        right_axis.grid(False)

        # title, x_label
        axes[i].set_title('Daily Realized and Conditional Volatility for {}'.format(ticker), fontsize=16)
        axes[i].set_xlabel('Time', fontsize=16)
    plt.tight_layout()
