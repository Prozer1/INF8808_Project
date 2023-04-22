"""This file contains functions for processing and analyzing data related to goals scored by football teams"""
import pandas as pd

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

    xls = pd.ExcelFile("./datasets/cristiano/goals.xlsx")
    goals_df = sheetX = xls.parse(0)
    
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
