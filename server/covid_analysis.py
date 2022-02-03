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
        column_title: str = 'New Cases') -> str:
    """Create natural language anlysis of daily stats"""

    df = df.sort_values('submission_date')
    start_date = df['submission_date'].iloc[0].date()
    end_date = df['submission_date'].iloc[-1].date()

    mean_diff = df[column].mean()
    max_diff = int(df[column].max())

    sentence = 'In {0}, the average number of daily {1} from {2} to {3} was {4}, with a maximum of {5} {1} in a single day.'.format(
        group_title, column_title.lower(), start_date, end_date, round(mean_diff, 2), max_diff
    )

    return sentence





