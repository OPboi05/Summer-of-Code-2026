import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
data = yf.download(["AUDUSD=X", "CADUSD=X"], start="2010-01-01", end="2025-01-01")["Close"]
data = data.dropna()
aud = data["AUDUSD=X"].to_numpy().flatten()
cad = data["CADUSD=X"].to_numpy().flatten()
dates = data.index

arr = np.zeros(cad.shape)
import pandas as pd
# First I do the ADF test. 
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
X = aud
Y = cad
X_with_constant = sm.add_constant(X)
model = sm.OLS(Y,X_with_constant).fit()
pnl = 0
print(model.summary())
c = model.params[0]
beta = model.params[1]
# Y = beta*X + c + epsilon(Residual)
residual = Y - beta*X - c
plt.plot(dates,residual)
plt.show()
result1 = adfuller(residual)
print("ADF Statistic:", result1[0])
print("p-value:", result1[1])
print("Critical Values:")
for key, value in result1[4].items():
    print(f"   {key}: {value}") 
# The resiudal is indeed stationary !  
# we run regression between y_t - y_t-1 and y_t-1 
x = residual[1:] #[s_1, s_2, ... ]
y = residual[:-1] #[s_0, s_1, s_2, ... ]
temp = y.copy() # s_{t-1} 
y = x - y
x_with_constant = sm.add_constant(temp)
model1 = sm.OLS(y,x_with_constant).fit()
theta = -model1.params[1]
half_life = np.log(2)/theta
print(half_life)
print(model1.summary())
half_life = max(2,int(round(half_life)))
lookback = half_life
in_trade = False
cad_cash = 0
aud_cash = 0
trade_ct = 0
entry_cad = 0
entry_aud = 0
prev_sign = 1
for i in range(lookback,arr.shape[0]):
    mean = np.mean(residual[(i-lookback):(i)])
    std_dev = np.std(residual[(i-lookback):(i)],ddof=1)
    Z = (residual[i] - mean)/(std_dev) if std_dev!= 0 else 0
    arr[i] = arr[i-1]
    if in_trade:
        arr[i] =  cad_cash*(cad[i]-entry_cad)+aud_cash*(aud[i]-entry_aud) + pnl
    else:
        arr[i] = pnl
    if Z > 2 and not in_trade:
        # Short cad and long beta*aud 
        cad_cash = -1
        aud_cash = beta
        in_trade = True
        entry_cad = cad[i]
        entry_aud = aud[i]
    if Z < -2 and not in_trade:
        # Short beta*aud and long cad  
        cad_cash = 1
        aud_cash = -beta
        in_trade = True
        entry_cad = cad[i]
        entry_aud = aud[i]
    if (abs(Z)<=0.5) and in_trade:
        trade_ct += 1
        pnl += cad_cash*(cad[i]-entry_cad)+aud_cash*(aud[i]-entry_aud) 
        cad_cash = 0
        aud_cash = 0
        in_trade = False
        arr[i] = pnl
    prev_sign = Z
plt.plot(dates,arr)
plt.show()
