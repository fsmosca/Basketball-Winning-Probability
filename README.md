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
  
  * Generate ranking after semi-final but before final.  
  `python basketball_perf.py ./data/tokyo2021_olympics_basketball_team_stats_3.csv`
  
## Data
There is a selenium python script crawler that can be found under tool folder, that can get data from FIBA. It saves data to csv file similar to files in data folder but without average records.

The data file `tokyo2021_olympics_basketball_team_stats.csv` is in data folder. There are team records after 3 games each team in the preliminary stage.

#### Tokyo Olympics 2020/2021 Basketball Men
```
   PHASE     CAT            NAME             OPP  PTS  FGM  FGA   FG%  2PM  2PA   2P%  3PM  3PA   3P%  FTM  FTA   FT%  OREB  DREB  REB  AST  FO  TO  STL  BLK  +/-  EFF  RES
0  Group  Single            Iran  Czech Republic   78   31   62  0.50   25   43  0.58    6   19  0.32   10   17  0.59     7    26   33   20  18  21    9    1   -6   79  0.0
1  Group  Single  Czech Republic            Iran   84   33   74  0.45   27   44  0.61    6   30  0.20   12   18  0.67    16    27   43   29  17  15   12    2    6  105  1.0
2  Group  Single         Germany           Italy   82   30   64  0.47   15   32  0.47   15   32  0.47    7    9  0.78     9    25   34   15  16  14    6    2  -10   84  0.0
3  Group  Single           Italy         Germany   92   34   68  0.50   19   37  0.51   15   31  0.48    9   12  0.75     9    26   35   20  15   9   11    4   10  112  1.0
4  Group  Single       Australia         Nigeria   84   28   71  0.39   17   47  0.36   11   24  0.46   17   19  0.90    13    31   44   21  20  21   12    1   17   90  1.0
...
```

#### Features considered in multiple linear regression.
```python
X = df[['2P%', '3P%', 'FT%', 'AST', 'OREB', 'DREB', 'TO', 'STL']]
```

You can change the features to include the Fouls and EFF using
```python
X = df[['2P%', '3P%', 'FT%', 'AST', 'OREB', 'DREB', 'TO', 'STL', 'FO', 'EFF']]
```

#### Target is the result.
```python
y = df['RES']
```

#### Legend
```
2PM       : 2 Points Made
2PA       : 2 Points Attempt
2P%       : 2 Points percentage
3P%       : 3 Points percentage
FT%       : Free Throw percentage
AST       : num assists
REB       : num rebounds
TO        : num turnovers
STL       : num steals
2P%_we    : 2 Point percentage weight
```

#### Plot
Scatter plot from all data points in the the data file. You need to install matplotlib with the command `pip install matplotlib`.

##### (1) 2 point percentage plot, higher percentage has higher winning probability.
```python
    # Plot win probability vs 2 point percentage.
    ax = df.plot.scatter(x='RES', y='2P%', alpha=0.5, title='2 Point Percentage on Win Probability')
    ax.set_xlabel("Win Probability")
    ax.set_ylabel("2 Point Percentage")
    ax.figure.savefig('2p-winprob.pdf')
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


## Regression feature weights after group phase but before quarter-final
```
2P%_we: 109.95%
3P%_we: 54.63%
FT%_we: 55.01%
AST_we: 1.55%
OREB_we: 1.36%
DREB_we: 1.96%
TO_we: 0.03%
STL_we: 0.81%
intercept: -1.743135327438301
```

## Formula
```
winprob = 2P%_we*2p + 3P%_we*3p + FT%_we*ft + AST_we*as + OREB_we*oreb + DREB_we*dreb + TO_we*to + STL_we*stl + intercept
```

## Sample Calculation

#### Model win probability ranking based on team average stats after preliminaries but before quarter-finals.
Slovenia team average in 3 games on the features:
```
slovenia_ave = [0.613,0.36,0.71,23,17,38,12,5]

