# robinhoodMarket
This repository showcases work for the Risk Management (230H) final project.

# Question
In respect with the recent rise in popularity of the website Robinhood, what is the effect of widespread amateur trading on stock prices? What are some implications thereof for risk management?

# Motivation
During the coronavirus lock-in, amateur trading has boomed to the point of becoming a considerable share of total trading 
on the market for many shares. Therefore, it makes sense to wonder whether massive trading by 
amateur, usually young, and inexperienced investors have implications for risk management. The mainly young and inexperienced 
users of Robinhood now represent a considerable share of total trading volume for some companies. 
Does this new source of trading have implications for risk management? Did this trading activity lead to new volatility 
patterns in stock volatility? Does Robinhood trading now represent a significant market risk factor?


# Approach
We will examine whether the continuous increase of robinhood trades for some given stock led to new patterns in price series since the beginning of the coronavirus. We can investigate qualitatively whether stylized financial facts that are specific to the current 
financial crisis are due to widespread amateur trading.
Finally, we could create a representative portfolio for aggregated positions of robinhood traders, and analyze its risk properties. We can also investigate whether such a portfolio can serve as a risk factor.

# Repository overview
* The notebook `Study of Robinhood Market Impact for Risk Management` calls the relevent `.py` files. It summarizes our analysis.
* The file ```moment_calculation.py``` has methods to calculate summary statistics on returns that are of interest for Risk management
(the standard deviation of returns, the Hill estimator, the VaR).
* The file `dataset.py` contains the functions used to construct the datatset.
* The file `project_parameter.py` controls project aesthetics and libraries.
* The file `summary_portfolio_stats.py` contains functions to deal with portfolio construction and analysis, used for the Robinhood portfolio in our case.
* The file `coronavirus_data.py` hardcodes dates and key facts regarding the coronavirus episode which are relevant to our analysis.
* The folder `presentation_material` contains slides and graphs used for the presentation.

# Data sources
## Sources
* Robintrack.net gives us the hour-by-hour number of users that own any particular stock at any given time, up to Aug 2020.
The data used for this project can be downloaded from https://robintrack.net/data-download.
* Stock quotes are from Yahoo Finance API, accessed through Pandas DataReader.
* Factors and Benchmarks used are from http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html.

## Comments on the data source
* Our dataset reflects Robinhood’s popularity data about particular stocks, exported 
through the website robintrack.net. The dataset gives the number of users who own 
any particular stock for 8597 stocks which are traded on Robinhood. The level of 
granularity is at least daily; data is available many times a day for some stocks. 
Data is available as early as May 2, 2018, for some stocks, and until August 13, 
2020, which is the date when Robinhood deactivated its API which allowed users to 
access stock popularity data. 
* As noted by the creator of the dataset, “Robinhood gives free shares of a certain 
set of stocks as rewards to users for referring others to their platform. Some of the 
most popular stocks are at the top because of this.”. Given the free share that is 
offered to users is randomly chosen from Robinhood’s inventory, it is not possible 
for us to correct for this effect. Therefore, we ignored this effect, and the stock 
data we have access to does not perfectly represent the intentional trading decisions 
of Robinhood users.
* Another issue is that we only know we only know the number of users who own any 
particular stock at any given time. We do not know the size of the position. If a 
user who already owns a stock changes their weight in this stock, it will not appear 
in our data. Therefore, our dataset only gives an approximation for the interest any
 particular stock may receive, but we need to make assumptions on the quantity 
 detained by each user to proceed. We will assume all the stocks detained are 
 detained in equal quantity, i.e. if 10 users own some shares of company X and 10 
 users own some shares of company Y, then, the aggregated Robinhood users own the 
 same number of shares in company X and in company Y.

# Run instructions
The raw dataset used, exported from https://robintrack.net/data-download, should be available in this repository. Alternatively, you can download it 
again from this link, and put it in a folder named "popularity_export", in the same repository as the code. Then, run our Jupyter notebook.
