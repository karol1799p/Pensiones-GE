import linearmodels
import pandas as pd
import matplotlib as mpl
data=pd.read_csv(r"C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\limpio\datos_entrada.csv",encoding="latin1",sep=";",decimal=",")
data["const"]=1
data["DPTO"]=data["DPTO"].astype("str")
data["DPTO","bartik_M"]


ivolsmodM = linearmodels.IV2SLS(data["salgrow_M"],data[["const"]+["DPTO"]],data["crecimiento_M"],data["bartik_M"])
ivolsmodH = linearmodels.IV2SLS(data["salgrow_H"],data[["const"]+["DPTO"]],data["crecimiento_H"],data["bartik_H"])
prueba=linearmodels.IV2SLS(data["crecimiento_M"],data[["bartik_M","const"]],None,None)
prueba2=prueba.fit()
print(prueba2)

res_olsH = ivolsmodH.fit()
res_olsM = ivolsmodM.fit()
print(res_olsH)
print(res_olsM)
print(res_olsH.first_stage)

print(res_olsM.first_stage)