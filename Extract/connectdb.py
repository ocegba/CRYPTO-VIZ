import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "DataViz"
url = "http://influxdb:8086"
bucket="DataViz"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


# Créez une instance du client InfluxDB
client = InfluxDBClient(url=url, token=token)

# Créez un objet WriteApi pour écrire des données
write_api = client.write_api(write_options=SYNCHRONOUS)

# Créez une table (measurement) appelée "exemple"
measurement = "exemple"

# Créez un point de données
point = Point(measurement).tag("type", "test").field("valeur", 42)

# Écrivez le point de données dans la base de données
write_api.write(bucket=bucket, org=org, record=point)

# Exemple de requête pour extraire toutes les données de la table "exemple"
query = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "{measurement}")'
result = client.query_api().query(query=query, org=org)
for table in result:
    for record in table.records:
        print(record.values)
