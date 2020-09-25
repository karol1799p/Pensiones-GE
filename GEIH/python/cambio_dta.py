import pandas as pd
dir2=os.chdir(r'C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\DTA')
for i in os.listdir(dir2):
    acsv=pd.read_stata(i)
    acsv.to_csv(str(i))
