#!/usr/bin/env python
"""Utilities for the Data Decipher API

Functions:

    read_csv_file(flask.Request, str) -> pandas.DataFrame
    package_error(str) -> object
    package_response(str) -> object

Misc Variables:

    __name__

"""

from flask import Request
import pandas as pd

__name__ = 'utils'


def read_csv_file(request: Request, file_key: str = 'data') -> pd.DataFrame:
    """Read CSV from multipart/form-data request to pandas DataFrame"""        
    return pd.read_csv(request.files[file_key])

def package_error(error: str) -> object:
    """Package API error response into JSON"""
    return { 'error': error }

def package_response(response: str) -> object:
    """Package API response into JSON"""
    return { 'analysis': response }

def format_number(number: float) -> str:
    """Generate pretty-printable number with commas"""
    return '{:,}'.format(number)

def format_percent(percent: float) -> str:
    """Generate pretty-printable percent from decimal"""
    return '{0}%'.format(format_number(round(percent * 100, 2)))

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
