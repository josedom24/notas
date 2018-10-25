from gsheets import Sheets

class Notas:
	def __init__(self,modulo):
		sheets = Sheets.from_files('~/github/notas/client_secret.json', '~/github/notas/storage.json')
		self.url={}
		self.url["Servicios"]="1KcimLuIx2SCvJtGX2gdoafSKiOCzZJBjVPOKg4M50qc"
		self.url["IAW"]="1RGvTli2W-vXmqWECq1IreHokveZQi-TGaA1mtCB9Q9k"
		s=sheets[self.url[modulo]]
		self.info=s.findall()
	def es_alumno(self,nombre):
		return  nombre in [x[0] for x in self.info[0].values()[:-2]]	
	
	def general(self,nombre):
		general=self.info[0]
		titulos=general.values()[0][2:]
		valores=[x[2:] for x in general.values()[:-2] if x[0]==nombre][0]
		return [[x[0] for x in [(x,y) for x,y in zip(titulos,valores) if y!=""]],[round(x,2) if type(x)==float else x for x in [x[1] for x in [(x,y) for x,y in zip(titulos,valores) if y!=""]]]]
	
	def datos(self,nombre):
		general=self.info[0]
		valores=[x[2:] for x in general.values()[:-2] if x[0]==nombre][0]
		res=[]
		tit=[]
		for i in range(1,len([x for x in valores if x!=""][:-5])+1):
			hoja=self.info[i]
			titulos=hoja.values()[0][2:]
			valores=[x[2:] for x in hoja.values()[:-2] if x[0]==nombre][0]
			res.append([titulos,[round(x,2) if type(x)==float else x for x in valores]])
			tit.append(hoja.title)
		return zip(tit,res)