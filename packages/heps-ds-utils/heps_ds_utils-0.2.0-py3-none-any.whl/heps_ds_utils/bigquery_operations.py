""" This Module is created to enable Hepsiburada Data Science to communicate with BigQuery. """

import os
import time

from colorama import Fore, init ##Style
from google.cloud import bigquery
from google.oauth2 import service_account
# import pandas_gbq

init(autoreset=True)

class BigQueryOperations:
    """ This class is created to enable Hepsiburada Data Science to communicate with BigQuery """
    _implemented_returns = ['dataframe', 'numpy', 'list', 'dict']


    def __init__(self, **kwargs) -> None:
        self.bqclient = None
        self.credentials = None
        self.gcp_key = kwargs.get('gcp_key_path')

    def __repr__(self) -> str:
        if self.bqclient is None:
            return f"{self.__class__.__name__}()"
        return f"{self.__class__.__name__}(Project ID: {self.credentials.project_id}, " \
                f"Service Account: {self.credentials._service_account_email.split('@')[0]})"

    def connect_to_bq(self):
        """This function is to connect to BQ using credentials. """
        try:
            # key_path = os.environ.get('SERVICE_ACCOUNT_KEY_PATH')
            self.credentials = service_account.Credentials.from_service_account_file(
                    self.gcp_key, scopes=["https://www.googleapis.com/auth/cloud-platform"],)

            self.bqclient = bigquery.Client(credentials=self.credentials,
                                        project=self.credentials.project_id,)

            # pandas_gbq.Context.credentials = self.credentials
            # pandas_gbq.Context.project = self.credentials.project_id

        except TypeError:
            raise TypeError(Fore.RED + "Failed to connect to BigQuery: "
                            "VPN is possibly not connected") from None
        except FileNotFoundError:
            raise FileNotFoundError(Fore.RED + "Failed to connect to BigQuery: "
                                    "Service Account Key File is not found") from None

        print(Fore.GREEN + "Connection Succeded !!")

    def get_bq_client(self):
        """This function is to get BQ client. """
        return self.bqclient

    def get_bq_table(self, table_name):
        """This function is to get BQ table. """
        return self.bqclient.get_table(table_name)

    def execute_query(self, query_string, return_type='dataframe', **kwargs):
        """This function is to query BQ. """
        if return_type not in BigQueryOperations._implemented_returns:
            raise NotImplementedError(Fore.RED + f'Return type {return_type} not implemented !!')

        if self.bqclient is None:
            raise ValueError(Fore.RED + "BQ client is not connected")

        execution_start = time.time()
        query_result = self.bqclient.query(query_string, **kwargs).result()
        execution_duration = time.time() - execution_start
        print(Fore.YELLOW + f'Query executed in {execution_duration:.2f} seconds !')

        if return_type == 'dataframe':
            return query_result.to_dataframe(progress_bar_type='tqdm')

        return self.bqclient.query(query_string)

    def create_dataset(self, dataset_name):
        """This function is to create dataset. """
        self.bqclient.create_dataset(dataset_name)
        pass

    def load_data_to_table(self, table_name, data_frame, **kwargs):
        """This function is to load data to table. """
        self.bqclient.load_table_from_dataframe(data_frame, table_name, **kwargs)

    def create_table_with_data(self):
        """This function is to create table with data. """
        pass

    @property
    def gcp_key(self):
        """This function is to get GCP key. """
        return self._gcp_key

    @gcp_key.setter
    def gcp_key(self, provided_gcp_key):
        """This function is to set GCP key. """
        if provided_gcp_key is not None:
            self._gcp_key = str(provided_gcp_key)
        elif os.environ.get("SERVICE_ACCOUNT_KEY_PATH"):
            self._gcp_key = os.environ.get("SERVICE_ACCOUNT_KEY_PATH")
        else:
            self._gcp_key = None
            print(Fore.RED + "Warning!! GCP Key Path for Service Account is not specified")
