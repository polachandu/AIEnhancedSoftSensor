import csv 
import mysql.connector
mysql=mysql.connector.connect(host="localhost",user="root",password="1234",database="pumpexample")

myCursor=mysql.cursor()
command="select * from pumpexample"
myCursor.execute(command)

file=open('extract_data.txt','w',encoding='UTF8')
header="STC,S_Pin_kPa,S_F_kgh,S_E_kW,S_Pout_kPa\n"
file.write(header)

resultTwo=myCursor.fetchall()
print("Total rows are:  ", len(records))
print("Printing each row")
for row in resultTwo:
    resultRow=str(row[0])+','+ str(row[1])+','+str(row[2])+','+ str(row[3])+','+ str(row[4])+'\n'
    print(resultRow)
    file.write(resultRow)
file.close()    
print("finish")    

# -----------------------------------------------------------------------------------------------