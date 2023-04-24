import pandas as pd  

def get_data_from_file(file_path):  

     # read the excel file using the pandas ExcelFile method and assign it to the variable xls
    xls = pd.ExcelFile(file_path) 
    sheetX = xls.parse(0) 
    return sheetX 
