import plotly.graph_objs as go
import numpy as np
import glob
import os
import datetime
import requests
import collections
from wsse.client.requests.auth import WSSEAuth
from plotly.offline import plot


def avgscore_class_data(attempt_data):
    # Map questions to users, and users to all grades for that question
    quiz_grades = collections.defaultdict(lambda: collections.defaultdict(list))

    for attempt in attempt_data:
        title = attempt['question']['title']
        user = attempt['user']['username']
        grade = float(attempt['score']) / float(attempt['question']['max_score']) * 100
        quiz_grades[title][user].append(grade)

    # Find averages by only considering the highest score across each student's attempts
    averages = {}
    for k, v in quiz_grades.items():
        averages[k] = 0
        for k2, v2 in v.items():
            averages[k] += max(v2)
        averages[k] = round((averages[k] / len(v)), 2)

    return (list(averages.keys()), list(averages.values()))

def attempts_class_data(attempt_data):
    # Map questions to users, and users to all grades for that question
    quiz_grades = collections.defaultdict(lambda: collections.defaultdict(int))

    for attempt in attempt_data:
        title = attempt['question']['title']
        user = attempt['user']['username']
        quiz_grades[title][user] += 1

    # Find average number of attempts
    attempts = {}
    for k, v in quiz_grades.items():
        attempts[k] = 0
        for k2, v2 in v.items():
            attempts[k] += v2
        attempts[k] = round((float(attempts[k]) / len(v.items())), 2)

    return (list(attempts.keys()), list(attempts.values()))

def completion_time_class_data(attempt_data):
    # Map questions to users, and users to all grades for that question
    quiz_grades = collections.defaultdict(lambda: collections.defaultdict(int))

    for attempt in attempt_data:
        title = attempt['question']['title']
        user = attempt['user']['username']
        quiz_grades[title][user] += attempt['elapsed_seconds']

    # Find average number of attempts
    times = {}
    for k, v in quiz_grades.items():
        times[k] = 0
        for k2, v2 in v.items():
            times[k] += v2
        times[k] = round((float(times[k]) / len(v.items())), 2)

    return (list(times.keys()), list(times.values()))


def avgscore_class_plot(attempt_data):
    plot_data = avgscore_class_data(attempt_data)
    return get_class_plot(plot_data, False)

def attempts_class_plot(attempt_data):
    plot_data = attempts_class_data(attempt_data)
    return get_class_plot(plot_data, True)

def completion_time_class_plot(attempt_data):
    plot_data = completion_time_class_data(attempt_data)
    return get_class_plot(plot_data, True)


def avgscore_student_plot(attempt_data, student_id):
    # Map quiz to all grades
    averages = collections.defaultdict(int)

    for attempt in attempt_data:
        if attempt['user']['username'] == student_id:
            quiz_index = attempt['question']['title']
            grade = float(attempt['score']) / float(attempt['question']['max_score']) * 100
            if (grade > averages[quiz_index]):
                averages[quiz_index] = (grade)

    class_data = avgscore_class_data(attempt_data)
    student_data = (list(averages.keys()), list(averages.values()))
    return get_student_plot(class_data, student_data, False)

def attempts_student_plot(attempt_data, student_id):
    # Map quiz to all grades
    attempts = collections.defaultdict(int)

    for attempt in attempt_data:
        if attempt['user']['username'] == student_id:
            quiz_index = attempt['question']['title']
            attempts[quiz_index] += 1

    class_data = attempts_class_data(attempt_data)
    student_data = (list(attempts.keys()), list(attempts.values()))
    return get_student_plot(class_data, student_data, True)

def completion_time_student_plot(attempt_data, student_id):
    # Map quiz to all grades
    times = collections.defaultdict(int)

    for attempt in attempt_data:
        if attempt['user']['username'] == student_id:
            quiz_index = attempt['question']['title']
            times[quiz_index] += attempt['elapsed_seconds']

    class_data = completion_time_class_data(attempt_data)
    student_data = (list(times.keys()), list(times.values()))
    return get_student_plot(class_data, student_data, True)

def get_class_plot(plot_data, autorange):
    trace1 = go.Scatter(
        x=plot_data[0],
        y=plot_data[1],
    )
    data = [trace1]

    layout = None
    if autorange:
        layout = go.Layout(
            xaxis=dict(
                autorange=True
            ),
            yaxis=dict(
                rangemode='tozero',
                autorange=True
            )
        )
    else:
        layout = go.Layout(
            xaxis=dict(
                autorange=True
            ),
            yaxis=dict(
                rangemode='tozero',
                range=[0, 100]
            )
        )
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def get_student_plot(class_data, student_data, autorange):
    trace1 = go.Scatter(
        x=class_data[0],
        y=class_data[1],
        name="Class"
    )
    trace2 = go.Scatter(
        x=student_data[0],
        y=student_data[1],
        name="Student"
    )
    data = [trace1, trace2]

    layout = None
    if autorange:
        layout = go.Layout(
            xaxis=dict(
                autorange=True
            ),
            yaxis=dict(
                rangemode='tozero',
                autorange=True
            )
        )
    else:
        layout = go.Layout(
            xaxis=dict(
                autorange=True
            ),
            yaxis=dict(
                rangemode='tozero',
                range=[0, 100]
            )
        )
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
