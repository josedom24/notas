from lxml import html
import requests
class Notas:
	def __init__(self):
		self.url=["https://docs.google.com/spreadsheets/d/e/2PACX-1vQ4-twYojuwv8QEbSJdIDT3JCpOKYVNo3sL-kTGSz_aaIa6835nCJFRkniw12zwBqnh73YSHZppF56G/pubhtml#"]
		self.titulos=["IAW"]
		
		for url,titulo in zip(self.url,self.titulo):
			page = requests.get(url)
			tree = html.fromstring(page.content)
			titulos=tree.xpath('//a[@href="#"]/text()')
			cont=2
			tables=[]
			for titulo in titulos[1:]:
				tables.append([cont,titulo])
				cont+=1
			info=[]
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
					if  len(i)>10: break
					dic["cabeceras"].append(i)
				datos2=datos2[cont-1:]
						
				
				
				dic["datos"]={}
				self.info[titulo].append(dic)
				for i in datos2:
					if len(i)>10:
						nombre=i
						dic["datos"][nombre]=[]
					else:
						dic["datos"][nombre].append(i)


