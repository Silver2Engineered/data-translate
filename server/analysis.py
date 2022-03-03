#!/usr/bin/env python
""" Module with tools to analyze general datasets

Functions:

    recent_statistics(pandas.DataFrame, str, str, str, list, str, str, str, bool) -> str
    similarity_statistics(pandas.DataFrame, str, str, str, str, Callable, int, str, str) -> str
    timeframe_statistics(pandas.DataFrame, str, str, str, str, str, Callable, bool, bool) -> str

Misc Variables:

    __name__

"""

import pandas as pd
from typing import Callable

from utils import format_number, state_names, format_percent, percent_change

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


def _interval_similarity_rankings(
        df: pd.DataFrame,
        target_group: str,
        group_col: str = 'state',
        feature_col: str = 'new_case',
        interval_size: int = 7,
        interval_combination_func: Callable = percent_change,
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
        target_group: str,
        feature_col: str = 'new_case',
        feature_title: str = 'Daily New Cases',
        group_col: str = 'state',
        group_title_map: Callable = lambda x: state_names[x],
        interval_size: int = 7,
        interval_title: str = 'two weeks',
        interval_increment_title: str = 'week',
    ) -> str:
    """Generate natural language from comparing a target group to others in dataset"""

    rank_df = _interval_similarity_rankings(
        df,
        target_group=target_group,
        group_col=group_col,
        feature_col=feature_col,
        interval_size=interval_size)
    
    target_change = rank_df.iloc[0]['percent_change']

    def rank_information(entry: pd.DataFrame) -> list:
        return [group_title_map(entry[group_col]), entry['percent_change']]

    [target_group_name, target_change] = rank_information(rank_df.iloc[0])
    [first_group_name, first_change] = rank_information(rank_df.iloc[1])
    [second_group_name, second_change] = rank_information(rank_df.iloc[2])

    target_sentence = 'When compared with {0} ago, the average {1} in {2} has {3} by {4} in the last {5}.'.format(
        interval_title,
        feature_title.lower(),
        target_group_name,
        'increased' if target_change >= 0 else 'decreased',
        format_percent(abs(target_change)),
        interval_increment_title)

    similar_sentence = 'This is most similar to {0} and {1}, who had a percent change of {2} and {3} respectively over the same time frame.'.format(
        first_group_name,
        second_group_name,
        format_percent(abs(first_change)),
        format_percent(abs(second_change)))
    
    return '{0} {1}'.format(target_sentence, similar_sentence)


def timeframe_statistics(
        df: pd.DataFrame,
        group_title: str,
        timeframe_column: str = 'submission_date',
        target_column: str = 'new_case',
        target_column_title: str = 'new cases',
        target_column_metric_title: str = 'number of daily',
        timeframe_step_title: str = 'day',
        timeframe_format: Callable = lambda s: s.date().strftime('%B %d, %Y'),
        include_group_title: bool = True,
        include_timeframe: bool = True,
    ) -> str:
    """Create natural language analysis of daily stats"""

    mean_diff = df[target_column].mean()
    max_diff = int(df[target_column].max())

    start_date = timeframe_format(df[timeframe_column].iloc[0])
    end_date = timeframe_format(df[timeframe_column].iloc[-1])

    start = 'In {0}, t'.format(group_title) if include_group_title else 'T'
    date = 'from {0} to {1} '.format(start_date, end_date) if include_timeframe else ''

    sentence = '{0}he average {1} {2} {3}was {4}, with a maximum of {5} {2} in a single {6}.'.format(
        start,
        target_column_metric_title,
        target_column_title,
        date,
        format_number(round(mean_diff, 2)),
        format_number(max_diff),
        timeframe_step_title,
    )

    return sentence
