#NMAPA_PRE_ID_SPRING - 2019.
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
import openpyxl

# how to set display
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

# increase column width
pd.set_option('display.max_colwidth', 1000)

#PRE-ID FIELDS
# District IRN
# District Name
# School IRN
# School Name
# Grade
# Student ID
# Last Name
# First Name
# Middle Initial
# Birth Date(MMDDYYYY)
# Gender
# Ethnicity


# read Test Data files
df_ELA = pd.read_csv("merged_ELA_882019.csv",sep=',', header=0, low_memory=False)
df_MA = pd.read_csv("ADDED DEMO NMAlt MA.csv",sep=',', header=0, low_memory=False)
df_SC = pd.read_csv("ADDED DEMO NMAlt SC.csv",sep=',', header=0, low_memory=False)


# Add columns to df_ELA
df_ELA['S_STUDENT_ID'] = float
#df_ELA['S_DISTRICT_CODE'] = float
#df_ELA['S_DISTRICT_NAME'] = str
#df_ELA['S_LOCATION_CODE'] = float
#df_ELA['S_LOCATION_NAME'] = str
#df_ELA['S_LASTNAME'] = str
#df_ELA['S_FIRSTNAME'] = str
#df_ELA['S_MIDDLE_NAME'] = str
#df_ELA['S_DOB'] = str
df_ELA['S_BMONTH'] = float
df_ELA['S_BDAY'] = float
df_ELA['S_BYEAR'] = float
#df_ELA['S_GENDER'] = str
#df_ELA['S_ETNICITY'] = str
#df_ELA['S_GRADE'] = str
#df_ELA['S_SPECIAL_ED'] = str
#df_ELA['S_MIGRANT'] = str
#df_ELA['S_ELL_STATUS'] = str
#df_ELA['S_HISPANIC_INDICATOR'] = str
#df_ELA['S_FRLP'] = str
#df_ELA['S_STUDENTNAME'] = float
df_ELA['S_BEP'] = str
df_ELA['S_TITLE1'] = str
#df_ELA['S_MILITARY'] = str
#df_ELA['S_GIFTED'] = str
#df_ELA['S_PLAN504'] = str
#df_ELA['S_ELL_LEVEL'] = float
#df_ELA['S_IMMIGRANT'] = str
df_ELA['S_NEW_ARRIVAL'] = str
df_ELA['S_TITLE_III'] = str
df_ELA['S_FOSTER'] = str
#df_ELA['S_HOMELESS'] = str
df_ELA['STATUS'] = 120.0

df_ELA['S_STUDENT_ID'] = df_ELA['STARS_STUDENT_ID']

# Rename Variables
df_ELA.rename(columns={'DISTRICT_CODE':'S_DISTRICT_CODE'}, inplace=True)
df_ELA.rename(columns={'DISTRICT_NAME':'S_DISTRICT_NAME'}, inplace=True)
df_ELA.rename(columns={'LOCATION_ID':'S_LOCATION_CODE'}, inplace=True)
df_ELA.rename(columns={'LOCATION_NAME':'S_LOCATION_NAME'}, inplace=True)
df_ELA.rename(columns={'STUDENT_LAST_NM':'S_LASTNAME'}, inplace=True)
df_ELA.rename(columns={'STUDENT_FIRST_NM':'S_FIRSTNAME'}, inplace=True)
df_ELA.rename(columns={'STUDENT_MID_INIT':'S_MIDDLE_NAME'}, inplace=True)
df_ELA.rename(columns={'STUD_BIRTHDATE':'S_DOB'}, inplace=True)
df_ELA.rename(columns={'STUDENT_GENDER':'S_GENDER'}, inplace=True)
df_ELA.rename(columns={'ETHNIC_DESC':'S_ETNICITY'}, inplace=True)
df_ELA.rename(columns={'CURR_GRADE_LVL':'S_GRADE'}, inplace=True)
df_ELA.rename(columns={'SPECIAL_ED_CODE':'S_SPECIAL_ED'}, inplace=True)
df_ELA.rename(columns={'MIGRANT_CODE':'S_MIGRANT'}, inplace=True)
df_ELA.rename(columns={'LEP_ELIGIBIL_CODE':'S_ELL_STATUS'}, inplace=True)
df_ELA.rename(columns={'HISPANIC_IND':'S_HISPANIC_INDICATOR'}, inplace=True)
df_ELA.rename(columns={'ECONOMIC_CODE':'S_FRLP'}, inplace=True)
df_ELA.rename(columns={'STUDENT_NAME':'S_STUDENTNAME'}, inplace=True)
df_ELA.rename(columns={'MILITARY_FAMILY_DESC':'S_MILITARY'}, inplace=True)
df_ELA.rename(columns={'GIFTED_TALENTED':'S_GIFTED'}, inplace=True)
df_ELA.rename(columns={'PLAN_504':'S_PLAN504'}, inplace=True)
df_ELA.rename(columns={'ENG_PROF_CODE':'S_ELL_LEVEL'}, inplace=True)
df_ELA.rename(columns={'IMMIGRANT_IND':'S_IMMIGRANT'}, inplace=True)
df_ELA.rename(columns={'HOMELESS':'S_HOMELESS'}, inplace=True)
df_ELA.rename(columns={'STUDENT_ID':'STUID'}, inplace=True)


