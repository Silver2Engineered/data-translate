#!/usr/bin/env python
""" Module with tools to analyze covid specific datasets

Functions:
    
    daily_statistics(pandas.DataFrame, str, str, str) -> str

Misc Variables:

    __name__

"""

import pandas as pd

__name__ = 'covid_analysis'


def daily_statistics(
        df: pd.DataFrame,
        group_title: str,
        column: str = 'new_case',
        column_title: str = 'New Cases',
        include_state: bool = True,
        include_date: bool = True) -> str:
    """Create natural language anlysis of daily stats"""

    df = df.sort_values('submission_date')
    start_date = df['submission_date'].iloc[0].date().strftime('%B %d, %Y')
    end_date = df['submission_date'].iloc[-1].date().strftime('%B %d, %Y')

    mean_diff = df[column].mean()
    max_diff = int(df[column].max())

    start = 'In {0}, t'.format(group_title) if include_state else 'T'
    date = 'from {0} to {1}'.format(start_date, end_date) if include_date else ''

    sentence = '{0}he average number of daily {1} {2} was {3}, with a maximum of {4} {1} in a single day.'.format(
        start, column_title.lower(), date, round(mean_diff, 2), max_diff
    )

    return sentence


def recent_statistics(
        df: pd.DataFrame,
        group_title: str,
        colum: str = 'new_case',
        column_title: str = 'New Cases') -> str:

    df = df.sort_values('submission_date')

    week_stats = df.iloc[-1:-7]

    print(week_stats)

    sentence = 'For the most recent week in the data the average number of daily new cases was x. This is higher/lower than the total average over the pandemic'


