import os
from os.path import join, dirname, realpath

import uuid
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join('.env'))

from weasyprint import HTML

from utils.utils import parseNsaveCSV, generatePdf


# instantiate the app
app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Upload folder
UPLOAD_FOLDER = 'media/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER       

# setup db connection


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


# csv upload route
# Get the uploaded files
@app.route("/generate-invoice", methods=['POST'])
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
            parseNsaveCSV(file_path)
        except Exception as e:
            # error saving csv
            print(e)
        finally:
            rendered = generatePdf()

        # rendered = render_template('invoice.html',
        #                         date = today,
        #                         from_addr = from_addr,
        #                         to_addr = to_addr,
        #                         items = items,
        #                         total = total,
        #                         invoice_number = invoice_number,
        #                         duedate = duedate)
        html = HTML(string=rendered)
        rendered_pdf = html.write_pdf('./media/invoice.pdf')
    return send_file(
                    './media/invoice.pdf'
            )



# @app.route('/books', methods=['GET', 'POST'])
# def all_books():
#     response_object = {'status': 'success'}
#     if request.method == 'POST':
#         post_data = request.get_json()
#         BOOKS.append({
#             'id': uuid.uuid4().hex,
#             'title': post_data.get('title'),
#             'author': post_data.get('author'),
#             'read': post_data.get('read')
#         })
#         response_object['message'] = 'Book added!'
#     else:
#         response_object['books'] = BOOKS
#     return jsonify(response_object)


# @app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
# def single_book(book_id):
#     response_object = {'status': 'success'}
#     if request.method == 'PUT':
#         post_data = request.get_json()
#         remove_book(book_id)
#         BOOKS.append({
#             'id': uuid.uuid4().hex,
#             'title': post_data.get('title'),
#             'author': post_data.get('author'),
#             'read': post_data.get('read')
#         })
#         response_object['message'] = 'Book updated!'
#     if request.method == 'DELETE':
#         remove_book(book_id)
#         response_object['message'] = 'Book removed!'
#     return jsonify(response_object)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
