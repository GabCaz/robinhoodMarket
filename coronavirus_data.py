'''
This file contains some dates and important facts about the coronavirus, to help us link together the sanitary
crisis, the explosion in activity on website Robinhood, and the market turmoil
'''
from project_parameter import *
# Timeline: https://www.ajmc.com/view/a-timeline-of-covid19-developments-in-2020
WHO_ANNOUNCES_VIRUS = dt.datetime(2020, 1, 9)
# Date when the USA banned flights from China to the USA
USA_TRAVEL_BAN = dt.datetime(2020, 2, 2)
# Date when President Trump announces coronavirus emergency situation in the USA
USA_NATIONAL_EMERGENCY = dt.datetime(2020, 3, 13)
CALIFORNIA_STAY_AT_HOME = dt.datetime(2020, 3, 19)

EVENTS = {
    'WHO Discovers the Coronavirus':WHO_ANNOUNCES_VIRUS,
    'USA announces China Travel Ban':USA_TRAVEL_BAN,
    'USA National Emergency Declared':USA_NATIONAL_EMERGENCY,
    'California Stay-At-Home order':CALIFORNIA_STAY_AT_HOME
}