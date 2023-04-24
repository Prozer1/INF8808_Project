import pandas as pd
def get_opponents():
    """_summary_

    Returns:
        _type_: _description_
    """
    df = pd.DataFrame()
    for i in range(2002, 2023):
        df = pd.concat([df, pd.read_csv("./datasets/matches/" + str(i) + "-" + str(i+1) + ".csv")[['Date', 'Adversaire', 'Buts', 'PD']]])
    df = df.dropna(subset=['Date'])
    df['PD'].fillna(0, inplace=True)
    # Group the dataframe by team and aggregate the total Buts and PD, as well as the number of matches played
    team_stats = df.groupby('Adversaire').agg({'Buts': 'sum', 'PD': 'sum', 'Date': 'count'})
    # Rename the 'Date' column to 'Matches'
    team_stats.rename(columns={'Date': 'Matches'}, inplace=True)
    # Print the resulting dataframe
    team_stats = team_stats.sort_values('Matches', ascending=False)
    team_stats = team_stats.iloc[:15].reset_index()
    return team_stats