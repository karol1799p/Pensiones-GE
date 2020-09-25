import pandas as pd
import numpy as np
import linearmodels
import os
import numpy as np
os.chdir(r'C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\GEIH')
dir1=r'C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\GEIH'


##la idea es descargar todos los archivos de GEIH posibles y que despues de limpios devuelva un DataFrame
##con la serie de tiempo /panel de cada sector con el tiempo de trabajo domèstico promedio por sector
##la participación laboral por sector, el promedio de salarios por sector y el promedio del mayor nùmero de
##controles posibles
##de pronto mas adelante hacerlo con regiones, por ahora me da miedo
CIIU=pd.read_csv(r"C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\limpio\CIIU v3.csv",sep=";",encoding="latin-1",index_col="RAMA2D_R4")
Meses=pd.read_csv(r"C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\meses.csv",sep=";",index_col="Mes_l")
var_pan=["año","mes","nombre","share_M","share_H","RAMA2D_R4","total_M","total_H","salario_M","salario_H"]
Final=pd.DataFrame(columns=var_pan)


##iterare por el año y el mes tomando las siguientes variables para fuerza laboral
varf=['DIRECTORIO','SECUENCIA_P','ORDEN','P6430','P6800','RAMA4D_R4','OFICIO','RAMA2D_R4','P6500','MES','AREA','FEX_C_2011','DPTO']
varf2=['DIRECTORIO','SECUENCIA_P','ORDEN','P6430','P6800','OFICIO','RAMA2D','P6500','MES','AREA','FEX_C_2011','DPTO']
varp=['DIRECTORIO','SECUENCIA_P','ORDEN','P6020']




for i in os.listdir(dir1):
    for j in os.listdir(dir1+"\\"+i+""):
        print(i+j)
        GEIHC=pd.read_csv(dir1+"\\"+i+"\\"+j+"\\"+"Cabecera - Ocupados.csv",sep=";",decimal=',')
        GEIHC.columns = map(str.upper, GEIHC.columns)

        try:
            GEIHCL=GEIHC[varf]

        except:
            GEIHCL = GEIHC[varf2]
            GEIHCL.rename(columns={'RAMA2D': 'RAMA2D_R4'}, inplace=True)
            print("la base es nueva:)")


        GEIHR=pd.read_csv(dir1+"\\"+i+"\\"+j+"\\"+"Resto - Ocupados.csv",sep=";",decimal=',')
        GEIHR.columns = map(str.upper, GEIHR.columns)
        try:
            GEIHRL = GEIHC[varf]
        except:
            GEIHRL = GEIHC[varf2]
            GEIHRL.rename(columns={'RAMA2D': 'RAMA2D_R4'}, inplace=True)
            print("la base es nueva:)")

        GEIHA=pd.read_csv(dir1+"\\"+i+"\\"+j+"\\"+"Área - Ocupados.csv",sep=";",decimal=',')
        GEIHA.columns = map(str.upper, GEIHA.columns)
        try:
            GEIHAL = GEIHC[varf]
        except:
            GEIHAL = GEIHC[varf2]
            GEIHAL.rename(columns={'RAMA2D': 'RAMA2D_R4'}, inplace=True)
            print("la base es nueva:)")
        ##Precaución, el Dane (como la mayoria de nosotros) es propenso a cometer errores de ortografía , Enero 2019 tiene características sin tilde
        ##no tengo la capacidad ni el tiempo para hacer un corrector ortográfico por tanto es mas facil corregir en las bases
        GEIHPC = pd.read_csv(dir1 + "\\" + i + "\\" + j + "\\" + "Cabecera - Características generales (Personas).csv", sep=";",decimal=',')
        GEIHPC.columns = map(str.upper, GEIHPC.columns)
        GEIHPCL = GEIHPC[varp]

        GEIHPR = pd.read_csv(dir1 + "\\" + i + "\\" + j + "\\" + "Resto - Características generales (Personas).csv", sep=";",decimal=',')
        GEIHPR.columns = map(str.upper, GEIHPR.columns)
        GEIHPRL = GEIHPR[varp]

        GEIHPA = pd.read_csv(dir1 + "\\" + i + "\\" + j + "\\" + "Área - Características generales (Personas).csv", sep=";",decimal=',')
        GEIHPA.columns = map(str.upper, GEIHPA.columns)
        GEIHPAL = GEIHPA[varp]

        ##ya tenemos cargadas las bases por mes, ahora vamos a hacer el dataframe y agregar
        GEIHL=GEIHCL
        GEIHL=GEIHL.append(GEIHRL,sort=False, ignore_index=True)
        GEIHL=GEIHL.append(GEIHAL,sort=False,ignore_index=True)
        GEIHPL = GEIHPCL
        GEIHPL = GEIHPL.append(GEIHPRL, sort=False, ignore_index=True)
        GEIHPL = GEIHPL.append(GEIHPAL, sort=False, ignore_index=True)
        datos=pd.merge(GEIHL,GEIHPL,how="left",on=['DIRECTORIO','SECUENCIA_P','ORDEN'])
        datos=datos.drop_duplicates(subset=['DIRECTORIO','SECUENCIA_P','ORDEN'])
        datos.loc[datos["P6020"]==2,"mujeres"]=1
        datos.loc[datos["P6020"] == 1, "mujeres"] = 0
        datos.loc[datos["P6020"] == 1, "hombres"] = 1
        datos.loc[datos["P6020"] == 2, "hombres"] = 0
        datos.loc[datos["P6430"] == 3, "doméstico"] = 1
        datos.loc[datos["P6020"] == 2, "mujeresT"] = 1*datos["FEX_C_2011"]
        datos.loc[datos["P6020"] == 1, "mujeresT"] = 0
        datos.loc[datos["P6020"] == 1, "hombresT"] = 1*datos["FEX_C_2011"]
        datos.loc[datos["P6020"] == 2, "hombresT"] = 0
        datos.loc[datos["P6430"] == 3, "domésticoT"] = 1*datos["FEX_C_2011"]

        datos=datos.replace(" ",float('nan'))
        datos.apply(pd.to_numeric)
        datos=pd.merge(datos,CIIU,on=["RAMA2D_R4"],how="left")
        Data=datos.groupby(by=['nombre']).sum()

        print(Data.sum())
        ##voy a agregar a un mismo dataset el resumen de resutado con año, mes y cosas de interes
        resultado=pd.DataFrame(columns=var_pan)
        resultado["total_M"] = Data["mujeresT"]
        resultado["total_H"] = Data["hombresT"]
        datos["P6500"] = datos["P6500"].astype(float)

        salsex = datos.groupby(['mujeres'])["P6500"].mean()
        resultado["salario_M"] = salsex[1]
        resultado["salario_H"] = salsex[0]

        resultado["share_M"]=Data["mujeresT"]/Data.sum()["mujeresT"]

        resultado["share_H"] = Data["hombresT"] / Data.sum()["hombresT"]
        resultado["año"]=int(i)
        resultado["mes"]=Meses.loc[j[:-4]]["Mes_n"]
        resultado["RAMA2D_R4"]=Data["RAMA2D_R4"]



        resultado["nombre"]=Data.index

        Final=Final.append(resultado,sort=False, ignore_index=True)

