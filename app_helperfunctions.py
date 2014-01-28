def calcDist(lat1,long1,lat2,long2):
    import math
    delta_lat = abs(math.radians(lat1)-math.radians(lat2))
    mean_lat = 0.5*(math.radians(lat1)+math.radians(lat2))
    delta_long = abs(math.radians(long1)-math.radians(long2))
    R = 3958.761 # radius of the Earth in statute miles
    D_sq = (R**2)*(delta_lat**2+(math.cos(mean_lat)*delta_long)**2)
    return D_sq


def filterResults(latitude,longitude,query_results):
    from operator import itemgetter
    uniquelocations = []
    distarray = []
    for i,entry in enumerate(query_results):
        loc_latlong = [float(entry[1]),float(entry[2])]
        # This is bad hack to get rid of duplicates by just throwing out any additional titles at that location.
        if loc_latlong not in uniquelocations:
            uniquelocations.append(loc_latlong)
            location_identifier = uniquelocations.index(loc_latlong)
            dsq = calcDist(latitude,longitude,float(entry[1]),float(entry[2]))
            notes = formatNotes(entry[3])
            distarray.append([entry[0],entry[1],entry[2],notes,entry[4],entry[5],location_identifier,dsq])
        
    distarray_sorted = sorted(distarray,key=itemgetter(7))
    
    return_array = []
    iterator = 0
    returned_locations = 0
    while len(return_array)<=10 and iterator<len(query_results):
        entry = distarray_sorted[iterator]
        return_array.append([entry[0],entry[1],entry[2],entry[3],entry[4],entry[5]])
        iterator = iterator+1
        
    #print distarray_sorted
    return return_array
    
def formatNotes(notes):
    notes = notes.strip(' ')
    notes = notes.strip('(')
    notes = notes.strip(')')
    firstletter = notes[0].upper()
    newnotes = firstletter+notes[1:]+'.'
    return newnotes

def searchNearby(db,latitude,longitude,lrange):
    # Select statement is very long. Break into pieces for readability
    select_statement = 'SELECT title,latitude,longitude,notes,image_url,address FROM locations_with_description WHERE '
    where_statement1 = 'latitude > %f AND latitude < %f' % (latitude-lrange,latitude+lrange)
    where_statement2 = ' AND longitude > %f AND longitude < %f' % (longitude-lrange,longitude+lrange)
    notes_statement = ' AND notes IS NOT NULL;'
    thisquery = select_statement+where_statement1+where_statement2+notes_statement
    db.query(thisquery)
    query_results = db.store_result().fetch_row(maxrows=0)
    return query_results