#!/usr/bin/env python
"""Utilities for the Data Translate API

Functions:

    read_csv_file(flask.Request, str) -> pandas.DataFrame

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