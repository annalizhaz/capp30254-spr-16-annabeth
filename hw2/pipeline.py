import pandas as pd

def get_description(df, file_name):
    df1 = df.describe().T
    modes = df.mode().T
    modes.rename(columns={0 : "mode"}, inplace = True)
    medians = pd.DataFrame(df.median())
    medians.rename(columns={0 : "median"}, inplace = True)
    stats_final = df1.join(modes, how="left").join(medians, how="left")
    stats_final.to_csv(file_name)
    return

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

def build(df):
    return

def predict(df):
    return

def test_accuracy(results, truth):
    return

def hw2_go(file_name, desc_file_name, has_index=True):
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
    df1 = fill_in(df)
    df2 = discretize_q(df1, ["age"], 4)
    df3 = cat_to_binary(df2, ["age_cat"])
    #build(df3)
    #predict(df4)