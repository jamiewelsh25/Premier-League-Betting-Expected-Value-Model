import requests
from selenium import webdriver
import os
import pandas as pd
import numpy as np
import warnings
from scipy.stats import poisson

# Ignore all warnings
warnings.filterwarnings("ignore")

def download_csv():
    # Edit chromedriver options to save csv file to current directory
    options=webdriver.ChromeOptions()
    prefs={"download.default_directory":"/Users/jamiewelsh/Python/football"}
    options.add_experimental_option("prefs",prefs)

    # URL to fetch csv file from
    url = "https://fixturedownload.com/download/csv/epl-2023"

    # Create a new instance of the Chrome web browser
    driver = webdriver.Chrome(options=options)

    # Open the webpage
    driver.get(url)

    # Quit chromedriver
    driver.quit()

    # Rename the csv file
    os.rename('epl-2023-GMTStandardTime.csv', 'EPL_results_2024.csv')


def get_prediction_df():
    # Get the list of files in the current directory
    files = os.listdir()

    # Filter CSV files
    csv_files = [file for file in files if file.endswith('.csv')]

     # Get the name of the CSV file
    csv_filename = csv_files[0]

    # Load csv file of EPL fixtures and results
    df = pd.read_csv('EPL_results_2024.csv')

    # Splitting the DataFrame based on the 'result' column
    results = df.dropna(subset=['Result'])
    fixtures = df[df['Result'].isna()]

    # Splitting the 'result' column into 'FTGH' and 'FTGA' (corresponding to full-time goals home and full-time goals away)
    results[['FTHG', 'FTAG']] = results['Result'].str.split(' - ', expand=True)

    # Converting the 'FTGH' and 'FTGA' columns to integers
    results['FTHG'] = results['FTHG'].astype(int)
    results['FTAG'] = results['FTAG'].astype(int)

    for i, row in results.iterrows():
        if row['FTHG'] > row['FTAG']:
            results.at[i, 'Result'] = 'H'
        elif row['FTHG'] < row['FTAG']:
            results.at[i, 'Result'] = 'A'
        else: 
            results.at[i, 'Result'] = 'D'

    # Group by home teams to find average goals for and against for every EPL team home and away
    home_teams = results.groupby('Home Team').agg({'FTHG': 'mean', 'FTAG': 'mean', 'Date': 'count'}).rename({'Date':'GP'}, axis=1).reset_index()
    away_teams = results.groupby('Away Team').agg({'FTHG': 'mean', 'FTAG': 'mean', 'Date': 'count'}).rename({'Date':'GP'}, axis=1).reset_index()

    # Calculate league average goals by thew home and away teams
    league_average_home = np.average(home_teams['FTHG'], weights=home_teams['GP'])
    league_average_away = np.average(away_teams['FTAG'], weights=away_teams['GP'])

    # Caculate offensive and defensive strength ratings for the home and away teams
    home_teams['o_strength'] = home_teams['FTHG']/league_average_home
    home_teams['d_strength'] = home_teams['FTAG']/league_average_away
    away_teams['o_strength'] = away_teams['FTAG']/league_average_away
    away_teams['d_strength'] = away_teams['FTHG']/league_average_home

    # Change date column to pandas datetime format and sort from soonest fixture onwards
    fixtures['Date'] = pd.to_datetime(fixtures['Date'], format='%d/%m/%Y %H:%M')
    fixtures.sort_values(by='Date', inplace=True)
    fixtures.reset_index(drop=True, inplace=True)

    # Initialize columns for home expected goals, away expected goals, and probabilities in the fixtures DataFrame
    fixtures['home_xg'] = 0
    fixtures['away_xg'] = 0
    fixtures['home_win%'] = 0
    fixtures['away_win%'] = 0
    fixtures['draw%'] = 0

    # Initialize an empty list to store unique team names
    teams = []

    # Iterate over each row in the fixtures DataFrame
    for i, row in fixtures.iterrows():
        # Check if the home team is already in the list of teams
        if row['Home Team'] in teams:
            # If yes, continue to the next iteration of the loop
            continue
        else:
            # If no, add the home team to the list of teams
            teams.append(row['Home Team'])

        # Check if the away team is already in the list of teams
        if row['Away Team'] in teams:
            # If yes, continue to the next iteration of the loop
            continue
        else:
            # If no, add the away team to the list of teams
            teams.append(row['Away Team'])

        # Find home and away teams o/d strength from results tables
        home_o_strength = home_teams[home_teams['Home Team'] == row['Home Team']]['o_strength'].item()
        home_d_strength = home_teams[home_teams['Home Team'] == row['Home Team']]['d_strength'].item()
        away_o_strength = away_teams[away_teams['Away Team'] == row['Away Team']]['o_strength'].item()
        away_d_strength = away_teams[away_teams['Away Team'] == row['Away Team']]['d_strength'].item()

        # Calculate home and away team expected goals
        home_xg = home_o_strength * away_d_strength * league_average_home
        away_xg = away_o_strength * home_d_strength * league_average_away
        fixtures.loc[i, 'home_xg'] = home_xg
        fixtures.loc[i, 'away_xg'] = away_xg

        # Generate the range of values from 0 to 9
        values = np.arange(10)

        # Calculate the home and away probability distribution using the Poisson PMF
        probabilities_home = poisson.pmf(values, home_xg)
        probabilities_away = poisson.pmf(values, away_xg)

        # Create porbability matrix by broadcasting
        matrix = np.outer(probabilities_home, probabilities_away)

        # Initialize variables to store probabilities
        home_win_prob = 0.0
        away_win_prob = 0.0
        draw_prob = 0.0

        # Iterate over the matrix to calculate probabilities
        for j in range(matrix.shape[0]):
            for k in range(matrix.shape[1]):
                if j > k:
                    home_win_prob += matrix[j, k]
                elif j < k:
                    away_win_prob += matrix[j, k]
                else:
                    draw_prob += matrix[j, k]

        # Assign the calculated probabilities (in percentage) to the corresponding columns in the fixtures DataFrame
        fixtures.at[i, 'home_win%'] = home_win_prob * 100
        fixtures.at[i, 'away_win%'] = away_win_prob * 100
        fixtures.at[i, 'draw%'] = draw_prob * 100

        # Check if the number of unique teams is equal to 20
        if len(teams) == 20:
            # If yes, exit the loop
            break
    
    # Get dataframe of predictions
    predictions = fixtures.drop(['Match Number', 'Round Number', 'Location', 'Result'], axis=1)
    predictions = predictions[predictions['home_xg'] != 0]

    return predictions

def get_bet_ev(fixtures_df, home_team, away_team, result, odds):
    game = fixtures_df[fixtures_df['Home Team'] == home_team][fixtures_df['Away Team'] == away_team]
    if len(game) == 0:
        return "Cannot Make Predictions for This Game"

    else:
        if result == "home_win":
            home_win_percentage = game['home_win%'].item()
            ev = ((home_win_percentage*odds)/100)-1
        elif result == "away_win":
            away_win_percentage = game['away_win%'].item()
            ev = ((away_win_percentage*odds)/100)-1
        elif result == "draw":
            draw_percentage = game['draw%'].item()
            ev = ((draw_percentage*odds)/100)-1
        else:
            return "Invalid result, please enter one of the following: {home_win, away_win, draw}"

        return f"Expected Value of betting £1 on {result} at odds of {odds} is: £{np.round(ev, 3)}"
