#!/usr/bin/env python
""" Module with tools to analyze general datasets

Functions:

    recent_statistics(pandas.DataFrame, str, str, str) -> str

Misc Variables:

    __name__

"""

import pandas as pd

from utils import format_number

__name__ = 'analysis'


def recent_statistics(
        df: pd.DataFrame,
        group_title: str,
        column: str = 'new_case',
        column_title: str = 'New Cases',
        interval: list = [-7, -1],
        interval_title: str = 'week',
        timeframe_step_title: str = 'daily',
        timeframe_title: str = 'over the pandemic',
        show_total_average: bool = False,
    ) -> str:
    """Generate natural language analysis of most recent stats over specified timeframe"""

    interval_stats = df.iloc[interval[0]:interval[1]]
    interval_mean = interval_stats[column].mean()
    tot_mean = df[column].mean()

    relation = ''
    if interval_mean > tot_mean:
        relation = 'higher than'
    elif interval_mean < tot_mean:
        relation = 'lower than'
    else:
        relation = 'the same as'

    total_average_str = ''
    if show_total_average:
        total_average_str = ' of {0}'.format(format_number(round(tot_mean, 2)))

    sentence = 'For the most recent {0} in {1}, the average number of {6} {2} was {3}. This is {4} the total average {5}{7}.'.format(
        interval_title, group_title, column_title.lower(), format_number(round(interval_mean, 2)), relation, timeframe_title, timeframe_step_title, total_average_str
    )
    return sentence
