#NMAPA SPRING - 2019.
#Jeanho Rodriguez.
#Date: 7/17/2019.

import pprint
import pandas as pd
import json
import xlrd
import numpy as np
import os
#import jinja2
import datetime
os.getcwd()
os.listdir(os.getcwd())
from numpy import nan as NA
from pandas import Series, DataFrame
from functools import reduce
from collections import Counter

# how to set display
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

# increase column width
pd.set_option('display.max_colwidth', 1000)

# read csv file-- unicode errors -- use unicode_escape

df = pd.read_csv("NMAPA_merged_schools.csv", sep=',', header=0, skipinitialspace=True, low_memory=False)

df.rename(columns={'distcode':'DistrictCode'}, inplace=True)

df['Code'] = df['Code'].astype(str)
# last three of Code
df['SchoolCode'] = df['Code'].str[-5:]



df['Proficient'] = float

df.loc[(df['PL'] == 3.0), 'Proficient'] = 1.0
df.loc[(df['PL'] == 4.0), 'Proficient'] = 1.0
df.loc[(df['PL'] == 2.0), 'Proficient'] = 0.0
df.loc[(df['PL'] == 1.0), 'Proficient'] = 0.0




###################################SOAP#################################################################################
# School level
#df_school = df[['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code','PL']].copy()
#df_school = (df_school.groupby(['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code','PL'])['PL'].count().reset_index(name='N_PL')) #reset index moves index to columns
#df_school= df_school.pivot_table(index=['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code'] , columns='PL', values='N_PL',
                    #aggfunc ='sum', margins=True, dropna=True, fill_value=0)
#df_school_index = df_school.reset_index()


# District Level
df_district = df[['DistrictCode','SchoolCode','District','Test_Grade','Subtest','Sort_Code','PL']].copy()
df_district['SchoolCode'] = 000.0
df_district['School'] = 'Districtwide'
df_district['Code'] = df_district['DistrictCode'] * 1000
df_district = (df_district.groupby(['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code','PL'])['PL'].count().reset_index(name='N_PL')) #reset index moves index to columns
df_district= df_district.pivot_table(index=['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code'] , columns='PL', values='N_PL',
                    aggfunc ='sum', margins=True, dropna=True, fill_value=0)
df_district_index = df_district.reset_index()

# District Level Proficient
#df_district_prof = df[['DistrictCode','SchoolCode','District','Test_Grade','Subtest','Sort_Code','Proficient']].copy()
#df_district_prof['SchoolCode'] = 000.0
#df_district_prof['School'] = 'Districtwide'
#df_district_prof['Code'] = df_district_prof['DistrictCode'] * 1000
#df_district_prof = (df_district_prof.groupby(['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code','Proficient'])['Proficient'].count().reset_index(name='N_Proficient')) #reset index moves index to columns
#df_district_prof= df_district_prof.pivot_table(index=['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code'] , columns='Proficient', values='N_Proficient',
                    #aggfunc ='sum', margins=True, dropna=True, fill_value=0)
#df_district_prof_index = df_district_prof.reset_index()


#df_district_prof_index = df_district_prof_index[['Code',1,'All']]
#df_district_prof_index.rename(columns={1:'1_prof'}, inplace=True)
#df_district_prof_index.rename(columns={'All':'All_prof'}, inplace=True)




# State Level
df_state = df[['DistrictCode','SchoolCode','District','Test_Grade','Subtest','Sort_Code','PL']].copy()
df_state['DistrictCode'] = 99
df_state['SchoolCode'] = 999.0
df_state['School'] = 'All Students'
df_state['Code'] = 999999
df_state['District'] = 'Statewide'
df_state = (df_state.groupby(['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code','PL'])['PL'].count().reset_index(name='N_PL')) #reset index moves index to columns
df_state= df_state.pivot_table(index=['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code'] , columns='PL', values='N_PL',
                    aggfunc ='sum', margins=True, dropna=True, fill_value=0)
df_state_index = df_state.reset_index()



