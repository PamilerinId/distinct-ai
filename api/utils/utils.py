import pandas as pd



def parseNsaveCSV(filePath):
    # Column Names
    col_names = ['employee_id', 'billable_rate', 'project', 'date', 'start_time', 'end_time']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath,names=col_names, header=None)
    # Loop through the Rows
    for i,row in csvData.iterrows():
        print(i,row['employee_id'],row['billable_rate'],row['project'],row['date'],row['start_time'],row['end_time'],)

def generatePdf():
    pass