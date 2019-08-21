import pandas as pd

df_SS = pd.read_csv("ADDED DEMO NMAlt SS.csv",sep=',', header=0, low_memory=False)


cross_tab_grade = pd.crosstab(df_SS.Grade, df_SS.Test, margins=True)  # school code 126 missing from vendor
cross_tab_gradeII = pd.crosstab(df_SS.Grade, df_SS.S_GRADE, margins=True)


