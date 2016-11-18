# -*- coding: utf-8 -*-_
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
import gspread
from oauth2client.service_account import ServiceAccountCredentials

@login_required(login_url='/admin/login/')

def index(request):

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('notas.json', scope)
    gc = gspread.authorize(credentials)
    gs=gc.open("ServiciosGS")
    gm=gc.open("ServiciosGM")
    gengs=gs.worksheet("General")
    gengm=gm.worksheet("General")
    values_list_gs = gengs.col_values(1)
    values_list_gm = gengm.col_values(1)
    nombre=request.user.last_name+", "+request.user.first_name

    if nombre in values_list_gs:
        return grado_sup(request,gs) 
    elif nombre in values_list_gm: 
        return HttpResponse("gm")
    else:
        return HttpResponse("adios")

def grado_sup(request,gs):
    context={}
    context["alumno"]=request.user.last_name+", "+request.user.first_name
    datos=[]
    cabeceras=[]
    cabeceras2=[]
    datos2=[]
    info=[]
    col=[]
    p1ev={'puntos':0,'total_puntos':0,'puntos_vol':0,'total_puntos_vol':0}
    p={'puntos':0,'total_puntos':0,'puntos_vol':0,'total_puntos_vol':0}
    cont=0
    for hoja in gs.worksheets():
        cell = hoja.find(context["alumno"])
        
        cabeceras.append(hoja.row_values(1)[1:])
        datos.append(hoja.row_values(cell.row)[1:])
        dic={}       
        dic['titulo']=hoja.title
        dic['porcentaje']=porcentaje(cabeceras,datos)
        dic['total_puntos']=puntos(cabeceras,0)
        dic['puntos']=datos[-1][-1]
        dic['total_puntos_vol']=puntos(cabeceras,1)
        dic['puntos_vol']=puntos_vol(cabeceras,datos)
        dic['porcentaje_vol']=porcentaje_vol(cabeceras,datos)
        dic['tareas']=tareas_que_faltan(cabeceras,datos)
        info.append(dic)
        if cont<7:
            for k,v in p1ev.items():
                try:
                    p1ev[k]=p1ev[k]+int(dic[k])
                except:
                    pass
        for k,v in p.items():
            try:
                p[k]=p[k]+int(dic[k])
            except:
                pass
        cont=cont+1
        col=color(cabeceras,datos)
        cab=zip(col,hoja.row_values(1)[1:])
        dat=zip(col,hoja.row_values(cell.row)[1:])
        cabeceras2.append(cab)
        datos2.append(dat)
    context["combi"]=zip(info,cabeceras2,datos2)
    context["p"]=p
    context["p1ev"]=p1ev
    context["por1ev"]=int(p1ev['puntos']*100/p1ev['total_puntos'])
    context["porvol1ev"]=int(p1ev['puntos_vol']*100/p1ev['total_puntos_vol'])
    context["por"]=int(p['puntos']*100/p['total_puntos'])
    context["porvol"]=int(p['puntos_vol']*100/p['total_puntos_vol'])

    #print context["combi"]
    #return HttpReponse(context["datos"])
    return render(request,"index.html",context)

@login_required(login_url='/admin/login/')
def salir(request):
       logout(request)
       return redirect('/admin/login/')

def puntos(cab,indice):
    try:
        return cab[-1][-1].split(" - ")[indice]
    except:
        return "0"

def puntos_vol(cab,dat):
    lista=zip(cab[-1],dat[-1])
    cont=0
    for c,v in lista:
        if "*" in c:
            try:
                cont=cont+int(v)
            except:
                pass
    return cont

def porcentaje(cab,dat):
        try:
            return int(dat[-1][-1])*100/int(cab[-1][-1].split(" - ")[0])
        except:
            return 0

def porcentaje_vol(cab,dat):
    try:
        return int(puntos_vol(cab,dat)*100/int(puntos(cab,1)))
    except:
        return 100

def tareas_que_faltan(cab,dat):
    lista=zip(cab[-1],dat[-1])
    resp=[]
    for c,v in lista:
        if "*" in c and v=="":
            resp.append(c[:3].replace("T","Tarea").strip())
    return resp

def color(cab,dat):
    lista=zip(cab[-1],dat[-1])
    resp=[]
    for c,v in lista:
        if v=="":
            resp.append("active")
        elif "*" in c:
            resp.append("danger")
        else:
            resp.append("info")
    return resp

