import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	#  port=3360,
	user="root",
	password="1122cccc",
	database = "mybase"
)

mycursor = mydb.cursor()
'''
try:
	# create database mybase
	mycursor.execute("CREATE DATABASE mybase")
	mydb.database = "mybase"
except:
	try:
		# create table root, insert data
		mycursor.execute("CREATE TABLE root (path_ VARCHAR(255), file_name VARCHAR(255))")
		insert = "INSERT INTO root (path_, file_name) VALUES (%s, %s)"
		value = ("path", "highway 21")
		mycursor.execute(insert, value)
	except: 
		()
finally:
	# fetch data'''
mycursor.execute("SELECT value FROM vlist")

result = mycursor.fetchall()

# delete table root
delete = "DROP TABLE IF EXISTS vlist"
mycursor.execute(delete)

for x in result:
	print(x)
	
mydb.commit() # acquired to make the changes