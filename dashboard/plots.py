import plotly.graph_objs as go
import numpy
import glob
import os
import datetime
import requests
import collections
from wsse.client.requests.auth import WSSEAuth
from plotly.offline import plot
from sklearn.cluster import KMeans


def avgscore_class_data(attempt_data, quiz_titles):
    # Map quizzes to questions, questions to users, and users to all grades for that question
    quiz_grades = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))

    for attempt in attempt_data:
        quiz = quiz_titles[attempt['question']['quiz']]
        question = attempt['question']['title']
        user = attempt['user']['username']
        grade = float(attempt['score']) / float(attempt['question']['max_score']) * 100
        quiz_grades[quiz][question][user].append(grade)

    # Find averages by only considering the highest score across each student's attempts
    quiz_averages = {}
    for quiz, questions in quiz_grades.items():
        quiz_averages[quiz] = 0
        question_averages = {}
        for question, users in questions.items():
            question_averages[question] = 0
            for user, grades in users.items():
                question_averages[question] += max(grades)
            question_averages[question] = question_averages[question] / len(users)
        quiz_averages[quiz] = sum(avg for avg in question_averages.values()) / len(question_averages)
        quiz_averages[quiz] = round(quiz_averages[quiz], 2)

    return (list(quiz_averages.keys()), list(quiz_averages.values()))

def attempts_class_data(attempt_data, quiz_titles):
    # Map questions to users, and users to all grades for that question
    quiz_grades = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))

    for attempt in attempt_data:
        quiz = quiz_titles[attempt['question']['quiz']]
        title = attempt['question']['title']
        user = attempt['user']['username']
        quiz_grades[quiz][title][user] += 1

    quiz_attempts = {}
    for quiz, questions in quiz_grades.items():
        quiz_attempts[quiz] = 0
        question_attempts = {}
        for question, users in questions.items():
            question_attempts[question] = 0
            for user, attempts in users.items():
                question_attempts[question] += attempts
            question_attempts[question] = question_attempts[question] / len(users)
        quiz_attempts[quiz] = sum(attempts for attempts in question_attempts.values()) / len(question_attempts)
        quiz_attempts[quiz] = round(quiz_attempts[quiz], 2)

    return (list(quiz_attempts.keys()), list(quiz_attempts.values()))

def completion_time_class_data(attempt_data, quiz_titles):
    # Map questions to users, and users to all grades for that question
    quiz_grades = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))

    for attempt in attempt_data:
        quiz = quiz_titles[attempt['question']['quiz']]
        title = attempt['question']['title']
        user = attempt['user']['username']
        quiz_grades[quiz][title][user] += attempt['elapsed_seconds']

    quiz_times = {}
    for quiz, questions in quiz_grades.items():
        quiz_times[quiz] = 0
        question_times = {}
        for question, users in questions.items():
            question_times[question] = 0
            for user, time in users.items():
                question_times[question] += time
            question_times[question] = question_times[question] / len(users)
        quiz_times[quiz] = sum(attempts for attempts in question_times.values()) / len(question_times)
        quiz_times[quiz] = round(quiz_times[quiz], 2)

    return (list(quiz_times.keys()), list(quiz_times.values()))

def stddev_class_data(attempt_data, quiz_titles):
    # Map questions to users, and users to all grades for that question
    quiz_grades = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))

    for attempt in attempt_data:
        quiz = quiz_titles[attempt['question']['quiz']]
        title = attempt['question']['title']
        user = attempt['user']['username']
        grade = float(attempt['score']) / float(attempt['question']['max_score']) * 100
        quiz_grades[quiz][title][user].append(grade)

    # Find averages by only considering the highest score across each student's attempts
    quiz_stddev = {}
    for quiz, questions in quiz_grades.items():
        quiz_stddev[quiz] = 0
        question_stddev = {}
        averages = collections.defaultdict(list)
        for question, users in questions.items():
            question_stddev[question] = 0
            for user, grades in users.items():
                averages[question].append(max(grades))
            question_stddev[question] = numpy.std(averages[question])
        quiz_stddev[quiz] = sum(avg for avg in question_stddev.values()) / len(question_stddev)
        quiz_stddev[quiz] = round(quiz_stddev[quiz], 2)

    return (list(quiz_stddev.keys()), list(quiz_stddev.values()))

