import pandas as pd
import numpy as np
import linearmodels
import os
import numpy as np
import matplotlib as mpl
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
varf=['DIRECTORIO','SECUENCIA_P','ORDEN','P6430','P6800','RAMA4D_R4','OFICIO','RAMA2D_R4','P6500','MES','AREA','FEX_C_2011','DPTO','P388']
varf2=['DIRECTORIO','SECUENCIA_P','ORDEN','P6430','P6800','OFICIO','RAMA2D','P6500','MES','FEX_C_2011','P388']
varp=['DIRECTORIO','SECUENCIA_P','ORDEN','P6020']
varc=['DIRECTORIO','SECUENCIA_P','ORDEN','P7480S1','P7480S3','P7480S4','P7480S5','P7480S6','P7480S7','P7480S8','P7480S9','P7480S10','P7480S11']

###los numeros que comienzan en 100 son cabecera en 200 rurales, en 300 area, pero no deberia existir area, si ves un 300 quema el computador... o busca el error, lo que sea mejor


for i in os.listdir(dir1):
    for j in os.listdir(dir1+"\\"+i+""):
        print(i+j)
        ##vamos a cargar tres subsets de cada mes, ocupados para trabajo y salario, características generales para sexo
        ##y otras actividades para trabajo domestico
        GEIHC=pd.read_csv(dir1+"\\"+i+"\\"+j+"\\"+"Cabecera - Ocupados.csv",sep=";",decimal=',')
        GEIHC.columns = map(str.upper, GEIHC.columns)
        GEIHC["P388"]=GEIHC["P388"].apply(lambda x: x+100)

        try:
            GEIHCL=GEIHC[varf]

        except:
            GEIHCL = GEIHC[varf2]
            GEIHCL.rename(columns={'RAMA2D': 'RAMA2D_R4'}, inplace=True)
            print("la base es nueva:)")


        GEIHR=pd.read_csv(dir1+"\\"+i+"\\"+j+"\\"+"Resto - Ocupados.csv",sep=";",decimal=',')
        GEIHR.columns = map(str.upper, GEIHR.columns)
        GEIHR["P388"]=GEIHR["P388"].apply(lambda x: x+200)
        try:
            GEIHRL = GEIHR[varf]
        except:
            GEIHRL = GEIHR[varf2]
            GEIHRL.rename(columns={'RAMA2D': 'RAMA2D_R4'}, inplace=True)
            print("la base es nueva:)")

        GEIHA=pd.read_csv(dir1+"\\"+i+"\\"+j+"\\"+"Área - Ocupados.csv",sep=";",decimal=',')
        GEIHA.columns = map(str.upper, GEIHA.columns)
        GEIHA["P388"]=GEIHA["P388"].apply(lambda x: x+300)
        try:
            GEIHAL = GEIHR[varf]
        except:
            GEIHAL = GEIHR[varf2]
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

        ##trabajo Doméstico, vamos a cargar TDCNR
        GEIHAC = pd.read_csv(dir1 + "\\" + i + "\\" + j + "\\" + "Cabecera - Otras actividades y ayudas en la semana.csv",
                             sep=";", decimal=',')
        GEIHAC.columns = map(str.upper, GEIHAC.columns)
        GEIHACL = GEIHAC[varc]

        GEIHAR = pd.read_csv(dir1 + "\\" + i + "\\" + j + "\\" + "Resto - Otras actividades y ayudas en la semana.csv",
                             sep=";", decimal=',')
        GEIHAR.columns = map(str.upper, GEIHAR.columns)
        GEIHARL = GEIHAR[varc]

        GEIHAA = pd.read_csv(dir1 + "\\" + i + "\\" + j + "\\" + "Área - Otras actividades y ayudas en la semana.csv",
                             sep=";", decimal=',')
        GEIHAA.columns = map(str.upper, GEIHAA.columns)
        GEIHAAL = GEIHAA[varc]

        ##ya tenemos cargadas las bases por mes, ahora vamos a hacer el dataframe y agregar
        GEIHL=GEIHCL
        GEIHL=GEIHL.append(GEIHRL,sort=False, ignore_index=True)
        GEIHL=GEIHL.append(GEIHAL,sort=False,ignore_index=True)
        GEIHPL = GEIHPCL
        GEIHPL = GEIHPL.append(GEIHPRL, sort=False, ignore_index=True)
        GEIHPL = GEIHPL.append(GEIHPAL, sort=False, ignore_index=True)
        GEIHAAL2=GEIHACL
        GEIHAAL2 = GEIHAAL2.append(GEIHARL, sort=False, ignore_index=True)
        GEIHAAL2 = GEIHAAL2.append(GEIHAAL, sort=False, ignore_index=True)
        GEIHAAL2["CUIDADO"]=GEIHAAL2.iloc[:,3:].sum(axis=1)
        GEIHAAL2["CUIDADO"]=GEIHAAL2["CUIDADO"].apply(lambda x: (x-10)/10)


        datos=pd.merge(GEIHL,GEIHPL,how="left",on=['DIRECTORIO','SECUENCIA_P','ORDEN'])
        datos=datos.merge(GEIHAAL2,how="left",on=['DIRECTORIO','SECUENCIA_P','ORDEN'])
        datos1=datos
        datos=datos.drop_duplicates(subset=['DIRECTORIO','SECUENCIA_P','ORDEN'])
        print(datos['P388'].max(axis=0))

        ##generamos variables de trabajo de hombres y mujeres
        datos.loc[datos["P6020"]==2,"mujeres"]=1
        datos.loc[datos["P6020"] == 1, "mujeres"] = 0
        datos.loc[datos["P6020"] == 1, "hombres"] = 1
        datos.loc[datos["P6020"] == 2, "hombres"] = 0
        datos.loc[datos["P6430"] == 3, "doméstico"] = 1
        datos.loc[datos["P6020"] == 2, "mujeresT"] = 1
        datos.loc[datos["P6020"] == 1, "mujeresT"] = 0
        datos.loc[datos["P6020"] == 1, "hombresT"] = 1
        datos.loc[datos["P6020"] == 2, "hombresT"] = 0

        ##ahora trabajo de cuidado
        datos["hombresC"]=datos["hombres"]*datos["CUIDADO"]
        datos["mujeresC"] = datos["mujeres"] * datos["CUIDADO"]
        datos=datos.replace(" ",float('nan'))
        datos.apply(pd.to_numeric)
        datos=pd.merge(datos,CIIU,on=["RAMA2D_R4"],how="left")
        Data=datos.groupby(['Categoria',"P388"]).sum()
        Data=Data.reset_index()

        ##voy a agregar a un mismo dataset el resumen de resutado con año, mes y cosas de interes
        resultado=pd.DataFrame(columns=var_pan)
        resultado["total_M"] = Data["mujeresT"]
        resultado["total_H"] = Data["hombresT"]
        resultado["total_MC"] = Data["mujeresC"]
        resultado["total_HC"] = Data["hombresC"]
        datos["P6500"] = datos["P6500"].astype(float)

        salsex = datos.groupby(['mujeres','P388'])["P6500"].mean().unstack(level='mujeres')

        resultado["P388"] = Data["P388"]
        resultado = resultado.merge(salsex,"left",on=["P388"])

        ##encontrando shares de un sector tanto en trabajo como en trabajo domestico

        resultado["share_H"] = Data["hombresT"] / Data.sum()["hombresT"]
        resultado["share_M"]=Data["mujeresT"]/Data.sum()["mujeresT"]
        resultado["share_MC"] = Data["mujeresC"] / Data.sum()["mujeresC"]
        resultado["share_HC"] = Data["hombresC"] / Data.sum()["hombresC"]

        resultado["año"]=int(i)
        resultado["mes"]=Meses.loc[j[:-4]]["Mes_n"]
        resultado["RAMA2D_R4"]=Data["RAMA2D_R4"]



        resultado["nombre"]=Data["Categoria"]

        Final=Final.append(resultado,sort=False, ignore_index=True)

