
import os
from flask import Flask, render_template
import MySQLdb

app = Flask(__name__)
db = MySQLdb.connect(user="root", host="localhost", port=3306, db="world")

@app.route("/")
def hello():
    return render_template('index.html') 

@app.route("/db")
def cities_page():
    db.query("SELECT Name FROM city;")

    query_results = db.store_result().fetch_row(maxrows=0)
    cities = ""
    for result in query_results:
        cities += unicode(result[0], 'utf8')
        cities += "<br>"
    return cities

@app.route("/db_fancy")
def cities_page_fancy():
    db.query("SELECT Name, CountryCode, Population FROM city;")

    query_results = db.store_result().fetch_row(maxrows=0)
    cities = []
    for result in query_results:
        cities.append(dict(name=unicode(result[0], 'utf8'), country=result[1], population=result[2]))
    return render_template('cities.html', cities=cities) 


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


