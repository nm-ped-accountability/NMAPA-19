#NMAPA Grade_Check - 2019.
#Jeanho Rodriguez.
#Date: 7/23/2019.

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

# Load M-Schools V3
schools_web_df = pd.read_csv('Master Schools 2019 V3.csv', header=0,dtype={'schnumb':float},low_memory=False)

# Choose SY = 2019
schools_web_df = schools_web_df.loc[schools_web_df['SY'] == '2019']

schools_web_df = schools_web_df[['schnumb','LoGrade','HiGrade','level','schname','distname']]

schools_web_df.rename(columns={'schnumb':'Code'}, inplace=True)
schools_web_df.rename(columns={'schname':'v_schname'}, inplace=True)
schools_web_df.rename(columns={'distname':'v_distname'}, inplace=True)




df['Code'] = df['Code'].astype(float)
dataframe = [df,schools_web_df]


#merge dataframe to add school names
merged_df = reduce(lambda left,right: pd.merge(left,right,on=['Code'], how='outer'), dataframe)

merged_df['School_Grade_Range'] = merged_df['LoGrade'] + '-' + merged_df['HiGrade'] + ' '+ 'Grade'

cross_tab_grade = pd.crosstab(merged_df.School_Grade_Range, merged_df.Test_Grade, margins=True)  # school code 126 missing from vendor
cross_tab_gradeII = pd.crosstab(merged_df.level, merged_df.Test_Grade, margins=True)

#cross_tab_grade.to_csv("school_grade_grade_cross.csv", sep=',', encoding='utf-8-sig', index = True)
#cross_tab_gradeII.to_csv("school_grade_grade_crossII.csv", sep=',', encoding='utf-8-sig', index = True)

####### Merge MasterSchools with S_SCHNUMB #############################################################################
merged_df['S_SCHNUMB'] = merged_df['S_DISTRICT_CODE'] * 1000 + merged_df['S_LOCATION_CODE']

S_schools_web_df = schools_web_df.copy()

S_schools_web_df.rename(columns={'Code':'S_SCHNUMB'}, inplace=True)
S_schools_web_df.rename(columns={'LoGrade':'S_LoGrade'}, inplace=True)
S_schools_web_df.rename(columns={'HiGrade':'S_HiGrade'}, inplace=True)
S_schools_web_df.rename(columns={'level':'S_level'}, inplace=True)
S_schools_web_df.rename(columns={'v_schname':'S_schname'}, inplace=True)
S_schools_web_df.rename(columns={'v_distname':'S_distname'}, inplace=True)

dataframe = [merged_df,S_schools_web_df]

#merge dataframe to add school names
S_merged_df = reduce(lambda left,right: pd.merge(left,right,on=['S_SCHNUMB'], how='outer'), dataframe)


S_merged_df['S_School_Grade_Range'] = S_merged_df['S_LoGrade'] + '-' + S_merged_df['S_HiGrade'] + ' '+ 'Grade'

S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-4 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'Code'] = S_merged_df['S_SCHNUMB']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-4 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'District'] = S_merged_df['S_schname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-4 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'School'] = S_merged_df['S_distname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-4 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'School_Grade_Range'] = S_merged_df['S_School_Grade_Range']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-4 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'DistrictCode'] = S_merged_df['S_DISTRICT_CODE']

S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'Code'] = S_merged_df['S_SCHNUMB']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'District'] = S_merged_df['S_schname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'School'] = S_merged_df['S_distname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'School_Grade_Range'] = S_merged_df['S_School_Grade_Range']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '-1-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'DistrictCode'] = S_merged_df['S_DISTRICT_CODE']

S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '0-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'Code'] = S_merged_df['S_SCHNUMB']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '0-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'District'] = S_merged_df['S_schname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '0-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'School'] = S_merged_df['S_distname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '0-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'School_Grade_Range'] = S_merged_df['S_School_Grade_Range']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '0-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'DistrictCode'] = S_merged_df['S_DISTRICT_CODE']

S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '3-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'Code'] = S_merged_df['S_SCHNUMB']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '3-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'District'] = S_merged_df['S_schname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '3-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'School'] = S_merged_df['S_distname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '3-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'School_Grade_Range'] = S_merged_df['S_School_Grade_Range']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '3-5 Grade') & (S_merged_df['Test_Grade'] == '6-8 Grade'), 'DistrictCode'] = S_merged_df['S_DISTRICT_CODE']

S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '6-8 Grade') & (S_merged_df['Test_Grade'] == '10-11 Grade'), 'Code'] = S_merged_df['S_SCHNUMB']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '6-8 Grade') & (S_merged_df['Test_Grade'] == '10-11 Grade'), 'District'] = S_merged_df['S_schname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '6-8 Grade') & (S_merged_df['Test_Grade'] == '10-11 Grade'), 'School'] = S_merged_df['S_distname']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '6-8 Grade') & (S_merged_df['Test_Grade'] == '10-11 Grade'), 'School_Grade_Range'] = S_merged_df['S_School_Grade_Range']
S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '6-8 Grade') & (S_merged_df['Test_Grade'] == '10-11 Grade'), 'DistrictCode'] = S_merged_df['S_School_Grade_Range']


#S_merged_df.loc[(S_merged_df['School_Grade_Range'] == '0-8 Grade') & (S_merged_df['Test_Grade'] == '10-11 Grade'), 'School_Grade_Range'] = S_merged_df['S_School_Grade_Range']




S_cross_tab_grade = pd.crosstab(S_merged_df.School_Grade_Range, S_merged_df.Test_Grade, margins=True)  # school code 126 missing from vendor
S_cross_tab_gradeII = pd.crosstab(S_merged_df.S_level, S_merged_df.Test_Grade, margins=True)

# select for a spcific value in a column in  a dataframe
df_filter = (S_merged_df['School_Grade_Range'].isin(['-1-5 Grade']) == True) & (S_merged_df['Test_Grade'].isin(['6-8 Grade']))  # the ==False means not of isin 'variable'
df_filter2 = (S_merged_df['School_Grade_Range'].isin(['0-8 Grade']) == True) & (S_merged_df['Test_Grade'].isin(['10-11 Grade']))  # the ==False means not of isin 'variable'

# command returns the specific record.
discrepant = (S_merged_df[df_filter2])
#discrepant.to_csv("discrepant.csv", sep=',',encoding='utf-8', index = False )

# 537984189 is a 3rd grade who took a 6th grade NMAPA test....
#print(S_cross_tab_grade)
#print(discrepant)

#print(S_merged_df.head(5))
#S_merged_df.to_csv("S_merged_df.csv", sep=',', encoding='utf-8-sig', index = True)


