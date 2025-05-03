import json
import pandas as pd

def load_airpot_data():
    with open ('./data/airport.json', 'r') as f: 
        data = json.load(f)
        return data
    

if __name__=='__main__':
    data = load_airpot_data()
    df = pd.DataFrame(data)
    departures = df['departures']
    departures = departures.explode("departure")
    departures_time = departures.map(lambda ele : ele['departure'].get('scheduledTime', {}).get('utc', None))
    print (f"Data contains records from {departures_time.min()} to {departures_time.max()} with {len(departures_time)} records ")
    
