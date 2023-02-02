import os
from os.path import join, dirname, realpath

import uuid
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
import pandas as pd

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join('.env'))

from flask_weasyprint import HTML, render_pdf

# from .utils import parseNsaveCSV
from models import db, Billables


import random
number = random.randint(1000,9999)


# instantiate the app
app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db.init_app(app)
migrate = Migrate(db)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Upload folder
UPLOAD_FOLDER = 'media/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER       

# setup db connection
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



# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


# csv upload route
# Get the uploaded files
@app.route("/generate-invoice", methods=['GET','POST'])
def generate_invoice():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # set the file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # save the file
        uploaded_file.save(file_path)
        # parse csv and update db
        try:
            parseNsaveCSV(uploaded_file)
            billables_data = Billables.query.order_by(Billables.employee_id).all()
        except Exception as e:
            # error saving csv
            print(e)
        finally:
            rendered = render_template('invoice.html',
                                    date = datetime.today().strftime('%Y-%m-%d'),
                                    items = billables_data,
                                    invoice_number = number)
            html = HTML(string=rendered)
    return render_pdf(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
