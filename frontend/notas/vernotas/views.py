from django.shortcuts import render,redirect
from .libldap import LibLDAP
from requests import get
# Create your views here.
def index(request):
    if request.method=="GET":
            return render(request,'login.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"].encode('utf-8')
        modulo = request.POST["modulo"]
        request.session["username"]=username
        lldap=LibLDAP(username,password)
        if lldap.isbind:
        		request.session["username"]=username
        		busqueda='(uid=%s)'%username
        		resultados=lldap.buscar(busqueda)
        		info=resultados[0].get_attributes()
        		return index2(request,username,info["sn"][0].decode()+", "+info["givenname"][0].decode(),modulo) 
        
        else:
        	   info={"error":True}
        	   return render(request,"login.html",info)
        #return index2(request,"jesus.arias","Jesús Arias","servicios")
def index2(request,username,nombre,modulo):
    return HttpResponse("Hello, world. You're at the polls index.")
    r = get("http://notas.gonzalonazareno.org:5000/alumnos/{}/{}".format(modulo,username))
    if r.status_code==200:
        info={"nombre":nombre,"modulo":modulo,"datos":r.json()}
        print(r.json())
        return render(request,"index.html",info)    
    else:
        info={"error":True}
        return render(request,'login.html')
    
    
    
def salir(request):
    del request.session["username"]
    return redirect('/notas')
