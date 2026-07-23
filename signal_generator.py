# In this file I have only focused on signal generation and not on size of the position
import indicator 
import filters

choices = []
for i in range(50,len(arr)): # I start from 50 to give EMA, RSI etc enough run-up
    if (signal(aud,i)==1 and RSI(aud,i)>=70):
        choices.append("BUY")
    elif (signal(aud,i)==-1 and RSI(aud,i)<=30):
        choices.append("SELL")
    else:
        choices.append("HOLD")
