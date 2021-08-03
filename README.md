# Basketball Winning Probability
Calculate feature weights such as 2 Point percentage, steals and others to determine win probability. It uses the [sklearn linear regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html) to estimate the feature weights.

## Setup
* Install python
* Install requirements  
  * pip install -r requirements.txt
* Download the repo [here](https://github.com/fsmosca/Basketball-Winning-Probability/archive/refs/heads/main.zip)
* Command line  
  `python basketball_perf.py`
  
## Data
The data file `tokyo2021_olympics_basketball_team_stats.csv` is in data folder. There are team records after 3 games each team in the preliminary stage.

#### Tokyo Olympics 2020/2021 Basketball Men
```
        CAT            NAME             OPP        P2        P3        FT         AS         RE         TO         BL         ST    RES
0    Single       Argentina        Slovenia  0.620000  0.160000  0.840000  20.000000  32.000000  10.000000   2.000000  12.000000  0.000
1    Single        Slovenia       Argentina  0.630000  0.370000  0.670000  17.000000  59.000000  19.000000   4.000000   3.000000  1.000
2    Single        Slovenia           Japan  0.680000  0.380000  0.680000  27.000000  54.000000   7.000000   4.000000   5.000000  1.000
...
```

#### Features considered in multiple linear regression.
```python
X = df[['P2', 'P3', 'FT', 'AS', 'RE', 'TO', 'ST']]
```

#### Target is the result.
```python
y = df['RES']
```

#### Legend
```
P2       : 2 Points percentage
P3       : 3 Points percentage
FT       : Free Throw percentage
AS       : num assists
RE       : num rebounds
TO       : num turnovers
ST       : num steals
```

#### Plot
Scatter plot from all data points in the the data file.
You need to install matplot plot lib with the command `pip install matplotlib`.

##### (1) 2 point percentage plot, higher percentage has higher winning probability.
```python
    # Plot win probability vs 2 point percentage.
    ax = df.plot.scatter(x='RES', y='P2', alpha=0.5, title='2 Point Percentage on Win Probability')
    ax.set_xlabel("Win Probability")
    ax.set_ylabel("2 Point Percentage")
    ax.figure.savefig('p2-winprob.pdf')
```
    
![winprob-p2](https://user-images.githubusercontent.com/22366935/127969585-ba456933-fb65-4dc9-b994-d1a0082c2b3c.png)

***

##### (2) Turnover plot, higher turnovers has lower winning probability.
```python
    ax = df.plot.scatter(x='RES', y='TO', alpha=0.5, title='Turnovers on Win Probability')
    ax.set_xlabel("Win Probability")
    ax.set_ylabel("Turnovers")
    ax.figure.savefig('to-winprob.pdf')
```

![turnover](https://user-images.githubusercontent.com/22366935/127970286-c67ba9ba-41e2-4e1c-809c-a5c8ed43b1ca.png)


## Regression Weights
```
Regression Model Feature Weights Results:
P2_we: 55.978%
P3_we: 12.094%
FT_we: 23.039%
AS_we: 2.703%
RE_we: 2.936%
TO_we: -0.725%
ST_we: 2.284%
intercept: -1.7308056325819758
```

## Formula
```
winprob = P2_we*p2 + P3_we*p3 + FT_we*ft + AS_we*as + RE_we*re + TO_we*to + ST_we*st + intercept
```

## Sample Calculation

#### Model win probability ranking based on team average stats after preliminaries but before quarter-finals.
Slovenia team average in 3 games on the features:
```
slovenia_ave = [0.613333333,0.356666667,0.71,23,55,12,5]

The 0.613333333 is the average of 2 Points percentage after 3 games in the preliminary.
p3 = 0.356666667
ft = 0.71
as = 23
re = 55
to = 12
st = 5
```

```
winprob = 0.56*0.6133 + 0.12*0.3566 + 0.23*0.71 + 0.027*23 + 0.03*55 - 0.007*12 + 0.02*5 - 1.73
```

#### Summary of win probability before the quarter-finals.
```
        team   winprob
0   Slovenia  1.000000
1        USA  0.806730
2  Australia  0.700358
3     France  0.697910
4  Argentina  0.549768
5      Spain  0.408472
6      Italy  0.388679
7    Germany  0.346867
```

## Tokyo Olympics 2020/2021 Basketball Quarter-final results
```
match: Slovenia - Germany, score: 94 - 70
match: Spain - USA, score: 81 - 95
match: Italy - France, score: 75 - 84
match: Australia - Argentina, score: ? - ?
```

## Credits
* [FIBA Olympics](http://www.fiba.basketball/olympics/men/2020)
