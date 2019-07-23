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

schools_web_df = schools_web_df[['schnumb','LoGrade','HiGrade','level']]

schools_web_df.rename(columns={'schnumb':'Code'}, inplace=True)

df['Code'] = df['Code'].astype(float)
dataframe = [df,schools_web_df]


#merge dataframe to add school names
merged_df = reduce(lambda left,right: pd.merge(left,right,on=['Code'], how='outer'), dataframe)

merged_df['School_Grade_Range'] = merged_df['LoGrade'] + '-' + merged_df['HiGrade'] + ' '+ 'Grade'

cross_tab_grade = pd.crosstab(merged_df.School_Grade_Range, merged_df.Test_Grade, margins=True)  # school code 126 missing from vendor
cross_tab_gradeII = pd.crosstab(merged_df.level, merged_df.Test_Grade, margins=True)

cross_tab_grade.to_csv("school_grade_grade_cross.csv", sep=',', encoding='utf-8-sig', index = True)
cross_tab_gradeII.to_csv("school_grade_grade_crossII.csv", sep=',', encoding='utf-8-sig', index = True)
print(cross_tab_grade)
print(cross_tab_gradeII)
