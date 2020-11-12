import sys
import requests
import json
import math
import numpy as np 
import matplotlib.pyplot as plt
from pyproj import Transformer

# lat/lon to mercator
TRAN_4326_TO_3857 = Transformer.from_crs("EPSG:4326", "EPSG:3857")

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

# returns coordinates in meters east of 0 and meters north of 0
# so the lower left corner of the map is (0,0)
def mercator(lat, lon, scaling_factor):
  x, y = TRAN_4326_TO_3857.transform(lat, lon)
  return round(x/scaling_factor), round(y/scaling_factor)


def visualize_xy(coords):
    X = np.array(coords)
    plt.plot(X[:, 0], X[:, 1], 'o')
    plt.title('Nodes')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.axis('equal')
    plt.show()

def remove_whitespace(str):
    return str.strip().replace(" ", "_")


def convert_to_instance(infile, outfile, height, width_factor, scaling_factor):

    with open(infile) as json_file:
        data = json.load(json_file)

    cities = []
    for element in data['elements']:
        if element['type'] == 'node':

            tags = element['tags']
            if('name' in tags):
                name = remove_whitespace(tags['name'])
                lon = element['lon']
                lat = element['lat']
                x, y = mercator(lat, lon, scaling_factor)
                cities.append((x, y, name))

    
    coords = []

    with open(outfile, 'w') as out:

        out.write(str(len(cities)) + '\n')

        for x, y, name in cities:
            coords.append((x, y))
            out.write(str(x) + " " 
                        + str(y) + " " 
                        + str(int(len(name) * width_factor)) + " "
                        + str(height) + " " 
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
        print("6. integer for the scaling factor (1 = meters, 1000 = kilometers etc)")
        print("Example argument: python3 city.py germantowns.query ../res/germantowns.json ../res/germantowns.txt 300 100 4")
        # python3 city.py ../res/queries/americantowns.query ../res/json/americantowns.json ../res/instances/americantowns.txt 6 5 1000
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
    