import json
from bs4 import BeautifulSoup
import os

def parse_xml(xml_file):
    with open(xml_file, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, features="xml")
    placemarks = Bs_data.find_all('Placemark')

    # Dictionary to map feature IDs to names
    locations = {}
    for placemark in placemarks:
        # value = placemark.get('id')
        name = placemark.find('name')

        # cleaned_id = value.strip("ID_")
        split_name = name.text.split(":")[0]
        try:
            cleaned_id = split_name.split("-")[0].strip()
            cleaned_name = split_name.split("-")[1].strip()
        except IndexError:
            cleaned_name = split_name.strip()
        
        locations[cleaned_id] = cleaned_name
    
    return locations

def create_clean_geojson(locations, geojson_data, zone_name="Emory University"):
    clean_geojson = {"type": "FeatureCollection", "name": "rooms", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": []}

    for feature in geojson_data['features']:
        feature_id = feature['properties'].get('BLDG')

        if feature_id in locations:
            clean_feature = {
                "type": "Feature",
                "properties": {
                    "name": locations[feature_id],
                    "zone_name": zone_name
                },
                "geometry": feature['geometry']
            }
            clean_geojson["features"].append(clean_feature)
    return clean_geojson

def save_geojson(geojson_data, output_file):
    with open(output_file, 'w') as f:
        json.dump(geojson_data, f, indent=1)
    print(f"GeoJSON file saved with required properties only. Output saved to {output_file}.")

def main(geojson_file, xml_file, output_file='updated_geojson.json'):
    locations = parse_xml(xml_file)
    with open(geojson_file, 'r') as f:
        geojson_data = json.load(f)
    clean_geojson_data = create_clean_geojson(locations, geojson_data)
    save_geojson(clean_geojson_data, output_file)

# Usage example
main('universities/emory/MN_BLDG_01.geojson', 'universities/emory/MN_Label.xml', 'universities/emory/updated_MN.geojson')
