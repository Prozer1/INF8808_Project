import pandas as pd
import plotly.express as px
import utils

def get_data_from_file(file_name):
    # file_name = "./datasets/cr7_goals.xlsx"

    xls = pd.ExcelFile(file_name)

    sheetX = xls.parse(0)
    return sheetX


def visualisation_1_data():
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

def visualisation_2_data():
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
    
def categorize_team(team_list):
    return 'OthersWithNT' if 'Portugal' in team_list else 'Others'

def get_visualization_data():
    df = get_data_from_file("./datasets/cristiano/goals.xlsx")
    df = df[['Clt', 'Comp', 'Équipe']]
    goals_by_comp = df.groupby(['Comp'])['Clt'].count().reset_index(name='Goals')
    teams_by_comp = df.groupby(['Comp'])['Équipe'].unique().reset_index().rename(columns={'Comp': 'Comp_teams', 'Équipe': 'Teams'})
    teams_by_comp['Teams'] = teams_by_comp['Teams'].apply(lambda x: x.tolist())
    merged_data = pd.merge(goals_by_comp, teams_by_comp, left_on='Comp', right_on='Comp_teams').drop('Comp_teams', axis=1)
    df_sorted = merged_data.sort_values("Goals", ascending=False)

    top_comps = df_sorted.head(7)['Comp'].tolist()
    df_sorted['Comp_Category'] = df_sorted['Comp'].apply(lambda x: x if x in top_comps else 'Others')
    df_sorted['Team_Category'] = df_sorted['Teams'].apply(categorize_team)
    return df_sorted

def visualization_4():
    df_sorted = get_visualization_data().copy()
    df_sorted['Comp_Category'] = df_sorted.apply(lambda row: row['Team_Category'] if row['Comp_Category'] == 'Others' else row['Comp_Category'], axis=1)
    df_sorted = df_sorted[['Comp', 'Goals', 'Teams', 'Comp_Category']]

    comps_by_category = df_sorted.groupby(['Comp_Category'])['Comp'].unique().reset_index().rename(columns={'Comp_Category': 'Comp_Category1'})
    comps_by_category['Comp'] = comps_by_category['Comp'].apply(lambda x: x.tolist())

    goals_by_category = df_sorted.groupby(['Comp_Category'])['Goals'].sum().reset_index(name='Goals')
    merged_data = pd.merge(comps_by_category, goals_by_category, left_on='Comp_Category1', right_on='Comp_Category').drop('Comp_Category1', axis=1)

    teams_by_category = df_sorted.groupby('Comp_Category').agg({'Teams': sum}).reset_index().rename(columns={'Comp_Category': 'Comp_Category1'})
    teams_by_category['Teams'] = teams_by_category['Teams'].apply(lambda x: list(set(x)))
    merged_data = pd.merge(teams_by_category, merged_data, left_on='Comp_Category1', right_on='Comp_Category').drop('Comp_Category1', axis=1).drop('Teams', axis=1)

    df_final = merged_data.sort_values("Comp_Category").rename(columns={'Teams': 'Teams'})
    return df_final

def visualization_5():
    df_team_sorted = get_visualization_data().copy()
    df_team_sorted['Team_Category'] = df_team_sorted['Team_Category'].apply(lambda x: 'National Team' if 'OthersWithNT' in x else 'Clubs')

    goals_by_team_category = df_team_sorted.groupby(['Team_Category'])['Goals'].sum().reset_index(name='Goals')
    return goals_by_team_category

def visualization_10() : 
    # Load data and select only relevant columns
    df_assist = pd.read_excel("./datasets/cristiano/goals.xlsx", usecols=['Clt', 'Passe décisive'])

    # Drop rows with missing values in the 'Passe décisive' column
    df_assist.dropna(subset=['Passe décisive'], inplace=True)

    # Count number of goals per player and sort in descending order
    df_assist = df_assist.groupby('Passe décisive').agg(nbPasse=('Clt', 'count')).sort_values('nbPasse', ascending=False).reset_index()

    # Keep only the top ten players with the highest number of assists and sort by player name
    df_assist = df_assist.nlargest(10, 'nbPasse').sort_values('Passe décisive')
    
    return df_assist

    
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



if __name__ == "__main__":
   print(visualization_10())