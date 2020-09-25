import pandas as pd
import numpy as np
import xlrd
import openpyxl
EMM=pd.ExcelFile(r"C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\EMM\anex_EMM_dic18.xlsx")
sh8=EMM.parse("8. Enlace legal series Prod ",header=[9])
sh8mod= sh8.drop([sh8.index[0] , sh8.index[1]])
sh8mod["crecimiento empleo"]=sh8mod["Empleo  Total"].div(sh8mod["Empleo  Total"].shift(1))

