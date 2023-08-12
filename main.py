import seaborn as sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from propertyUtils.database import DatabaseMongo
from services.etl.etl_data_gov_sg import etl_data_gov_sg


def add_leading_zero(age_range: str):
    if "+" not in age_range:
        start_age: int = int(age_range.split("-")[0])
        if start_age < 10:
            return f"0{age_range}"
    return age_range


if __name__ == '__main__':
    # ToDo : Put on different Runner
    # Load data into mongodb
    # Pre_Step_Load_Data_From_Local_Datasets_Into_MongoDB()
    # etl = etl_data_gov_sg()
    # etl.extract(source="dataset")
    # etl.load()

    # Step_1_define_all_variables
    database_name: str = "Covid_19_Weekly_Stats"
    db: DatabaseMongo = DatabaseMongo(environment_name="DEV")

    # # Step_2_setup_pie_chart_for_number_of_covid_19_deaths_by_month()
    # df = db.read_all_records(database_name=database_name,
    #                          collection_name="number-of-covid-19-deaths-by-month.csv")
    # death_by_age_groups = df.groupby('age_groups').agg(age_group=('count', sum))
    # pie_chart = death_by_age_groups.plot(kind='pie',
    #                                      y='age_group',
    #                                      autopct="%.1f%%",
    #                                      colormap='Wistia')
    # pie_chart.set_title('Number of Covid Death by age group')
    # plt.show()

    # Step_3_get_vaccination_status_by_age_group()
    # Definition of minimum vaccine recommendation = 3 Doses
    df_2 = db.read_all_records(database_name=database_name,
                               collection_name="vaccination-status-by-age-group.csv")
    df_2['age'] = df_2['age'].apply(add_leading_zero)
    df_2.sort_values(by=['age']).plot(x="age",
                                      y=["no_minimum_protection", "minimum_protection"],
                                      kind="bar")
    plt.xticks(rotation=45)
    plt.show()
