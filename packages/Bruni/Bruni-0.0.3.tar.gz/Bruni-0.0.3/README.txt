This package allows you to compute the standard deviation of a portfolio, whatever it is the number of
stocks are in it.
------------------------------------------------------------------------------------------------------
Arguments needed:
-list of the stock's tickers
-list of respective weights
-starting year from when collect data
-starting month from when collect data
-starting day from when collect data
--------------------------------------
The algorithm follow this formula and it's based on the returns of the stocks:

             σ² = Σ°Σ'[w°w'σ(R°,R')]

Note:
The functions import pandas,numpy,pandas-datareader and DateTime.

