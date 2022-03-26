# -*- coding: utf-8 -*-

# import python libraries
import os
import numpy as np
import pandas as pd
from modules.functions_modules import *     # custom functions 

# go to the most recent folder then get the log filename
try:
    move_to_the_most_recent_folder()
    log_filename = get_type_filename('log')
except:
    print('reading file error')
print(os.getcwd())

# get the data date from the filename, read the log file then resolve error 2 (see errors list)
date = get_date_from_filename(log_filename) 
lines = read_file(log_filename)
lines = remove_files_with_more_than_3_strings_separated(lines)

# then transform the remaining list into a dataframe
streams_df = pd.DataFrame(lines, columns = ['sng_id', 'user_id', 'country'])
streams_df["country"] = streams_df["country"].astype("category")

"""##Handling missing values"""

streams_df.fillna(value=np.nan, inplace=True)

# delete rows with no song_id information -> their correspond to empty rows in the file or there is no interest to analyse data where there is no song id
streams_df.drop(streams_df[streams_df.sng_id == ''].index, inplace=True)


"""- [x] there are some lines where the pipe separator is missing, causing null values in country columns (lines 1007459-1007463)"""
rows = streams_df.loc[(streams_df.user_id.notnull()) & (streams_df.country.isna())]
streams_df.loc[(streams_df.user_id.notnull()) & (streams_df.country.isna())] = rows.apply(resolve_error_one, axis=1)

"""- [x] some country codes are duplicated"""
rows = streams_df.loc[streams_df.country.str.len() > 2]
streams_df.iloc[rows.index] = rows.apply(keep_real_country_value, axis=1)


"""- [x] some are simply separated by a comma instead of a pipe"""
rows = streams_df.loc[(streams_df.user_id.isna()) & (streams_df.country.isna())]
streams_df.loc[(streams_df.user_id.isna()) & (streams_df.country.isna())] = rows.apply(resolve_error_four, axis=1)

"""- [x] some of them are negatives (line 1243014 - 1243017)"""
# we chose to delete these rows because negative values don't give us much information about a streamed song
# streams_df.drop(streams_df.loc[streams_df.sng_id == '-1'].index, inplace=True)
streams_df.drop(streams_df.loc[streams_df.sng_id.astype(int) <= -1].index, inplace=True)

# we delete malformed lines then copy the dataframe in a new one to get users top50s
# rows = streams_df.loc[(streams_df.user_id == '') | (streams_df.user_id == 'null') | (streams_df.user_id == '-1')].index
# user_stream_df = streams_df.drop(rows).drop('country', axis=1)
streams_df.drop('user_id', axis=1, inplace=True)

# we add a date column
streams_df['date'] = date
# user_stream_df['date'] = date

# save dfs
save_df(streams_df, ''log_filename)
# save_df(user_stream_df, 'user_'+log_filename)