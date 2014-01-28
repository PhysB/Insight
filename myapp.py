import os, json
from flask import Flask, render_template, request
import MySQLdb
from operator import itemgetter
import math
from app_helperfunctions import calcDist, filterResults, searchNearby

app = Flask(__name__)
db = MySQLdb.connect(user="root", host="localhost", port=3306, db="movie_locations")

@app.route("/")
def hello():
    return render_template('index.html') 

@app.route('/locations')
def locations():
    movie = request.args.get('title', '')
    thisquery1 = 'SELECT title,latitude,longitude,notes,image_url,address '
    thisquery2 = 'FROM locations_with_description WHERE title="%s" AND notes IS NOT NULL;' % movie
    #print thisquery
    thisquery = thisquery1+thisquery2
    db.query(thisquery)
    query_results = db.store_result().fetch_row(maxrows=0)
    print query_results
    address = []
    for i,result in enumerate(query_results):
        address.append({str(i): (str(result[0]),float(result[1]),float(result[2]),str(result[3]),str(result[4]),str(result[5]))})
    return json.dumps(address)

@app.route('/moviesearch')
def moviesearch():
    q = request.args.get('q')
    thisquery = 'SELECT title FROM locations_with_description WHERE title LIKE "{}%" LIMIT 10;'.format(q)
    print thisquery
    db.query(thisquery)
    query_results = db.store_result().fetch_row(maxrows=0)
    print query_results
    movies = []
    for i,result in enumerate(query_results):
        movies.append(result[0])
    return json.dumps(movies)

@app.route('/nearby')
def nearby():
    # Latitude and longitude refer the address of the user
    latitude = request.args.get('latitude', '')
    longitude = request.args.get('longitude','')
    latitude = float(latitude)
    longitude = float(longitude)
    lrange = 0.25
    query_results = searchNearby(db,latitude,longitude,lrange)
    while len(query_results)<1:
        lrange = lrange+0.25
        query_results = searchNearby(db,latitude,longitude,lrange)
    #print 'Number of query results = ' + str(len(query_results))
    return_array = filterResults(latitude,longitude,query_results)
    address = []
    for i,result in enumerate(return_array):
        address.append({str(i): (str(result[0]),float(result[1]),float(result[2]),str(result[3]),str(result[4]),str(result[5]))})
    return json.dumps(address)

@app.route('/altsearch')
def altsearch():
    return render_template('altsearch.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/<pagename>') 
def regularpage(pagename=None): 
    """ 
    Route not found by the other routes above. May point to a static template. 
    """ 
    return "You've arrived at " + pagename
    #if pagename==None: 
    #    raise Exception, 'page_not_found' 
    #return render_template(pagename) 

if __name__ == '__main__':
    print "Starting debugging server."
    app.run(debug=True, host='localhost', port=8000)