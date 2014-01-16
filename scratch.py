city = None
state = None
country = None
street_address = None
location_name = None
title = None
episode = None
year = None
    
match = re.search(r'".*"',line)
if match:
    title = match.group()
    title = title.strip(' ')
    title = title[1:-1]

match = re.search(r'\(.*?\)',line)
if match:
    year = match.group()
    year = year.strip(' ' )
    year = year[1:-1]
 
match = re.search(r'\{.*\}',line)
if match:
    episode = match.group()
    episode = episode.strip(' ')
    episode = episode[1:-1]
    
match = re.search(r'\t.*',line)
if match:
    location = match.group()
    location = location.strip('\t') # Strip out any excess tabs
    location = location.strip(' ')
        
    place = location.split(' - ') # Split at the dash - typically place names come first
    if len(place)==2:
        location_name = place[0]
        location_name = location_name.strip(' ')
        address = place[1]
    else:
        location_name = None
        address = location
            
    # Split at the commas, format is typically street address, city, state, country, though not always complete
    address = address.split(',') 
    parts = len(address)
    if parts==1:
        country = address
        country = country.strip(' ')
    elif parts==2: 
        state = address[0]
        country = address[1]
        state = state.strip(' ')
        country = country.strip(' ')
    elif parts==3:
        city = address[0]
        state = address[1]
        country = address[2]
        city = city.strip(' ')
        state = state.strip(' ')
        country = country.strip(' ')
    elif parts==4:
        city = address[1]
        state = address[2]
        country = address[3]
        city = city.strip(' ')
        state = state.strip(' ')
        country = country.strip(' ')
        nameornum = address[0]
        nameornum = nameornum.strip(' ')
        if nameornum[0] in digits:
            street_address = nameornum
            street_address = street_address.strip(' ')
        else:
            location_name = nameornum
            location_name = location_name.strip(' ')
    elif parts>=5:
        city = address[-3]
        state = address[-2]
        country = address[-1]
        city = city.strip(' ')
        state = state.strip(' ')
        country = country.strip(' ')
        nameornum = address[0]
        nameornum = nameornum.strip(' ')
        if nameornum[0] in digits:
            street_address = nameornum
            street_address = street_address.strip(' ')
        else:
            location_name = nameornum
            location_name = location_name.strip(' ')

    # One last check on the country parameter
    csplit = country.split('\t')
    country = csplit[0]
print "INSERT INTO imdb_locations (title, year, episode, location_name, street_address, city, state, country) \
        VALUES ('%s', %s, '%s', '%s', '%s', '%s', '%s', '%s')" % (title, year, episode, location_name, street_address, city, state, country)
