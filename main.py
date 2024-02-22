from functions import download_csv
from functions import get_prediction_df
from functions import get_bet_ev
import sys
import pandas as pd
import numpy as np


if __name__ == "__main__":
    # Donwload latest fixtures/results and get the predictions from the poisson strengbth model
    download_csv()
    fixtures = get_prediction_df()

    # Check if the number of command-line arguments is correct
    if len(sys.argv) != 5:
        print("Usage: python main.py team1 team2 bet_type odds")
        sys.exit(1)

    # Extracting command-line arguments
    team1 = sys.argv[1]
    team2 = sys.argv[2]
    bet_type = sys.argv[3]
    odds = float(sys.argv[4])

    # Calling get_bet_ev with command-line arguments
    print(get_bet_ev(fixtures, team1, team2, bet_type, odds))
   




        