# State Level Proficient
#df_state_prof = df[['DistrictCode','SchoolCode','District','Test_Grade','Subtest','Sort_Code','Proficient']].copy()
#df_state_prof['DistrictCode'] = 99
#df_state_prof['SchoolCode'] = 999.0
#df_state_prof['School'] = 'All Students'
#df_state_prof['Code'] = 999999
#df_state_prof['District'] = 'Statewide'
#df_state_prof = (df_state_prof.groupby(['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code','Proficient'])['Proficient'].count().reset_index(name='N_Proficient')) #reset index moves index to columns
#df_state_prof= df_state_prof.pivot_table(index=['Code','DistrictCode','SchoolCode','District','School','Test_Grade','Subtest','Sort_Code'] , columns='Proficient', values='N_Proficient',
                    #aggfunc ='sum', margins=True, dropna=True, fill_value=0)
#df_state_prof_index = df_state_prof.reset_index()
#df_state_prof_index = df_state_prof_index[['Code',1,'All']]

#df_state_prof_index.rename(columns={1:'1_prof'}, inplace=True)
#df_state_prof_index.rename(columns={'All':'All_prof'}, inplace=True)



# merge school, district, and state levels
df_soap_merge_final = pd.concat([df_district_index,df_state_index], axis =0)

#data_frames = [df_soap_merge_final_no_proficient, df_state_prof_index,df_district_prof_index]

#merge dataframe to add school names
#df_soap_merge_final = reduce(lambda left,right: pd.merge(left,right,on=['Code'], how='outer'), data_frames)

# fill value 0.0
#df_soap_merge_final.fillna(0.0, inplace=True)


#df_soap_merge_final['1_prof'] = df_soap_merge_final['1_prof_x'] + df_soap_merge_final['1_prof_y']
#df_soap_merge_final['All_prof'] = df_soap_merge_final['All_prof_x'] + df_soap_merge_final['All_prof_y']



#check columns names
df_soap_merge_final.rename(columns={1.0:'Level 1'}, inplace=True)
df_soap_merge_final.rename(columns={2.0:'Level 2'}, inplace=True)
df_soap_merge_final.rename(columns={3.0:'Level 3'}, inplace=True)
df_soap_merge_final.rename(columns={4.0:'Level 4'}, inplace=True)

# function for calculating percentage
def division_rule(x, y):
    return (x / y) * 100

df_soap_merge_final['check'] = df_soap_merge_final.apply(lambda x: division_rule(x['Level 1'], x['All']), axis=1)
df_soap_merge_final['check1'] = df_soap_merge_final.apply(lambda x: division_rule(x['Level 2'], x['All']), axis=1)
df_soap_merge_final['check2'] = df_soap_merge_final.apply(lambda x: division_rule(x['Level 3'], x['All']), axis=1)
df_soap_merge_final['check3'] = df_soap_merge_final.apply(lambda x: division_rule(x['Level 4'], x['All']), axis=1)



# Round to nearest tenth
df_soap_merge_final['Proficient'] = df_soap_merge_final['check2'] + df_soap_merge_final['check3']
df_soap_merge_final['check'] = df_soap_merge_final['check'].round(1)
df_soap_merge_final['check1'] = df_soap_merge_final['check1'].round(1)
df_soap_merge_final['check2'] = df_soap_merge_final['check2'].round(1)
df_soap_merge_final['check3'] = df_soap_merge_final['check3'].round(1)
df_soap_merge_final['Proficient'] = df_soap_merge_final['Proficient'].round(1)



# Order and Select Columns by index
df_soap_merge_final = df_soap_merge_final.iloc[:, np.r_[0,1,2,3,4,5,6,7,12,13,14,15,16,17]]


# Remove 'All' Rows & State Charters if 1 school per district
df_soap_merge_final.drop(df_soap_merge_final[df_soap_merge_final.Code == 'All'].index, inplace=True)
df_soap_merge_final.drop(df_soap_merge_final[df_soap_merge_final.District== 'All'].index, inplace=True)
#df_soap_merge_final.drop(df_soap_merge_final[df_soap_merge_final.District== 'State Charter'].index, inplace=True) ### drops schools..... investigate further.

#filter = df_soap_merge_final['DistrictCode'].isin([33]) == True # the ==False means not of isin 'variable'
# command returns the specific record.
#print(df_soap_merge_final[filter])


