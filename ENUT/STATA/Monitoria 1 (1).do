*****************************************************************************
*******************************MONITORIA 1***********************************
*****************************************************************************

/*Tipos de archivos
En Stata existen cuatro tipos de archivos:
.dta contiene la base de datos
.do  contiene los programas desarrollados por los usuarios
.log contiene la informaciÛn de lo que se realiza en Stata
.ado contiene los programas desarrollados por especialistas (por ahora nos vamos a olvidar de ellos)*/


/* Descripción de la base de datos que usaremos.

La Encuesta nacional de uso del tiempo (ENUT), es una investigación desarrollada por el DANE, 
con el fin de generar información sobre el tiempo dedicado por la población de 10 años y más a actividades de trabajo remunerado,
no remunerado y personales.

La investigación está definida para tomar información de viviendas, hogares y personas, dentro de una estructura típica de encuesta de hogares. 
De las viviendas se indaga sobre: el tipo y cobertura de servicios públicos.

En cuanto a los hogares se pregunta por: la tenencia de la vivienda que habitan, 
la recepción de subsidios, la tenencia y uso de bienes, la contratación de servicio doméstico y la recepción de trabajo doméstico no remunerado.

Respecto al apartado sobre las personas, la ENUT toma información demográfica básica y sobre salud de todas las personas del hogar,
así como sobre el cuidado de menores de 5 años, la educación para las personas de 5 años y más, 
el mercado laboral y el uso del tiempo para las personas de 10 años y más.

Para esta encuesta se constituyeron los siguientes dominios: Región Caribe, Región Oriental, Región Central, Región Pacífica,
Bogotá D.C. y la cabecera de la isla de San Andrés.
*/


***********************Comandos básicos en STATA*****************************

*****************************************************************************
*update all
*cd		    cambiar el directorio
*set mem	modificar la memoria empleada
*use		abrir el documento
*insheet	importar datos de otros documentos
*edit 		puede importar los datos desde la ventana (copiar pegar)
*compress	si necesita mȳ memoria
*clear  	limpiar la base
*log using  guarda los resultados en un archivo de texto
*help 		AYUDA
*lookup 	AYUDA
*serach 	AYUDA
*findit		buscar comandos creados por usuarios
*display 	displays strings and values of scalar expressions
*exit 		cierra el programa
*****************************************************************************

********************************Ejemplos*************************************

*¿Cómo crear un directorio de trabajo?**
cd"C:\Users\User\Downloads\Monitoria\MONITORIAS\SESIONES\Monitoria 1"

*¿Cómo guardar mis resultados en formato texto?
set logtype text, perm
log using resultados1.txt

*¿Cómo abrir mi base de datos?
use "C:\Users\User\Downloads\Monitoria\MONITORIAS\STATA\ENUT_2016_2017.dta", clear

*¿Cómo abrir una basa que está en formato csv o xls,etc*
import excel "C:\Users\User\Downloads\Investigaciones\Exportaciones\Bases_DANE\TOTPART\TOTPART.xlsx", sheet("TOTPART Version 68")clear

*¿Qué comando es útil para borrar todas mis resultados y limpiar mi actual base de datos?
clear

*¿Qué comando usaria para eliminar un variable que tiene un error, sin limpiar todo?
tab p6040
gen eda=p6040
drop eda

gen edad=p6040
tab edad

*Buscar las especificaciones de un comanda o simplemente enterder como usar*
help sum
h reg

display "Monitoria de Género & Economía"
display 225678/89
display "2+6"

*Para salir de Stata uso los comandos:
*exit
*exit, clear
log close

*****************************************************************************
*Modificar la base de datos						
*****************************************************************************
*label data	 	darle un nombre a la base de datos
*order	 		ordenar las variables de la base de datos
*label variable	darle un nombre a una variable
*label define	
*label values	aplicar los nombres a una variables 
*rename		    renombrar una variable
*recode		    recodificar los valores de una variable
*notes			poenr notas a la base de datos
*generate		crear una variable nueva
*egen			tiene funciones especiales
*replace		reemplazar un valor 
*by				ejecutar el comando basado en valores de varlist
*if				condición al final del comando
*in 			condición al final del comando
*****************************************************************************
/****************************************************************************
Operadores 
*****************************************************************************
> 			mayor a
< 			menor a 
== 			igual a
>= 			mayor o igual
<= 			menor o igual
!= 			diferente a
&			Y
|			o
!			no
*****************************************************************************/
/****************************************************************************
Operadores Aritméticos
*****************************************************************************
+ 			Suma
- 			Resta
* 			Multiplicación
/ 			División
^			Exponencial
*****************************************************************************/
*****************************************************************************
/* Funciones matemáticas para usar con generate
*****************************************************************************
abs(x)		Valor absoluto
sqrt(x)		Raíz cuadrada
ln(x) 		Log natural
log10(x)	Log en base 10
exp(x)		Exponencial
round(x) 	Redondea al entero mas cercano
uniform()	Varible de una distribución uniforme
rnormal()	Variable de una distribución normal estándar
para ver todas las funciones help math functions
*****************************************************************************/

