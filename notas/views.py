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
	print notas.alumnos()
	if notas.es_alumno(username):
		return alumno(request,username,nombre)
	else:
		return render(request,'login.html')
	
def alumno(request,username,nombre):
	notas=Notas()
	datos=notas.datos(username)

	total={}
	lleva={}
	nota={}
	for keys,values in datos.items():
		acum=0
		acum2=0
		for prac in values:
			if "-" in prac["cabeceras"][-1]:
				prac["total"]=int(prac["cabeceras"][-1].split("-")[0])
			else:
				prac["total"]=int(prac["cabeceras"][-1])
			acum+=prac["total"]
			print prac["datos"]
			acum2+=int(prac["datos"].values()[0][-1])
		total[keys]=acum
		lleva[keys]=acum2
		nota[keys]=round(float(acum2*10)/acum,2)
		print total
	info={"datos":datos,"nombre":nombre,"total":total,"lleva":lleva,"nota":nota}
	return render(request,"index.html",info)    

def salir(request):
	del request.session["username"]
	return redirect('/')
