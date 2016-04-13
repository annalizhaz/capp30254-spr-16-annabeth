import pandas as pd
import random
from sklearn.linear_model import LogisticRegression

def get_description(df, file_name):
    df1 = df.describe().T
    modes = df.mode().T
    modes.rename(columns={0 : "mode"}, inplace = True)
    medians = pd.DataFrame(df.median())
    medians.rename(columns={0 : "median"}, inplace = True)
    stats_final = df1.join(modes, how="left").join(medians, how="left")
    stats_final.to_csv(file_name)
    return

def make_plots(df, column_headers):
    '''
    Takes dataframe and plots histograms for age, gpa, and days of school missed
    '''
    for attribute in column_headers:
        plot = df[attribute].plot.hist()
        fig = plot.get_figure()
        fig.savefig(attribute + ".png")
        fig.clear()

def fill_in(df):
    new_df = df.fillna(df.mean())
    return new_df

def discretize_q(df, column_headers, division, remove_originals=True):
    '''
    column_headers is a list
    '''
    all_bins = []
    new_columns = []

    for attribute in column_headers:
        cutting, bins = pd.qcut(df[attribute], division, labels=False, retbins=True)
        cutting_df = cutting.to_frame(name=attribute)
        new_columns.append(cutting_df)
        bins_se=pd.Series(bins, name=attribute)
        all_bins.append(bins_se)

    new_df = df.join(cutting_df, how="left", rsuffix="_cat")

    bin_dictionary = pd.DataFrame(all_bins)
    bin_file_name = "-".join(column_headers) + "_bin_dictionary.csv"
    bin_dictionary.to_csv(bin_file_name)

    if remove_originals:
        for attribute in column_headers:
            del new_df[attribute]

    return new_df

def discretize_bins(df, column_headers, division):
    '''
    location for by-division discretize function in future
    '''

def cat_to_binary(df, column_headers):
    '''
    column_headers is a list of strings
    '''
    binary_dfs = []

    for attribute in column_headers:
        dummies = pd.get_dummies(df[attribute], prefix=attribute)
        binary_dfs.append(dummies)

    new_df = df.join(binary_dfs, how="left")

    return new_df

def build_train_test(df_train, df_test, predictor_columns, predicted_column):
    model = LogisticRegression()
    model.fit(df_train[predictor_columns], df_train[predicted_column])
    predicted_results = model.predict(df_test[predictor_columns])
    actual_results = df_test[predicted_column]
    actual_results.rename(index="true_results", inplace=True)
    predicted_results_se = pd.Series(predicted_results, name="test_results")
    true_df = pd.DataFrame(actual_results)
    true_df.reset_index(drop=True, inplace=True)
    test_df = pd.DataFrame(predicted_results_se)
    comparison = true_df.join(test_df, how="left")
    comparison.loc[comparison["true_results"]==comparison["test_results"], "match"] = 1
    print(true_df.head())
    print(test_df.head())
    print(len(df_test))
    print(len(df_train))
    return (comparison["match"].sum()/len(df_test))*100

def hw2_go(file_name, desc_file_name, predict, drop_attr, has_index=True):
    '''
    function to call other functions as needed for hw2
    hard coded variables here
    '''
    if has_index:
        index_col_number = 0
    else:
        index_col_number = None

    df = pd.read_csv(file_name, index_col=index_col_number)
    get_description(df, desc_file_name)
    make_plots(df, list(df.columns))
    df1 = fill_in(df)
    df2 = discretize_q(df1, ["age"], 4)
    df3 = cat_to_binary(df2, ["age_cat"])

    predictor_columns = list(set(df3.columns) - set(drop_attr))

    rand_list = random.sample(range(len(df3)), len(df3))
    divide_point = int(.8*len(df3))

    train_list = rand_list[:divide_point]
    test_list = rand_list[divide_point:]

    train_df = df3.iloc[train_list, :]
    test_df = df3.iloc[test_list, :]

    accuracy = build_train_test(train_df, test_df, predictor_columns, predict)

    return accuracy

#hw2_go("cs-training.csv", "test5.csv", "SeriousDlqin2yrs", ["SeriousDlqin2yrs", "NumberOfTimes90DaysLate", "RevolvingUtilizationOfUnsecuredLines", "NumberOfTime30-59DaysPastDueNotWorse", "NumberOfTime30-59DaysPastDueNotWorse", "NumberOfTime30-59DaysPastDueNotWorse", "NumberOfTime30-59DaysPastDueNotWorse", "DebtRatio", "NumberOfDependents", "MonthlyIncome"])