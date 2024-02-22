## Premier League EV Model

This project uses a Poisson model with home and away strength ratings based on 2023/24 season form to estimate the probabilities of all three outcomes of upcoming English Premier League matches.

If you run python main.py 'Home Team', 'Away Team', 'Result', 'Odds'. Replace 'Home Team' with the home team and 'Away Team' with the away team for an upcoming EPL fixture. You will also need to replace 'Result' with either 'home_win', 'away_win' or 'draw' depending on which bet you are interested in as well as replacing 'Odds' with the decimal odds of that particular bet. The script should return the expected value of the bet that you are interested in.

When entering the team name, enter one of the following strings:
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
