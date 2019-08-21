#jeanho_rodriguez
#08/21/2019
#NMAPA_SPRING_2019_DAD

import pandas as pd
import numpy as np

df = pd.read_csv("NMAPA_merged_schools1.csv", sep=',', header=0, low_memory=False)

# add variables
df['Tested_Grade_Listen'] = str
df['Tested_Grade_Read'] = str
df['Tested_Grade_Speak'] = str
df['Tested_Grade_Write'] = str
df['CBT_Listen'] = str
df['CBT_Read'] = str
df['CBT_Speak'] = str
df['CBT_Write'] = str
df['PL_Listen'] = str
df['PL_Read'] = str
df['PL_Speak'] = str
df['PL_Write'] = str
df['PL_Comprehension'] = str
df['PL_Oral'] = str
df['PL_Literacy'] = str
df['NewSS'] = str
df['SS_Listen'] = str
df['SS_Read'] = str
df['SS_Speak'] = str
df['SS_Write'] = str
df['SS_Comprehension'] = str
df['SS_Oral'] = str
df['SS_Literacy'] = str
df['IstationTime'] = str
df['Pearson_SGP'] = str

# rename variables
df.rename(columns={'STUID':'StID'}, inplace=True)
df.rename(columns={'Code':'Vendor_SchNumb'}, inplace=True)
df.rename(columns={'DistrictCode':'Vendor_DistCode'}, inplace=True)
df.rename(columns={'distname_x':'Vendor_DistName'}, inplace=True)
df.rename(columns={'SchoolCode':'Vendor_SchCode'}, inplace=True)
df.rename(columns={'schname_x':'Vendor_SchName'}, inplace=True)
df.rename(columns={'LNAME':'Last'}, inplace=True)
df.rename(columns={'FNAME':'First'}, inplace=True)
df.rename(columns={'MI':'MI'}, inplace=True)
df.rename(columns={'Grade':'Tested_Grade'}, inplace=True)
df.rename(columns={'S_GRADE':'STARS_Grade'}, inplace=True)
df.rename(columns={'AccYN':'Accomm'}, inplace=True)
df.rename(columns={'Test':'TestCode'}, inplace=True)
df.rename(columns={'Testlang':'TestLang'}, inplace=True)
df.rename(columns={'ScaleScore':'SS'}, inplace=True)

# add pref_grade
df['Pref_Grade'] = df['STARS_Grade']

df = df[['TestbookID','StID','Vendor_SchNumb','Vendor_DistCode','Vendor_DistName','Vendor_SchCode','Vendor_SchName','Last'
         ,'First','MI','Tested_Grade','Tested_Grade_Listen','Tested_Grade_Read','Tested_Grade_Speak','Tested_Grade_Write',
         'Pref_Grade','STARS_Grade','Accomm','CBT','CBT_Listen','CBT_Read','CBT_Speak','CBT_Write','Testname','Subtest',
         'TestCode','TestLang','PL','PL_Listen','PL_Read','PL_Speak','PL_Write','PL_Comprehension','PL_Oral','PL_Literacy',
         'Proficient','SS','NewSS','SS_Listen','SS_Read','SS_Speak','SS_Write','SS_Comprehension','SS_Oral','SS_Literacy',
         'IstationTime','Pearson_SGP']]


Subtest_map = {'SCI':'SCIENCE ','MATH':'MATH','READ':'ELA'}

df['Subtest'] = df['Subtest'].map(Subtest_map) #map function applied with map rule

TestCode_map = {'(NewMexico)NM-ALT-SUM-UD-MA-OP-6-Spring-2018-2019':'MAT06','(NewMexico)NM-ALT-SUM-UD-ELA-OP-6-Spring-2018-2019':'ELA06',
                '(NewMexico)NM-ALT-SUM-UD-MA-OP-3-Spring-2018-2019':'MAT03','(NewMexico)NM-ALT-SUM-UD-ELA-OP-3-Spring-2018-2019':'ELA03',
                '(NewMexico)NM-ALT-SUM-UD-MA-OP-11-Spring-2018-2019':'MAT11','(NewMexico)NM-ALT-SUM-UD-ELA-OP-11-Spring-2018-201':'ELA11',
                '(NewMexico)NM-ALT-SUM-UD-SC-OP-4-Spring-2018-2019':'SCI04','(NewMexico)NM-ALT-SUM-UD-SC-OP-7-Spring-2018-2019':'SCI07',
                '(NewMexico)NM-ALT-SUM-UD-SC-OP-11-Spring-2018-2019':'SCI11'}

df['TestCode'] = df['TestCode'].map(TestCode_map) #map function applied with map rule

#print(df['TestCode'].value_counts(dropna=False))




df.to_csv("NMAPA for 2019 DAD 2019-08-21V3.csv", sep=',', encoding='utf-8-sig', index = False)