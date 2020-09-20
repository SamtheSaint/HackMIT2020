import os
import pandas as pd

lookup = pd.read_csv('data/lookup.csv')

for filename in os.listdir('exports'):
    loc = filename.replace('marquee', '').replace('gov', '').replace('.csv', '')
    df = pd.read_csv(os.path.join('exports', filename))
    print(lookup.loc[lookup['AreaCodes'] == loc]['Latitude'])
    print(lookup.loc[lookup['AreaCodes'] == loc][' Longitude'])
