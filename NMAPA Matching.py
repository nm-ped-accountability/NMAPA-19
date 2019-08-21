#NMAPA Matching - 2019.
#Jeanho Rodriguez.
#Date: 4/24/2019.

import pandas as pd
import json
import xlrd
import numpy as np
import os
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

# read csv file-- unicode errors used unicode_escape
#df = pd.read_csv('MATCHED NMAPA 0422 - WORK.csv',header=0, low_memory=False, encoding = 'unicode_escape')

#df['Match'] = 'No'

# flag BIE

#df.loc[df['School'].isin(['601_001','604_004','605_005','606_006','607_007','608_008','612_012','614_014','618_018',
                        #'619_019','621_021','624_024','625_025','626_026','630_030','631_031','634_034','635_035',
                        #'636_036','637_037','639_039','640_040','641_041','695_014']), 'Match'] = 'BIE'



# mathing algos

#df.loc[(df['_Match'] == 'Match'), 'Match'] = 'yes'

#df.loc[(df['_Match'].isin(['Near','Not'])) & (df['NASIS_ID'] == df['STARS_STUDENT_ID']), 'Match'] = 'yes'

#df.loc[(df['_Match'].isin(['Near' or 'Not'])) & (df['StudentID_DS'] == df['STARS_STUDENT_ID']) &
       #(df['STARS_DOB1'] == df['BirthString']), 'Match'] = 'yes'

#df.loc[(df['_Match'].isin(['Near','Not'])) & (df['STARS_DOB1'] == df['BirthString']) &
#(df['N_Fname_DS'] == df['STARS_STUDENT_FIRST_NM']) &
#(df['N_Lname_DS'] == df['STARS_STUDENT_LAST_NM']), 'Match'] = 'yes'


#df.to_csv("NMAPA Matching I 042519.csv", sep=',', encoding='utf-8', index = False)

# read csv file-- unicode errors used unicode_escape
# import both full extract and nmapa matching
# keep fields from NMAPA matching
# crosswalk field values from NMAPA matching to full extract values and field.
# merge both files together
# replace values in full extract with full information from nmapa matching
# keep necessary fields
# output and send via move-it



df = pd.read_csv('NMAPA Matching I 042619 - II.csv',header=0, low_memory=False, encoding = 'unicode_escape')
#print(df.info())


df = df[['StudentID_DS','STARS_STUDENT_ID','STARS_DOB1','BirthString','S_GENDER','S_ETNICITY','S_GRADE','S_SPECIAL_ED',
    'S_MIGRANT','S_ELL_STATUS','S_HISPANIC_INDICATOR','S_FRLP','S_BEP','S_TITLE1','S_MILITARY','S_GIFTED','S_PLAN504',
    'S_IMMIGRANT','S_NEW_ARRIVAL','S_TITLE1','Match']]



df.rename(columns={'StudentID_DS':'ExternalID'}, inplace=True)
df.rename(columns={'STARS_STUDENT_ID':'STARS_STUDENT_ID2'}, inplace=True)
df.rename(columns={'STARS_DOB1':'STARS_DOB2'}, inplace=True)
df.rename(columns={'BirthString':'BirthString2'}, inplace=True)
df.rename(columns={'S_GENDER':'S_GENDER2'}, inplace=True)
df.rename(columns={'S_ETNICITY':'S_ETNICITY2'}, inplace=True)
df.rename(columns={'S_GRADE':'S_GRADE2'}, inplace=True)
df.rename(columns={'S_SPECIAL_ED':'S_SPECIAL_ED2'}, inplace=True)
df.rename(columns={'S_MIGRANT':'S_MIGRANT2'}, inplace=True)
df.rename(columns={'S_HISPANIC_INDICATOR':'S_HISPANIC_INDICATOR2'}, inplace=True)
df.rename(columns={'S_FRLP':'S_FRLP2'}, inplace=True)
df.rename(columns={'S_BEP':'S_BEP2'}, inplace=True)
df.rename(columns={'S_TITLE1':'S_TITLE2'}, inplace=True)
df.rename(columns={'S_MILITARY':'S_MILITARY2'}, inplace=True)
df.rename(columns={'S_GIFTED':'S_GIFTED2'}, inplace=True)
df.rename(columns={'S_PLAN504':'S_PLAN5042'}, inplace=True)
df.rename(columns={'S_IMMIGRANT':'S_IMMIGRANT2'}, inplace=True)
df.rename(columns={'S_NEW_ARRIVAL':'S_NEW_ARRIVAL2'}, inplace=True)
df.rename(columns={'S_ELL_STATUS':'S_ELL_STATUS2'}, inplace=True)


