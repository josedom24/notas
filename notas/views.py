# -*- coding: utf-8 -*-_
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from libldap import LibLDAP
from libnotas import Notas

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
    notas=Notas()
    print notas.info
    if username=="josedom":
        return admin(request)
    else:
        return render(request,'login.html')
	
def admin(request):
    context={}
    return render(request,"index3.html",context)

def salir(request):
    del request.session["username"]
    return redirect('/')
