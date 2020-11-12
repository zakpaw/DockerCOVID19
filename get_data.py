import pandas as pd
from covid import Covid
from decimal import Decimal
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


covid = Covid()
data = json.dumps(covid.get_data(), cls=DecimalEncoder)
df = pd.read_json(data, convert_dates=['last_update'])
print(df.head())
