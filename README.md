# Basketball Winning Probability
Calculate feature weights such as 2 Point percentage, steals and others to determine win probability. It uses the [sklearn linear regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html) to estimate the feature weights.

## Setup
* Install python
* Install requirements  
  * pip install -r requirements.txt
* Download the repo [here](https://github.com/fsmosca/Basketball-Winning-Probability/archive/refs/heads/main.zip)
* Command line  
  * Generate ranking after group phase but before quarter-final.  
  `python basketball_perf.py ./data/tokyo2021_olympics_basketball_team_stats.csv`
  
  * Generate ranking after quarter-final but before semi-final.  
  `python basketball_perf.py ./data/tokyo2021_olympics_basketball_team_stats_2.csv`
  
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
RES      : game result can be 0 or 1
```

#### Plot
Scatter plot from all data points in the the data file. You need to install matplotlib with the command `pip install matplotlib`.

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
P2_we: 117.82%
P3_we: 33.31%
FT_we: 44.52%
AS_we: 1.59%
RE_we: 1.41%
TO_we: -0.27%
ST_we: 0.85%
intercept: -1.4574659532047058
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
winprob = 1.178*0.6133 + 0.333*0.3566 + 0.445*0.71 + 0.016*23 + 0.014*55 - 0.0027*12 + 0.0085*5 - 1.46
```

#### Summary of win probability before the quarter-finals.
```
        team   winprob
0   Slovenia  0.850260
1        USA  0.769014
2     France  0.673783
3  Australia  0.619803
4  Argentina  0.533384
5      Spain  0.486418
6      Italy  0.467634
7    Germany  0.462015
```

## Tokyo Olympics 2020/2021 Basketball Quarter-final results
```
match: Slovenia - Germany, score: 94 - 70
match: Spain - USA, score: 81 - 95
match: Italy - France, score: 75 - 84
match: Australia - Argentina, score: 97 - 59
```

## Ranking after Quarter-Final
The regression uses the data file `tokyo2021_olympics_basketball_team_stats_2.csv`.

#### Command line
`python basketball_perf.py ./data/tokyo2021_olympics_basketball_team_stats_2.csv`

#### Regression Feature Weights
```
P2_we: 118.30%
P3_we: 61.65%
FT_we: 38.76%
AS_we: 2.05%
RE_we: 1.48%
TO_we: -0.10%
ST_we: 0.92%
intercept: -1.695916059067152
```

#### Ranking Summary before semi-final
```
Win Probability Ranking Summary
        team   winprob
0   Slovenia  0.833057
1        USA  0.737728
2  Australia  0.688941
3     France  0.682080
4      Spain  0.412434
5  Argentina  0.390209
6      Italy  0.383580
7    Germany  0.375616
```

## Credits
* [FIBA Olympics](http://www.fiba.basketball/olympics/men/2020)
