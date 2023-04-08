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

def question_7_data():
    raw_data = get_data_from_file("./datasets/cr7_club_ranking.xlsx")
    filtered_data = raw_data.filter(['Saison','Équipe', 'CltChamp'], axis=1)
    mapping = {'1er': 1, '2e': 2, '3e': 3, '4e': 4, '5e': 5, '6e': 6}
    result = filtered_data.replace({'CltChamp': mapping})
    pivoted = pd.pivot_table(result, index='Saison', columns='Équipe', values='CltChamp')
    return pivoted

def question_8_data():
    raw_data = get_data_from_file("./datasets/cr7_goals.xlsx")
    filtered_data = raw_data.filter(['Date', 'Minute'], axis=1)
    goal_by_minute = filtered_data.groupby(['Minute']).count()
    return goal_by_minute.loc[2:90]
    
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
    return filtered_data
