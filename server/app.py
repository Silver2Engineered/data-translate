#!/usr/bin/env python
""" API for the Data Decipher platform
"""

from flask import Flask, request
from flask_cors import CORS
import pandas as pd

import utils
import covid_analysis as covid
import birth_analysis as birth
import analysis

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '<h1>Data Decipher API</h1>'

@app.route('/analyze', methods=['POST'])
def analyze():
    df = utils.read_csv_file(request)
    is_covid = utils.is_covid_data(request)

    sort_col = df.columns[0]
    group_col = df.columns[1]

    group = request.args.get('group', '')
    if not group:
        return utils.package_error('Please include a ' + group_col + ' to analyze as a keyword argument, such as "datadecipher.com/analyze?' + group_col + '=IL"'), 400

    '''
    # Filter out state names we don't know (temporary fix)
    # Reasoning: some of the entries in dataset are cities like NYC
    if group not in df[group_col].values:
        return package_error('Provided data does not include information for specified state "{0}"'.format(group)), 400
    '''
    df[sort_col] = pd.to_datetime(df[sort_col])
    df.sort_values(sort_col, inplace=True)
    filtered_df = df[df[group_col] == group]
        
    paragraph = ''

    if (is_covid):
        state_name = utils.state_names[group]
        daily_case_sentence = covid.daily_statistics(filtered_df, state_name)
        daily_death_sentence = covid.daily_statistics(
            filtered_df, state_name, 
            column='new_death', column_title='Deaths', 
            include_state=False, include_date=False)
        recent_sentence = analysis.recent_statistics(filtered_df, state_name)

        similarity_sentence = analysis.similarity_statistics(df, group)

        paragraph = daily_case_sentence + ' ' + daily_death_sentence + '\n' + recent_sentence + '\n' + similarity_sentence

    else:
        merged_df = utils.transform_birth_data(df, ['Year', 'County'])
        county_name = group

        filtered_df = merged_df[merged_df[group_col] == county_name]

        recent_sentence = analysis.recent_statistics(
            merged_df, 
            county_name+' county',
            column='Total',
            column_title='number of births',
            interval=[-5, -1],
            interval_title='five years',
            timeframe_step_title='annual',
            timeframe_title='across all counties',
            show_total_average=True)
        
        similarity_sentence = analysis.similarity_statistics(
            merged_df,
            target_group=county_name,
            feature_col='Total',
            feature_title='number of births',
            group_col='County',
            group_title_map=lambda x: x+' county',
            interval_size=2,
            interval_title='two years',
            interval_increment_title='year')

        paragraph = recent_sentence+'\n'+similarity_sentence

    return utils.package_response(paragraph)

if __name__ == "__main__":
    app.run()
    