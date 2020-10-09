import pandas as pd
import numpy as np
import os
os.chdir(r'C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\GEIH')
dir1=r'C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\GEIH'
varf=['DIRECTORIO','SECUENCIA_P','ORDEN',"P6040","P6030S3","P6030S1","P6020","DPTO","P6050","P6220","P6210S1",
                            "P6210S1","P6090",'FEX_C_2011']
Final=pd.DataFrame(columns=varf)

for i in os.listdir(dir1):
    for j in os.listdir(dir1+"\\"+i+""):
        GEIHC=pd.read_csv(dir1+"\\"+i+"\\"+j+"\\"+"Área - Características generales (Personas).csv",sep=";",decimal=',')
        GEIHC.columns = map(str.upper, GEIHC.columns)
        GEIHC=GEIHC[varf]
        Final=Final.append(GEIHC)
        print(i,j)




