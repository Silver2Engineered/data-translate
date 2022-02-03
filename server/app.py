#!/usr/bin/env python
""" API for the Data Translate platform
"""

from flask import Flask, request
import pandas as pd

from utils import read_csv_file
from covid_analysis import daily_statistics

app = Flask(__name__)

state_names = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

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

    daily_sentence = daily_statistics(df[df['state'] == state], state_names[state])
    return daily_sentence

if __name__ == "__main__":
    app.run()
    