
import os, json
from flask import Flask, render_template, request
import MySQLdb

app = Flask(__name__)
db = MySQLdb.connect(user="root", host="localhost", port=3306, db="movie_locations")

@app.route("/")
def hello():
    return render_template('index.html') 

@app.route('/waypoints')
def waypoints():
    movie = request.args.get('title', '')
    thisquery = 'SELECT latitude,longitude FROM sf_locations WHERE title="%s";' % movie
    print thisquery
    db.query(thisquery)
    query_results = db.store_result().fetch_row(maxrows=0)
    print query_results
    address = []
    for i,result in enumerate(query_results):
        address.append({str(i): (float(result[0]),float(result[1]))})
    return json.dumps(address)

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

