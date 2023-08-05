# Hepsiburada Data Science Utilities

This module includes utilities for Hepsiburada Data Science Team.

Library is available via PyPi. 
Library can be downloaded using pip as follows: `pip install heps-ds-utils`
Existing library can be upgraded using pip as follows: `pip install heps-ds-utils --upgrade`

***
## Available Modules

1. Hive Operations

```python
import os
from heps_ds_utils import HiveOperations

# A connection is needed to be generated in a specific runtime.
# There are 3 ways to set credentials for connection.

# 1) Instance try to set default credentials from Environment Variables.
hive_ds = HiveOperations()
hive_ds.connect_to_hive()

# 2) One can pass credentials to instance initiation to override default.
hive_ds = HiveOperations(HIVE_HOST="XXX", HIVE_PORT="YYY", HIVE_USER="ZZZ", HIVE_PASS="WWW", HADOOP_EDGE_HOST="QQQ")
hive_ds.connect_to_hive()

# 3) One can change any of the credentials after initiation using appropriate attribute.
hive_ds = HiveOperations()
hive_ds.hive_username = 'XXX'
hive_ds.connect_to_hive()

# Execute an SQL query to retrieve data.
# Currently Implemented Types: DataFrame, Numpy Array, Dictionary, List.
SQL_QUERY = "SELECT * FROM {db}.{table}"
data, columns = hive_ds.execute_query(SQL_QUERY, return_type="dataframe", return_columns=False)

# Execute an SQL query to create and insert data into table.
SQL_QUERY = "INSERT INTO .."
hive_ds.create_insert_table(SQL_QUERY)

# Send Files to Hive and Create a Table with the Data.
# Currently DataFrame or Numpy Array can be sent to Hive.
# While sending Numpy Array columns have to be provided.
SQL_QUERY = "INSERT INTO .."
hive_ds.send_files_to_hive("{db}.{table}", data, columns=None)

# Close the connection at the end of the runtime.

hive_ds.disconnect_from_hive()

```

2. BigQuery Operations