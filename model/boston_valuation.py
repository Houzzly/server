from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np

# Gather Data
boston_dataset = load_boston()
data = pd.DataFrame(data=boston_dataset.data,
                    columns=boston_dataset.feature_names)
features = data.drop(['INDUS', 'AGE'], axis=1)

log_prices = np.log(boston_dataset.target)
target = pd.DataFrame(log_prices, columns=['PRICE'])

# feature indices
RM_IDX = 1
CHAS_IDX = 2
DIS_IDX = 5
PTRATIO_IDX = 8

# modern day scale factor
ZILLOW_MEDIAN_PRICE = 583.3
SCALE_FACTOR = ZILLOW_MEDIAN_PRICE / np.median(boston_dataset.target)

# average out all the property stats
property_stats = features.mean().values.reshape(1, 11)

# calculate regression and root mean squared error
regr = LinearRegression().fit(features, target)
fitted_vals = regr.predict(features)
MSE = mean_squared_error(target, fitted_vals)
RMSE = np.sqrt(MSE)


def get_log_estimate(rooms,
                     area_demographic,
                     distance_from_town,
                     close_to_river=False,
                     high_confidence=True):

    # Configure property
    property_stats[0][RM_IDX] = rooms

    if area_demographic == "poor":
        property_stats[0][PTRATIO_IDX] = 17.400000
    elif area_demographic == "moderate":
        property_stats[0][PTRATIO_IDX] = 19.050000
    else:
        property_stats[0][PTRATIO_IDX] = 20.200000

    if distance_from_town == "close":
        property_stats[0][DIS_IDX] = 2.100175
    elif distance_from_town == "moderate":
        property_stats[0][DIS_IDX] = 3.207450
    else:
        property_stats[0][DIS_IDX] = 5.188425

    if close_to_river:
        property_stats[0][CHAS_IDX] = 1
    else:
        property_stats[0][CHAS_IDX] = 0

    # Make prediction
    log_estimate = regr.predict(property_stats)[0][0]

    # Calc Range
    if high_confidence:
        upper_bound = log_estimate + 2*RMSE
        lower_bound = log_estimate - 2*RMSE
        interval = 95
    else:
        upper_bound = log_estimate + RMSE
        lower_bound = log_estimate - RMSE
        interval = 68

    return log_estimate, upper_bound, lower_bound, interval


def get_dollar_estimate(rooms, area_demographic, distance_from_town, close_to_river, high_confidence=True):
    if rooms < 1:
        print('That is unrealistic. Try again.')
        return

    log_est, upper, lower, conf = get_log_estimate(rooms,
                                                   area_demographic,
                                                   distance_from_town,
                                                   close_to_river,
                                                   high_confidence)

    # Convert to today's dollars
    dollar_est = np.e**log_est * 1000 * SCALE_FACTOR
    dollar_hi = np.e**upper * 1000 * SCALE_FACTOR
    dollar_low = np.e**lower * 1000 * SCALE_FACTOR

    # Round the dollar values to nearest thousand
    rounded_est = np.around(dollar_est, -3)
    rounded_hi = np.around(dollar_hi, -3)
    rounded_low = np.around(dollar_low, -3)

    print(f'The estimated property value is {rounded_est}.')
    print(f'At {conf}% confidence the valuation range is')
    print(
        f'USD {rounded_low} at the lower end to USD {rounded_hi} at the high end.')
