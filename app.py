from flask import Flask, render_template
from sqlalchemy  import create_engine
from flask_sqlalchemy import SQLAlchemy
import click
import pandas as pd
import os 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'qwerty$asdf#123'

basedir =    os.getcwd()
# '~/Desktop/fproj/pandasdatabase'#os.path.abspath(os.path.dirname(__file__))


#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#        'sqlite:///' + os.path.join(basedir, 'app.db')

app.config['SQLALCHEMY_DATABASE_URI'] =    'sqlite:///' + os.path.join(basedir, 'app.db') #  'sqlite:////tmp/test.db'#'sqlite://db.sqlite3'  os.environ.get('DATABASE_URL') or \

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
	passengerID = db.Column(db.Integer, primary_key = True)
	name      = db.Column(db.String(250), nullable = False)
	survived  = db.Column(db.Integer , nullable = False)
	sex       =  db.Column(db.String(10), default = None)
	age       = db.Column(db.Integer,  default = -1)
	fare      = db.Column (db.Float, default = -1)

	def __init__(self, passengerID , name , survived, sex , age , fare):
		self.passengerID = passengerID
		self.name        = name
		self.survived    = survived
		self.sex         = sex
		self.age         = age
		self.fare        = fare


	def __repr__(self):
		return str(self.passengerID)+'-'+str(self.name)+'-'+str(self.survived)+'-'+ str(self.sex) + '-' + str(self.age) + '-' + str(self.fare)


@app.cli.command("load_data")
@click.argument("fname")

def load_data(fname):
	print(' load data from file: ' + fname)

	df = pd.read_csv(fname)

	for row in df.itertuples(index=False):

		print('*************')

		v_passengerId 	= row[0]
		v_survived    	= row[1]
		v_name        	= row[3]
		v_sex			= row[4]
		v_age 			= row[5]
		v_fare			= row[9]

		obj = Data(v_passengerId, v_name, v_survived, v_sex, v_age, v_fare)
		db.session.add( obj )

	db.session.commit()

@app.route('/')
def hello_world():
	retVal = 'Hello, the database has ('+str(len(Data.query.all()))+')'
	retVal += '<br /> see loaded '
	retVal += '<br /><a href = "/data">data</a>.'
	retVal += '<br /><a href = "/male">male</a>.'
	return retVal

@app.route('/data')
def data():
	retVal = 'Rows = ' + str( len(Data.query.all()) ) + '<br />' 
	for row in Data.query.all():
		retVal += '<br />' + str( row.__repr__() )             
	return retVal


@app.route('/male')
def male():
	'''retval = 'Rows = ' + str( Data.query.filter(Data.sex == 'male').count()) + '<br />' 
	for row in Data.query.filter(Data.sex == 'male'):
		retval += '<br />' + str( row.__repr__() )
	return retval
	'''
	data = Data.query.filter(Data.sex == 'male')
	return render_template('tables.html',heading = "males", data = data )

@app.route('/female')
def female():
	retval = 'Rows = ' + str( Data.query.filter(Data.sex == 'female').count() ) + '<br />' 
	for row in Data.query.filter(Data.sex == 'female'):
		retval += '<br />' + str( row.name )
	return retval

if __name__ == "__main__":
	app.run(debug = True, host = "0.0.0.0", port = 3000)