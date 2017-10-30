from lxml import html
import requests
page = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQ4-twYojuwv8QEbSJdIDT3JCpOKYVNo3sL-kTGSz_aaIa6835nCJFRkniw12zwBqnh73YSHZppF56G/pubhtml#')
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
			
	info.append(dic)
	dic["datos"]=datos2

print info[0]
print "#"*20
print info[1]
print "#"*20
print info[2]
print "#"*20
print info[3]
print "#"*20