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
		#lldap=LibLDAP(username,password)
		#if lldap.isbind:
		if True:
				request.session["username"]=username
				#busqueda='(uid=%s)'%username
				#resultados=lldap.buscar(busqueda)
				#info=resultados[0].get_attributes()
				#return index2(request,username,info["sn"][0]+", "+info["givenname"][0]) 
				return index2(request,username,"Adan Reina") 
		else:
			   info={"error":True}
			   return render(request,"login.html",info)


def index2(request,username,nombre):
	notas=Notas()
	if notas.es_alumno(username):
		return alumno(request,username,nombre)
	else:
		return render(request,'login.html')
	
def alumno(request,username,nombre):
	notas=Notas()
	info={"datos":notas.datos(username),"nombre":nombre}
	return render(request,"index.html",info)    

def salir(request):
	del request.session["username"]
	return redirect('/')
