# robinhoodMarket
This repository showcases work for the Risk Management (230H) final project.

# Question
In respect with the recent rise in popularity of the website Robinhood, what is the effect of widespread amateur trading on stock prices? What are some implications thereof for risk management?

# Approach
We will examine whether the continuous increase of robinhood trades for some given stock led to new patterns in price series since the beginning of the coronavirus. We can investigate qualitatively whether stylized financial facts that are specific to the current 
financial crisis are due to widespread amateur trading.
Finally, we could create a representative portfolio for aggregated positions of robinhood traders, and analyze its risk properties. We can also investigate whether such a portfolio can serve as a risk factor.

# Data sources
* Robintrack.net gives us the hour-by-hour number of users that own any particular stock at any given time, up to Aug 2020.
The data used for this project can be downloaded from https://robintrack.net/data-download.
* Stock quotes are from Yahoo Finance API, accessed through Pandas DataReader.
* Factors and Benchmarks used are from http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html.

# Repository overview
* The notebook `Study of Robinhood Market Impact for Risk Management` calls the relevent `.py` files. It summarizes our analysis.
* The file ```moment_calculation.py``` has methods to calculate summary statistics on returns that are of interest for Risk management
(the standard deviation of returns, the Hill estimator, the VaR).
* The file `dataset.py` contains the functions used to construct the datatset.
* The file `project_parameter.py` controls project aesthetics and libraries.
* The file `summary_portfolio_stats.py` contains functions to deal with portfolio construction and analysis, used for the Robinhood portfolio in our case.
* The file `coronavirus_data.py` hardcodes dates and key facts regarding the coronavirus episode which are relevant to our analysis.


# Run instructions
The raw dataset used, exported from https://robintrack.net/data-download, should be available in this repository. Alternatively, you can download it 
again from this link, and put it in a folder named "popularity_export", in the same repository as the code. Then, run our Jupyter notebook.
