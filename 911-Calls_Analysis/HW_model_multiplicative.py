
def initial_trend(series, slen):
    sum = 0.0
    for i in range(slen):
        sum += float(series[i+slen] - series[i]) / slen
    return sum / slen


def initial_seasonal_components(series, slen):
    seasonals = {}
    season_averages = []
    n_seasons = int(len(series)/slen)
    # compute season averages
    for j in range(n_seasons):
        season_averages.append(sum(series[slen*j:slen*j+slen])/float(slen))
    # compute initial values
    for i in range(slen):
        sum_of_vals_over_avg = 0.0
        for j in range(n_seasons):
            sum_of_vals_over_avg += series[slen*j+i]-season_averages[j]
        seasonals[i] = sum_of_vals_over_avg/n_seasons
    return seasonals


def triple_exponential_smoothing(series, slen, alpha, beta, gamma, n_preds):
    result = []
    seasonals = initial_seasonal_components(series, slen)
    for i in range(len(series)+n_preds):
        if i == 0: # initial values
            smooth = series[0]
            trend = initial_trend(series, slen)
            result.append(series[0])
            continue
        if i >= len(series): # we are forecasting
            m = i - len(series) + 1
            result.append((smooth+(trend*m))*seasonals[i%slen])
        else:
            val = series[i]
            last_smooth, smooth = smooth, alpha*(val/seasonals[i%slen]) + (1-alpha)*(smooth+trend)
            last_trend, trend =trend, beta * (smooth-last_smooth) + (1-beta)*trend
            seasonals[i%slen] = gamma*(val/(last_smooth + last_trend)) + (1-gamma)*seasonals[i%slen]
            result.append((smooth+trend)*seasonals[i%slen])
    return result



