import MySQLdb
from pygeocoder import Geocoder

db = MySQLdb.connect(user="root", host="localhost", port=3306, db="movie_locations")
c = db.cursor()

#myquery= 'SELECT distinct locations FROM sf_locations;'
#db.query(myquery)
#good_locations = []
#sf_locations_all = db.store_result().fetch_row(maxrows=0)

#for i,location in enumerate(sf_locations_all):
#    thislocation = location[0] #.encode('latin-1').decode('utf-8')
#    if thislocation:
#        address = ''
#        full_address = 'San Francisco' + ',' + 'CA'
#        locsplit = thislocation.split('(')
#        location_name = locsplit[0]
#        if len(locsplit) == 2:
#            address = locsplit[1]
#            address = address[0:-1]
#            full_address = address + ',' + full_address
#        else:
#            full_address = location_name + full_address
#        try:
#            results = Geocoder.geocode(full_address)
#            coord = results[0].coordinates
#            lat = coord[0]
#            longitude = coord[1]
#            formatted_address = results.formatted_address
#            good_locations.append((thislocation, formatted_address, lat, longitude))
#        except:
#            print thislocation + 'Not Found'
        
        
for entry in good_locations:
    a = 'UPDATE sf_locations SET latitude=%f, longitude=%f WHERE locations="%s";' % (entry[2],entry[3],entry[0])
    c.execute(a)
c.close()
db.commit()
db.close()
