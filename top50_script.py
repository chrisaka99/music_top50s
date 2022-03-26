# -*- coding: utf-8 -*-
# import python libraries
from json import load
import os
import pandas as pd
from modules.functions_modules import *     # custom functions 

print('top50 files')
# we move to log folder, check if previous days record CSVs exist, if it does we load we get their filenames
move_to_log_folder()
last_country_filename, last_users_filename = None, None

country_csv_exists = os.path.exists('country_last_saved_df.csv')
user_csv_exists = os.path.exists('users_last_saved_df.csv')

# get filenames of last saved data
last_country_filename, last_users_filename = get_last_data(country_csv_exists, user_csv_exists, last_country_filename, last_users_filename)

# get the csv filename and the date from the cleaning
try:
    country_csv_filename = get_recent_csv('country')
    user_csv_filename = get_recent_csv('user')
    date = get_date_from_filename(country_csv_filename)
except:
    print('error')
print(os.getcwd())

# load data from the files, concatenated or not
streams_df = load_csv(country_csv_filename, last_country_filename)
user_streams_df = load_csv(user_csv_filename, last_users_filename)


keep_last_seven_days_data(streams_df)
keep_last_seven_days_data(user_streams_df)

 # save for upcoming days
save_df(streams_df, country_csv_filename)
save_df(user_streams_df, user_csv_filename)

# rename files
rename_to_last_df(country_csv_filename)
rename_to_last_df(user_csv_filename)


# TOP 50 MOST LISTENED SONGS BY COUNTRY

make_top50_files(streams_df, 'country', date)
make_top50_files(user_streams_df, 'user_id', date)