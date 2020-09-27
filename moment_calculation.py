'''
Util functions to calculate moments through the program
'''
import numpy as np
from arch import arch_model
from statsmodels.tsa.stattools import acf
from scipy.stats import kurtosis, skew

def get_realized_daily_vol(returns, log_ret=True, make_pct=True):
    '''
    :param returns: 1D np array of doubles, corresponding to financial returns
    :param log_ret: True iif the returns given are log-returns (True by default, since ABM model models log prices)
    :return: the squared returns
    '''
    returns = returns.copy()
    if log_ret:
        returns = get_simple_r(returns)
    if make_pct:
        returns *= 100
    return np.sqrt((returns) ** 2)

def get_acvs(returns, lags=[1, 5, 50], log_ret=True):
    '''
    :param returns: 1D array
    :param lags: list of integers for which we want to compute the autocovariance
    :param log_ret: True iif the returns given are log-returns (True by default, since ABM model models log prices)
    :return: the corresponding autocovariances in a dict, where the key is the lag, and the value is the acv
    '''
    returns = returns.copy()
    if log_ret:
        returns = get_simple_r(returns)
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

def hill_estimator(returns, perc=0.95, log_ret=True, make_pct=True):
    '''
    :param returns: 1D np array of doubles
    :param perc: a double strictly between 0 and 1, corresponding to the percentile of the Hill estimator we are
            trying to use, e.g. for 95%, we are going to estimate the size of the 95% tails
    :param log_ret: True iif the returns given are log-returns (True by default, since ABM model models log prices)
    :param make_pct: if you want to multiply the returns given by 100
    :return: the Hill estimator for that given threshold
    '''
    returns = returns.copy()
    if not log_ret: # if you have log-returns, get simple returns
        returns = get_log_r(returns)
    if make_pct:
        returns *= 100
    abs_returns = np.abs(returns).squeeze()
    sorted_abs_returns = np.sort(abs_returns)[::-1] # sorting in descending order
    k = int((1.0 - perc) * len(sorted_abs_returns))  # position of the perc-percentile (eg 95%-percentile) largest abs return
    returns_in_tail = sorted_abs_returns[:k] - sorted_abs_returns[k] # subtracting the perc-percentile largest abs return
    gamma = np.mean(returns_in_tail)
    hill_estimator = 1.0 / gamma
    return hill_estimator

def get_simple_r(log_r):
    '''
    :param log_r: np array of log returns (doubles)
    :return: Compute simple returns from log returns
    '''
    return np.exp(log_r) - 1.0

def get_log_r(simple_r):
    '''
    :param simple_r: np array of simple returns (doubles)
    :return: log returns
    '''
    return np.log(simple_r + 1)