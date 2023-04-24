"""This file contains a function for cleaning and transforming data for visualisation,
   which displays the number of goals scored per game across different age groups by 
   Cristiano Ronaldo.# import necessary libraries"""

import pandas as pd  # pandas for data manipulation
import utils  # custom module for extracting title from column names

def get_data():
    """
    Load data from a CSV file and clean it up for visualization 1.
    Returns:
        group_by_age (pandas.DataFrame): Dataframe with age, total goals, and goals per game.
    """
    # Load data and select only relevant columns
    df = pd.read_csv('./datasets/cristiano/stats.csv')
    
    # Rename columns with proper titles
    for title in df.columns:
        if title.startswith("Unnamed"):
            df.rename(columns={title: df[title][0]}, inplace=True)
        else:
            head_title = utils.extract_title(title)
            df.rename(columns={title: head_title  + '.' + str(df[title][0])}, inplace=True)
    df = df.drop([0])
    df.rename(columns={'Âge': 'Age'}, inplace=True)
    df.rename(columns={'Performance.Buts': 'Buts'}, inplace=True)
    
    # Select relevant columns and convert data types
    goal_stats = df[['Age', 'MJ', 'Buts']]
    goal_stats['Age'] = goal_stats['Age'].astype(int)
    goal_stats['MJ'] = goal_stats['MJ'].astype(int)
    goal_stats['Buts'] = goal_stats['Buts'].astype(int)
    
    # Group by age and calculate total goals and goals per game
    group_by_age = goal_stats.groupby(['Age']).sum().reset_index()
    group_by_age['Goals per game'] = group_by_age['Buts'] / group_by_age['MJ']
    group_by_age.rename(columns={'Buts': 'Total goals'}, inplace=True)
    
    # Return cleaned-up data
    return group_by_age
