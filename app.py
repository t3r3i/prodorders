from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app=Flask(__name__)

absdir=os.path.abspath(os.path.dirname(__file__))

#database connection URL

db_url = "sqlite:///" + os.path.join(absdir, "orders.db")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config ['JSON_SORT_KEYS'] = False

db=SQLAlchemy(app)
ma=Marshmallow(app)

import modules,upload,order,reports
db.create_all()

app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  #16 megabytes

app.add_url_rule('/upload/', view_func=upload.upload,methods=['POST'])
app.add_url_rule('/order/', view_func=order.orders,methods=['POST'])   
app.add_url_rule('/reports/', view_func=reports.reports,methods=['GET']) 

if __name__=='__main__' :
	app.run(debug = True)