df = df.set_index('ExternalID')

df1 = pd.read_csv('NMAPA_NM_FullExtract_04122019.csv',header=0, low_memory=False, encoding = 'unicode_escape')

df1 = df1.set_index('ExternalID')





final_data_frames = [df1,df]

#merge all dataframes
final_df = reduce(lambda left,right: pd.merge(left,right,on=['ExternalID'], how='outer'), final_data_frames)
final_df = reduce(lambda left,right: pd.merge(left,right,on=['ExternalID'], how='outer'), final_data_frames).fillna('void')



print(final_df.info())
print(final_df.head(10))




# Crosswalks for Match == Yes

final_df.loc[final_df['Match'] == 'yes', 'ExternalID'] = final_df['STARS_STUDENT_ID2']
final_df.loc[final_df['Match'] == 'yes', 'REPORTINGID'] = final_df['STARS_STUDENT_ID2']
final_df.loc[final_df['Match'] == 'yes', 'GNDR'] = final_df['S_GENDER2']
final_df.loc[final_df['Match'] == 'yes', 'BirthDtTxt'] = final_df['STARS_DOB2']
final_df.loc[final_df['Match'] == 'yes', 'ETHNICITY'] = final_df['S_ETNICITY2']
#final_df.loc[final_df['Match'] == 'yes', 'SpanishFlag'] = final_df['S_HISPANIC_INDICATOR2']
final_df.loc[final_df['Match'] == 'yes', '504Plan'] = final_df['S_PLAN5042']
final_df.loc[final_df['Match'] == 'yes', 'MIGRNTEDFG'] = final_df['S_MIGRANT2']
final_df.loc[final_df['Match'] == 'yes', 'ProgramBilingualEd'] = final_df['S_BEP2']
final_df.loc[final_df['Match'] == 'yes', 'ELL'] = final_df['S_ELL_STATUS2']
final_df.loc[final_df['Match'] == 'yes', 'SPED'] = final_df['S_SPECIAL_ED2']
final_df.loc[final_df['Match'] == 'yes', 'Title1Fg'] = final_df['S_TITLE2']

# Crosswalks for Match == fix

#final_df.loc[final_df['Match'] == 'fix', 'GNDR'] = final_df['S_GENDER2']
final_df.loc[final_df['Match'] == 'fix', 'BirthDtTxt'] = final_df['STARS_DOB2']
final_df.loc[final_df['Match'] == 'fix', 'ETHNICITY'] = final_df['S_ETNICITY2']
#final_df.loc[final_df['Match'] == 'fix', 'SpanishFlag'] = final_df['S_HISPANIC_INDICATOR2']
#final_df.loc[final_df['Match'] == 'fix', '504Plan'] = final_df['S_PLAN5042']
final_df.loc[final_df['Match'] == 'fix', 'MIGRNTEDFG'] = final_df['S_MIGRANT2']
final_df.loc[final_df['Match'] == 'fix', 'ProgramBilingualEd'] = final_df['S_BEP2']
final_df.loc[final_df['Match'] == 'fix', 'ELL'] = final_df['S_ELL_STATUS2']
final_df.loc[final_df['Match'] == 'fix', 'SPED'] = final_df['S_SPECIAL_ED2']
#final_df.loc[final_df['Match'] == 'fix', 'Title1Fg'] = final_df['S_TITLE2']

# Crosswalks for Match == change id

final_df.loc[final_df['Match'] == 'change id', 'ExternalID'] = final_df['STARS_STUDENT_ID2']
final_df.loc[final_df['Match'] == 'change id', 'REPORTINGID'] = final_df['STARS_STUDENT_ID2']
final_df.loc[final_df['Match'] == 'change id', 'GNDR'] = final_df['S_GENDER2']
final_df.loc[final_df['Match'] == 'change id', 'BirthDtTxt'] = final_df['STARS_DOB2']
final_df.loc[final_df['Match'] == 'change id', 'ETHNICITY'] = final_df['S_ETNICITY2']
#final_df.loc[final_df['Match'] == 'change id', 'SpanishFlag'] = final_df['S_HISPANIC_INDICATOR2']
final_df.loc[final_df['Match'] == 'change id', '504Plan'] = final_df['S_PLAN5042']
final_df.loc[final_df['Match'] == 'change id', 'MIGRNTEDFG'] = final_df['S_MIGRANT2']
final_df.loc[final_df['Match'] == 'change id', 'ProgramBilingualEd'] = final_df['S_BEP2']
final_df.loc[final_df['Match'] == 'change id', 'ELL'] = final_df['S_ELL_STATUS2']
final_df.loc[final_df['Match'] == 'change id', 'SPED'] = final_df['S_SPECIAL_ED2']
final_df.loc[final_df['Match'] == 'change id', 'Title1Fg'] = final_df['S_TITLE2']

