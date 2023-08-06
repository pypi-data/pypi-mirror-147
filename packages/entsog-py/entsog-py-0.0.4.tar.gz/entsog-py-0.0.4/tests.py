
from entsog import EntsogRawClient, EntsogPandasClient
import pandas as pd
import json
import time

from entsog.mappings import BalancingZone

from entsog.mappings import Country

def get_area():
    client = EntsogRawClient()
    data = json.loads(client.query_operator_point_directions(limit = -1))

    df = pd.json_normalize(data['operatorpointdirections'])

    df_drop = df.drop_duplicates(subset=['tSOCountry'])

    c = {}
    for idx, item in df_drop.iterrows():
        country = item['tSOCountry']

        filtered = df[df['tSOCountry'] == country]

        operatorKey = filtered.loc[:,'operatorKey'].drop_duplicates()
        #print(operatorKey)
        operatorLabel = filtered.loc[:,'operatorLabel'].drop_duplicates()

        if country is None:
            country = 'misc'

        print(f"{country}   =   {list(operatorKey)},  {list(operatorLabel)} ,")


client = EntsogPandasClient()

start = pd.Timestamp(2021, 1, 1)
end = pd.Timestamp(2021,1, 6)
country_code = 'DE'

tik = time.time()
data = client.query_operational_data_all(
    start = start,
    end = end,
    verbose = False,
    indicators= ['physical_flow', 'renomination']
)


tok = time.time()
print(data)
print(data.columns)
print(f'All Operational took: {(tok-tik)/60} minutes')


tik = time.time()
data = client.query_operational_data(
    start = start,
    end = end,
    verbose = False,
    country_code=country_code,
    indicators= ['physical_flow', 'renomination']
)


tok = time.time()
print(data)
print(data.columns)
print(f'{country_code} took: {(tok-tik)/60} minutes')