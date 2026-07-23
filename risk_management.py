import yfinance as yf
import numpy as np
#Exctract data
data = yf.download(["AAPL","SPY"], start="2010-01-01", end="2025-01-01")["Close"]
data = data.dropna()
asset = data["AAPL"].to_numpy().flatten()
benchmark = data["SPY"].to_numpy().flatten()
dates = data.index
import statsmodels.api as sm
import matplotlib.pyplot as plt

asset_return = (asset[1:] - asset[:-1])/asset[:-1]
benchmark_return = (benchmark[1:] - benchmark[:-1])/benchmark[:-1]

# Run the regression
X = benchmark_return
Y = asset_return

X_with_constant = sm.add_constant(X)
model = sm.OLS(Y,X_with_constant).fit()

print(model.summary())

#Extract the coefficients
alpha = model.params[0]
beta = model.params[1]

print("Alpha:",alpha)
print("Beta:",beta)
# Hedged portfolio
hedged_return = asset_return - beta*benchmark_return

pnl = np.cumsum(hedged_return)

plt.plot(dates[1:],pnl)
plt.title("Hedged Portfolio")
plt.show()
