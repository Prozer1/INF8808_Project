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

def question_1_data():
    goal_data = get_data_from_file("./datasets/cr7_goals.xlsx")
    filtered_data = goal_data.filter(['Date','Comp','Équipe', 'Partie du corps', 'Distance', 'Minute'], axis=1)
    return filtered_data

def question_7_data():
    raw_data = get_data_from_file("./datasets/cr7_club_ranking.xlsx")
    filtered_data = raw_data.filter(['Saison','Équipe', 'CltChamp'], axis=1)
    mapping = {'1er': 1, '2e': 2, '3e': 3, '4e': 4, '5e': 5, '6e': 6}
    result = filtered_data.replace({'CltChamp': mapping})
    pivoted = pd.pivot_table(result, index='Saison', columns='Équipe', values='CltChamp')
    return pivoted
    
def question_8_data():
    raw_data = get_data_from_file("./datasets/all_goals.xlsx")
    filtered_data = raw_data.filter(['Date', 'Minute'], axis=1)
    goal_by_minute = filtered_data.groupby(['Minute']).count()
    goal_by_minute = goal_by_minute[~goal_by_minute.index.str.contains('\+')]
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
