"""
Basketball winning probability calculation based on team statistics.

"""


__version__ = '0.5.0'
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
    
    # (2) Define model to use
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

    # Calculate ranking before quarter-finals based on teams' average stats.
    names = ['Slovenia', 'France', 'Australia', 'USA', 'Italy', 'Argentina', 'Germany', 'Spain']
    for name in names:
        namedf = df.loc[(df['CAT'] == 'Average') & (df['NAME'] == name)]
        features = namedf[['P2', 'P3', 'FT', 'AS', 'RE', 'TO', 'ST']]
        winprob = win_probability(modelcoef, modelintercept, features)
        avedata_name.append(name)
        avedata_winprob.append(max(0.001, min(1.0, winprob)))

        print(f'{name} average features and winprob:')
        print(features.to_string(index=False))
        print(f'winprob: {winprob}')
        print()

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
