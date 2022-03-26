"""custom functions module"""

import os
import re
import itertools
import pandas as pd
import shutil # module for copying files

def move_to_log_folder(folder='logs'):
    """This function get the folder where log files are stored ('logs' by default)"""
    os.chdir(os.path.join(os.getcwd(), folder))

def get_recent_log():
    """Return the most recent log files. Log we received that day"""
    lst = [_ for _ in os.listdir() if _.endswith('.{}'.format('log'))]
    lst.sort()
    return lst[-1]

def get_last_csv(type):
    """Return the last_csvs files (filtered to keep the last 7 seven days data) """
    lst = [_ for _ in os.listdir() if _.endswith('.{}'.format('csv')) and _.startswith('{}_'.format(type))]
    lst.sort()
    return lst[0]

def get_recent_csv(type):
    """Return the csv we just cleaned with the cleaning script"""
    lst = [_ for _ in os.listdir() if _.endswith('.{}'.format('csv')) and not _.__contains__('last') and _.startswith('{}_'.format(type))]
    lst.sort()
    return lst[0]

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

def get_last_data(country_file, user_file, last_country_filename, last_users_filename):
    """ Return if it exists files names of last saved country and user df """
    if country_file:
        last_country_filename = get_last_csv('country')
    if user_file:
        last_users_filename = get_last_csv('user')
    return last_country_filename, last_users_filename


def keep_last_seven_days_data(data):
    """Convert date column into datetime then keep the last 7 days data"""
    data["date"] = pd.to_datetime(data["date"])
    data = data.set_index('date').last('7D').reset_index().reindex(columns=['sng_id', 'country', 'date'])


def load_csv(csv_file, last_df_file):
    """Load the csv file, if there is old records (last_df) we concatenate both then return them"""
    data = read_file(csv_file)
    if last_df_file != None:
        last_df_file = read_file(last_df_file)
        data = pd.concat([data, last_df_file])
    return data

def rename_to_last_df(file):
    """Rename a file to _last_saved_df"""
    if file.__contains__('country'):
        os.rename(file, 'country_last_saved_df.csv')
    elif file.__contains__('user'):
        os.rename(file, 'users_last_saved_df.csv')


def copy_file_to_special_dir(file):
    """Copies a dataFrame to special top50s directory"""
    shutil.copy(file, '../top50s/')


def make_top50_files(data, type, date):
    """ Create txt files and write top 50 songs whether it is for country or users [type]."""

    # we group rows by type and sng_id and count the number of song per countries (streams_count)
    groupby_df = data.groupby([type, 'sng_id']).agg(streams_count = ('sng_id', len))
    unique_ = list(data[type].unique()) # get unique list of type
        # for each countries we get the streams_count then put it in the format country:sng_id:streams_count and add it in a txt file
    filename = '{}_top50_{}.txt'.format(type, date)
    for elt in unique_:
        arr = groupby_df.xs(key=elt).reset_index().sort_values('streams_count', ascending=False).iloc[:50].values.tolist()
        arr = transform_list_to_inline_format(arr, elt)
        with open(filename, 'a') as f:
            f.writelines(arr)
    
    print('file created.')
    copy_file_to_special_dir(filename)
    # delete create files in the log directory
    os.remove(filename)