##En teoría ya quedo el panel :) ahora falta sacar el aumento porcentual y deberia quedar la base limpia
##hay problemas con los ciiu, a partir del 2020 lo detallaron má, entonces tocarà decidir si antes de esta fecha o despues
##por ahora lo haré con antes

###quitando valores de 0 absoluto (evita problemas con infinitos) y sacando diferencia porcentual del total
Final=Final.sort_values(["nombre","P388","año","mes"])
Final["salario_M"]=Final[1.0]
Final["salario_H"]=Final[0.0]
###esto no me enorgullece pero fue una soluciòn rapida, tenia que quitar los 0 estadìsticos para evitar problemas, suponien
Final=Final.drop(Final[Final['total_M']==0].index)
for i in range(0,len(os.listdir(dir1))*12):
    Final.loc[Final['total_M']==0,"total_M"]=1
    Final.loc[Final['total_H']==0,"total_H"]=1
    Final.loc[Final['total_MC'] == 0, "total_MC"] = 1
    Final.loc[Final['total_HC'] == 0, "total_HC"] = 1

Final["diferenciasp_M"]=Final["total_M"].diff()/Final["total_M"].shift(1)
Final["diferenciasp_H"]=Final["total_H"].diff()/Final["total_H"].shift(1)
Final["diferenciasp_MC"]=Final["total_MC"].diff()/Final["total_MC"].shift(1)
Final["diferenciasp_HC"]=Final["total_HC"].diff()/Final["total_HC"].shift(1)