#check columns names
df_soap_merge_final.rename(columns={'check':'Level 1'}, inplace=True)
df_soap_merge_final.rename(columns={'check1':'Level 2'}, inplace=True)
df_soap_merge_final.rename(columns={'check2':'Level 3'}, inplace=True)
df_soap_merge_final.rename(columns={'check3':'Level 4'}, inplace=True)
df_soap_merge_final.rename(columns={'All':'N'}, inplace=True)

# Map for sortcodes
sort_code_map = {'1':'ALLSTU','2':'FEMALE','3':'MALE','4':'WHITE','5':'BLACK','6':'HISPANIC','7':'ASIAN','8':'NATIVE',
                 '9':'FRL','10':'SWD','11':'ELL','12':'HOMELESS','13':'MILITARY','14':'FOSTER','15':'MIGRANT'}

df_soap_merge_final = df_soap_merge_final.astype({'Sort_Code':str})
df_soap_merge_final = df_soap_merge_final.astype({'Code':str})
df_soap_merge_final = df_soap_merge_final.astype({'SchoolCode':str})


df_soap_merge_final['Sort_Code'] = df_soap_merge_final['Sort_Code'].map(sort_code_map) #map function applied with map rule



print(df_soap_merge_final.head(10))
df_soap_merge_final.to_csv("NMAPA_soap_merge_finalV5.csv", sep=',', encoding='utf-8', index = False)

################################################Web Files###############################################################
df_web = pd.read_csv("merged_web_schools.csv", sep=',', header=0, low_memory=False)

# School Level
#df_copy_school = df[['Code','District','School','Subtest','PL']].copy()
#df_copy_school = (df_copy_school.groupby(['Code','District','School','Subtest','PL'])['PL'].count().reset_index(name='N_PL')) #reset index moves index to columns
#df_copy_school= df_copy_school.pivot_table(index=['Code','District','School','Subtest'] , columns='PL', values='N_PL',
                    #aggfunc ='sum', margins=True, dropna=True, fill_value=0)
#df_copy_school_index = df_copy_school.reset_index()

#df_multi_school_final = df_copy_school.div( df_copy_school.iloc[:,-1], axis =0 ).reset_index()
#df_multi_school_final['N'] = df_copy_school_index.All

# District Level
df_copy_district = df_web[['distcode','District','Subtest','PL']].copy()
df_copy_district['School'] = 'Districtwide'
df_copy_district['Code'] = df_copy_district['distcode'] * 1000
df_copy_district = (df_copy_district.groupby(['Code','District','School','Subtest','PL'])['PL'].count().reset_index(name='N_PL')) #reset index moves index to columns
df_copy_district= df_copy_district.pivot_table(index=['Code','District','School','Subtest'] , columns='PL', values='N_PL',
                    aggfunc ='sum', margins=True, dropna=True, fill_value=0)
df_copy_district_index = df_copy_district.reset_index()
df_multi_district_final = df_copy_district.div( df_copy_district.iloc[:,-1], axis =0 ).reset_index()
df_multi_district_final['N'] = df_copy_district_index.All

# State Level
df_copy_state = df_web[['distcode','District','Subtest','PL']].copy()
df_copy_state['School'] = 'All Students'
df_copy_state['Code'] = 999999
df_copy_state['District'] = 'Statewide'
df_copy_state = (df_copy_state.groupby(['Code','District','School','Subtest','PL'])['PL'].count().reset_index(name='N_PL')) #reset index moves index to columns
df_copy_state= df_copy_state.pivot_table(index=['Code','District','School','Subtest'] , columns='PL', values='N_PL',
                    aggfunc ='sum', margins=True, dropna=True, fill_value=0)
df_copy_state_index = df_copy_state.reset_index()
df_multi_state_final = df_copy_state.div( df_copy_state.iloc[:,-1], axis =0 ).reset_index()
df_multi_state_final['N'] = df_copy_state_index.All

# stack data frames
MERGED_NMAPA= pd.concat([df_multi_district_final,df_multi_state_final], axis =0)

