import pandas as pd

def get_data_from_file(file_name):
    # file_name = "./datasets/cr7_goals.xlsx"

    xls = pd.ExcelFile(file_name)

    sheetX = xls.parse(0)
    return sheetX

def question_1_data():
    goal_data = get_data_from_file("./datasets/cr7_goals.xlsx")
    filtered_data = goal_data.filter(['Date','Comp','Équipe', 'Partie du corps', 'Distance', 'Minute'], axis=1)
    return filtered_data