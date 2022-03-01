#!/usr/bin/env python
""" Module with tools to analyze covid specific datasets

Functions:
    
    daily_statistics(pandas.DataFrame, str, str, str) -> str

Misc Variables:

    __name__

"""

import pandas as pd

from utils import format_number

__name__ = 'covid_analysis'


def daily_statistics(
        df: pd.DataFrame,
        group_title: str,
        column: str = 'new_case',
        column_title: str = 'New Cases',
        include_state: bool = True,
        include_date: bool = True
    ) -> str:
    """Create natural language analysis of daily stats"""

    df = df.sort_values('submission_date')
    start_date = df['submission_date'].iloc[0].date().strftime('%B %d, %Y')
    end_date = df['submission_date'].iloc[-1].date().strftime('%B %d, %Y')

    mean_diff = df[column].mean()
    max_diff = int(df[column].max())

    start = 'In {0}, t'.format(group_title) if include_state else 'T'
    date = 'from {0} to {1}'.format(start_date, end_date) if include_date else ''

    sentence = '{0}he average number of daily {1} {2} was {3}, with a maximum of {4} {1} in a single day.'.format(
        start, column_title.lower(), date, format_number(round(mean_diff, 2)), format_number(max_diff)
    )

    return sentence