# Rename PL columns
MERGED_NMAPA.rename(columns={1.0:'Level 1'}, inplace=True)
MERGED_NMAPA.rename(columns={2.0:'Level 2'}, inplace=True)
MERGED_NMAPA.rename(columns={3.0:'Level 3'}, inplace=True)
MERGED_NMAPA.rename(columns={4.0:'Level 4'}, inplace=True)

# sort columns by sortcode ascending.
MERGED_NMAPA = MERGED_NMAPA.sort_values(['Code','District','School'], ascending=[True,True,True])


# clean Code... adds leading zeros
MERGED_NMAPA.drop(MERGED_NMAPA[MERGED_NMAPA.Code == 'All'].index, inplace=True)
MERGED_NMAPA = MERGED_NMAPA.astype({'Code':int})
#MERGED_NMAPA['Code'] = MERGED_NMAPA['Code'].apply(lambda x: '{0:0>6}'.format(x))

# convert to percentage
MERGED_NMAPA['Level 1'] = MERGED_NMAPA['Level 1'] * 100
MERGED_NMAPA['Level 2'] = MERGED_NMAPA['Level 2'] * 100
MERGED_NMAPA['Level 3'] = MERGED_NMAPA['Level 3'] * 100
MERGED_NMAPA['Level 4'] = MERGED_NMAPA['Level 4'] * 100

# Format str
MERGED_NMAPA['District'] = MERGED_NMAPA['District'].str.title()
#MERGED_NMAPA['School'] = MERGED_NMAPA['School'].str.title()

#MERGED_NMAPA.to_csv("NMAPA_web_merge_final.csv", sep=',', encoding='utf-8', index = False)

####### MASKING ######################################################################################################
# round to nearest integer
MERGED_NMAPA['Level 1'] = MERGED_NMAPA['Level 1'].round(0)
MERGED_NMAPA['Level 2'] = MERGED_NMAPA['Level 2'].round(0)
MERGED_NMAPA['Level 3'] = MERGED_NMAPA['Level 3'].round(0)
MERGED_NMAPA['Level 4'] = MERGED_NMAPA['Level 4'].round(0)

# remove records with fewer than 10 students
WEB_MERGED_NMAPA = MERGED_NMAPA
#print(WEB_MERGED_NMAPA['N'].sum()) # 9503

WEB_MERGED_NMAPA = WEB_MERGED_NMAPA.loc[WEB_MERGED_NMAPA['N'] >= 10]
#print(WEB_MERGED_NMAPA['N'].sum()) # 8866


