def vol(volume,W,c,t):
    sma = 0
    for i in range(W):
        sma += volume[t-i]
    sma /= W 
    if (volume[t] > c*sma):
        return True
    else:
        return False