# valid value conversion
final_df.loc[final_df['ETHNICITY'] == 2, 'ETHNICITY'] = 7
final_df.loc[final_df['ETHNICITY'] == 'Multi-Racial', 'ETHNICITY'] = 0
final_df.loc[final_df['ETHNICITY'] == 'American Indian/Alaskan Native', 'ETHNICITY'] = 1
final_df.loc[final_df['ETHNICITY'] == 'Asian', 'ETHNICITY'] = 3
final_df.loc[final_df['ETHNICITY'] == 'Hispanic', 'ETHNICITY'] = 4
final_df.loc[final_df['ETHNICITY'] == 'African American', 'ETHNICITY'] = 5
final_df.loc[final_df['ETHNICITY'] == 'White', 'ETHNICITY'] = 6
final_df.loc[final_df['ETHNICITY'] == 'Hawaiian/Pacific Islander', 'ETHNICITY'] = 7
final_df.loc[final_df['ETHNICITY'] == 'Caucasian', 'ETHNICITY'] = 6
final_df.loc[final_df['ETHNICITY'] == 'Native Hawaiian or Other Pacific Islander', 'ETHNICITY'] = 7
final_df.loc[final_df['ETHNICITY'] == 'Black or African American', 'ETHNICITY'] = 5
final_df.loc[final_df['GNDR'] == 'Male', 'GNDR'] = 'M'
final_df.loc[final_df['GNDR'] == 'Female', 'GNDR'] = 'F'
final_df.loc[final_df['504Plan'] == 'No', '504Plan'] = 'N'
final_df.loc[final_df['504Plan'] == 'Yes', '504Plan'] = 'Y'
final_df.loc[final_df['ProgramBilingualEd'] == 'Yes', 'ProgramBilingualEd'] = 'Y'
final_df.loc[final_df['ProgramBilingualEd'] == 'BEP', 'ProgramBilingualEd'] = 'Y'
final_df.loc[final_df['ProgramBilingualEd'] == 'No', 'ProgramBilingualEd'] = 'N'
final_df.loc[final_df['ELL'] == 0, 'ELL'] = 'N'
final_df.loc[final_df['ELL'] == 1, 'ELL'] = 'Y'
final_df.loc[final_df['SpanishFlag'] == 'Yes', 'SpanishFlag'] = 'Y'
final_df.loc[final_df['SpanishFlag'] == 'No', 'SpanishFlag'] = 'N'
final_df.loc[final_df['Title1Fg'] == 'T1A', 'Title1Fg'] = 'Y'
final_df.loc[final_df['SPED'] == 'N', 'SPED'] = 'Y'

#final_df.loc[(final_df['ETHNICITY'] == 6) & (final_df['SpanishFlag'] == 'Y'), 'ETHNICITY'] = 4

# use this to update hispanic ethnicity
final_df.loc[(final_df['S_HISPANIC_INDICATOR2'] == 'Yes'), 'ETHNICITY'] = 4
final_df.to_csv("NMAPA_06/11/201999.csv", sep=',', encoding='utf-8', index = False)
#print(final_df['Match'].value_counts())


final_df = final_df[['District','DistrictName','School','SchoolName','LglFNm','LglLNm','ExternalID','EnrlGrdCd',
    'NASIS_ID','LglMNm','GNDR','BirthDtTxt','REPORTINGID','ETHNICITY','PD','SpanishFlag','SECONDRATER',
    '504Plan','Title1Fg','MIGRNTEDFG','ProgramBilingualEd','ELL','USPublicSchools3Years','DistrictUseOnlyA','SPED','OELPABraille',
    'SpecialCodes','TestIDs']]

#final_df.to_csv("NMAPA_Demo_06102019_no_hisp.csv", sep=',', encoding='utf-8', index = False)
final_df.to_csv("NMAPA_Demo_06112019.csv", sep=',', encoding='utf-8', index = False)





#final_df.to_csv("NMAPA_Demo_Final06072019V2.csv", sep=',', encoding='utf-8', index = False)








