from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as pg2

app = Flask(__name__)

def connectDB(db,user,host,port):
	
	try:
		conn = pg2.connect(database=db,user=user,host=host,port=port)
		cur = conn.cursor()
	except Exception as e:
		print(e)
	return (conn,cur)

def readDBConfigFile(dbConfigFile):

	db_param = {}
	f = open(dbConfigFile,"r")
	for line in f:
		if 'database' in line:
			database = line.split("=")[1].strip()
		elif 'username' in line:
			username = line.split("=")[1].strip()
		elif 'host' in line:
			host = line.split("=")[1].strip()
		elif 'port' in line:
			port = line.split("=")[1].strip()

	db_param['database'] = database
	db_param['username'] = username
	db_param['host'] = host
	db_param['port'] = port

	return db_param

param = readDBConfigFile("config/dbconfig.cfg")

database = param['database']
username = param['username']
host = param['host']
port = param['port']

conn, cur = connectDB(database,username,host,port)

query = "SELECT title,price,rating,in_stock FROM books"
cur.execute(query) 
books = cur.fetchall()

@app.route('/',methods=['GET','POST'])
def index():

	if request.method == "POST":
		name = request.form.get("name")
		
		query = "SELECT title,price,rating,in_stock FROM books WHERE title=%s"
		cur.execute(query,(name,))
		book = cur.fetchall()
		return render_template('index.html',books=book)
	else:
		return render_template('index.html',books=books)

if __name__ == "__main__":
	app.run(debug=True)