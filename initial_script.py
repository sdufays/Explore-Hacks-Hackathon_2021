#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 06:38:42 2021

@author: sarahdufays
"""

import numpy as np
import pandas as pd
import plotly.offline as py
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio

color = sns.color_palette()
py.init_notebook_mode(connected=True)
get_ipython().run_line_magic('matplotlib', 'inline')
pio.renderers.default='browser'


#open the text file to see
def run_profile_report(csv):
    df = pd.read_csv(csv)
    profile = df.profile_report(title="Demographic Analysis",
        dataset={
        "description": "This profiling report was generated for Explore Hacks by Sarah Dufays, Jennifer Chiou, Mudit Marwaha, and Alizain Fatehali",
        "copyright_holder": "Sarah Dufays",
        "copyright_year": "2021"
        })
    profile.to_file(output_file="<test>.html")

# use this to find how many occurences of a value there is in a column
def sum(csv,column, value):
    df = pd.read_csv(csv)
    result = (df[column].values == value).sum()
    return result


def pi_graph(csv, column, graph_title):
    df = pd.read_csv(csv)
    dist = df[column].value_counts()
    colors = ['mediumturquoise', 'darkorange']
    trace = go.Pie(values=(np.array(dist)),labels=dist.index)
    layout = go.Layout(title=graph_title)
    fig = go.Figure(trace, layout)
    fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.show()

    
def box_and_whisker(csv, x_axis, y_axis, title):
    df = pd.read_csv(csv)
    fig = px.box(df, x=x_axis, y=y_axis)
    fig.update_traces(marker_color="midnightblue", marker_line_color='rgb(80,203,147)',
                      marker_line_width=1.5)
    fig.update_layout(title_text=title)
    fig.show()


def scatter_plot(csv, horizontal_axis, vertical_axis, plot_title):
    df = pd.read_csv(csv)
    fig = px.scatter(df, x=horizontal_axis, y=vertical_axis)
    fig.update_traces(marker_color="turquoise", marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5)
    fig.update_layout(title_text=plot_title)
    fig.show()


def diversity(csv):
    df = pd.read_csv(csv)
    
    #gender
    total_males = sum(csv,'Sex','M ')
    num_rows = df.shape[0]
    percentage_male = total_males / num_rows * 100
    total_females = sum(csv,'Sex','F')
    num_rows = df.shape[0]
    percentage_female = total_females / num_rows * 100
    pi_graph(csv, "Sex", "Number of Males vs. Females")
    print("\n{:0.1f} % of your company is male and {:0.1f} % of your company is female\n".format(percentage_male,percentage_female))
    if percentage_female < 45:
        print("\nConsider hiring more female employees and addressing implicit gender biases in your company\n")
    elif percentage_male < 45:
        print("Consider hiring more male employees and addressing implicit gender biases in your company")
    else:
        print("You have incredible an gender ratio in your company!")
    #race
    pi_graph(csv, "RaceDesc", "Race Distribution")
    num_races = df.RaceDesc.nunique()
    if num_races < 5:
        print("Consider hiring diversely. In your business, you only have representation from %d races. Workplace diversity is key to success in your business, whether for different perspectives, unique approaches,increased creativity, or valuable insights that can increase DEI, productivity and profits within your company." %num_races)
    else:
        print("\nYou have representation from %d different races in your company! Check the pi chart of your company's Race Distribution to ensure that minorities are fairly represented." %num_races)
   # i really wanna put a if more than blabla percent of people are white blabla and if theres a minority group thats less than _ percent but i dont have tine to :(( if one of u can it would be great 
   
    # maybe add a column for family income + education status in the dataset to do the same afterwards

def equity(csv):
    df = pd.read_csv(csv)
    average_salary = df['Salary'].mean()
    print("The average salary in your company is" + int(average_salary))
    
    #need to zoom in on the box to ignore the max/min so we can actually see the data
    box_and_whisker(csv, "Sex", "Salary", "Correlation Between Employee Gender and Salary")
    box_and_whisker(csv, "RaceDesc", "Salary", "Correlation Between Employee Race and Salary")


def inclusion(csv):
    # demographic vs. satisfaction
    box_and_whisker(csv, "RaceDesc", "EmpSatisfaction", "Correlation Between Employee Race and Satisfaction")
    box_and_whisker(csv, "Sex", "EmpSatisfaction", "Correlation Between Employee Gender and Satisfaction")
    # engagement by race
    scatter_plot(csv, "RaceDesc", "EngagementSurvey", "Employee Engagement by Race")


if __name__ == "__main__":
   # run_profile_report("Downloads/HRDataset_v14.csv")
    #diversity("Downloads/HRDataset_v14.csv")
    equity("Downloads/HRDataset_v14.csv")
    #inclusion("Downloads/HRDataset_v14.csv")
    # download_dataset("Downloads/HRDataset_v14.csv")
    # run_profile_report("Downloads/HRDataset_v14.csv")
    # pi_graph("Downloads/HRDataset_v14.csv","RaceDesc","Race Distribution")