def kmeans_class_plot(attempt_data):
    quiz_grades = collections.defaultdict(lambda: collections.defaultdict(list))
    quiz_attempts = collections.defaultdict(lambda: collections.defaultdict(int))

    for attempt in attempt_data:
        title = attempt['question']['title']
        user = attempt['user']['username']
        grade = float(attempt['score']) / float(attempt['question']['max_score']) * 100
        quiz_grades[user][title].append(grade)
        quiz_attempts[user][title] += 1

    # Find averages by only considering the highest score across each student's attempts
    averages = {}
    for k, v in quiz_grades.items():
        averages[k] = 0
        for k2, v2 in v.items():
            averages[k] += max(v2)
        averages[k] = round((averages[k] / len(v)), 2)

    attempts = {}
    for k, v in quiz_attempts.items():
        attempts[k] = 0
        for k2, v2 in v.items():
            attempts[k] += v2
        attempts[k] = round((float(attempts[k]) / len(v.items())), 2)

    coords = [[list(averages.values())[i], list(attempts.values())[i]] for i in range(len(averages))]
    kmeans = KMeans(n_clusters=3, max_iter = 1000, n_init = 100).fit(coords)


    colors = ['red', 'green', 'blue']
    marker_colors = [colors[i] for i in kmeans.labels_]
    trace = go.Scatter(
        x = list(attempts.values()),
        y = list(averages.values()),
        text= list(averages.keys()),
        mode = 'markers',
        marker = dict(
            size = 10,
            color = marker_colors,
            line = dict(
                width = 2,
            )
        )
    )

    data = [trace]

    layout = go.Layout(
        xaxis=dict(
            autorange=True,
            title='Average Number of Attempts'
        ),
        yaxis=dict(
            autorange=True,
            title='Average Score'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div



def avgscore_class_plot(attempt_data, quiz_titles):
    plot_data = avgscore_class_data(attempt_data, quiz_titles)
    return get_class_plot(plot_data, False)

def attempts_class_plot(attempt_data, quiz_titles):
    plot_data = attempts_class_data(attempt_data, quiz_titles)
    return get_class_plot(plot_data, True)

def completion_time_class_plot(attempt_data, quiz_titles):
    plot_data = completion_time_class_data(attempt_data, quiz_titles)
    return get_class_plot(plot_data, True)

def stddev_class_plot(attempt_data, quiz_titles):
    plot_data = stddev_class_data(attempt_data, quiz_titles)
    return get_class_plot(plot_data, True)


def avgscore_student_plot(attempt_data, quiz_titles, student_id):
    # Map quizzes to questions, questions to users, and users to all grades for that question
    quiz_grades = collections.defaultdict(lambda: collections.defaultdict(int))

    for attempt in attempt_data:
        if attempt['user']['username'] == student_id:
            quiz = quiz_titles[attempt['question']['quiz']]
            question = attempt['question']['title']
            grade = float(attempt['score']) / float(attempt['question']['max_score']) * 100
            if (grade > quiz_grades[quiz][question]):
                quiz_grades[quiz][question] = grade

    quiz_averages = {}
    for quiz, questions in quiz_grades.items():
        quiz_averages[quiz] = sum(grades for grades in questions.values()) / len(questions.values())
        quiz_averages[quiz] = round(quiz_averages[quiz], 2)

    class_data = avgscore_class_data(attempt_data, quiz_titles)
    student_data = (list(quiz_averages.keys()), list(quiz_averages.values()))
    return get_student_plot(class_data, student_data, False)

def attempts_student_plot(attempt_data, quiz_titles, student_id):
    quiz_attempts = collections.defaultdict(lambda: collections.defaultdict(int))

    for attempt in attempt_data:
        if attempt['user']['username'] == student_id:
            quiz = quiz_titles[attempt['question']['quiz']]
            question = attempt['question']['title']
            quiz_attempts[quiz][question] += 1

    average_attempts = {}
    for quiz, questions in quiz_attempts.items():
        average_attempts[quiz] = sum(grades for grades in questions.values()) / float(len(questions.values()))
        average_attempts[quiz] = round(average_attempts[quiz], 2)

    class_data = attempts_class_data(attempt_data, quiz_titles)
    student_data = (list(average_attempts.keys()), list(average_attempts.values()))
    return get_student_plot(class_data, student_data, True)

def completion_time_student_plot(attempt_data, quiz_titles, student_id):
    quiz_attempts = collections.defaultdict(lambda: collections.defaultdict(int))

    for attempt in attempt_data:
        if attempt['user']['username'] == student_id:
            quiz = quiz_titles[attempt['question']['quiz']]
            question = attempt['question']['title']
            quiz_attempts[quiz][question] += attempt['elapsed_seconds']

    average_attempts = {}
    for quiz, questions in quiz_attempts.items():
        average_attempts[quiz] = sum(grades for grades in questions.values()) / float(len(questions.values()))
        average_attempts[quiz] = round(average_attempts[quiz], 2)

    class_data = completion_time_class_data(attempt_data, quiz_titles)
    student_data = (list(average_attempts.keys()), list(average_attempts.values()))
    return get_student_plot(class_data, student_data, True)

def question_avgscore_class_data(attempt_data, quiz_id):
    question_grades = collections.defaultdict(lambda: collections.defaultdict(list))

    for attempt in attempt_data:
        if attempt['question']['quiz'] == quiz_id:
            title = attempt['question']['title']
            user = attempt['user']['username']
            grade = float(attempt['score']) / float(attempt['question']['max_score']) * 100
            question_grades[title][user].append(grade)

    # Find averages by only considering the highest score across each student's attempts
    averages = {}
    for k, v in question_grades.items():
        averages[k] = 0
        for k2, v2 in v.items():
            averages[k] += max(v2)
        averages[k] = round((averages[k] / len(v)), 2)

    return (list(averages.keys()), list(averages.values()))

def question_attempts_class_data(attempt_data, quiz_id):
    question_attempts = collections.defaultdict(lambda: collections.defaultdict(int))

    for attempt in attempt_data:
        if attempt['question']['quiz'] == quiz_id:
            title = attempt['question']['title']
            user = attempt['user']['username']
            question_attempts[title][user] += 1

    # Find average number of attempts
    attempts = {}
    for k, v in question_attempts.items():
        attempts[k] = 0
        for k2, v2 in v.items():
            attempts[k] += v2
        attempts[k] = round((float(attempts[k]) / len(v.items())), 2)

    return (list(attempts.keys()), list(attempts.values()))

def question_completion_time_class_data(attempt_data, quiz_id):
    question_times = collections.defaultdict(lambda: collections.defaultdict(int))

    for attempt in attempt_data:
        if attempt['question']['quiz'] == quiz_id:
            title = attempt['question']['title']
            user = attempt['user']['username']
            question_times[title][user] += attempt['elapsed_seconds']

    # Find average number of attempts
    times = {}
    for k, v in question_times.items():
        times[k] = 0
        for k2, v2 in v.items():
            times[k] += v2
        times[k] = round((float(times[k]) / len(v.items())), 2)

    return (list(times.keys()), list(times.values()))

def question_stddev_class_data(attempt_data, quiz_id):
    question_sttdev = collections.defaultdict(lambda: collections.defaultdict(list))

    for attempt in attempt_data:
        if attempt['question']['quiz'] == quiz_id:
            title = attempt['question']['title']
            user = attempt['user']['username']
            grade = float(attempt['score']) / float(attempt['question']['max_score']) * 100
            question_sttdev[title][user].append(grade)

    # Find averages by only considering the highest score across each student's attempts
    averages = collections.defaultdict(list)
    stddev = {}
    for k, v in question_sttdev.items():
        for k2, v2 in v.items():
            averages[k].append(max(v2))
        stddev[k] = numpy.std(averages[k])

    return (list(stddev.keys()), list(stddev.values()))


def question_avgscore_class_plot(attempt_data, quiz_id):
    plot_data = question_avgscore_class_data(attempt_data, quiz_id)
    return get_class_plot(plot_data, False)

def question_attempts_class_plot(attempt_data, quiz_id):
    plot_data = question_attempts_class_data(attempt_data, quiz_id)
    return get_class_plot(plot_data, True)

def question_completion_time_class_plot(attempt_data, quiz_id):
    plot_data = question_completion_time_class_data(attempt_data, quiz_id)
    return get_class_plot(plot_data, True)

def question_stddev_class_plot(attempt_data, quiz_id):
    plot_data = question_stddev_class_data(attempt_data, quiz_id)
    return get_class_plot(plot_data, True)

def question_avgscore_student(attempt_data, quiz_id, student_id):
    averages = collections.defaultdict(int)

    for attempt in attempt_data:
        if attempt['user']['username'] == student_id and attempt['question']['quiz'] == quiz_id:
            quiz_index = attempt['question']['title']
            grade = float(attempt['score']) / float(attempt['question']['max_score']) * 100
            if (grade > averages[quiz_index]):
                averages[quiz_index] = (grade)

    class_data = question_avgscore_class_data(attempt_data, quiz_id)
    student_data = (list(averages.keys()), list(averages.values()))
    return get_student_plot(class_data, student_data, False)

def question_attempts_student(attempt_data, quiz_id, student_id):
    attempts = collections.defaultdict(int)

    for attempt in attempt_data:
        if attempt['user']['username'] == student_id and attempt['question']['quiz'] == quiz_id:
            quiz_index = attempt['question']['title']
            attempts[quiz_index] += 1

    class_data = question_attempts_class_data(attempt_data, quiz_id)
    student_data = (list(attempts.keys()), list(attempts.values()))
    return get_student_plot(class_data, student_data, True)

def question_completion_time_student(attempt_data, quiz_id, student_id):
    times = collections.defaultdict(int)

    for attempt in attempt_data:
        if attempt['user']['username'] == student_id and attempt['question']['quiz'] == quiz_id:
            quiz_index = attempt['question']['title']
            times[quiz_index] += attempt['elapsed_seconds']

    class_data = question_completion_time_class_data(attempt_data, quiz_id)
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

# Sort items in dict based on lexicographic order of keys
def get_sorted_items(dict):

