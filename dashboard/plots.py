from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np
import glob
import os
import datetime


def plot1d():
    x_data = np.arange(0, 120,0.1)
    trace1 = go.Scatter(
        x=x_data,
        y=np.sin(x_data)
    )

    data = [trace1]
    layout = go.Layout(
        # autosize=False,
        # width=900,
        # height=500,

        xaxis=dict(
            autorange=True
        ),
        yaxis=dict(
            autorange=True
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    print("Number of points: %s" % len(x_data))
    return plot_div

def fake_quiz_avg():
    x_data = ["Stacks and Queues", "Binary Search", "Binary Trees", "Graph Search", "Hashing", "Compression"]
    #x_data = np.arange(1, 10, 1)
    y_data = [100, 75, 90, 95, 100, 80]
    trace1 = go.Scatter(
        x=x_data,
        y=y_data,
    )
    data = [trace1]
    layout = go.Layout(
        # autosize=False,
        # width=900,
        # height=500,

        xaxis=dict(
            #rangemode='tozero',
            autorange=True
        ),
        yaxis=dict(
        rangemode='tozero',
        autorange=True
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #print("Number of points: %s" % len(x_data))
    return plot_div

def fake_student_avg():
    x_data = ["Stacks and Queues", "Binary Search", "Binary Trees", "Graph Search", "Hashing", "Compression"]
    #x_data = np.arange(1, 10, 1)
    y_data = [100, 75, 90, 95, 100, 80]
    trace1 = go.Scatter(
        x=x_data,
        y=y_data,
        name="Student"
    )
    trace2 = go.Scatter(
        x=x_data,
        y=[96, 100, 95, 99, 85, 97.5],
        name="Class Average"
    )
    data = [trace1, trace2]
    layout = go.Layout(
        # autosize=False,
        # width=900,
        # height=500,

        xaxis=dict(
            #rangemode='tozero',
            autorange=True
        ),
        yaxis=dict(
        rangemode='tozero',
        autorange=True
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #print("Number of points: %s" % len(x_data))
    return plot_div
