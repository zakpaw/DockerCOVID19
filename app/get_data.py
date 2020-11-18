from decimal import Decimal
from covid import Covid
import pandas as pd
import sqlalchemy
import pymysql
import json


# ==== Extract & Transform ====
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


# todays covid data from 191 countries
data = json.dumps(Covid().get_data(), cls=DecimalEncoder)
df = pd.read_json(data, convert_dates=['last_update'])


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
new = True

try:
    newest_date = engine.execute('select max(last_update) from covid19;')
    if newest_date.first()[0] == df.last_update.max().to_pydatetime():
        new = False
except sqlalchemy.exc.OperationalError:
    print("'covid19' table does not exist!")
if new:
    df.to_sql(
        table_name,
        engine,
        if_exists='replace',
        index=False
    )

print(pd.read_sql_query('select * from covid19 limit1', engine).head(5))