def masking_rule(x, y):
    # N = 301 or higher
    if x >= 99.0 and y > 300:
        return '≥99'
    elif x <= 1.0 and y > 300:
        return '≤1'
    elif x < 99.0 and y > 300:
        return str(x)

    # N = 201 - 300
    elif x >= 98.0 and 200 < y <= 300:
        return '≥98'
    elif x <= 2.0 and 200 < y <= 300:
        return '≤2'
    elif 2.0 < x < 98.0 and 200 < y <= 300:
        return str(x)

    # N = 101 - 200
    elif x < 3.0 and 100 < y <= 200:
        return '≤2'
    elif 3.0 <= x < 5.0 and 100 < y <= 200:
        return '3-4'
    elif 5.0 <= x < 10.0 and 100 < y <= 200:
        return '5-9'
    elif 10.0 <= x < 15.0 and 100 < y <= 200:
        return '10-14'
    elif 15.0 <= x < 20.0 and 100 < y <= 200:
        return '15-19'
    elif 20.0 <= x < 25.0 and 100 < y <= 200:
        return '20-24'
    elif 25.0 <= x < 30.0 and 100 < y <= 200:
        return '25-29'
    elif 30.0 <= x < 35.0 and 100 < y <= 200:
        return '30-34'
    elif 35.0 <= x < 40.0 and 100 < y <= 200:
        return '35-39'
    elif 40.0 <= x < 45.0 and 100 < y <= 200:
        return '40-44'
    elif 45.0 <= x < 50.0 and 100 < y <= 200:
        return '45-49'
    elif 50.0 <= x < 55.0 and 100 < y <= 200:
        return '50-54'
    elif 55.0 <= x < 60.0 and 100 < y <= 200:
        return '55-59'
    elif 60.0 <= x < 65.0 and 100 < y <= 200:
        return '60-64'
    elif 65.0 <= x < 70.0 and 100 < y <= 200:
        return '65-69'
    elif 70.0 <= x < 75.0 and 100 < y <= 200:
        return '70-74'
    elif 75.0 <= x < 80.0 and 100 < y <= 200:
        return '75-79'
    elif 80.0 <= x < 85.0 and 100 < y <= 200:
        return '80-84'
    elif 85.0 <= x < 90.0 and 100 < y <= 200:
        return '85-89'
    elif 90.0 <= x < 95.0 and 100 < y <= 200:
        return '90-94'
    elif 95.0 <= x < 98.0 and 100 < y <= 200:
        return '95-97'
    elif 98.0 <= x and 100 < y <= 200:
        return 'GE 98'

    # N = 41 - 100
    elif 6.0 > x and 40 < y <= 100:
        return '≤5'
    elif 6.0 <= x < 10.0 and 40 < y <= 100:
        return '6-9'
    elif 10.0 <= x < 15.0 and 40 < y <= 100:
        return '10-14'
    elif 15.0 <= x < 20.0 and 40 < y <= 100:
        return '15-19'
    elif 20.0 <= x < 25.0 and 40 < y <= 100:
        return '20-24'
    elif 25.0 <= x < 30.0 and 40 < y <= 100:
        return '25-29'
    elif 30.0 <= x < 35.0 and 40 < y <= 100:
        return '30-34'
    elif 35.0 <= x < 40.0 and 40 < y <= 100:
        return '35-39'
    elif 40.0 <= x < 45.0 and 40 < y <= 100:
        return '40-44'
    elif 45.0 <= x < 50.0 and 40 < y <= 100:
        return '45-49'
    elif 50.0 <= x < 55.0 and 40 < y <= 100:
        return '50-54'
    elif 55.0 <= x < 60.0 and 40 < y <= 100:
        return '55-59'
    elif 60.0 <= x < 65.0 and 40 < y <= 100:
        return '60-64'
    elif 65.0 <= x < 70.0 and 40 < y <= 100:
        return '65-69'
    elif 70.0 <= x < 75.0 and 40 < y <=100:
        return '70-74'
    elif 75.0 <= x < 80.0 and 40 < y <=100:
        return '75-79'
    elif 80.0 <= x < 85.0 and 40 < y <= 100:
        return '80-84'
    elif 85.0 <= x < 90.0 and 40 < y <= 100:
        return '85-90'
    elif 90.0 <= x < 95.0 and 40 < y <= 100:
        return '90-94'
    elif 95.0 <= x and 40 < y <= 100:
        return '≥95'

    # N = 21-40
    elif 11.0 > x and 20 < y <= 40:
        return '≤ 10'
    elif 11.0 <= x < 20.0 and 20 < y <= 40:
        return '11-19'
    elif 20.0 <= x < 30.0 and 20 < y <= 40:
        return '20-29'
    elif 30.0 <= x < 40.0 and 20 < y <= 40:
        return '30-39'
    elif 40.0 <= x < 50.0 and 20 < y <= 40:
        return '40-49'
    elif 50.0 <= x < 60.0 and 20 < y <= 40:
        return '50-59'
    elif 60.0 <= x < 70.0 and 20 < y <= 40:
        return '60-69'
    elif 70.0 <= x < 80.0 and 20 < y <=40:
        return '70-79'
    elif 80.0 <= x < 90.0 and 20 < y <=40:
        return '80-89'
    elif 90.0 <= x and 20  < y <= 40:
        return '≥90'


# apply masking rule
WEB_MERGED_NMAPA['check'] = WEB_MERGED_NMAPA.apply(lambda x: masking_rule(x['Level 1'], x['N']), axis = 1)
WEB_MERGED_NMAPA['check2'] = WEB_MERGED_NMAPA.apply(lambda x: masking_rule(x['Level 2'], x['N']), axis = 1)
WEB_MERGED_NMAPA['check3'] = WEB_MERGED_NMAPA.apply(lambda x: masking_rule(x['Level 3'], x['N']), axis = 1)
WEB_MERGED_NMAPA['check4'] = WEB_MERGED_NMAPA.apply(lambda x: masking_rule(x['Level 4'], x['N']), axis = 1)

