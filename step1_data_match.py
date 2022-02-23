################# IMPORTS  ################

import os 
from os import listdir
from os.path import isfile, join

import pandas as pd
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt


from io import StringIO
from io import BytesIO

import matplotlib.pyplot as plt
from astropy.io import ascii, fits
from astropy.table import Table, join, hstack,vstack,QTable
from astropy.table import Table

from esutil import htm

#################  FUNCTIONS  ################

def match(cat_1, cat_2, column_1, column_2, column_3, column_4, error):
    'Function to make the matching with two tables, using the esutil'
    h = htm.HTM(depth=10)
    m1, m2, d12 = h.match(np.array(cat_1[column_1]), 
                          np.array(cat_1[column_3]),
                          np.array(cat_2[column_2]), 
                          np.array(cat_2[column_4]),
                          error, maxmatch=1)
    
    submatched = cat_1[m1]
    manmatched = cat_2[m2]
    matched = hstack([submatched, manmatched])
      
    return matched

def load_data_from_multiples_files(directory):
    '''
    directory = '/media/new-drive/CamilaCardoso/DES/'
    input-> string with the path from the folder that has the fits files
    output-> pandas dataframe with the complete data
    '''
    table_list = []
    for directory, subfolders, archives in os.walk(directory):
        for archive in archives:
            # table read and transform to a pandas dataframe
            df = Table.read(os.path.join(directory, archive)).to_pandas()
            table_list.append(df)
            # log the process whith the next line
            #print(os.path.join(directory, archive))
    concat_data = pd.concat(table_list, axis=0, ignore_index=True)
    return concat_data


#################  LOAD DATA  ################

# DES DATA
directory_des_data = '/media/new-drive/CamilaCardoso/DES/'
des_data = load_data_from_multiples_files(directory_des_data)

# SLOAN DATA
directory_sloan_data = '/media/new-drive/CamilaCardoso/SLOAN'
sloan_data_file = 'SLOAN_DR16_sloan_data_quasar_all.fits'
sloan_data_dr16 = Table.read(os.path.join(directory_sloan_data, sloan_data_file))

#################  MATCH  ################

# Convert a pandas data frame to a table
des_data_table = Table.from_pandas(des_data)

# Match
error = 0.0002 # 1 second of arc = 0.0002778 degrees
match_des_sloan = match(sloan_data_dr16,des_data_table,'ra','RA','dec','DEC',error)


#################  SAMPLING  ################


match_des_sloan = match_des_sloan.to_pandas()
# Convert the column 'class' from bits to string
match_des_sloan['class'] = match_des_sloan['class'].str.decode("utf-8")

# Dividing the objects by type
match_qso = match_des_sloan[match_des_sloan['class'] == 'QSO']
match_star = match_des_sloan[match_des_sloan['class'] == 'STAR']
match_galaxy = match_des_sloan[match_des_sloan['class'] == 'GALAXY']

##### Quasars sampling #####

# Group all objects by Npix and count the quantities
group_npix = match_qso.groupby(['Npix']).size().reset_index(name='counts')
# Sorts all values based on the 'counts' column in descending order 
group_npix_ordered = group_npix.sort_values(by='counts',ascending=False)
# Resets the index count
group_npix_ordered = group_npix_ordered.reset_index()
# Selects 20% of the most populated pixels of quasars
quasars_sample = group_npix_ordered.loc[0:(len(group_npix_ordered)//5)-1]

##### Star sampling #####

# Group all objects by Npix and count the quantities
group_npix = match_star.groupby(['Npix']).size().reset_index(name='counts')
# Sorts all values based on the 'counts' column in descending order 
group_npix_ordered = group_npix.sort_values(by='counts',ascending=False)
# Resets the index count
group_npix_ordered = group_npix_ordered.reset_index()
# Selects 20% of the most populated pixels of quasars
star_sample = group_npix_ordered.loc[0:(len(group_npix_ordered)//5)-1]

##### Galaxy sampling #####

# Group all objects by Npix and count the quantities
group_npix = match_galaxy.groupby(['Npix']).size().reset_index(name='counts')
# Sorts all values based on the 'counts' column in descending order 
group_npix_ordered = group_npix.sort_values(by='counts',ascending=False)
# Resets the index count
group_npix_ordered = group_npix_ordered.reset_index()
# Selects 20% of the most populated pixels of quasars
galaxy_sample = group_npix_ordered.loc[0:(len(group_npix_ordered)//5)-1]

##### Treating all the three samples  #####

# Group all the three samples(quasars, galaxy and stars)
group_samples = [quasars_sample, star_sample, galaxy_sample]
grouped_samples = pd.concat(group_samples)
# Restart the index and drop the oldest index column and counts
grouped_samples.drop(['index', 'counts'], axis=1, inplace=True)
# Select uniques Npix values
Npix_uniques = grouped_samples['Npix'].unique()
# Create a new data frame to put the uniques Npix
Npix_selection = pd.DataFrame()
Npix_selection['Npix'] = Npix_uniques

##### Sampling per Npix #####

# 50% of the Npix values to trainning sample and the rest to test sample
# Getting the trainning sample
npix_sample_50_training = Npix_selection.sample(frac=0.5)
# Getting the testing sample subtracting the training sample Npix values from the original dataframe
npix_sample_50_testing = pd.merge(Npix_selection,npix_sample_50_training,on=['Npix'],how="outer",indicator=True)
npix_sample_50_testing = npix_sample_50_testing[npix_sample_50_testing['_merge']=='left_only']
# Exclud the colunm _merge of the testing sample DF
npix_sample_50_testing.drop(['_merge'], axis=1, inplace=True)

npix_sample_50_training_objects = pd.merge(npix_sample_50_training, match_des_sloan, on = ['Npix'])
npix_sample_50_testing_objects = pd.merge(npix_sample_50_testing, match_des_sloan, on = ['Npix'])

#################  EXTRACTING DATA  ################

path = 'SAMPLES/'

npix_sample_50_training_table = Table.from_pandas(npix_sample_50_training_objects)
npix_sample_50_training_table.write(path + 'sample_per_npix_50_training.fits') 

npix_sample_50_testing_table = Table.from_pandas(npix_sample_50_testing_objects)
npix_sample_50_testing_table.write(path + 'sample_per_npix_50_test.fits')

path = 'MATCH/'
match_table = Table.from_pandas(match_des_sloan)
match_table.write(path + 'match_des_sloan.fits') 
