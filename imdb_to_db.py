import MySQLdb
import re

'''
This is a script to get the IMDb data from text files to a MySQL data base.
'''
def strip_all(str):
    str = str.strip(' ')
    str = str.strip('"')
    str = str.strip('\t')
    str = str.strip('(')
    str = str.strip(')')
    str = str.strip('{')
    str = str.strip('}')
    str = str.replace('"',"'")
    str = str.strip(' ')
    return str

filepath = '/Users/BeckyTucker/Insight/data/IMDb/'
loc_file = 'locations.list'

db = MySQLdb.connect(user="root", host="localhost", port=3306, db="movie_locations")
c = db.cursor()
locations = []
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
f = open(filepath+loc_file,'r')

text = f.readlines()
k=0
for i in range(100,len(text)):
    line = text[i]
    # Set some default values
    city = None
    state = None
    country = None
    street_address = None
    location_name = None
    title = None
    episode = None
    year = 0
    skip = 0
    stop = len(line)
    notes = None
    
    # Get the title
    match = re.search(r'".*?"',line)
    if match:
        title = match.group()
        skip = len(title)
        title = strip_all(title)

    # Get the release year
    match = re.search(r'\(.*?\)',line[skip:])
    if match:
        year = match.group()
        skip = skip+len(year)
        year = strip_all(year)
        year = year[0:4]
        if year[0]!='1' and year[0]!='2':
            year = 0
 
    # Get the episode name, if there is one
    match = re.search(r'\{.*\}',line[skip:])
    if match:
        episode = match.group()
        skip = skip+len(episode)
        episode = strip_all(episode)
    
    # Get the notes at the end of the line
    match = re.search(r'\(.*?\)',line[skip:])
    if match:
        notes = match.group()
        stop = len(line)-len(notes)
        notes = strip_all(notes)
    
    # Get the location information
    match = re.search(r'\t.*',line[skip:stop])
    if match:
        location = match.group()
        location = strip_all(location)
        
        place = location.split(' - ') # Split at the dash - typically place names come first
        if len(place)==2:
            location_name = place[0]
            location_name = strip_all(location_name)
            address = place[1]
        else:
            location_name = None
            address = location
            
        # Split at the commas, format is typically street address, city, state, country, though not always complete
        address = address.split(',') 
        parts = len(address)
        if parts==1:
            country = address[0]
        elif parts==2: 
            state = address[0]
            country = address[1]
        elif parts==3:
            city = address[0]
            state = address[1]
            country = address[2]
        elif parts==4:
            city = address[1]
            state = address[2]
            country = address[3]
            nameornum = address[0]
            nameornum = strip_all(nameornum)
            if nameornum[0] in digits:
                street_address = nameornum
            else:
                location_name = nameornum
        elif parts>=5:
            city = address[-3]
            state = address[-2]
            country = address[-1]
            nameornum = address[0]
            nameornum = strip_all(nameornum)
            if nameornum[0] in digits:
                street_address = nameornum
            else:
                location_name = nameornum
                
        # One last clean-up of the parameters
        if country:
            country = strip_all(country)
            # One last check on the country parameter
            csplit = country.split('\t')
            country = csplit[0]
        if state:
            state = strip_all(state)
        if city:
            city = strip_all(city)
        if street_address:
            street_address = strip_all(street_address)
        if location_name:
            location_name = strip_all(location_name)
        
                

    if title and country=='USA':
        a = 'INSERT INTO imdb_locations (title, year, episode, location_name, street_address, city, state, country, notes) \
        VALUES ("%s", %s, "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
        (title, year, episode, location_name, street_address, city, state, country, notes)
        #print a
        #print ' '
        c.execute(a)
    #if mod(i,20)==0:
    #    raw_input()
c.close()
db.commit()
f.close()

