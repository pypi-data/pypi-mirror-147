# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heps_ds_utils']

package_data = \
{'': ['*']}

install_requires = \
['PyHive>=0.6.5,<0.7.0',
 'colorama>=0.4.4,<0.5.0',
 'google-cloud-bigquery[bqstorage,pandas]>=3.0.1,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'paramiko>=2.10.3,<3.0.0',
 'scp>=0.14.4,<0.15.0',
 'thrift-sasl>=0.4.3,<0.5.0',
 'thrift>=0.15.0,<0.16.0',
 'tqdm>=4.64.0,<5.0.0']

extras_require = \
{':sys_platform == "linux" or sys_platform == "darwin"': ['sasl>=0.3.1,<0.4.0']}

setup_kwargs = {
    'name': 'heps-ds-utils',
    'version': '0.2.1a0',
    'description': 'A Module to enable Hepsiburada Data Science Team to utilize different tools.',
    'long_description': '# Hepsiburada Data Science Utilities\n\nThis module includes utilities for Hepsiburada Data Science Team.\n\nLibrary is available via PyPi. \nLibrary can be downloaded using pip as follows: `pip install heps-ds-utils`\nExisting library can be upgraded using pip as follows: `pip install heps-ds-utils --upgrade`\n\n***\n## Available Modules\n\n1. Hive Operations\n\n```python\nimport os\nfrom heps_ds_utils import HiveOperations\n\n# A connection is needed to be generated in a specific runtime.\n# There are 3 ways to set credentials for connection.\n\n# 1) Instance try to set default credentials from Environment Variables.\nhive_ds = HiveOperations()\nhive_ds.connect_to_hive()\n\n# 2) One can pass credentials to instance initiation to override default.\nhive_ds = HiveOperations(HIVE_HOST="XXX", HIVE_PORT="YYY", HIVE_USER="ZZZ", HIVE_PASS="WWW", HADOOP_EDGE_HOST="QQQ")\nhive_ds.connect_to_hive()\n\n# 3) One can change any of the credentials after initiation using appropriate attribute.\nhive_ds = HiveOperations()\nhive_ds.hive_username = \'XXX\'\nhive_ds.connect_to_hive()\n\n#\xc2\xa0Execute an SQL query to retrieve data.\n# Currently Implemented Types: DataFrame, Numpy Array, Dictionary, List.\nSQL_QUERY = "SELECT * FROM {db}.{table}"\ndata, columns = hive_ds.execute_query(SQL_QUERY, return_type="dataframe", return_columns=False)\n\n# Execute an SQL query to create and insert data into table.\nSQL_QUERY = "INSERT INTO .."\nhive_ds.create_insert_table(SQL_QUERY)\n\n# Send Files to Hive and Create a Table with the Data.\n# Currently DataFrame or Numpy Array can be sent to Hive.\n# While sending Numpy Array columns have to be provided.\nSQL_QUERY = "INSERT INTO .."\nhive_ds.send_files_to_hive("{db}.{table}", data, columns=None)\n\n# Close the connection at the end of the runtime.\n\nhive_ds.disconnect_from_hive()\n\n```\n\n2. BigQuery Operations',
    'author': 'FarukBuldur',
    'author_email': 'faruk.buldur@hepsiburada.com',
    'maintainer': 'F\xc4\xb1rat\xc3\x96nc\xc3\xbc',
    'maintainer_email': 'firat.oncu@hepsiburada.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
