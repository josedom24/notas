from lxml import html
import requests
import copy
class Notas:
	def __init__(self):
		self.url=["https://docs.google.com/spreadsheets/d/e/2PACX-1vQ4-twYojuwv8QEbSJdIDT3JCpOKYVNo3sL-kTGSz_aaIa6835nCJFRkniw12zwBqnh73YSHZppF56G/pubhtml#",
				"https://docs.google.com/spreadsheets/d/e/2PACX-1vTsiimXZWscMXe7HGFeTdOg60aHBbHjbbRVQlawgig3mB9Kcudwxht_AvUufj30ncbdPgK9m8q-2yQe/pubhtml"]
		self.titulos=["IAW","Servicios"]
		self.info={}
		for url,tit in zip(self.url,self.titulos):
			page = requests.get(url)
			utf8_parser = html.HTMLParser(encoding='utf-8')
			tree = html.fromstring(page.content,parser=utf8_parser)
			titulos=tree.xpath('//a[@href="#"]/text()')
			cont=2
			tables=[]
			for titulo in titulos[1:]:
				tables.append([cont,titulo])
				cont+=1
			
			
			lista=[]
			for table in tables:
				
				datos=tree.xpath("(//table)[%d]//td"%table[0])
				datos2=[]
				for d in datos:
					try:
						if d.text==None:
							try:
								datos2.append(d.find("div").text)
							except:
			 					datos2.append("")
			 			else: datos2.append(d.text)
			 		except:
			 			datos2.append("")
			 	
			 	
				dic={}
				dic["titulo"]=table[1]
				dic["cabeceras"]=[]			

				
				
				datos2.pop(0)
				cont=0
				for i in datos2:
					cont+=1
					if  len(i)>8: break
					dic["cabeceras"].append(i)
				datos2=datos2[cont-1:]
						
				
				dic["datos"]={}
				
				for i in datos2:
					if len(i)>8:
						nombre=i
						dic["datos"][nombre]=[]
					else:
						dic["datos"][nombre].append(i)
				lista.append(dic)

			self.info[tit]=lista
				

	def alumnos(self):
		alumnos={}
		for tit in self.titulos:
			alumnos[tit]=self.info[tit][0]["datos"].keys()
		return alumnos

	def es_alumno(self,nombre):
		for key,valor in self.alumnos().items():
			return nombre in valor

	def es_alumno_modulo(self,nombre,modulo):
		return nombre in self.alumnos()[modulo]

	def datos(self,nombre):
		datos=copy.deepcopy(self.info)
		print datos is self.info
		for tit in self.titulos:
			if not self.es_alumno_modulo(nombre,tit):
				del datos[tit]
			else:
				for practicas in datos[tit]:
					dat=practicas["datos"]
					for key,value in dat.items():
						if key!=nombre:
							del dat[key]

			
		return datos
