"""
Basketball winning probability calculation based on team statistics.

"""


__version__ = '0.1.0'


import pandas as pd
import sklearn.linear_model
import sklearn.metrics
from sklearn.model_selection import train_test_split
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def main():   
    # (1) Prepare data
    csvfn = './data/tokyo2021_olympics_basketball_team_stats.csv'
    df = pd.read_csv(csvfn)

    print(df.to_string())

    # Selected features for multiple linear regression
    # P2=2-Point %, P3=3-Point %, FT=Free Throw %, AS=assists, Re=Rebound, TO=Turnovers, ST=Steals
    X = df[['P2', 'P3', 'FT', 'AS', 'RE', 'TO', 'ST']]
    # print(X)

    # Our target or objective value
    y = df['RES']
    # print(y)

    # Split data into training and test for validation.
    # 15% of the data is for testing.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=1)
    
    # models
    # Ridge - https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ridge_regression.html?highlight=ridge#sklearn.linear_model.ridge_regression
    models = dict()
    models.update({'Ridge': sklearn.linear_model.Ridge()})
    
    # (3) Fit data
    modelcoef = None
    modelintercept = None
    cnt = 0

    for k, model in models.items():
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        # Regression metrics
        mse = sklearn.metrics.mean_squared_error(y_test, y_pred)        
        mae = sklearn.metrics.mean_absolute_error(y_test, y_pred)
        r2_score = sklearn.metrics.r2_score(y_test, y_pred)
        
        print(f'model {cnt+1}: {k}')  
        print('=======================\n')
        
        print('Metrics:')
        print(f'mse: {mse}')
        print(f'mae: {mae}') 
        print(f'r2_score: {r2_score}\n')

        print('Regression Model Feature Weights:')
        print(f'P2_we: {model.coef_[0]*100:0.3f}%')
        print(f'P3_we: {model.coef_[1]*100:0.3f}%')
        print(f'FT_we: {model.coef_[2]*100:0.3f}%')
        print(f'AS_we: {model.coef_[3]*100:0.3f}%')
        print(f'RE_we: {model.coef_[4]*100:0.3f}%')
        print(f'TO_we: {model.coef_[5]*100:0.3f}%')
        print(f'ST_we: {model.coef_[6]*100:0.3f}%')
        
        cnt += 1
        modelcoef = np.array(model.coef_)
        modelintercept = model.intercept_
        print(f'intercept: {modelintercept}')
        print()

    print(f'Formula:')
    print(f'winprob = P2_we*p2 + P3_we*p3 + FT_we*ft + AS_we*as + RE_we*re + TO_we*to + ST_we*st + intercept')
    print()

    print('Model win probability ranking based on team average stats after preliminaries but before quarter-finals.')
    avedata_name = []
    avedata_winprob = []

    # Teams average preliminary stats:
    # The 0.613333333 is the average of 2 Points percentage after 3 games in the preliminary.
    slovenia_ave = np.array([0.613333333,0.356666667,0.71,23,54.66666667,12,4.666666667])
    winprob = np.sum(np.multiply(modelcoef, slovenia_ave)) + modelintercept
    avedata_name.append('Slovenia')
    avedata_winprob.append(max(0.001, min(1.0, winprob)))

    france_ave = np.array([0.596666667,0.376666667,0.776666667,23,39.66666667,15,7.666666667])
    winprob = np.sum(np.multiply(modelcoef, france_ave)) + modelintercept
    avedata_name.append('France')
    avedata_winprob.append(max(0.001, min(1.0, winprob)))

    australia_ave = np.array([0.51,0.386666667,0.86,23,38.66666667,12.66666667,9.666666667])
    winprob = np.sum(np.multiply(modelcoef, australia_ave)) + modelintercept
    avedata_name.append('Australia')
    avedata_winprob.append(max(0.001, min(1.0, winprob)))

    usa_ave = np.array([0.61,0.426666667,0.816666667,27,37,9.333333333,8.666666667])
    winprob = np.sum(np.multiply(modelcoef, usa_ave)) + modelintercept
    avedata_name.append('USA')
    avedata_winprob.append(max(0.001, min(1.0, winprob)))

    italy_ave = np.array([0.4075,0.265,0.6225,13,26.25,6.75,5.5])
    winprob = np.sum(np.multiply(modelcoef, italy_ave)) + modelintercept
    avedata_name.append('Italy')
    avedata_winprob.append(max(0.001, min(1.0, winprob)))

    germany_ave = np.array([0.523333333,0.42,0.846666667,16,38,17.33333333,5])
    winprob = np.sum(np.multiply(modelcoef, germany_ave)) + modelintercept
    avedata_name.append('Germany')
    avedata_winprob.append(max(0.001, min(1.0, winprob)))

    tdict = {'team': avedata_name, 'winprob': avedata_winprob}

    avedf = pd.DataFrame(tdict)
    avedf = avedf.sort_values(by=['winprob'], ascending=False).reset_index(drop=True)
    print(avedf)

    print()
    print('References:')
    print('mse      : mean squared error')
    print('mae      : mean absolute error')
    print('r2_score : coefficient of determination')
    print('P2       : 2 Points percentage')
    print('P3       : 3 Points percentage')
    print('FT       : Free Throw percentage')
    print('AS       : num assists')
    print('RE       : num rebounds')
    print('TO       : num turnovers')
    print('ST       : num steals')
    print('P2_we    : 2 Point percentage weight')


if __name__ == '__main__':
    main()
