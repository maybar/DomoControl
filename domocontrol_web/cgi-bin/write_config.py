#!/usr/bin/env python3

#import modules for CGI handling
import cgi, cgitb
import json

#create instance of FieldStorage
form =cgi.FieldStorage()

#Get data from fields
Temp1 = form.getvalue('temp_1')
Temp2 = form.getvalue('temp_2')
Temp3 = form.getvalue('temp_3')

#leemos datos de archivo
with open('config.json', 'r') as file:
    datos = json.load(file)


print ("Content-type:text/html\r\n\r\n") 
print ("<html>" )

print ("    <head>" )
print ("        <title>Domo Control</title>")
print ("    </head>")
print("    <body >")
print ( "<h2>Datos recibidos: %s %s %s</h2>" % (Temp1,Temp2,Temp3))
print("    </body >")
print("</html>")  

datos['temp_1'] = str(Temp1)
datos['temp_2'] = str(Temp2)
datos['temp_3'] = str(Temp3)

with open('config.json', 'w') as file:
    json.dump(datos, file)