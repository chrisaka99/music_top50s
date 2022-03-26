Get Started
======

To run this file, first clone the repo `git clone https://github.com/kayann99/music_top50s.git`.

Install necessary librairies:
```
pip install pandas
pip install numpy
pip install shutil
pip install itertools

```

Then go the clone repo directory `cd music_top50s`. In the directory, run `chmod u+x script.sh` to make script.sh executable.
Finally run `./script.sh`


How does it work ?
======

This is a set of scripts which generate the 50 most listened songs in a country and per user.

The repository the structure as shown below:

    .
    ├── logs                                            # Folder containing first-day lo²g file
    │   └── sample_listen-2021-12-01_2Mlines.log                # streams file  
    ├── modules                                         # Custom module directory
    │   └── functions_modules.py                                # Functions written to                
    ├── cleaning_script.py                              # python script to clean log files and saved cleaned version as csv
    ├── script.sh                                       # bash file which run both python scripts
    ├── top50s                                          # folder to store top 50 files
    ├── top50_script.py                                 # python script to generate top50 files
    └── README.md

We are receiving each day in a folder, a text file which contains streamed songs (sample_listen-2021-12-01_2Mlines.log) on the current date.

In order to get the top 50s songs per country and per user, we need first to clean the data. This is some of the corrupted rows that we found during the data analysis

| #        | Description           | Lines (in the log file)  |
| ------------- |:-------------:| -----:|
| 1      | there are lines where the pipe separator is missing, causing null values in country columns | 1007459-1007463 |
| 2     | some where there are not separator between the current line and the next one      |   1144490-1144491 |
| 3 | lines where there are no information have to be deleted      |    1144561~ |
| 4      | some are simply separated by a comma instead of a pipe | 1242927-1242931 |
| 5     | some country codes are duplicated      |   ~ |
| 6 | some of them are negatives   |    1243014 - 1243017 |
| 7     | there are ' ' values in user_id      |   151343 - 151346 |
| 8 | there are null values in user_id     |    1564822 - 1564828 |

To clean these data, we wrote the `cleaning_script`. It first loads the data and date from the log file, 'flatten' lines which contains more than one stream on the same line (error #2), and treat other errors.
After cleaning the data, it saves in the same diretory, two csv files: one for top 50 songs by country and another for top 50 songs by users.

After execution we should have this structure:

    .
    ├── logs                                         
    │   │── sample_listen-2021-12-01_2Mlines.log
    │   ├── country_sample_listen-2021-12-01_2Mlines.csv       [*]  
    │   └── user_sample_listen-2021-12-01_2Mlines.csv          [*]      
    ├── modules                                         
    │   └── functions_modules.py                                       
    ├── cleaning_script.py                              
    ├── script.sh
    ├── top50s                                                                               
    ├── top50_script.py
    └── README.md

`sample_listen-2021-12-01_2Mlines.csv` is csv file which have sng_id, country and date as columns, used to generate top 50 songs by country

`sample_listen-2021-12-01_2Mlines.csv` is csv file which have sng_id, user_id and date as columns, used to generate top 50 songs by user

Then the `top50_script` comes into play. It loads the saved dataframes, check if there's csv files (country_last_saved_df, user_last_saved_df) in the initial directory. These csv files normally contain the last record of the 7 last days for the top 50 songs. If this file exists we load it then concatenate with the data of the new day. If not (the first day), we simply use the data of that day. We apply a filter on the dataset to keep only the last 7 days records, save data as CSVs (and rename it to last_saved_df) then generate the Top 50 songs files.

After execution of the script we should have:

    .
    ├── logs                                         
    │   │── sample_listen-2021-12-01_2Mlines.log
    │   ├── country_last_saved_df.csv
    │   ├── user_last_saved_df.csv       
    ├── modules                                         
    │   └── functions_modules.py                                       
    ├── cleaning_script.py                              
    ├── script.sh
    ├── top50s
    │   │── country_top50_2021-12-01.txt                    [*]
    │   └── user_top50_2021-12-01.txt                       [*]
    ├── top50_script.py
    └── README.md                                

`functions_module` contains functions written to make the code modular and more. maintainable. The functions are documented.

The `script` bash run first cleaning_script and top50_script. It is this file which will be running each day, at a certain time to compute the files we receive.


How to run it every day to compute the files ?
======

To automate the running of the scripts, make sure cron is installed `crontab -l` if not, install it `apt-get install cron`.

We supposed we run the cleaning_script each day at 01h00 and top50_script at 01h10. In a terminal type `crontab -e` and add at the end of the file these commands  `0 1 * * * /usr/bin/python3 'full path'/cleaning_script.py >> cleaning.log 2>&1` and `10 1 * * * python3 'full path'/top50_script.py >> top50.log 2>&1` save and close the editor. You're all set.


Note: The `main` branch have the version where we consider that we are getting all log in one same folder and `many folders` we are getting each log file in its own folder.