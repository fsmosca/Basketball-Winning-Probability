"""
Basketball winning probability calculation based on team statistics.

"""


__version__ = '0.8.1'
__author__ = 'fsmosca'


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


def main():   
    # (1) Prepare data
    csvfn = './data/tokyo2021_olympics_basketball_team_stats.csv'
    df = pd.read_csv(csvfn)

    # Print all data
    # print(df.to_string())

    # Plot win probability vs 2 point percentage.
    ax = df.plot.scatter(x='RES', y='P2', alpha=0.5, title='2 Point Percentage on Win Probability')
    ax.set_xlabel("Win Probability")
    ax.set_ylabel("2 Point Percentage")
    ax.figure.savefig('p2-winprob.pdf')

    # Selected features for multiple linear regression
    reg_features = ['P2', 'P3', 'FT', 'AS', 'RE', 'TO', 'ST']
    # P2=2-Point %, P3=3-Point %, FT=Free Throw %, AS=assists, Re=Rebound, TO=Turnovers, ST=Steals
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

        print('Model win probability ranking based on team average stats after preliminaries but before quarter-finals.')
        avedata_name = []
        avedata_winprob = []

        # Calculate ranking before quarter-finals based on teams' average stats.
        names = ['Slovenia', 'France', 'Australia', 'USA', 'Italy', 'Argentina', 'Germany', 'Spain']
        for name in names:
            namedf = df.loc[(df['CAT'] == 'Average') & (df['NAME'] == name)]
            features = namedf[reg_features]
            winprob = win_probability(modelcoef, modelintercept, features)
            avedata_name.append(name)
            avedata_winprob.append(winprob)

            print(f'{name} average features and winprob:')
            print(features.to_string(index=False))
            print(f'winprob: {winprob}')
            print()

        tdict = {'team': avedata_name, 'winprob': avedata_winprob}

        avedf = pd.DataFrame(tdict)
        avedf = avedf.sort_values(by=['winprob'], ascending=False).reset_index(drop=True)

        print('Win Probability Ranking Summary before quarter-finals')
        print(avedf)
        print()

    print(f'Formula:')
    print(f'winprob = P2_we*p2 + P3_we*p3 + FT_we*ft + AS_we*as + RE_we*re + TO_we*to + ST_we*st + intercept')
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
