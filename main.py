from services.etl.etl_data_gov_sg import etl_data_gov_sg

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Load data into mongodb
    etl = etl_data_gov_sg()
    etl.extract()
    etl.load()
