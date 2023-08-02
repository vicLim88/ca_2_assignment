from services.etl.etl_data_gov_sg import etl_data_gov_sg
from pymongo.mongo_client import MongoClient

import os

def test():
    uri = "mongodb+srv://viclim:Tt1o2eSfkIEDUmRt@cluster0.jowdxmj.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        print(client.list_database_names())
    except Exception as e:
        print(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # test()
    # Load data into mongodb
    etl = etl_data_gov_sg()
    etl.extract(source="dataset")
    etl.load()
