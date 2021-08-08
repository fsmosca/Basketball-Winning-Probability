"""
Basketball winning probability calculation based on team statistics.

"""


__version__ = '0.10.0'
__author__ = 'fsmosca'


import sys

import pandas as pd
import sklearn.linear_model
import sklearn.metrics
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def win_probability(modelcoef, modelintercept, features):
    return np.sum(np.multiply(modelcoef, features.to_numpy())) + modelintercept


def main(argv):
    # Check input data file.
    if len(argv) == 0:
        print('usage:')
        print('python basketball_perf.py <data filename>')
        print('python basketball_perf.py ./data/tokyo2021_olympics_basketball_team_stats.csv')
        raise Exception('Missing data file!')

    # (1) Prepare data
    csvfn = argv[0]
    df = pd.read_csv(csvfn)

    # Print all data
    # print(df.to_string())

    # Print data summary
    # print(df.describe().to_string())

    # Plot win probability vs 2 point percentage.
    ax = df.plot.scatter(x='RES', y='2P%', alpha=0.5, title='2 Point Percentage on Win Probability')
    ax.set_xlabel("Win Probability")
    ax.set_ylabel("2 Point Percentage")
    ax.figure.savefig('2p-winprob.pdf')

    # Selected features for multiple linear regression
    reg_features = ['2P%', '3P%', 'FT%', 'OREB', 'DREB', 'AST', 'FO', 'TO', 'STL', 'BLK']
    X = df[reg_features]
    # print(X)

    # Our target or objective value
    y = df['RES']
    # print(y)

    # Split data into training and test for validation.
    # 15% of the data is for testing.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=1)
    
    # (2) Define model to use
    # Ridge - https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge
    models = dict()
    normalize = True  # False, default
    models.update({'Ridge': sklearn.linear_model.Ridge(
        alpha=1.0,
        fit_intercept=True,
        normalize=normalize,
        copy_X=True,
        max_iter=None,
        tol=0.001,
        solver='auto',
        random_state=None)})
    
    # (3) Fit data
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

        modelcoef = model.coef_
        modelintercept = model.intercept_

        print('Regression Model Feature Weights:')
        for i, f in enumerate(reg_features):
            print(f'{f}_we: {modelcoef[i]*100:0.2f}%')
        print(f'intercept: {modelintercept}')
        
        cnt += 1
        print()

        print('Model win probability ranking based on team single and average statistics.')
        avedata_name = []
        avedata_winprob = []

        # Calculate ranking before quarter-finals based on teams' average stats using tokyo2021_olympics_basketball_team_stats.csv.
        # Calculate ranking before semi-finals based on teams' average stats using tokyo2021_olympics_basketball_team_stats_2.csv.
        names = ['Slovenia', 'France', 'Australia', 'USA', 'Italy', 'Argentina', 'Germany', 'Spain',
                 'Japan', 'Iran', 'Nigeria', 'Czech Republic']
        for name in names:
            namedf = df.loc[(df['CAT'] == 'Average') & (df['NAME'] == name)]
            features = namedf[reg_features]
            winprob = win_probability(modelcoef, modelintercept, features)
            avedata_name.append(name)
            avedata_winprob.append(winprob)

            # print(f'{name} average features and winprob:')
            # print(features.to_string(index=False))
            # print(f'winprob: {winprob}')
            # print()

        tdict = {'team': avedata_name, 'winprob': avedata_winprob}

        avedf = pd.DataFrame(tdict)
        avedf = avedf.sort_values(by=['winprob'], ascending=False).reset_index(drop=True)

        print('Win Probability Ranking Summary')
        print(avedf)
        print()

    print(f'Formula:')
    print(f'winprob = 2P%_we*2p + 3P%_we*3p + FT%_we*ft + AST_we*ast + REB_we*reb + TO_we*to + STL_we*stl + intercept')
    print()

    print('References:')
    print('mse      : mean squared error')
    print('mae      : mean absolute error')
    print('r2_score : coefficient of determination')
    print('2PM       : 2 Points Made')
    print('2PA       : 2 Points Attempt')
    print('2P%       : 2 Points percentage')
    print('3P%       : 3 Points percentage')
    print('FT%       : Free Throw percentage')
    print('AST       : num assists')
    print('REB       : num rebounds')
    print('TO        : num turnovers')
    print('STL       : num steals')
    print('2P%_we    : 2 Point percentage weight')


if __name__ == '__main__':
    main(sys.argv[1:])
