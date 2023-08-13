import pandas as pd
import matplotlib.pyplot as plt

from propertyUtils.database import DatabaseMongo
from services.etl.etl_data_gov_sg import etl_data_gov_sg


def add_leading_zero(age_range: str):
    if "+" not in age_range:
        start_age: int = int(age_range.split("-")[0])
        if start_age < 10:
            return f"0{age_range}"
    return age_range


def pre_step_000_load_from_dataset_to_mongoDB() -> None:
    # Load data into mongodb
    etl = etl_data_gov_sg()
    etl.extract(source="dataset")
    etl.load()


def step_1_setup_mongo_db_instance(environment_name="DEV") -> DatabaseMongo:
    return DatabaseMongo(environment_name)


def step_2_setup_pie_chart_for_number_of_covid_19_deaths_by_month(db: pd, db_name: str) -> None:
    df = db.read_all_records(database_name=db_name,
                             collection_name="number-of-covid-19-deaths-by-month.csv")
    death_by_age_groups = df.groupby('age_groups').agg(age_group=('count', sum))
    pie_chart = death_by_age_groups.plot(kind='pie',
                                         y='age_group',
                                         autopct="%.1f%%",
                                         colormap='Wistia')
    pie_chart.set_title('Number of Covid Death by age group')
    plt.show()


def step_3_setup_scatter_plot_to_find_out_why_so_many_deaths_are_from_senior(db: pd, db_name: str) -> None:
    """
    note : Could be due to high number of counts of seniors who are hospitalized and in icu
    :param db:
    :param db_name:
    :return:
    """
    df = db.read_all_records(database_name=db_name,
                             collection_name="average-daily-hospitalised-icu-cases-by-epi-week.csv")
    df.boxplot(by="age_groups",
               column=["count"])
    plt.xticks(rotation=45)
    plt.show()


def step_4_get_vaccination_status_by_age_group(db: pd, db_name: str) -> None:
    """
    note : Definition of minimum vaccine recommendation = 3 Doses
    :param db:
    :param db_name:
    :return:
    """
    df_2 = db.read_all_records(database_name=database_name,
                               collection_name="vaccination-status-by-age-group.csv")
    df_2['age'] = df_2['age'].apply(add_leading_zero)
    df_2.sort_values(by=['age']).plot(x="age",
                                      y=["no_minimum_protection", "minimum_protection"],
                                      kind="bar")
    plt.xticks(rotation=45)
    plt.show()


def step_5_setup_line_graph_for_progress_of_vaccination(db: pd, db_name: str) -> None:
    """
        Note : Completed primary series = (3 x Pfizer/Novavex); (4 x Sinovac)
    """
    df_3 = db.read_all_records(database_name=database_name,
                               collection_name="progress-of-covid-19-vaccination.csv")
    df_3.sort_values(by=["vacc_date"]).plot(x="vacc_date",
                                            y=["received_one_dose_pcttakeup",
                                               "full_regimen_pcttakeup",
                                               "minimum_protection_pcttakeup"],
                                            kind="line")
    plt.xticks(rotation=45)
    plt.show()


if __name__ == '__main__':
    database_name: str = "Covid_19_Weekly_Stats"
    db: DatabaseMongo = step_1_setup_mongo_db_instance("DEV")
    step_2_setup_pie_chart_for_number_of_covid_19_deaths_by_month(db=db,
                                                                  db_name=database_name)
    step_3_setup_scatter_plot_to_find_out_why_so_many_deaths_are_from_senior(db=db,
                                                                             db_name=database_name)
    step_4_get_vaccination_status_by_age_group(db=db,
                                               db_name=database_name)

    step_5_setup_line_graph_for_progress_of_vaccination(db=db,
                                                        db_name=database_name)
