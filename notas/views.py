# -*- coding: utf-8 -*-_
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
import gspread
from notas.libldap import LibLDAP
from oauth2client.service_account import ServiceAccountCredentials
from settings import FILE_CREDENCIALES

def index(request):
    if request.method=="GET":
            return render(request,'login.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"].encode('utf-8')
        lldap=LibLDAP(username,password)
        if lldap.isbind:
                request.session["username"]=username
                busqueda='(uid=%s)'%username
                resultados=lldap.buscar(busqueda)
                info=resultados[0].get_attributes()
                return index2(request,username,info["sn"][0]+", "+info["givenname"][0]) 
        else:
               info={"error":True}
               return render(request,"login.html",info)


def index2(request,username,nombre):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(FILE_CREDENCIALES, scope)
    gc = gspread.authorize(credentials)
    gs=gc.open("ServiciosGS")
    gm=gc.open("ServiciosGM")
    gengs=gs.worksheet("General")
    gengm=gm.worksheet("Windows")
    values_list_gs = gengs.col_values(1)
    values_list_gm = gengm.col_values(1)
    
    #if username in values_list_gs:
    if any(username in elem for elem in values_list_gs):
        return grado_sup(request,gs,values_list_gs.index(username)+1,nombre) 
    elif username in values_list_gm: 
        return grado_med(request,gm,values_list_gm.index(username)+1,nombre)
    elif username=="josedom":
        return admin(request,gengs.col_values(2)[1:-2],gengm.col_values(2)[2:])
    else:
        return render(request,'login.html')
	

def ver(request,tipo,num):
    if request.session.has_key("username") and request.session["username"]=="josedom":
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(FILE_CREDENCIALES, scope)
        gc = gspread.authorize(credentials)
        if tipo=="gs":
                gs=gc.open("ServiciosGS")
                gengs=gs.worksheet("General")
                values_list_gs = gengs.col_values(2)
                nombre=values_list_gs[int(num)+1]
                return grado_sup(request,gs,int(num)+2,nombre)
        else:
                gm=gc.open("ServiciosGM")
                gengm=gm.worksheet("Windows")
                values_list_gm = gengm.col_values(2)
                nombre=values_list_gm[int(num)+2]
                return grado_med(request,gm,int(num)+3,nombre)
    else:
        return redirect('/')


def grado_med(request,gm,celda,nombre):
    context={}
    context["alumno"]=nombre
    wdatos=[]
    wcabeceras=[]
    wpuntos=[]
    winfo=[]

    ldatos=[]
    lcabeceras=[]
    lpuntos=[]
    linfo=[]
    #windows

    cont=0
    for hoja in gm.worksheets()[0:4]:
        wcabeceras.append(hoja.row_values(1)[1:])
        wpuntos.append(hoja.row_values(2)[1:])
        wdatos.append(hoja.row_values(celda)[1:])
        dic={}       
        dic['titulo']=hoja.title
        if cont==0:
            wcabeceras[0]=wcabeceras[0][1:]
            wpuntos[0]=wpuntos[0][1:]
            wdatos[0]=wdatos[0][1:]
            dic['porcentaje']=int(float(wdatos[0][-2].replace(",","."))*100/int(wpuntos[0][-2]))
        else:
            dic['porcentaje']=int(float(wdatos[cont][-1].replace(",","."))*100/int(wpuntos[cont][-1]))
        cont=cont+1
        winfo.append(dic)
    context["combi"]=zip(winfo,wpuntos,wcabeceras,wdatos)
    combi2=[]
    for i,punt,cab,dat in context["combi"][1:]:
        combi2.append(zip(cab,dat,punt))
    context["combi2"]=zip(winfo[1:],combi2)
    print context["combi2"]
    #linux
    cont=0
    for hoja in gm.worksheets()[5:]:
        lcabeceras.append(hoja.row_values(1)[1:])
        lpuntos.append(hoja.row_values(2)[1:])
        ldatos.append(hoja.row_values(celda)[1:])
        dic={}       
        dic['titulo']=hoja.title
        if cont==0:
            lcabeceras[0]=lcabeceras[0][1:]
            lpuntos[0]=lpuntos[0][1:]
            ldatos[0]=ldatos[0][1:]
            dic['porcentaje']=int(float(ldatos[0][-2].replace(",","."))*100/int(lpuntos[0][-2]))
        else:
            dic['porcentaje']=int(float(ldatos[cont][-1].replace(",","."))*100/int(lpuntos[cont][-1]))
        cont=cont+1
        linfo.append(dic)
    context["combi3"]=zip(linfo,lpuntos,lcabeceras,ldatos)
    combi4=[]
    for i,punt,cab,dat in context["combi3"][1:]:
        combi4.append(zip(cab,dat,punt))
    context["combi4"]=zip(linfo[1:],combi4)
    print context["combi4"]





    return render(request,"index2.html",context)







def grado_sup(request,gs,celda,nombre):
    context={}
    context["alumno"]=nombre
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
        
        cabeceras.append(hoja.row_values(1)[1:])
        datos.append(hoja.row_values(celda)[1:])
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
        if cont==1:
            col=['info','info','info','info','info','info','danger','danger','info','info','info','info','info','info','danger','danger','danger']
        cab=hoja.row_values(1)[1:]
        dat=hoja.row_values(celda)[1:]
        
        cab[-1]=cab[-1].join(['<strong>','</strong>'])
        dat[-1]=dat[-1].join(['<strong>','</strong>'])
        if cont==1:
            cab=cab[1:]
            dat=dat[1:]
            for i in [6,7,-2,-3]:
                cab[i]=cab[i].join(['<strong>','</strong>'])
                dat[i]=dat[i].join(['<strong>','</strong>'])
        cab=zip(col,cab)
        dat=zip(col,dat)
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

def salir(request):
       del request.session["username"]
       return redirect('/')

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

