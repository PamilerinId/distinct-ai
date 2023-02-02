from datetime import datetime
import pandas as pd
from models import db, Billables


def parseNsaveCSV(filePath):
    # Column Names
    col_names = ['employee_id', 'billable_rate', 'project', 'date', 'start_time', 'end_time']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath,names=col_names, header=0)
    # Loop through the Rows
    for i,row in csvData.iterrows():
        # calculate billables
        time_delta = datetime.strptime(row['end_time'], '%H:%M') - datetime.strptime(row['start_time'], '%H:%M')
        csvData.at[i,'time_difference'] = time_delta
        csvData.at[i,'total_cost'] = time_delta * row['billable_rate']

        # save to db
        billable = Billables(employee_id=row['employee_id'],
                                billable_rate=row['billable_rate'],
                                project=row['project'],
                                date=row['date'],
                                start_time=row['start_time'],
                                end_time=row['end_time'],
                                time_difference=row['time_difference'],
                                total_cost=row['total_cost'],
        )
        db.session.add(billable)
        db.session.commit()
        print (f"billable with employee id {billable.employee_id} has been created successfully.")
        print(i,row['employee_id'],row['billable_rate'],row['project'],row['date']
                ,row['start_time'],row['end_time'],row['time_difference'], row['total_cost'])