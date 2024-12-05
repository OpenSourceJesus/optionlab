import math
import requests
import datetime as dt
from optionlab import VERSION, run_strategy, Inputs, plot_pl

APPLE_ANNUAL_YIELDS = {  }
HISTORY_YEAR_COUNT = 30
US_BONDS_30_YEAR_YIELDS = 4.356
S_AND_P_ANNUAL_YIELDS = { 2024 : 29.24, 2023 : 26.29, 2022 : -18.11, 2021 : 28.71, 2020 : 18.40, 2019 : 31.49, 2018 : -4.38, 2017 : 21.83, 2016 : 11.96, 2015 : 1.38, 2014 : 13.69, 2013 : 32.39, 2012 : 16.00, 2011 : 2.11, 2010 : 15.06, 2009 : 26.46, 2008 : -37.00, 2007 : 5.49, 2006 : 15.79, 2005 : 4.91, 2004 : 10.88, 2003 : 28.68, 2002 : -22.10, 2001 : -11.89, 2000 : -9.10, 1999 : 21.04, 1998 : 28.58, 1997 : 33.36, 1996 : 22.96, 1995 : 37.58, 1994 : 1.32, 1993 : 10.08, 1992 : 7.62, 1991 : 30.47, 1990 : -3.10, 1989 : 31.69, 1988 : 16.61, 1987 : 5.25, 1986 : 18.67, 1985 : 31.73, 1984 : 6.27, 1983 : 22.56, 1982 : 21.55, 1981 : -4.91, 1980 : 32.42, 1979 : 18.44, 1978 : 6.56, 1977 : -7.18, 1976 : 23.84, 1975 : 37.20, 1974 : -26.47, 1973 : -14.66, 1972 : 18.98, 1971 : 14.31, 1970 : 4.01, 1969 : -8.50, 1968 : 11.06, 1967 : 23.98, 1966 : -10.06, 1965 : 12.45, 1964 : 16.48, 1963 : 22.80, 1962 : -8.73, 1961 : 26.89, 1960 : 0.47, 1959 : 11.96, 1958 : 43.36, 1957 : -10.78, 1956 : 6.56, 1955 : 31.56, 1954 : 52.62, 1953 : -0.99, 1952 : 18.37, 1951 : 24.02, 1950 : 31.71, 1949 : 18.79, 1948 : 5.50, 1947 : 5.71, 1946 : -8.07, 1945 : 36.44, 1944 : 19.75, 1943 : 25.90, 1942 : 20.34, 1941 : -11.59, 1940 : -9.78, 1939 : -0.41, 1938 : 31.12, 1937 : -35.03, 1936 : 33.92, 1935 : 47.67, 1934 : -1.44, 1933 : 53.99, 1932 : -8.19, 1931 : -43.34, 1930 : -24.90, 1929 : -8.42, 1928 : 43.61, 1927 : 37.49, 1926 : 11.62 }
α = 1.0 / 3

def GetVariance (data : list) -> float:
	mean = sum(data) / len(data)
	squaredVarianceSum = 0
	for element in data:
		variance = mean - element
		squaredVarianceSum += variance * variance
	squaredVarianceSum /= len(data) - 1
	return math.sqrt(squaredVarianceSum)

def GetCovariance (data : list, data2 : list) -> float:
	dataCount = min(len(data), len(data2))
	mean = sum(data) / dataCount
	mean2 = sum(data2) / dataCount
	sum = 0
	for i in range(dataCount):
		element = data[i]
		element2 = data2[i]
		variance = mean - element
		variance2 = mean2 - element2
		sum += variance * variance2
	return sum / (dataCount - 1)

def GetBeta (data : list, data2 : list):
	return GetCovariance(data, data2) / GetVariance(data2)

def GetAdjustedBeta (data : list, data2 : list) -> float:
	return (1.0 - α) * GetBeta(data, data2) + α

def GetExpectedReturn (data : list, data2 : list) -> float:
	sAndPMean = sum(S_AND_P_ANNUAL_YIELDS[: HISTORY_YEAR_COUNT]) / HISTORY_YEAR_COUNT
	return US_BONDS_30_YEAR_YIELDS + GetAdjustedBeta(data, data2) * (sAndPMean - US_BONDS_30_YEAR_YIELDS)

stockPrice = 164.04
volatility = 0.272
startDate = dt.date(2021, 11, 22)
endDate = dt.date(2021, 12, 17)
interestRate = GetExpectedReturn(APPLE_ANNUAL_YIELDS, S_AND_P_ANNUAL_YIELDS)
minStock = stockPrice - round(stockPrice * 0.5, 2)
maxStock = stockPrice + round(stockPrice * 0.5, 2)
strategy = [
    {'type': 'call', 'strike': 175.00, 'premium': 1.15, 'n': 100, 'action': 'sell'}
]
inputs = Inputs(
    stock_price=stockPrice,
    start_date=startDate,
    target_date=endDate,
    volatility=volatility,
    interest_rate=interestRate,
    min_stock=minStock,
    max_stock=maxStock,
    strategy=strategy,
)
output = run_strategy(inputs)
print('Max loss: %.2f' % abs(output.minimum_return_in_the_domain))
print('Max profit: %.2f' % output.maximum_return_in_the_domain)
for low, high in output.profit_ranges:
    print('Profitable stock price range: %.2f -> %.2f' % (low, high))
print('Probability of Profit (PoP): %.1f%%' % (output.probability_of_profit * 100))