***********************Ejemplos***********************************************

des p6020
gen sexo=p6020
tab sexo
recode sexo (1=0)(2=1), gen(mujer)
label variable mujer "mujer==1"
tab mujer
label define mujerlbl 0"Hombre"1"Mujer"
label values mujer mujerlbl
tab mujer
tab mujer, nolabel

/*6)Region:
6	San Andrés
5	Bogotá
4	Pacífica
3	Oriental
2	Central
1	Atlántica*/

tab region
label define regionlbl 1"Atlántica"2"Central"3"Oriental"4"Pacífica"5"Bogotá"6"San Andrés"
label values region regionlbl	
tab region

tab clase
label define claselbl 1"Cabeceras municipales"2"Centros poblados y rural disperso"
label values clase claselbl		
tab clase

des p6040
gen edad= p6040
br edad p6040

count if missing(p6040)
gen edad_10ymas= 1 if edad>=10
replace edad_10ymas=0 if edad<10 
tab edad_10ymas
br edad edad_10ymas

egen edad_promedio=mean(edad)
display edad_promedio

gen t_ayuda_tareas1=p1132s1a1+(p1132s1a2/60)
gen t_ayuda_tareas2=p1132s2a1+(p1132s2a2/60)
gen t_ayuda_tareas3=p1132s3a1+(p1132s3a2/60)
egen t_ayuda_tareas=rowtotal(t_ayuda_tareas1 t_ayuda_tareas2 t_ayuda_tareas3)
br t_ayuda_tareas1 t_ayuda_tareas2 t_ayuda_tareas3 t_ayuda_tareas
recode t_ayuda_tareas(0=.)


*****************************************************************************
*Análisis descriptivo
*****************************************************************************
*describe	describir la base de datos
*list		hacer una lista de los contenidos de la base
*codebook 	una descripciÛn detallada de los contenidos
*count		contar
*summarize	estadisticas descriptivas
*tabstat	tabla de estadÌsticas descriptivas
*tabulate	hace tablas de frecuencia
*table		tabla de estadÌsticas descriptivas
*graph	    graficar
*twoway		graficar
*kdensity	grafica de la densidad
*sort 	    ordena los datos	
*histogram  histograma
*correlate	correlaciones
******************************************************************************

*********************Ejemplos*************************************************

describe 
des p6020
des p1174s1*

list clase
codebook clase
count if missing(clase)

/*Preparar y servir alimentos
para las personas de este
hogar*/
gen t_alimentos=p1143s1a1+(p1143s1a2/60)
count if missing(p1143s1a1)
count if missing(p1143s1a2)
br t_alimentos p1143s1a1 p1143s1a2
tabstat t_alimentos,by(mujer) stat(mean)
tabstat t_alimentos,by(clase) stat(mean sd v)

sum edad
sum edad,d
sum edad if edad_10ymas
sum t_alimentos t_ayuda_tareas1

gen nivel_educativo=.
#delimit ;
replace nivel_educativo=1 if p6210==1;
replace nivel_educativo=2 if p6210==2|p6210==3;
replace nivel_educativo=3 if p6210==4;
replace nivel_educativo=4 if p6210==5|p6210==6|p6210==7|p6210==8;
replace nivel_educativo=5 if p6210==9|p6210==10;
replace nivel_educativo=6 if p6210==11|p6210==12;
label define nivel_educativolbl 1"Ninguno"2"Primaria"3"Bachiller"4"Técnico y Tecnológico"5"Universitario"6"Postgrado"
label values nivel_educativo nivel_educativolbl		

tab nivel_educativo
tab nivel_educativo, miss
tab nivel_educativo if mujer==1
tab nivel_educativo mujer


table mujer, c(mean t_alimentos mean t_ayuda_tareas1)
table mujer clase, c(mean t_alimentos)
table mujer clase, c(mean t_alimentos mean t_ayuda_tareas1)

histogram edad
kdensity edad
histogram edad, kdens

*****************************************************************************
/* Funciones matemáticas para usar con egen
*****************************************************************************
egen <new variable>= <function>(<expression(s)> or <variable(s)>) [, by (<variables>)]
mean()
rowmean()
sum()
rowtotal()
max()
rowmax()
min()
rowmin()
group()
concat()

*****************************************************************************/

egen min_edad=min(edad)
display min_edad

gen t_ayudar_vestir1=p1134s1a1+(p1134s1a2/60)
gen t_ayudar_vestir2=p1134s2a1+(p1134s2a2/60)
gen t_ayudar_vestir3=p1134s3a1+(p1134s3a2/60)
egen t_ayudar_vestir=rowtotal(t_ayudar_vestir1 t_ayudar_vestir2 t_ayudar_vestir3)
recode t_ayudar_vestir(0=.)
/*El día [...], sin que por ello
le pagaran, ¿a qué
persona(s) de este hogar
<...> bañó, vistió o le(s)
ayudó a hacerlo? (Persona 1)*/

egen media_t_ayudar_vestir=mean(t_ayudar_vestir)
display media_t_ayudar_vestir
