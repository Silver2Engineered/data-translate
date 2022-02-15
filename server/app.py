#!/usr/bin/env python
""" API for the Data Decipher platform
"""

from flask import Flask, request
from flask_cors import CORS
import pandas as pd

from utils import read_csv_file, package_error, package_response, state_names
from covid_analysis import daily_statistics, recent_statistics, similarity_statistics

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '<h1>Data Translate API</h1>'

@app.route('/analyze', methods=['POST'])
def analyze():
    df = read_csv_file(request)

     # Filter out state names we don't know (temporary fix)
     # Reasoning: some of the entries in dataset are cities like NYC
    df = df[df['state'].isin(state_names.keys())]

    state = request.args.get('state', '')
    if not state:
        return package_error('Please include a state to analyze as a keyword argument, such as "datatranslate.com/analyze?state=IL"'), 400

    if state not in df['state'].values:
        return package_error('Provided data does not include information for specified state "{0}"'.format(state)), 400

    df['submission_date'] = pd.to_datetime(df['submission_date'])
    state_df = df[df['state'] == state]
    state_name = state_names[state]

    daily_case_sentence = daily_statistics(state_df, state_name)
    daily_death_sentence = daily_statistics(
        state_df, state_name, 
        column='new_death', column_title='Deaths', 
        include_state=False, include_date=False)

    recent_sentence = recent_statistics(state_df, state_name)

    similarity_sentence = similarity_statistics(df, state)

    paragraph = daily_case_sentence + ' ' + daily_death_sentence + '\n' + recent_sentence + '\n' + similarity_sentence
    return package_response(paragraph)

if __name__ == "__main__":
    app.run()
    