# Order and Select Columns by index
df_ELA = df_ELA.iloc[:, np.r_[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
                              33,34,35,36,37,38,39,40,41,42,75,72,70,73,71,46,47,48,51,76,77,78,53,54,50,56,61,59,67,55,
                              49,79,80,65,58,57,63,60,81,82,83,74,84]]

# append dfs
NMAPA_PRE_DF = pd.concat([df_ELA,df_MA,df_SC], axis =0)

#N = 6206
#print(NMAPA_PRE_DF.info())

# Extract School Code and District Code
NMAPA_PRE_DF['Vendor_Dist_Code'] = NMAPA_PRE_DF['SchoolCode'].str[0:3]
NMAPA_PRE_DF['Vendor_Sch_Code'] = NMAPA_PRE_DF['SchoolCode'].str[-3:]

# populate NaNs
NMAPA_PRE_DF['Vendor_Dist_Code'].fillna('0', inplace=True)
NMAPA_PRE_DF['Vendor_Sch_Code'].fillna('0', inplace=True)
NMAPA_PRE_DF['Grade'].fillna('0', inplace=True)

# change data types
NMAPA_PRE_DF['Vendor_Dist_Code'] = NMAPA_PRE_DF['Vendor_Dist_Code'].astype(int)
NMAPA_PRE_DF['Vendor_Sch_Code'] = NMAPA_PRE_DF['Vendor_Sch_Code'].astype(int)
NMAPA_PRE_DF['Vendor_Sch_Numb'] = (NMAPA_PRE_DF['Vendor_Dist_Code']*1000) + NMAPA_PRE_DF['Vendor_Sch_Code']
NMAPA_PRE_DF['S_Sch_Numb'] = (NMAPA_PRE_DF['S_DISTRICT_CODE']*1000) + NMAPA_PRE_DF['S_LOCATION_CODE']

############################################# SS CUTS ##################################################################
NMAPA_PRE_DF['S_GRADE'] = NMAPA_PRE_DF['S_GRADE'].astype(str)

grades = ['12.0','12']

NMAPA_PRE_DF = NMAPA_PRE_DF.loc[NMAPA_PRE_DF['S_GRADE'].isin(grades)]

#cross_tab_grade = pd.crosstab(NMAPA_PRE_DF.Grade, NMAPA_PRE_DF.S_GRADE, margins=True)  # school code 126 missing from vendor
#cross_tab_sch_numb = pd.crosstab(NMAPA_PRE_DF.Vendor_Sch_Numb, NMAPA_PRE_DF.S_Sch_Numb, margins=True)  # school code 126 missing from vendor
#print(cross_tab_grade)
#print(cross_tab_sch_numb)
#print(NMAPA_PRE_DF.info())

NMAPA_PRE_DF['checker'] = 0

#NMAPA_READ
NMAPA_PRE_DF.loc[(NMAPA_PRE_DF['Subject'] == 'ELA') & (NMAPA_PRE_DF['ScaleScore'] < 479.0), 'checker'] = 1

#NMAPA_MATH
NMAPA_PRE_DF.loc[(NMAPA_PRE_DF['Subject'] == 'Mathmatics') & (NMAPA_PRE_DF['ScaleScore'] < 506.0), 'checker'] = 2

#NMAPA SCIENCE
NMAPA_PRE_DF.loc[(NMAPA_PRE_DF['Subject'] == 'Science') & (NMAPA_PRE_DF['ScaleScore'] < 501.0), 'checker'] = 3

checks = [1,2,3]
NMAPA_PRE_DF = NMAPA_PRE_DF.loc[NMAPA_PRE_DF['checker'].isin(checks)]

print(NMAPA_PRE_DF)

NMAPA_PRE_DF = NMAPA_PRE_DF[['S_DISTRICT_CODE','S_DISTRICT_NAME','S_LOCATION_CODE','S_LOCATION_NAME','S_GRADE','STUID',
                             'LNAME','FNAME','MI','DOB','S_GENDER','Ethnicity']]

NMAPA_PRE_DF.rename(columns={'S_DISTRICT_CODE':'District IRN'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'S_DISTRICT_NAME':'District Name'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'S_LOCATION_CODE':'School IRN'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'S_LOCATION_NAME':'School Name'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'S_GRADE':'Grade'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'STUID':'Student ID'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'LNAME':'Last Name'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'FNAME':'First Name'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'MI':'Middle Initial'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'DOB':'Birth Date(MMDDYYYY)'}, inplace=True)
NMAPA_PRE_DF.rename(columns={'S_GENDER':'Gender'}, inplace=True)


NMAPA_PRE_DF.to_csv("NMAPA_PRE_ID.txt", sep=',', encoding='utf-8-sig', index = False)






