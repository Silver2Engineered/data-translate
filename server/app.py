#!/usr/bin/env python
""" API for the Data Translate platform
"""

from flask import Flask, request
import pandas as pd

from utils import read_csv_file
from covid_analysis import daily_statistics

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Data Translate API</h1>'

@app.route('/analyze', methods=['POST'])
def analyze():
    df = read_csv_file(request)

    state = request.args.get('state', '')
    if not state:
        return 'Please include a state to anlyze as a keyword argument, such as "datatranslate.com/analyze?state=IL"', 400

    if state not in df['state'].values:
        return 'Provided data does not include information for specified state "{0}"'.format(state), 400
    
    df['submission_date'] = pd.to_datetime(df['submission_date'])

    daily_sentence = daily_statistics(df[df['state'] == state], state)
    return daily_sentence

if __name__ == "__main__":
    app.run()
    