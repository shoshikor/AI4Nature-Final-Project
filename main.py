import requests
import csv
import os
from datetime import datetime

LAYER_ID = "892" 
URL = f"https://gisn.tel-aviv.gov.il/arcgis/rest/services/WM/IView2WM/MapServer/{LAYER_ID}/query"
CSV_FILE = "historical_traffic_tel_aviv.csv"

FIELDS = ['capture_time', 'OBJECTID', 'street', 'level', 'speedKMH', 'delay', 
          'length', 'uuid', 'updateDate', 'pubMillis', 'country', 'city', 
          'turnType', 'type', 'endNode', 'speed', 'roadType', 'SHAPE_Length']

def fetch_data():
    params = {
        "where": "1=1",
        "outFields": "*", 
        "f": "json",
        "returnGeometry": "false"
    }
    try:
        # Retrieves real-time congestion data [cite: 66, 70]
        response = requests.get(URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json().get('features', [])
    except Exception as e:
        print(f"API Error: {e}")
        return []

def save_data(records):
    file_exists = os.path.exists(CSV_FILE)
    current_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
        
        if not file_exists:
            writer.writeheader()
        
        if records:
            for item in records:
                attributes = item.get('attributes', {})
                # Injecting the script's execution time
                attributes['capture_time'] = current_now
                writer.writerow(attributes)
            print(f"[{current_now}] Saved {len(records)} records.")
        else:
            print(f"[{current_now}] No records found.")

if __name__ == "__main__":
    data = fetch_data()
    save_data(data)
