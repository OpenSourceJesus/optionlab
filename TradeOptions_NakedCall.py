import math
import datetime as dt
import CollectionExtensions
from optionlab import VERSION, run_strategy, Inputs, plot_pl

HISTORY_YEAR_COUNT = 30
US_BONDS_30_YEAR_YIELDS = 4.356
APPLE_ANNUAL_YIELDS = { 2024 : 242.6500, 2023 : 191.5919, 2022 : 128.5816, 2021	: 174.7132, 2020 : 129.7556, 2019 : 71.1734, 2018 : 37.6645, 2017 : 39.8109, 2016 : 26.8131, 2015 : 23.8379, 2014 : 24.5797, 2013 : 17.4799, 2012 : 16.1760, 2011 : 12.2002, 2010 : 9.7168, 2009 : 6.3481, 2008	: 2.5711, 2007 : 5.9669, 2006 : 2.5557, 2005 : 2.1656, 2004	: 0.9700, 2003 : 0.3219, 2002 : 0.2158, 2001 : 0.3299, 2000 : 0.2241, 1999 : 0.7743, 1998 : 0.3083, 1997 : 0.0989, 1996	: 0.1572, 1995 : 0.2400, 1994 : 0.2904, 1993 : 0.2148, 1992	: 0.4335, 1991 : 0.4055, 1990 : 0.3063, 1989 : 0.2480, 1988	: 0.2805, 1987 : 0.2902, 1986 : 0.1396, 1985 : 0.0758, 1984	: 0.1004, 1983 : 0.0840, 1982 : 0.1029, 1981 : 0.0763 }
S_AND_P_ANNUAL_YIELDS = { 2024 : 29.24, 2023 : 26.29, 2022 : -18.11, 2021 : 28.71, 2020 : 18.40, 2019 : 31.49, 2018 : -4.38, 2017 : 21.83, 2016 : 11.96, 2015 : 1.38, 2014 : 13.69, 2013 : 32.39, 2012 : 16.00, 2011 : 2.11, 2010 : 15.06, 2009 : 26.46, 2008 : -37.00, 2007 : 5.49, 2006 : 15.79, 2005 : 4.91, 2004 : 10.88, 2003 : 28.68, 2002 : -22.10, 2001 : -11.89, 2000 : -9.10, 1999 : 21.04, 1998 : 28.58, 1997 : 33.36, 1996 : 22.96, 1995 : 37.58, 1994 : 1.32, 1993 : 10.08, 1992 : 7.62, 1991 : 30.47, 1990 : -3.10, 1989 : 31.69, 1988 : 16.61, 1987 : 5.25, 1986 : 18.67, 1985 : 31.73, 1984 : 6.27, 1983 : 22.56, 1982 : 21.55, 1981 : -4.91, 1980 : 32.42, 1979 : 18.44, 1978 : 6.56, 1977 : -7.18, 1976 : 23.84, 1975 : 37.20, 1974 : -26.47, 1973 : -14.66, 1972 : 18.98, 1971 : 14.31, 1970 : 4.01, 1969 : -8.50, 1968 : 11.06, 1967 : 23.98, 1966 : -10.06, 1965 : 12.45, 1964 : 16.48, 1963 : 22.80, 1962 : -8.73, 1961 : 26.89, 1960 : 0.47, 1959 : 11.96, 1958 : 43.36, 1957 : -10.78, 1956 : 6.56, 1955 : 31.56, 1954 : 52.62, 1953 : -0.99, 1952 : 18.37, 1951 : 24.02, 1950 : 31.71, 1949 : 18.79, 1948 : 5.50, 1947 : 5.71, 1946 : -8.07, 1945 : 36.44, 1944 : 19.75, 1943 : 25.90, 1942 : 20.34, 1941 : -11.59, 1940 : -9.78, 1939 : -0.41, 1938 : 31.12, 1937 : -35.03, 1936 : 33.92, 1935 : 47.67, 1934 : -1.44, 1933 : 53.99, 1932 : -8.19, 1931 : -43.34, 1930 : -24.90, 1929 : -8.42, 1928 : 43.61, 1927 : 37.49, 1926 : 11.62 }
α = 0.33

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
	_sum = 0
	for i in range(dataCount):
		element = data[i]
		element2 = data2[i]
		variance = mean - element
		variance2 = mean2 - element2
		_sum += variance * variance2
	return _sum / (dataCount - 1)

def GetBeta (data : list, data2 : list):
	return GetCovariance(data, data2) / GetVariance(data2)

def GetAdjustedBeta (data : list, data2 : list) -> float:
	return (1.0 - α) * GetBeta(data, data2) + α

def GetExpectedReturn (data : list, data2 : list) -> float:
	sAndPMean = sum(CollectionExtensions.Slice(S_AND_P_ANNUAL_YIELDS.values(), 0, HISTORY_YEAR_COUNT)) / HISTORY_YEAR_COUNT
	return US_BONDS_30_YEAR_YIELDS + GetAdjustedBeta(data, data2) * (sAndPMean - US_BONDS_30_YEAR_YIELDS)

stockPrice = 164.04
volatility = 0.272
startDate = dt.date(2024, 12, 4)
endDate = dt.date(2024, 12, 4)
interestRate = GetExpectedReturn(CollectionExtensions.Slice(APPLE_ANNUAL_YIELDS.values()), CollectionExtensions.Slice(S_AND_P_ANNUAL_YIELDS.values()))
minStock = stockPrice - round(stockPrice / 2, 2)
maxStock = stockPrice + round(stockPrice / 2, 2)
strategy = [
	{ 'type': 'call', 'strike': 175, 'premium': 1.15, 'n': 100, 'action': 'sell' }
]
inputs = Inputs(
	stock_price = stockPrice,
	start_date = startDate,
	target_date = endDate,
	volatility = volatility,
	interest_rate = interestRate,
	min_stock = minStock,
	max_stock = maxStock,
	strategy = strategy
)
output = run_strategy(inputs)
print('Max loss: %.2f' % abs(output.minimum_return_in_the_domain))
print('Max profit: %.2f' % output.maximum_return_in_the_domain)
for low, high in output.profit_ranges:
	print('Profitable stock price range: %.2f -> %.2f' % (low, high))
print('Probability of Profit (PoP): %.1f%%' % (output.probability_of_profit * 100))