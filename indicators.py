def EMA(arr,N,t):
    # i-N+1, i-N+1, .... , i
    ans = arr[t-N+1]
    for i in range(t-N+1,t+1):
        ans = arr[i] * (2/(N+1)) + ans * (1 - (2/(N+1)))
    return ans
def MACD(arr,t):
    # Return MACD_t
    return EMA(arr,12,t) - EMA(arr,26,t)
def signal_line(arr,t):
    array = [MACD(arr,t-8+i) for i in range(9)]
    return EMA(array,9,8)
def signal(arr,t):
    prev = MACD(arr,t-1) - signal_line(arr,t-1)
    curr = MACD(arr,t) - signal_line(arr,t)
    if prev <= 0 and curr > 0:
        return 1    
    elif prev >= 0 and curr < 0:
        return -1     
    return 0
def RSI(arr,t):
    gain = 0
    loss = 0
    for i in range(14):
        if((arr[t-14+i]-arr[t-15+i])>0):
            gain += abs(arr[t-15+i]-arr[t-14+i])
        else:
            loss += abs((arr[t-15+i]-arr[t-14+i])) 
    gain /= 14 
    loss /= 14 
    if loss==0: return 100
    return (100 - (100)/(1+(gain/loss)))
