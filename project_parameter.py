''' Project parameters controlling the aesthetics, libraries, etc. '''
import numpy as np
from arch import arch_model
from statsmodels.tsa.stattools import acf
from scipy.stats import kurtosis, skew
import matplotlib.pyplot as plt
import glob, os
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
cmap = plt.cm.get_cmap('Set1') # color palette