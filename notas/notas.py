from lxml import html
import requests
page = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vTsiimXZWscMXe7HGFeTdOg60aHBbHjbbRVQlawgig3mB9Kcudwxht_AvUufj30ncbdPgK9m8q-2yQe/pubhtml')
tree = html.fromstring(page.content)
titulos=tree.xpath('//a[@href="#"]/text()')
cont=2
tables=[]
for titulo in titulos[1:]:
	tables.append([cont,titulo])
	cont+=1
print tables
info=[]
for table in tables[1:2]:
	print "(//table)[%d]//td/text()"%table[0]
	datos=tree.xpath("(//table)[%d]//td"%table[0])
	print datos
	datos2=[]
	for d in datos:
		print d.text
		if d.text==None:
			print ">>>"+d.xpath("//div/text()")[0]
#			datos2.append(d)
#		else:
#			datos2.append()
#	print datos2
#	dic={}
#	dic["titulo"]=table[1]
#	dic["cabeceras"]=[]
#	for i in datos2:
#		print i
#		if i[0]=="T" and len(i)<10:
#			dic["cabeceras"].append(i)
#			
#	info.append(dic)
#print info