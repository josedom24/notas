from flask import Flask, request
from flask_restful import Resource, Api,reqparse
from gsheets import Sheets

app = Flask(__name__)
api = Api(app)

sheets = Sheets.from_files('client_secret.json','storage.json')
url={}
url["servicios"]="1KcimLuIx2SCvJtGX2gdoafSKiOCzZJBjVPOKg4M50qc"
url["iaw"]="1RGvTli2W-vXmqWECq1IreHokveZQi-TGaA1mtCB9Q9k"

def es_alumno(nombre,info):
		return  nombre in [x[0] for x in info[0].values()[:-2]]
class ConsultaModulos(Resource):
    def get(self):
        return {"modulos":list(url.keys())}

class ConsultaTitulos(Resource):
    def get(self,modulo):
        if modulo not in list(url.keys()):
            return {"error":"No existe el módulo"},404
        else:
            info=sheets[url[modulo]].findall()
            general=info[0]
            titulos=[x for x in general.values()[0] if x]
            return {"titulos":titulos}
    
class ConsultaAlumno(Resource):
    def get(self,modulo,nombre):
        if modulo not in list(url.keys()):
            return {"error":"No existe el módulo"},404
        else:
            info=sheets[url[modulo]].findall()
            if not es_alumno(nombre,info):
                return {"error":"No existe el alumno"},404
            else:
                res=[]
                for pestaña in info:
                    titulos=[x for x in pestaña.values()[0]]
                    valores=[round(x,2) if type(x)==float else x for x in[x for x in pestaña.values() if x and x[0]==nombre][0]]
                    if valores[-1]!=0:

                        res.append({pestaña.title:[(x,y) for x,y in zip(titulos,valores) if y and x]})
                return res
            


#api.add_resource(ConsultaModulos, '/<string:todo_id>')
api.add_resource(ConsultaModulos, '/modulos')
api.add_resource(ConsultaTitulos, '/titulos/<string:modulo>')
api.add_resource(ConsultaAlumno, '/alumnos/<string:modulo>/<string:nombre>')

if __name__ == '__main__':
    app.run(host=0.0.0.0,debug=True)

