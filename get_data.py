import pandas as pd
import plotly.express as px
import utils

def get_data_from_file(file_path):
    # file_name = "./datasets/cr7_goals.xlsx"

    xls = pd.ExcelFile(file_path)

    sheetX = xls.parse(0)
    return sheetX

def goal_ass_stats(player_name):
    """_summary_

    Args:
        player_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    df_goals_ass = pd.read_csv('./datasets/' + player_name + '/stats.csv')
    df_goals_ass = utils.format_dataframe(df_goals_ass)
    goal_ass_stats = df_goals_ass[['Saison', 'Par90minutes.Buts', 'Par90minutes.PD']]
    goal_ass_stats['Par90minutes.Buts'] = goal_ass_stats['Par90minutes.Buts'].astype(float)
    goal_ass_stats['Par90minutes.PD'] = goal_ass_stats['Par90minutes.PD'].astype(float)
    return goal_ass_stats

def shot_stats(player_name):
    """_summary_

    Args:
        player_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    df_shot = pd.read_csv('./datasets/' + player_name + '/shot_creation.csv')[["Season", "SCA90"]]
    return df_shot

def pass_stats(player_name):
    """_summary_

    Args:
        player_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    df_pass = pd.read_csv('./datasets/' + player_name + '/pass.csv')
    df_pass = utils.format_dataframe(df_pass)

    df_pass = df_pass[["Season", "Total.Cmp%"]]
    return df_pass

def group_last_5_years_data(df_shot, df_pass, df_shot_percentage, goal_ass_stats):
    """_summary_

    Args:
        df_shot (_type_): _description_
        df_pass (_type_): _description_
        df_shot_percentage (_type_): _description_
        goal_ass_stats (_type_): _description_

    Returns:
        _type_: _description_
    """
    df_shot = df_shot.tail(5)
    df_pass = df_pass.tail(5)
    df_shot_percentage = df_shot_percentage.tail(5)
    group_by_season = goal_ass_stats.groupby(['Saison']).sum()
    group_by_season = group_by_season.tail(5).reset_index()
    group_by_season['SCA90'] = list(df_shot['SCA90'])
    group_by_season['PassCompletion'] = list(df_pass['Total.Cmp%'])
    group_by_season['SoT%'] = list(df_shot_percentage['Standard.SoT%'])
    return group_by_season

def shot_percentage_stats(player_name):
    """_summary_

    Args:
        player_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    df_shot_percentage = pd.read_csv('./datasets/' + player_name + '/shot.csv')
    df_shot_percentage = utils.format_dataframe(df_shot_percentage)
    df_shot_percentage = df_shot_percentage[["Season", "Standard.SoT%"]]
    return df_shot_percentage

def standarize_df(df, max_goal_ratio, max_assist_ratio, max_sca, max_pass, max_sot):
    """_summary_

    Args:
        df (_type_): _description_
        max_goal_ratio (_type_): _description_
        max_assist_ratio (_type_): _description_
        max_sca (_type_): _description_
        max_pass (_type_): _description_
        max_sot (_type_): _description_

    Returns:
        _type_: _description_
    """
    df['Par90minutes.Buts'] = df['Par90minutes.Buts'] / max_goal_ratio
    df['Par90minutes.PD'] = df['Par90minutes.PD'] / max_assist_ratio
    df['SCA90'] = df['SCA90'] / max_sca
    df['PassCompletion'] = df['PassCompletion'] / max_pass
    df['SoT%'] = df['SoT%'] / max_sot
    return df

def visualisation_1_data():
    """_summary_

    Returns:
        _type_: _description_
    """
    df = pd.read_csv('./datasets/cristiano/stats.csv')
    for title in df.columns:
        if title.startswith("Unnamed"):
            df.rename(columns={title: df[title][0]}, inplace=True)
        else:
            head_title = utils.extract_title(title)
            df.rename(columns={title: head_title  + '.' + str(df[title][0])}, inplace=True)
    df = df.drop([0])
    df.rename(columns={'Âge': 'Age'}, inplace=True)
    df.rename(columns={'Performance.Buts': 'Buts'}, inplace=True)
    goal_stats = df[['Age', 'MJ', 'Buts']]
    goal_stats['Age'] = goal_stats['Age'].astype(int)
    goal_stats['MJ'] = goal_stats['MJ'].astype(int)
    goal_stats['Buts'] = goal_stats['Buts'].astype(int)
    group_by_age = goal_stats.groupby(['Age']).sum().reset_index()
    group_by_age['Goals per game'] = group_by_age['Buts'] / group_by_age['MJ']
    group_by_age.rename(columns={'Buts': 'Total goals'}, inplace=True)
    return group_by_age

def visualisation_6_data():
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