# N - 10 - 20
def masking_rule2(x, y, z):
    if z < 21:
        return str(x + y)

# apply masking rule 2
WEB_MERGED_NMAPA['check5'] = WEB_MERGED_NMAPA.apply(lambda x: masking_rule2(x['Level 1'], x['Level 2'], x['N']), axis=1)
WEB_MERGED_NMAPA['check6'] = WEB_MERGED_NMAPA.apply(lambda x: masking_rule2(x['Level 3'], x['Level 4'], x['N']), axis=1)

# formatting and removing columns
WEB_MERGED_NMAPA.loc[(WEB_MERGED_NMAPA['check'].isnull()) & (WEB_MERGED_NMAPA['N'] < 21), 'check'] = '^'
WEB_MERGED_NMAPA.loc[(WEB_MERGED_NMAPA['check4'].isnull()) & (WEB_MERGED_NMAPA['N'] < 21), 'check4'] = '^'

WEB_MERGED_NMAPA = WEB_MERGED_NMAPA.astype({'check5':float})
WEB_MERGED_NMAPA = WEB_MERGED_NMAPA.astype({'check6':float})

WEB_MERGED_NMAPA.loc[WEB_MERGED_NMAPA['check5'] >= 80.0, 'check2'] = '≥ 80'
WEB_MERGED_NMAPA.loc[WEB_MERGED_NMAPA['check6'] <= 20.0, 'check3'] = '≤ 20'


# Duplicated indexes.. reset index
#print(WEB_SBA_SPAN[WEB_SBA_SPAN.index.duplicated()])
WEB_NMAPA_FINAL = WEB_MERGED_NMAPA.reset_index()

WEB_NMAPA_FINAL.loc[(WEB_NMAPA_FINAL['check2'].isnull()) & (WEB_NMAPA_FINAL['N'] < 21), 'check2'] = WEB_NMAPA_FINAL['check5']
WEB_NMAPA_FINAL.loc[(WEB_NMAPA_FINAL['check3'].isnull()) & (WEB_NMAPA_FINAL['N'] < 21), 'check3'] = WEB_NMAPA_FINAL['check6']

# remove .0
WEB_NMAPA_FINAL['check'] = WEB_NMAPA_FINAL['check'].astype(str).replace('\.0', '', regex=True)
WEB_NMAPA_FINAL['check2'] = WEB_NMAPA_FINAL['check2'].astype(str).replace('\.0', '', regex=True)
WEB_NMAPA_FINAL['check3'] = WEB_NMAPA_FINAL['check3'].astype(str).replace('\.0', '', regex=True)
WEB_NMAPA_FINAL['check4'] = WEB_NMAPA_FINAL['check4'].astype(str).replace('\.0', '', regex=True)

# rename columns
WEB_NMAPA_FINAL.rename(columns={'check':'Level 1 %'}, inplace=True)
WEB_NMAPA_FINAL.rename(columns={'check2':'Level 2 %'}, inplace=True)
WEB_NMAPA_FINAL.rename(columns={'check3':'Level 3 %'}, inplace=True)
WEB_NMAPA_FINAL.rename(columns={'check4':'Level 4 %'}, inplace=True)

#WEB_NMAPA_FINAL['Level 1 %'] = WEB_NMAPA_FINAL['Level 1 %'].astype(int)
#WEB_NMAPA_FINAL['Level 2 %'] = WEB_NMAPA_FINAL['Level 2 %'].astype(int)
#WEB_NMAPA_FINAL['Level 3 %'] = WEB_NMAPA_FINAL['Level 3 %'].astype(int)
#WEB_NMAPA_FINAL['Level 4 %'] = WEB_NMAPA_FINAL['Level 4 %'].astype(int)


# need to mask compiled cells.

# N < 21
#def masking_rule3(x, y):
    #if y < 21 and 21 <= x < 30:
        #return '21-29'
    #elif y < 21 and 30 <= x < 40:
        #return '30-39'
    #elif y < 21 and 40 <= x < 50:
        #return '40-49'
    #elif y < 21 and 50 <= x < 60:
        #return '50-59'
    #elif y < 21 and 60 <= x < 70:
        #return '60-69'
    #elif y < 21 and 70 <= x < 80:
        #return '70-79'


