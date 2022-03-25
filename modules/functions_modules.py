"""custom functions module"""


import os
import re
import itertools
import pandas as pd
import shutil # module for copying files

def move_to_the_most_recent_folder():
    """This function get the most recent folder then change the working directory to this folder"""
    os.chdir(os.getcwd())
    last_created_folder = max([d for d in os.listdir('.') if os.path.isdir(d) and not(d.startswith('.') or d.__contains__('modules'))], key=os.path.getmtime) # get the last created folder name
    os.chdir(os.path.join(os.getcwd(), last_created_folder))


def get_type_filename(ext):
    """Return a filename based on his extension"""
    return [_ for _ in os.listdir() if _.endswith('.{}'.format(ext))][0]

def get_date_from_filename(filename):
    """Based on a regex extract the date from a file"""
    return re.search(r'\d{4}\-\d{2}\-\d{2}', filename).group()

def read_file(file):
    """This return file content whether it is a log file or a csv file (DataFrame)"""
    ext = file.split('.')[-1]
    if ext == 'log':
        with open(file) as f:
            return f.read().splitlines()
    elif ext == 'csv':
        return pd.read_csv(file)

def remove_files_with_more_than_3_strings_separated(arr):
    """Considering, a stream have sng_id|user_id|country format on each line, this function transforms lines that have more than one stream on the same line into multilines streams"""
    arr = [s.split('|') for s in arr] # we split each line by pipe separator
    back_up_list = []
    for elt in arr:
        if len(elt) > 3:
            back_up_list.append(elt)

    arr = [elt for elt in arr if len(elt) <=3] # we only keep lines with good number of elements (3)
    back_up_list = [re.findall(r'\d+\|\d+\|\w{2}', "|".join(s)) for s in back_up_list] # transform the surcharged streams into a proper stream list
    back_up_list = list(itertools.chain(*back_up_list))
    back_up_list = [s.split('|') for s in back_up_list]
    arr.extend(back_up_list)
    return arr

def get_na_values(df):
    """Function which gives rows containing nan values in the dataframe"""
    display(df[df.isna().any(axis=1)])

def resolve_error_one(x):
    """This function affects values to their appropriate columns. Please refer to error type 1 for more information"""
    x['country'] = x['user_id']
    x['user_id'] = x['sng_id'][-10:-1]
    x['sng_id'] = x['sng_id'][:-10]
    return x


def keep_real_country_value(x):
    """This function keep the first two characters from duplicated country codes. Please refer to error type 5 for more information"""
    x.country  = x.country[:2]
    return x

def resolve_error_four(x):
    """This function splits sng_id value by a comma then assigns resulted values to their actual column. Refer to error 4 for more information"""
    arr = x.sng_id.split(',')
    x.sng_id, x.user_id, x.country  = arr[0], arr[1], arr[2]
    return x

def save_df(df, filename):
    """This function saves the DataFrame into a csv file"""
    df.to_csv('{}.csv'.format(filename.split('.')[0]), index=False)
    print('DataFrame saved')

def transform_list_to_inline_format(l, country):
    """This function takes a list of the top 50 songs and the country then return a string 
        in the format country|sng_id1:n1,sng_id2:n2,sng_id3:n3,...,sng_id50:n50"""
    new_list = []
    # we convert integer into string
    for e in l:
        new_list.append([str(i) for i in e])
    new_list = [':'.join(s) for s in new_list] #join them by ':'
    ch = '{}|{}'.format(country, ','.join(new_list)) #then add country code to the beginning of the string
    ch+='\n'
    return ch

def copy_saved_df_to_initial_dir(old_file, new_directory):
    """Copies a dataFrame to initial directory"""
    new_file = shutil.copy(old_file, new_directory)
    os.rename(new_file, os.path.join(new_directory, 'last_saved_df.csv'))



