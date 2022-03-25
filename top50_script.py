# -*- coding: utf-8 -*-
# import python libraries
import os
import pandas as pd
from modules.functions_modules import *     # custom functions 

# we move to the initial directory, check if previous days record csv exists, if it does we load we get his filename
last_streams_df = None
initial_dir = os.getcwd()
last_csv_exists = os.path.exists(os.path.join(initial_dir, 'last_saved_df.csv'))
if last_csv_exists:
    last_streams_df = get_type_filename('csv')

# move to the lastest folder, get the csv filename and the date
try:
    move_to_the_most_recent_folder()
    csv_filename = get_type_filename('csv')
    date = get_date_from_filename(csv_filename)
except:
    print('reading file error')
os.getcwd()

# we load the csv file, if there is old records we concat both
streams_df = read_file(csv_filename)
if last_streams_df != None:
    last_streams_df = read_file(os.path.join(initial_dir, last_streams_df))
    streams_df = pd.concat([streams_df, last_streams_df])

# convert date column into datetime then keep only records on the last 7 days
streams_df["date"] = pd.to_datetime(streams_df["date"])
streams_df = streams_df.set_index('date').last('7D').reset_index()
save_df(streams_df, csv_filename)

# copy saved df to initial directory for upcoming days
try:
    file_to_copy = get_type_filename('csv')
    copy_saved_df_to_initial_dir(file_to_copy, initial_dir)
except:
    print('reading file error')


# Getting top 50 songs

# we group rows by country and sng_id and count the number of song per countries (streams_count)
group_per_country_sngid = streams_df.groupby(['country', 'sng_id']).agg(streams_count = ('sng_id', len))
unique_countries = list(streams_df.country.unique()) # get unique list of countries

# for each countries we get the streams_count then put it in the format country:sng_id:straams_count and add it in a txt file
for country in unique_countries:
  arr = group_per_country_sngid.xs(key=country).reset_index().sort_values('streams_count', ascending=False).iloc[:50].values.tolist()
  arr = transform_list_to_inline_format(arr, country)
  with open('country_top50_{}.txt'.format(date), 'a') as f:
    f.writelines(arr)

print('file created.')