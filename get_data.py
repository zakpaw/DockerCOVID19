import pandas as pd
from covid import Covid
from decimal import Decimal
import sqlalchemy as sqla
import json


# Extract
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


data = json.dumps(Covid().get_data(), cls=DecimalEncoder)

df = pd.read_json(data, convert_dates=['last_update'])
print(df.head(), '\nlength:', len(df))

# Load
DB_LOC = 'mysql+pymysql://root:passwel@localhost/covid19docker'
engine = sqla.create_engine(DB_LOC)

table_name = 'covid19'

df.to_sql(
    table_name,
    engine,
    if_exists='replace',
    index=False
)

result = engine.execute('show tables;')
for _r in result:
    print(_r)