def adjust_players_performance_data(name, df):
    """_summary_

    Args:
        name (_type_): _description_
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    values = []
    for i, row in df.iterrows():
        year = int(i+1)
        data = [row['Par90minutes.Buts'], row['Par90minutes.PD'], row['SCA90'], row['PassCompletion'], row['SoT%'], row['Par90minutes.Buts']]
        values.append({'year': year, 'data': data})
    return {'name': name, 'values': values}
    
def visualisation_2_data():
    """_summary_

    Returns:
        _type_: _description_
    """
    # Get goal/assist statistics for each player
    players = ['cristiano', 'rashford', 'messi', 'suarez', 'costa']
    goal_ass_stats_list = []
    for player in players:
        stats = goal_ass_stats(player)
        if player == 'cristiano':
            stats = stats.drop([23]) # Remove seasons with Alnassr
        goal_ass_stats_list.append(stats)

    # Get shot statistics for each player
    shot_stats_list = []
    for player in players:
        stats = shot_stats(player)
        if player == 'cristiano':
            stats = stats.drop([19, 22]) # Remove seasons with Alnassr
        shot_stats_list.append(stats)

    # Get pass statistics for each player
    pass_stats_list = []
    for player in players:
        stats = pass_stats(player)
        if player == 'cristiano':
            stats = stats.drop([19, 23]) # Remove seasons with Alnassr
        pass_stats_list.append(stats)

    # Get shot percentage statistics for each player
    shot_percentage_stats_list = []
    for player in players:
        stats = shot_percentage_stats(player)
        if player == 'cristiano':
            stats = stats.drop([20, 22]) # Remove seasons with Alnassr
        shot_percentage_stats_list.append(stats)

    # Get last 5 years of statistics for each player
    last_5_years_list = []
    for i in range(len(players)):
        last_5_years = group_last_5_years_data(shot_stats_list[i], pass_stats_list[i], shot_percentage_stats_list[i], goal_ass_stats_list[i])
        last_5_years.drop('Saison', axis=1, inplace=True)
        last_5_years = last_5_years.astype(float)
        last_5_years_list.append(last_5_years)

    # Standardize the data for each player
    max_values_list = []
    for player in last_5_years_list:
        max_values = player.apply(max, axis=0)
        max_values_list.append(max_values)

    concatenated_max_values = pd.concat(max_values_list, axis=1)
    max_goal_ratio, max_assist_ratio, max_sca, max_pass, max_sot = concatenated_max_values.iloc[0:].max(axis=1)

    standardized_data_list = []
    for i in range(len(players)):
        player_data = last_5_years_list[i]
        max_values = max_values_list[i]
        standardized_data = standarize_df(player_data, max_goal_ratio, max_assist_ratio, max_sca, max_pass, max_sot)
        standardized_data_list.append(standardized_data)

    # Adjust player names in the data
    players_list = ['Cristiano Ronaldo', 'Marcus Rashford', 'Lionel Messi', 'Luis Suarez', 'Diego Costa']
    adjusted_data_list = []
    for i in range(len(players)):
        adjusted_data = adjust_players_performance_data(players_list[i], standardized_data_list[i])
        adjusted_data_list.append(adjusted_data)

    return adjusted_data_list

def categorize_team(team_list):
    """Categorizes a list of teams as either club teams or national teams based on the presence of the word 'Portugal' in the list.
    Args:
        team_list (list): A list of teams
    Returns:
        str: A string indicating whether the teams in the list are club teams or national teams.
    """
    return 'OthersWithNT' if 'Portugal' in team_list else 'Others'

def get_goals_data():
    """Reads the goals data from a file and processes it to return a Pandas DataFrame.
    Returns:
        Pandas DataFrame: DataFrame with processed data on goals
    """
    # Read the goals data from a file
    goals_df = get_data_from_file("./datasets/cristiano/goals.xlsx")
    
    # Select only relevant columns from the DataFrame
    goals_df = goals_df[['Clt', 'Comp', 'Équipe']]
    
    # Group the goals data by competition and count the number of goals
    goals_by_comp_df = goals_df.groupby(['Comp'])['Clt'].count().reset_index(name='Goals')
    
    # Group the goals data by competition and list the teams
    teams_by_comp_df = goals_df.groupby(['Comp'])['Équipe'].unique().reset_index().rename(columns={'Comp': 'Competition', 'Équipe': 'Teams'})
    teams_by_comp_df['Teams'] = teams_by_comp_df['Teams'].apply(lambda x: x.tolist())
    
    # Merge the goals data by competition and teams
    merged_data_df = pd.merge(goals_by_comp_df, teams_by_comp_df, left_on='Comp', right_on='Competition').drop('Competition', axis=1)
    
    # Sort the merged data in descending order based on number of goals
    sorted_data_df = merged_data_df.sort_values("Goals", ascending=False)
    
    # Select the top 7 competitions based on number of goals
    top_competitions = sorted_data_df.head(7)['Comp'].tolist()
    
    # Categorize competitions as either top competitions or others
    sorted_data_df['Comp_Category'] = sorted_data_df['Comp'].apply(lambda x: x if x in top_competitions else 'Others')
    
    # Categorize teams as either club or national teams
    sorted_data_df['Team_Category'] = sorted_data_df['Teams'].apply(categorize_team)
    
    # Return the final processed data
    return sorted_data_df

def get_goals_visualization():
    """This function returns a sorted dataframe with aggregated goals, teams and competition data by category.
    Returns:
        df_final (pandas DataFrame): A sorted DataFrame containing goals data grouped by competition category
    """
    # Get goals data and create a copy
    goals_data = get_goals_data().copy()
    
    # Update competition category to use team category if it is 'Others'
    goals_data['Comp_Category'] = goals_data.apply(lambda row: row['Team_Category'] if row['Comp_Category'] == 'Others' else row['Comp_Category'], axis=1)
    
    # Select relevant columns
    goals_data = goals_data[['Comp', 'Goals', 'Teams', 'Comp_Category']]
    
    # Group competitions by category and create a list of competitions for each category
    competitions_by_category = goals_data.groupby(['Comp_Category'])['Comp'].unique().reset_index().rename(columns={'Comp_Category': 'Comp_Category1'})
    competitions_by_category['Comp'] = competitions_by_category['Comp'].apply(lambda x: x.tolist())

    # Sum goals by competition category
    goals_by_category = goals_data.groupby(['Comp_Category'])['Goals'].sum().reset_index(name='Goals')
    
    # Merge competitions and goals data
    merged_data = pd.merge(competitions_by_category, goals_by_category, left_on='Comp_Category1', right_on='Comp_Category').drop('Comp_Category1', axis=1)
    
    # Group teams by competition category and create a list of teams for each category
    teams_by_category = goals_data.groupby('Comp_Category').agg({'Teams': sum}).reset_index().rename(columns={'Comp_Category': 'Comp_Category1'})
    teams_by_category['Teams'] = teams_by_category['Teams'].apply(lambda x: list(set(x)))
    
    # Merge teams and competitions/goals data
    merged_data = pd.merge(teams_by_category, merged_data, left_on='Comp_Category1', right_on='Comp_Category').drop('Comp_Category1', axis=1)
    
    # Sort data by competition category
    df_final = merged_data.sort_values("Comp_Category").rename(columns={'Teams': 'Teams'})
    
    return df_final

def get_goals_by_team_category():
    """Returns a dataframe with the sum of goals scored by national teams and clubs.
    Returns:
        pandas.DataFrame: A dataframe with columns 'Team_Category' and 'Goals', where 'Team_Category' indicates if a team is a national team or a club, and 'Goals' is the sum of goals scored by teams in that category.
    """
    # Get the goals data and make a copy of it
    goals_data = get_goals_data().copy()

    # Map the team categories to 'National Team' or 'Clubs'
    goals_data['Team_Category'] = goals_data['Team_Category'].apply(lambda x: 'National Team' if 'OthersWithNT' in x else 'Clubs')

    # Group the data by team category and get the sum of goals for each category
    goals_by_team_category = goals_data.groupby(['Team_Category'])['Goals'].sum().reset_index(name='Goals')

    return goals_by_team_category

def get_top_assisting_players():
    """
    Loads data about goals and assists, selects relevant columns,
    drops missing values in the assists column, counts the number of
    assists per player, keeps only the top ten players with the most
    assists, and sorts them by player name.
    
    Returns:
        pandas.DataFrame: A DataFrame containing information about the top
        ten players with the highest number of assists.
    """
    # Load data and select only relevant columns
    goals_data = pd.read_excel("./datasets/cristiano/goals.xlsx", usecols=['Clt', 'Passe décisive'])

    # Drop rows with missing values in the 'Passe décisive' column
    goals_data.dropna(subset=['Passe décisive'], inplace=True)

    # Count number of assists per player and sort in descending order
    assists_data = goals_data.groupby('Passe décisive').agg(assists_count=('Clt', 'count')).sort_values('assists_count', ascending=False).reset_index()

    # Keep only the top ten players with the highest number of assists and sort by player name
    top_assisting_players = assists_data.nlargest(10, 'assists_count').sort_values('Passe décisive')
    
    return top_assisting_players

def question_7_ranking_data():
    """_summary_

    Returns:
        _type_: _description_
    """
    # Load raw data
    raw_data = get_data_from_file("./datasets/cr7_club_ranking.xlsx")
    
    # Filter data
    filtered_data = raw_data.filter(['Saison','Équipe', 'CltChamp'], axis=1)
    
    # Convert Ranking to numerical values
    mapping = {'1er': 1, '2e': 2, '3e': 3, '4e': 4, '5e': 5, '6e': 6}
    numerical_rank = filtered_data.replace({'CltChamp': mapping})
    
    # Grouping data by teams
    ranking_df = pd.pivot_table(numerical_rank, index='Saison', columns='Équipe', values='CltChamp')
    
    # Add Column of the current team
    ranking_df['Team'] = ranking_df.idxmax(axis=1)
    
    return ranking_df

def question_7_trophies_data():
    """_summary_

    Returns:
        _type_: _description_
    """
    # Load raw data
    ligue_data = get_data_from_file("./datasets/cr7_ligues_nat.xlsx")
    coup_nat_data = get_data_from_file("./datasets/cr7_coupes_nat.xlsx")
    coup_inter_data = get_data_from_file("./datasets/cr7_coupes_inter.xlsx")
    
    # Get the season, team name, competition, ranking
    filtered_ligue_data = ligue_data.filter(['Saison','Équipe', 'Comp', 'CltChamp'], axis=1)
    filtered_coup_nat_data = coup_nat_data.filter(['Saison','Équipe', 'Comp', 'CltChamp'], axis=1).fillna(0)
    filtered_coup_inter_data = coup_inter_data.filter(['Saison','Équipe', 'Comp', 'CltChamp'], axis=1)
    
    # Merge all competition categories
    merged_df = pd.merge(pd.merge(filtered_ligue_data, filtered_coup_nat_data, how="outer"), filtered_coup_inter_data, how="outer")
    
    # Replace "W" or "1er" with 1 and others with 0 in the specified columns
    merged_df[['CltChamp']] = merged_df[['CltChamp']].replace(['W', '1er'], 1)
    merged_df[['CltChamp']] = merged_df[['CltChamp']].replace(to_replace=r'\b(?!1\b)(?!W\b)\w+\b', value=0, regex=True)
    
    # filter the rows where CltChamp = 1, group by Saison and aggregate the Comp names
    trophies_df = merged_df[merged_df['CltChamp'] == 1].groupby(['Saison','Équipe'])['Comp'].agg(list)
    
    # Reset the index and rename the additional column
    trophies_df = trophies_df.reset_index().rename(columns={'value': 'Comp'})
    
    # Count trophies for each season
    trophies_df['Comp_count'] = trophies_df['Comp'].apply(lambda x: len(x))

    return trophies_df
    
def get_goals_by_minute(file_path):
    """Get the number of goals scored by minute

    Returns:
        dataframe: Pandas DF with Minute and Count as columns
    """
    # Load raw data
    raw_data = get_data_from_file(file_path)
    
    # Filter data
    filtered_data = raw_data.filter(['Date', 'Minute'], axis=1)
    
    # Count goals per minute
    goal_by_minute = filtered_data.groupby(['Minute']).count()
    
    # Remove extra time because it's not relevent as data
    goal_by_minute = goal_by_minute[~goal_by_minute.index.str.contains('\+')]
    
    # Sort Index
    goal_by_minute.index = pd.to_numeric(goal_by_minute.index)
    goal_by_minute = goal_by_minute.sort_index()
    
    return goal_by_minute.loc[:90]
    
def get_goals_by_type(file_path):
    """ Get the number of goals scored by type, per year

    Returns:
        dataframe: Pandas DF with Date, Type and Count as columns
    """
    all_goals = get_data_from_file(file_path)
    filtered_data = all_goals.filter(['Date','Type'], axis=1)
    for count, date in enumerate(filtered_data.Date):
        date = date.split('/')
        if len(date) == 1:
            date = date[0].split('-')
        filtered_data.Date[count] = '20'+date[2]
    filtered_data['Count'] = filtered_data.groupby(['Date', 'Type'])['Type'].transform('count')
    filtered_data = filtered_data.dropna(subset=['Type'])
    filtered_data = filtered_data.drop_duplicates()
    # Add rows with 0 count for the years where the type of goal is not present
    for year in range(2002, 2023):
        for type in filtered_data.Type.unique():
            if not filtered_data[(filtered_data['Date'] == str(year)) & (filtered_data['Type'] == type)].empty:
                continue
            filtered_data = filtered_data.append({'Date': str(year), 'Type': type, 'Count': 0}, ignore_index=True)

    # Drop the rows where the Type is Solo Run or Penalty rebound or counter attack or deflected shot on goal
    filtered_data = filtered_data[~filtered_data['Type'].isin(['Solo run', 'Penalty rebound', 'Counter attack goal', 'Deflected shot on goal'])]
    filtered_data = filtered_data.sort_values(by=['Date'])
    return filtered_data

