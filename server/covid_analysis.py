#!/usr/bin/env python
""" Module with tools to analyze covid specific datasets

Functions:
    
    daily_statistics(pandas.DataFrame, str, str, str) -> str
    recent_statistics(pandas.DataFrame, str, str, str) -> str

Misc Variables:

    __name__

"""

import pandas as pd
from typing import Callable

from utils import format_number, format_percent, state_names

__name__ = 'covid_analysis'


def daily_statistics(
        df: pd.DataFrame,
        group_title: str,
        column: str = 'new_case',
        column_title: str = 'New Cases',
        include_state: bool = True,
        include_date: bool = True
    ) -> str:
    """Create natural language anlysis of daily stats"""

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


def recent_statistics(
        df: pd.DataFrame,
        group_title: str,
        column: str = 'new_case',
        column_title: str = 'New Cases'
    ) -> str:
    """Generate natural language analysis of most recent week stats"""

    df = df.sort_values('submission_date')

    week_stats = df.iloc[-7:-1]
    week_mean = week_stats[column].mean()
    tot_mean = df[column].mean()

    relation = ''
    if week_mean > tot_mean:
        relation = 'higher'
    elif week_mean < tot_mean:
        relation = 'lower'
    else:
        relation = 'the same as'

    sentence = 'For the most recent week in {0}, the average number of daily {1} was {2}. This is {3} than the total average over the pandemic.'.format(
        group_title, column_title.lower(), format_number(round(week_mean, 2)), relation
    )
    return sentence

def __percent_change(cur: float, prev: float) -> float:
    """Calculate percent change with checks for zero values"""
    # Infinite percent change
    if cur != 0 and prev == 0: return

    # No change from 0
    if cur == 0 and prev == 0: return 0
    
    return (cur - prev) / prev


def _interval_similarity_rankings(
        df: pd.DataFrame,
        target_group: str,
        group_col: str = 'state',
        feature_col: str = 'new_case',
        interval_size: int = 7,
        interval_combination_func: Callable = __percent_change,
        interval_combination_col: str = 'percent_change'
    ) -> pd.DataFrame:
    """Rank groups based on their similarity to a target over two intervals merged by some combination
    
    Note: the first entry will always be the target group's entry
    """
    rank_columns = (
        group_col,
        'prev_{0}'.format(feature_col),
        'cur_{0}'.format(feature_col),
        interval_combination_col)
    rank_df = pd.DataFrame(columns=rank_columns)

    # Compute comparison metric for each group
    for group in df[group_col].unique():
        group_df = df[df[group_col] == group]

        prev_interval = group_df.iloc[-2*interval_size:-interval_size-1][feature_col].mean()
        cur_interval = group_df.iloc[-interval_size:-1][feature_col].mean()
        combination = interval_combination_func(cur_interval, prev_interval)

        entry = [group, prev_interval, cur_interval, combination]

        rank_df.loc[len(rank_df.index)] = entry

    # Retrieve comparison metric for target group
    target_combination = rank_df[rank_df[group_col] == target_group][interval_combination_col].iloc[0]
    
    # Compute closest other groups to target measured by comparison metric
    rankings = (rank_df[interval_combination_col] - target_combination).abs().argsort()

    return rank_df.iloc[rankings]

def similarity_statistics(
        df: pd.DataFrame,
        target_state: str,
        feature_col: str = 'new_case',
        feature_title: str = 'New Cases',
        group_col: str = 'state',
        group_title_map: object = state_names,
    ) -> str:
    """Generate natural language from comparing a target group to others in dataset"""

    df = df.sort_values('submission_date')
    rank_df = _interval_similarity_rankings(df, target_state, group_col, feature_col)
    
    target_change = rank_df.iloc[0]['percent_change']

    def rank_information(entry: pd.DataFrame) -> list:
        return [group_title_map[entry[group_col]], entry['percent_change']]

    [target_state_name, target_change] = rank_information(rank_df.iloc[0])
    [first_state_name, first_change] = rank_information(rank_df.iloc[1])
    [seconds_state_name, second_change] = rank_information(rank_df.iloc[2])

    target_sentence = 'When compared with two weeks ago, the average daily {0} in {1} has {2} by {3} in the last week.'.format(
        feature_title.lower(), target_state_name, 'increased' if target_change >= 0 else 'decreased', format_percent(abs(target_change))
    )
    similar_sentence = 'This is most similar to {0} and {1} , who had a percent change of {2} and {3} respectively over the same time frame.'.format(
        first_state_name, seconds_state_name, format_percent(abs(first_change)), format_percent(abs(second_change))
    )
    return '{0} {1}'.format(target_sentence, similar_sentence)