##En teoría ya quedo el panel :) ahora falta sacar el aumento porcentual y deberia quedar la base limpia
##hay problemas con los ciiu, a partir del 2020 lo detallaron má, entonces tocarà decidir si antes de esta fecha o despues
##por ahora lo haré con antes
Final["salgrow_M"]=Final["total_M"].diff()/Final["total_M"]
Final["salgrow_H"]=Final["total_H"].diff()/Final["total_H"]
###quitando valores de 0 absoluto (evita problemas con infinitos) y sacando diferencia porcentual del total
Final=Final.sort_values(["nombre","año","mes"])

###esto no me enorgullece pero fue una soluciòn rapida, tenia que quitar los 0 estadìsticos para evitar problemas
for i in range(0,len(os.listdir(dir1))*12):
    Final.loc[Final['total_M']==0,"total_M"]=1
    Final.loc[Final['total_H']==0,"total_H"]=1
Final["diferenciasp_M"]=Final["total_M"].diff()/Final["total_M"]
Final["diferenciasp_H"]=Final["total_H"].diff()/Final["total_H"]
Final["salgrow_M"]=Final["salario_M"].diff()/Final["salario_M"]
Final["salgrow_H"]=Final["salario_H"].diff()/Final["salario_H"]

##eliminando el primer dato y valores infinitos
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'diferenciasp_M']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'diferenciasp_H']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'salgrow_M']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'salgrow_H']=0

###creamos bartik
Shares=Final.groupby(["nombre"]).mean()
Shares["share_sect_M"]=Shares["share_M"]
Shares["share_sect_H"]=Shares["share_H"]

Final=Final.merge(Shares[["share_sect_M","share_sect_H"]],how="left",on=["nombre"])
Final["bartik_M"]=Final["share_sect_M"]*Final["diferenciasp_M"]
Final["bartik_H"]=Final["share_sect_H"]*Final["diferenciasp_H"]
Final["crecimiento_M"]=Final["share_M"]*Final["diferenciasp_M"]
Final["crecimiento_H"]=Final["share_H"]*Final["diferenciasp_H"]
reg=pd.DataFrame(columns=["sal_M","sal_H","bartik_H","bartik_M","growth_H","growth_M","growth_est_H","growth_est_M"])
prepreg=Final.groupby(["año","mes"])
reg["sal_M"]=prepreg.mean()["salgrow_M"]
reg["sal_H"]=prepreg.mean()["salgrow_H"]
reg["bartik_H"]=prepreg.sum()["bartik_H"]
reg["bartik_M"]=prepreg.sum()["bartik_M"]
reg["growth_H"]=prepreg.sum()["crecimiento_H"]
reg["growth_M"]=prepreg.sum()["crecimiento_M"]
Final.to_csv(r"C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\limpio\Panel.csv",encoding="latin1",sep=";",decimal=",")
reg.to_csv(r"C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\limpio\datos_entrada.csv",encoding="latin1",sep=";",decimal=",")