p2% = 0.613
p3% = 0.36
ft% = 0.71
ast = 23
oreb = 17
dreb = 38
to = 12
st = 5
```

```
winprob = 1.1*0.613 + 0.546*0.36 + 0.55*0.71 + 0.016*23 + 0.0136*17 + 0.0196*38 + 0.0003*12 + 0.0081*5 - 1.74
```

#### Summary of win probability before the quarter-final
```
Win Probability Ranking Summary
       team   winprob
0   Slovenia  0.895120
1        USA  0.785697
2     France  0.686635
3  Australia  0.628305
4      Spain  0.557405
5  Argentina  0.525046
6    Germany  0.490459
7      Italy  0.458668
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

#### Regression feature weights after quarter-final but before semi-final
```
2P%_we: 108.01%
3P%_we: 56.97%
FT%_we: 54.93%
AST_we: 1.65%
OREB_we: 1.56%
DREB_we: 2.02%
TO_we: -0.27%
STL_we: 1.00%
intercept: -1.7868833598225142
```

#### Summary of win probability before the semi-final
```
Win Probability Ranking Summary
        team   winprob
0   Slovenia  0.874822
1        USA  0.735948
2     France  0.720355
3  Australia  0.694822
4      Spain  0.497407
5      Italy  0.416237
6  Argentina  0.415951
7    Germany  0.396465
```

#### Tokyo Olympics 2020/2021 Basketball Semi-final results
```
match: USA - Australia, score: 97 - 78
match: France - Slovenia, score: 90 - 89
```

## Ranking after Semi-Final
The regression uses the data file `tokyo2021_olympics_basketball_team_stats_3.csv`.

#### Command line
`python basketball_perf.py ./data/tokyo2021_olympics_basketball_team_stats_3.csv`

#### Regression feature weights after semi-final but before final
```
2P%_we: 99.18%
3P%_we: 73.70%
FT%_we: 64.72%
AST_we: 1.29%
OREB_we: 1.56%
DREB_we: 2.08%
TO_we: -0.29%
STL_we: 1.32%
intercept: -1.8408441099337223

```

#### Summary of win probability before the final
```
Win Probability Ranking Summary
        team   winprob
0   Slovenia  0.781881
1        USA  0.745022
2     France  0.670351
3  Australia  0.609665
4      Spain  0.495007
5      Italy  0.433284
6    Germany  0.418237
7  Argentina  0.417896
```

#### Tokyo Olympics 2020/2021 Basketball final results
```
Gold/Silver:
match: France - USA, score: 82 - 87

Bronze:
match: Slovenia - Australia, score: 93 - 107
```

## Ranking after Final

#### Command line
`python basketball_perf.py ./data/tokyo2021_olympics_basketball_team_stats_4.csv`

#### Features
`reg_features = ['2P%', '3P%', 'FT%', 'OREB', 'DREB', 'AST', 'FO', 'TO', 'STL', 'BLK']`

#### Regression Model Feature Weight Results
```
2P%_we: 105.94%
3P%_we: 75.38%
FT%_we: 50.95%
OREB_we: 1.56%
DREB_we: 1.93%
AST_we: 1.16%
FO_we: -0.06%
TO_we: -0.57%
STL_we: 1.49%
BLK_we: 0.54%
intercept: -1.6896029023867132
```

#### Win Probability Ranking Summary
This ranking is based on average stats per team applying the feature weight results.
```
              team   winprob
0         Slovenia  0.764157
1              USA  0.696443
2           France  0.630511
3        Australia  0.618170
4            Spain  0.496014
5            Italy  0.445323
6        Argentina  0.396582
7          Germany  0.396354
8   Czech Republic  0.384329
9          Nigeria  0.293762
10           Japan  0.288418
11            Iran  0.186147
```

## Credits
* [FIBA Olympics](http://www.fiba.basketball/olympics/men/2020)
