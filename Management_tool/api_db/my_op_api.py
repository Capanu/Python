import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="example")

if mydb:
    print("Connection Succescfull!")
else:
    print("Connection NOT Succescfull!")

mycursor = mydb.cursor()

stringer = "insert into angajati values" + f'("{"Migdala"}", "{"Andrei"}")' +";"
print(stringer)
mycursor.execute(stringer)

mydb.commit()

print(mycursor.rowcount, "record inserted.")