# apply masking rule 2
#WEB_NMAPA_FINAL['check7'] = WEB_NMAPA_FINAL.apply(lambda x: masking_rule3(x['Level 2 %'], x['N']), axis=1)
#WEB_NMAPA_FINAL['check8'] = WEB_NMAPA_FINAL.apply(lambda x: masking_rule3(x['Level 3 %'], x['N']), axis=1)

#print(WEB_NMAPA_FINAL.head(10))


# Order and Select Columns by index
#WEB_NMAPA_FINAL = WEB_NMAPA_FINAL.iloc[:, np.r_[1,2,3,4,11,12,13,14]]


#WEB_NMAPA_FINAL.drop(WEB_NMAPA_FINAL[WEB_NMAPA_FINAL.District== 'State Charter'].index, inplace=True)

# encoding utf-8 producing undesirable characters.. use utf-8-sig or utf-16
# excel converting strings to dates, save file as txt and use import wizard as workaround
#WEB_NMAPA_FINAL.to_csv("WEB_NMAPA_FINAL.txt", sep=',', encoding='utf-8-sig', index = False)


















################################################# Scale Scores##########################################################
#merged_NMAPA['OldLo'] = 100
#merged_NMAPA['OldHi'] = 900
#merged_NMAPA['OldCut'] = 0
#merged_NMAPA['NewLo'] = 0
#merged_NMAPA['NewHigh'] = 200
#merged_NMAPA['NewCut'] = 100
#merged_NMAPA['NewSS'] = 0

#def Oldcut(x, y):
    #if x == 'MATH' and y in ['03','04','05']:
        #return 503
    #elif x == 'MATH' and y in ['06', '07', '08']:
        #return 500
    #elif x == 'MATH' and y in ['09', '10', '11', '12']:
        #return 506
    #elif x == 'READ' and y in ['03','04','05']:
        #return 463
    #elif x == 'READ' and y in ['06','07','08']:
        #return 459
    #elif x == 'READ' and y in ['09', '10', '11', '12']:
        #return 479
    #elif x == 'SCI' and y in ['03','04','05']:
        #return 491
    #elif x == 'SCI' and y in ['06', '07', '08']:
        #return 491
    #elif x == 'SCI' and y in ['09', '10', '11', '12']:
        #return 501
    #elif x == 'SS' and y in ['09', '10', '11', '12']:
        #return 500
    #else:
        #return 999

#merged_NMAPA['OldCut'] = merged_NMAPA.apply(lambda x: Oldcut(x['Subject'], x['Grade']), axis = 1)

#merged_NMAPA['OldSpanLo'] = merged_NMAPA['OldCut'] - merged_NMAPA['OldLo']
#merged_NMAPA['OldSpanHi'] = merged_NMAPA['OldHi'] - merged_NMAPA['OldCut']
#merged_NMAPA['NewSpanLo'] = merged_NMAPA['NewCut'] - merged_NMAPA['NewLo']
#merged_NMAPA['NewSpanHi'] = merged_NMAPA['NewHi'] - merged_NMAPA['NewCut']

#print(merged_NMAPA['OldCut'].value_counts(dropna=False))

#merged_NMAPA.to_csv("NMAPA_Df_06252019.csv", sep=',', encoding='utf-8', index = False)


# select for a spcific value in a column in  a dataframe
# ~ 50 missing student ids
#df_filter = merged_NMAPA['StudentID'].isin(['NaN']) == True
#df_filter = merged_NMAPA['Grade'].isin(['NaN']) == True

#def New_SS(x, y):
    #if x < y:
        #return x - merged_NMAPA['OldLo']
        #return 503
    #elif x == 'MATH' and y in ['6', '7', '8']:
        #return 700
    #elif x == 'SHOW':
        #return 200
    #else:
        #return 100

#merged_NMAPA['New_SS'] = merged_NMAPA.apply(lambda x: Oldcut(x['SS'], x['OldCut']), axis = 1)



#print(merged_NMAPA)



############################################################# NMAPA PRE-ID##############################################




















