import folium
import re
import requests

def read_param():
    s = input("Please write year\n")
    try:
        s = int(s)
        assert 1850 < s < 2020
        return s
    except:
        print("Incorrect data\n")
    

def find_films(year, file_name):
        st = set()
        f = open(file_name, 'r')
        
        for line in f:

            # Find the string "title of the film (year)"
            s1 = re.search(r'"?.+"? .\d+.', line)
            if not s1:
                continue

            # Get title and year from s1
            arr = s1.group(0).split(' ')
            title = ' '.join(arr[:-1])
            film_year = arr[-1][1:-1]  

            # Get location from line 
            if line[-2] == ')':
                location = line.split('\t')[-2].strip()
            else:
                location = line.split('\t')[-1].strip()
            # If data is correct add it in set
            if film_year.isdigit() and year == int(film_year):
                st.add((title, location))
                     
        lst = list(st)
        f.close()
        return lst
            

def draw_map(file_name, year):

    f = open(file_name, 'r')
    
    # Create an empty map
    my_map = folium.Map(location=[48.314775, 25.082925], zoom_start=4)
    
    # Add all coordinates from list into one feature group
    fg_f = folium.FeatureGroup(name="Films_map" + str(year))
    for line in f:
        location = [float(line.split()[0]), float(line.split()[1])]
        fg_f.add_child(folium.Marker(location=location,
                        popup=' '.join(line.split()[2:]), icon=folium.Icon()))

    # Add population on the map
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                    encoding='utf-8-sig').read(),
                    style_function=lambda x: {'fillColor':'green'
    if x['properties']['POP2005'] < 10000000
    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
    else 'red'}))
    # Add group and save map
    my_map.add_child(fg_f)
    my_map.add_child(fg_pp)
    my_map.add_child(folium.LayerControl())
    my_map.save('Map.html')

    
def get_coor(lst_films, file_name):
    coor_lst = list()
    f = open(file_name, 'w')
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    
    for el in lst_films[:500]:
        params = {
            'address': el[1],
            'sensor': 'false',
            'key': 'AIzaSyDdO3p0H7ortsOLqh2Pr4LtiVXY1JpPQSI'
        }

        # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()

        # Use the first result
        if not res['results']:
            print(res)
            continue
        result = res['results'][0]

        
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        coor_lst.append([lat, lng])
        f.write(str(lat) + ' ' + str(lng) + ' ' + el[0] + '\n')
    f.close()
    return coor_lst

        

if __name__ == "__main__":
    year = None
    while not year:
        year = read_param()
        
    lst_films = find_films(year, 'locations.list')
    coor_lst = get_coor(lst_films, 'coordinates_1960year.txt')
    draw_map('coordinates_1960year.txt', year)
