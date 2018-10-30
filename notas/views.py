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
		modulo = request.POST["modulo"]
		lldap=LibLDAP(username,password)
		if lldap.isbind:
				request.session["username"]=username
				busqueda='(uid=%s)'%username
				resultados=lldap.buscar(busqueda)
				info=resultados[0].get_attributes()
				return index2(request,username,info["sn"][0]+", "+info["givenname"][0],modulo) 
				#return index2(request,"jesus.arias","Jesús Arias","IAW")
		else:
			   info={"error":True}
			   return render(request,"login.html",info)


def index2(request,username,nombre,modulo):
	notas=Notas(modulo)
	if notas.es_alumno(username):
		#info={"datos":datos,"nombre":nombre,"total":total,"lleva":lleva,"nota":nota}
		info={"nombre":nombre,"modulo":modulo,"datos":notas.general(username),"datos2":notas.datos(username)}
		print notas.datos(username)
		return render(request,"index.html",info)    
	else:
		return render(request,'login.html')
	
def salir(request):
	del request.session["username"]
	return redirect('/')
