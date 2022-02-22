#!/usr/bin/env python
""" API for the Data Decipher platform
"""

from flask import Flask, request
from flask_cors import CORS
import pandas as pd

from utils import read_csv_file, package_error, package_response, state_names, is_covid_data
from covid_analysis import daily_statistics, recent_statistics, similarity_statistics

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '<h1>Data Decipher API</h1>'

@app.route('/analyze', methods=['POST'])
def analyze():
    df = read_csv_file(request)
    is_covid = is_covid_data(request)

    sort_col = df.columns[0]
    group_col = df.columns[1]

     # Filter out state names we don't know (temporary fix)
     # Reasoning: some of the entries in dataset are cities like NYC
    df = df[df[group_col].isin(state_names.keys())]

    group = request.args.get('group', '')
    if not group:
        return package_error('Please include a ' + group_col + ' to analyze as a keyword argument, such as "datadecipher.com/analyze?' + group_col + '=IL"'), 400

    '''
    if group not in df[group_col].values:
        return package_error('Provided data does not include information for specified state "{0}"'.format(group)), 400
    '''
    df[sort_col] = pd.to_datetime(df[sort_col])
    df.sort_values(sort_col, inplace=True)
    filtered_df = df[df[group_col] == group]
        
    paragraph = ''

    if (is_covid):
        state_name = state_names[group]
        daily_case_sentence = daily_statistics(filtered_df, state_name)
        daily_death_sentence = daily_statistics(
            filtered_df, state_name, 
            column='new_death', column_title='Deaths', 
            include_state=False, include_date=False)
        recent_sentence = recent_statistics(filtered_df, state_name)

        similarity_sentence = similarity_statistics(df, group)

        paragraph = daily_case_sentence + ' ' + daily_death_sentence + '\n' + recent_sentence + '\n' + similarity_sentence

    else:
        # group = county name for ca_birth_data.csv
        paragraph = 'not covid'

    return package_response(paragraph)

if __name__ == "__main__":
    app.run()
    