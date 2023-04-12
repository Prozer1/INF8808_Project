import pandas as pd
import plotly.express as px

def get_data_from_file(file_name):
    # file_name = "./datasets/cr7_goals.xlsx"

    xls = pd.ExcelFile(file_name)

    sheetX = xls.parse(0)
    return sheetX

def question_1_data():
    goal_data = get_data_from_file("./datasets/cr7_goals.xlsx")
    filtered_data = goal_data.filter(['Date','Comp','Équipe', 'Partie du corps', 'Distance', 'Minute'], axis=1)
    return filtered_data

def question_7_ranking_data():
    # Load raw data
    raw_data = get_data_from_file("./datasets/cr7_club_ranking.xlsx")
    
    # Filter data
    filtered_data = raw_data.filter(['Saison','Équipe', 'CltChamp'], axis=1)
    
    # Convert Ranking to numerical values
    mapping = {'1er': 1, '2e': 2, '3e': 3, '4e': 4, '5e': 5, '6e': 6}
    numerical_rank = filtered_data.replace({'CltChamp': mapping})
    
    # Grouping data by teams
    ranking_df = pd.pivot_table(numerical_rank, index='Saison', columns='Équipe', values='CltChamp')
    
    return ranking_df

def question_7_trophies_data():
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
    
    # Count trophies for each season
    count = merged_df.groupby(['Saison', 'Équipe'])['CltChamp'].sum()
    
    # Reset the index and rename the additional column
    trophies_df = count.reset_index().rename(columns={'value': 'Count'})

    # Grouping data by teams
    trophies_df = pd.pivot_table(trophies_df, index='Saison', columns='Équipe', values='CltChamp')

    return trophies_df
    
def question_8_data():
    # Load raw data
    raw_data = get_data_from_file("./datasets/all_goals.xlsx")
    
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
    
def question_9_data():
    """This is the function to get the data and filters it to answer the question 9.

    Returns:
        dataframe: Pandas DF with Date, Type and Count as columns
    """
    all_goals = get_data_from_file("./datasets/all_goals.xlsx")
    filtered_data = all_goals.filter(['Date','Type'], axis=1)
    # for count, date in enumerate(filtered_data.Date):
    #     date = date.split('/')
    #     if len(date) == 1:
    #         date = date[0].split('-')
    #     filtered_data.Date[count] = '20'+date[2]
    # filtered_data['Count'] = filtered_data.groupby(['Date', 'Type'])['Type'].transform('count')
    # filtered_data = filtered_data.dropna(subset=['Type'])
    # filtered_data = filtered_data.drop_duplicates()
    # # Add rows with 0 count for the years where the type of goal is not present
    # for year in range(2002, 2023):
    #     for type in filtered_data.Type.unique():
    #         if not filtered_data[(filtered_data['Date'] == str(year)) & (filtered_data['Type'] == type)].empty:
    #             continue
    #         filtered_data = filtered_data.append({'Date': str(year), 'Type': type, 'Count': 0}, ignore_index=True)
    
    # # Drop the rows where the Type is Solo Run or Penalty rebound or counter attack or deflected shot on goal
    # filtered_data = filtered_data[~filtered_data['Type'].isin(['Solo run', 'Penalty rebound', 'Counter attack goal', 'Deflected shot on goal'])]
    # filtered_data = filtered_data.sort_values(by=['Date'])
    return filtered_data