Final["salgrow_M"]=Final[0.0].diff()/Final[0.0].shift(1)
Final["salgrow_H"]=Final[1.0].diff()/Final[1.0].shift(1)

##eliminando el primer dato de mes
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'diferenciasp_M']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'diferenciasp_H']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'diferenciasp_MC']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'diferenciasp_HC']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'salgrow_M']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'salgrow_H']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'salgrow_M']=0
Final.loc[(Final['año']==Final.iloc[0]["año"]) & (Final['mes']==Final.iloc[0]["mes"]),'salgrow_H']=0


##eliminamos la region 900, que pues, no deberia existir
Final=Final[Final.P388 <900]


###creamos bartik
Shares=Final.groupby(["nombre","P388"]).mean().reset_index()
Shares["share_sect_M"]=Shares["share_M"]
Shares["share_sect_H"]=Shares["share_H"]
Shares["share_sect_MC"]=Shares["share_MC"]
Shares["share_sect_HC"]=Shares["share_HC"]


Final=Final.merge(Shares[["nombre","P388","share_sect_M","share_sect_H"]],how="left",on=["nombre","P388"])
Final["bartik_M"]=Final["share_sect_M"]*Final["diferenciasp_M"]
Final["bartik_H"]=Final["share_sect_H"]*Final["diferenciasp_H"]
Final["crecimiento_M"]=Final["share_M"]*Final["diferenciasp_M"]
Final["crecimiento_H"]=Final["share_H"]*Final["diferenciasp_H"]
Final["crecimiento_MC"]=Final["share_MC"]*Final["diferenciasp_MC"]
Final["crecimiento_HC"]=Final["share_HC"]*Final["diferenciasp_HC"]
reg=pd.DataFrame(columns=["sal_M","sal_H","bartik_H","bartik_M","growth_H","growth_M","growth_est_H","growth_est_M","P388"])
prepreg=Final.groupby(["año","mes","P388"]).agg({'salgrow_M': ['mean'],
                                                 'salgrow_H': ['mean'],
                                                 'bartik_H': ['sum'],
                                                 'bartik_M': ['sum'],
                                                 'crecimiento_H': ['sum'],
                                                 'crecimiento_M': ['sum'],
                                                 'crecimiento_HC': ['sum'],
                                                 'crecimiento_MC': ['sum'],
                                                 'total_M': ['sum'],
                                                 'total_H': ['sum']}).reset_index()

prepreg.columns=prepreg.columns.droplevel(1)
##para tener una variable fecha
prepreg["mes"]=prepreg["mes"].apply(lambda x:"0"+str(x) if x<10 else str(x))
prepreg["año"]=prepreg["año"].apply(lambda x:str(x))

prepreg["fecha"]=prepreg["año"]+prepreg["mes"]

Final.to_csv(r"C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\limpio\Panel.csv",encoding="latin1",sep=";",decimal=".")
prepreg.to_csv(r"C:\Users\usuario\Google Drive\observatorio\elasticidad del trabajo\datos\limpio\datos_entrada.csv",encoding="latin1",sep=";",decimal=".")


