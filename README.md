## Premier League EV Model

Tired of relying on gut feeling or generic predictions? This project brings you a powerful tool for analysing upcoming English Premier League matches. It uses a unique Poisson model that considers each team's home and away form based on the current season's data. Get data-driven win, draw, and loss probabilities to inform your bets or fantasy picks!

You will need to have Python 3.8 or higher installed along with NumPy, Pandas, SciPy and Selenium to run my code. In order to generate an expected value for a bet, run the following script:

python main.py 'Home Team' 'Away Team' Result Odds

Replace 'Home Team' with the home team and 'Away Team' with the away team for an upcoming EPL fixture. You will also need to replace Result with either 'home_win', 'away_win' or 'draw' depending on which bet you are interested in as well as replacing Odds with the decimal odds of that particular bet. The script should return the expected value of the bet that you are interested in.

When entering the home and away team names, use the following strings:
'Arsenal',
'Aston Villa',
'Bournemouth',
'Brentford',
'Brighton',
'Burnley',
'Chelsea',
'Crystal Palace',
'Everton',
'Fulham',
'Liverpool',
'Luton',
'Man City',
'Man Utd',
'Newcastle',
'Nottingham Forest',
'Sheffield Utd',
'Spurs',
'West Ham',
'Wolves'

The result_predictor.ipynb notebook is included in the repo so that you can see how the Poisson results model works step-by-step. 
