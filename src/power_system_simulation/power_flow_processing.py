import json
import pprint
import warnings

with warnings.catch_warnings(action="ignore", category=DeprecationWarning):
    # suppress warning about pyarrow as future required dependency
    from pandas import DataFrame

from power_grid_model import PowerGridModel
from power_grid_model.utils import json_deserialize, json_serialize

with open("src\power_system_simulation\input_network_data.json") as fp:
    data = fp.read()

pprint.pprint(json.loads(data))

dataset = json_deserialize(data)

print("components:", dataset.keys())
im.show(DataFrame(dataset["node"]))