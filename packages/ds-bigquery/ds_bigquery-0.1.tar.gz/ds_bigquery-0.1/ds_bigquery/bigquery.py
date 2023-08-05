from google.api_core.exceptions import NotFound
from google.cloud import bigquery
import pandas, pandas_gbq, json, os


def Authenticate_BigQuery():
  service_account_info = os.environ.get('service_account_info', 'Specified environment variable is not set')
  return bigquery.Client.from_service_account_info(service_account_info)

def Upload_Dataframe(dataframe, project_id, table_id):
  dataframe.to_gbq(table_id, project_id, if_exists='replace')

def Append_Dataframe(dataframe, project_id, table_id):
  dataframe.to_gbq(table_id, project_id, if_exists='append')

def Download_As_Dataframe(bigquery_client, project_id, table_id, query_string):
  try:
    return bigquery_client.query(query_string).result().to_dataframe()
  except NotFound:
    return pandas.DataFrame()

if __name__ == '__main__':
    pass
