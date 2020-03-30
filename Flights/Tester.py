from Utilities import Statistics as st
import json
import os

from tqdm import tqdm

from Utilities import General

with open(os.path.dirname(__file__) + '/../Data/Flights/json_files.json', 'r',
          encoding='utf-8') as f:
    append_data = json.load(f)
append_data=list(set(append_data))
with open(os.path.dirname(__file__) + '/../Data/Flights/json_files.json', 'w', encoding='utf-8') as f:
    json.dump(append_data, f, ensure_ascii=False,indent=4)

for json_file in tqdm(append_data):
    General.add_to_json_dict(json_file)


st.get_how_much_flights_per_airport()