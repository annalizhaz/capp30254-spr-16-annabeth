import pandas as pd
import requests
import json
import numpy as np

df = pd.read_csv("data/mock_student_data.csv")

df1 = df.describe()
df2 = df.describe(include = ["O"])

desc_stats = (df1.join(df2, how = "outer")).T
stats_final = desc_stats.assign(missing = len(df) - desc_stats["count"])

stats_final.to_csv("descriptive_statistics.csv")

genderless = df[df["Gender"].isnull()]
name_set = set(genderless["First_name"])

url_app = []

for i, name in enumerate(name_set):
    name_low = name.lower()
    name_i = str(i)
    new_seg = "name[" + name_i + "]=" + name_low
    url_app.append(new_seg)

url = "https://api.genderize.io/?" + "&".join(url_app)

result = requests.get(url)
result_j = json.loads(result.text)

gender_dict = {}

for row in result_j:
    gender_dict[row["name"].capitalize()] = row["gender"].capitalize()

for i, has_gender in df["Gender"].isnull():
    if not has_gender:
        df["Gender"][i] = gender_dict[(df["First_name"][i])]

df.to_csv("genders_added.csv")

method_A = df.fillna(df.mean())

method_A.to_csv("fill_means.csv")

graduated = df[df["Graduated"]=="Yes"]
not_grad = df[df["Graduated"]=="No"]

graduated_filled = graduated.fillna(graduated.mean())
not_grad_filled = not_grad.fillna(not_grad.mean())

method_B = graduated_filled.append(not_grad_filled)

method_B.to_csv("class_means.csv")