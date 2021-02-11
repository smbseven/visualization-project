from flask import Flask, render_template, jsonify, redirect
import json
from flask_pymongo import PyMongo
import app1_psL #to change depend of file
# import atlas_obscura_scraper_psL #to change depend file


# Instance of Flask app
app=Flask(__name__)

# connect to MongoDB for tourism
mongo1 = PyMongo(app, uri="mongodb://localhost:27017/tourism")

# connect to another MongoDB with coordenates
mongo2 = PyMongo(app, uri="mongodb://localhost:27017/coordinates")

# connect to another MongoDB with scraping
mongo3 = PyMongo(app, uri="mongodb://another.host:27017/scraping")


##Create a root route '/' that will query your Mongo database and pass Inbound and OutBbound data into HTML template
@app.route("/")
def index():
    

    tourism=mongo1.db.tourism
    coordinates=mongo2.db.coordinates
    
    coordinates_funtion=app1_psL.coordinates()    
    mylist=app1_psL.data_OCEDE()

    #Uptade to the BD Tourism
    for item in mylist:
        tourism.update({}, item, upsert=True)
    
    #Update to BD Coorfinates
    for item in coordinates_funtion:
        coordinates.update({}, item, upsert=True)
    
    countries=tourism.find()
    data_coordenates=coordinates.find()
    #Is necesary create more def with diferent methods 'get', 'render' 
    
    return render_template('index.html', countries=countries, coordenates=data_coordenates)#coordenates=coordenates)

if __name__ == "__main__":
    app.run(debug=True)