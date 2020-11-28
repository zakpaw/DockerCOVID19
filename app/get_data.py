from decimal import Decimal
from covid import Covid
import country_converter as coco
import pandas as pd
import sqlalchemy
import json


# ==== Extract & Transform ====
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


# todays covid data from 191 countries
data = json.dumps(Covid(source="worldometers").get_data(), cls=DecimalEncoder)
df = pd.read_json(data)

# add country code based on the 'country' column
fun = lambda c: coco.convert(names=c, to='ISO2') if len(c) > 2 else c
converted = df.country.apply(fun)
df.insert(0, 'country_code', converted)

# delete rows where code has not been set successfully or country name is '0'
df = df[(df.country_code != 'not found') & (df.country != '0')]
df.total_deaths_per_million = df.total_deaths_per_million.astype(int)


# ==== Load ====
def connect():
    URI = 'mysql+pymysql://root:passwel@db:3306/covid'
    try:
        return sqlalchemy.create_engine(URI)
    except sqlalchemy.exc.OperationalError:
        print('Cant connect to MySQL server')
        quit()


engine = connect()

table_name = 'covid19'

df.to_sql(
    table_name,
    engine,
    if_exists='replace',
    index=False
)

# show first 5 rows queried form covid19 table to verify successful insertion
print(pd.read_sql_query('select * from covid19 limit 5', engine).head())
