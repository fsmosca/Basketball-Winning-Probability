# Basketball Winning Probability
Calculate feature weights such as 2 Point percentage, steals and others to determine win probability

## Data
The data file is in data folder. There are team records after 3 games or preliminary stage.

#### Tokyo Mens' Basketball Olympics.
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

#### Legend:
```
P2       : 2 Points percentage
P3       : 3 Points percentage
FT       : Free Throw percentage
AS       : num assists
RE       : num rebounds
TO       : num turnovers
ST       : num steals
```

## Regression Weights
```
Regression Model Feature Weights:
P2_we: 48.346%
P3_we: 11.258%
FT_we: 12.833%
AS_we: 1.974%
RE_we: 2.727%
TO_we: -1.586%
ST_we: 1.979%
intercept: -1.2158539121219145
```

## Formula
```
winprob = P2_we*p2 + P3_we*p3 + FT_we*ft + AS_we*as + RE_we*re + TO_we*to + ST_we*st + intercept
```

## Sample Calculation
#### Model win probability ranking based on team average stats after preliminaries but before quarter-finals.
slovenia team average in 3 games on the features:
```
The 0.613333333 is the average of 2 Points percentage after 3 games in the preliminary.
slovenia_ave = [0.613333333,0.356666667,0.71,23,54.66666667,12,4.666666667]
winprob = 0.48346*0.6133 + 0.11258*0.3566 + 0.12833*0.71 + 0.01974*23 + 0.02727*54.67 - 0.01586*12 + 0.01979*4.67 - 1.2158
```

```
        team   winprob
0   Slovenia  1.000000
1        USA  0.797254
2  Australia  0.683377
3     France  0.664142
4    Germany  0.369150
5      Italy  0.065056
```

#### Legend
```
References:
P2       : 2 Points percentage
P3       : 3 Points percentage
FT       : Free Throw percentage
AS       : num assists
RE       : num rebounds
TO       : num turnovers
ST       : num steals
P2_we    : 2 Point percentage weight
```


## Credits
* [FIBA Olympics](http://www.fiba.basketball/olympics/men/2020)
