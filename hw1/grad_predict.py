#HW1 for Machine Learning for Public Policy
#Anna Hazard

import pandas as pd
import requests
import json
import numpy as np

def get_description(df, file_name):
    '''
    Takes pandas data frame and returns descriptive
    statistics for numerical and string data
    '''
    df1 = df.describe().T.assign(median=df.median()).T
    df2 = df.describe(include = ["O"])
    df3 = df.drop(["ID"], axis=1)

    desc_stats = (df1.join(df2, how = "outer")).append(df3.mode().dropna()).T
    stats_final = desc_stats.assign(missing = len(df) - desc_stats["count"])
    stats_final.rename(columns={0 : "mode"}, inplace = True)

    del stats_final["top"]
    del stats_final["count"]
    del stats_final["unique"]
    del stats_final["freq"]
    del stats_final["25%"]
    del stats_final["50%"]
    del stats_final["75%"]

    stats_final.to_csv(file_name)

def make_plots(df, gpa_fig, age_fig, days_fig):
    '''
    Takes dataframe and plots histograms for age, gpa, and days of school missed
    '''
    GPA_plot = df["GPA"].plot.hist()
    fig = GPA_plot.get_figure()
    fig.savefig(gpa_fig)
    fig.clear()

    Age_plot = df["Age"].plot.hist()
    fig = Age_plot.get_figure()
    fig.savefig(age_fig)
    fig.clear()

    Days_plot = df["Days_missed"].plot.hist()
    fig = Days_plot.get_figure()
    fig.savefig(days_fig)
    fig.clear()

def get_genders(df):
    '''
    Takes data frame and adds genders where they are missing based on querying
    genderize.io api
    '''
    genderless = df["Gender"].isnull()
    genderless_names = df["First_name"][genderless]
    name_set = set(genderless_names)
    gender_dict = {}

    for name in name_set:
        name_low = name.lower()
        url = "https://api.genderize.io/?name=" + name_low
        req = requests.get(url)
        result = json.loads(req.text)
        gender_dict[result["name"].capitalize()] = result["gender"].capitalize()


    for i in list(df[genderless].index):
        df["Gender"][i] = gender_dict[(df["First_name"][i])]

def method_A(df, file_name):
    '''
    Takes dataframe, fills in missing numerical data based on
    means for columns and saves to csv
    '''
    new_df = df.fillna(df.mean())
    new_df.to_csv(file_name)

def method_B(df, file_name):
    '''
    Takes dataframe, fills in missing numerical data based on
    means for columns and for category (graduated vs. not graduated)
    '''
    graduated = df[df["Graduated"]=="Yes"]
    not_grad = df[df["Graduated"]=="No"]
    graduated_filled = graduated.fillna(graduated.mean())
    not_grad_filled = not_grad.fillna(not_grad.mean())
    new_df = graduated_filled.append(not_grad_filled)
    new_df.to_csv(file_name)

df = pd.read_csv("data/mock_student_data.csv")

get_description(df, "descriptive_statistics.csv")

make_plots(df, "gpa.png", "age.png", "days.png")

get_genders(df)

df.to_csv("genders_added.csv")

method_A(df, "fill_means.csv")
method_B(df, "class_means.csv")
