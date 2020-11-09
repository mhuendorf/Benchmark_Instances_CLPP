import sys
import requests
import json
import numpy as np 
import matplotlib.pyplot as plt


def read_query_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

def query(query, outfilename):
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, 
                            params={'data': query})
    data = response.json()
    with open(outfilename, 'w') as outfile:
        json.dump(data, outfile)


def visualize_xy(coords):
    X = np.array(coords)
    plt.plot(X[:, 0], X[:, 1], 'o')
    plt.title('Nodes')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.axis('equal')
    plt.show()


def to_int(val, scaling_factor):
    return int(round(val, scaling_factor) * 10**scaling_factor) # 100000


def normalize(val, min, scaling_factor):
    return to_int(val, scaling_factor) - min


def remove_whitespace(str):
    return str.strip().replace(" ", "_")


def convert_to_instance(infile, outfile, height, width_factor, scaling_factor):

    with open(infile) as json_file:
        data = json.load(json_file)

    cities = []
    lon_min = 100000000
    lat_min = 100000000
    for element in data['elements']:
        if element['type'] == 'node':

            tags = element['tags']
            if('name' in tags):
                name = remove_whitespace(tags['name'])
                lon = element['lon']
                if lon < lon_min:
                    lon_min = lon
                lat = element['lat']
                if lat < lat_min:
                    lat_min = lat
                cities.append((lon, lat, name))

    lon_min = to_int(lon_min, scaling_factor)
    lat_min = to_int(lat_min, scaling_factor)
    
    coords = []

    with open(outfile, 'w') as out:

        out.write(str(len(cities)) + '\n')

        for lon, lat, name in cities:
            lon = normalize(lon, lon_min, scaling_factor)
            lat = normalize(lat, lat_min, scaling_factor)
            coords.append((lon, lat))
            out.write(str(lat) + " " 
                        + str(lon) + " " 
                        + str(height) + " " 
                        + str(int(len(name) * width_factor)) + " "
                        + name + '\n')
    
    return coords


if __name__ == "__main__":
    if(len(sys.argv) != 7):
        print("Call this script with 5 arguments:")
        print("1. path to the .query-file that contains the query")
        print("2. path to the .json-file to store the OSM result (to avoid running into too many request-issues)")
        print("3. path to the .txt-file that will contain the result")
        print("4. integer for the height of labels")
        print("5. integer for the width of a single letter of the label (will be multiplied with number of letters in the label)")
        print("6. integer for the scaling factor (how many decimals to round, use higher value for closer points (Paris=5, USA=4)")
        print("Example argument: python3 city.py germantowns.query ../res/germantowns.json ../res/germantowns.txt 300 100 4")
        # python3 city.py mcdonalds.query ../res/mcdonalds.json ../res/mcdonalds.txt 30 10 5
    else:

        # parsing arguments
        query_file = sys.argv[1]
        jsonfile = sys.argv[2]
        instance_file = sys.argv[3]
        height = int(sys.argv[4]) # how high the labels should be
        width_factor = int(sys.argv[5]) # how wide a letter should be 
        scaling_factor = int(sys.argv[6]) 
        
        # parsing the query into a string
        query_string = read_query_file(query_file)

        # querying OSM, storing json in jsonfile
        query(query_string, jsonfile)
        
        # converting the jsonfile to our instance
        coords = convert_to_instance(jsonfile, instance_file, height, width_factor, scaling_factor)

        # visualizing the generated dataset
        visualize_xy(coords)
    