import multiprocessing
import pandas as pd
import numpy as np
import pickle
import os


def isSyncingNow():
    with open("covid19Data/isSyncingNow", "rb") as f:
        status = pickle.load(f)
        return status


def writeSyncing(isTrue):
    with open("covid19Data/isSyncingNow", "wb") as f:
        pickle.dump(isTrue, f)


def sync(url="https://covid.ourworldindata.org/data/owid-covid-data.csv", dataToRemove=None):
    try:
        os.remove('D:\python\PycharmProjects\DataScienceAndMath\covid19Data\CovidData.csv')
    except FileNotFoundError:
        pass
    writeSyncing(True)
    if dataToRemove is None:
        dataToRemove = [
            "new_cases_smoothed",
            "new_deaths_smoothed",
            "new_cases_smoothed_per_million",
            "new_cases_per_million",
            "new_deaths_per_million",
            "new_tests_per_thousand",
            "new_deaths_smoothed_per_million",
            "reproduction_rate",
            "new_tests_smoothed",
            "new_tests_smoothed_per_thousand",
            "tests_units",
            "aged_65_older",
            "aged_70_older",
            "weekly_icu_admissions",
            "weekly_icu_admissions_per_million",
            "weekly_hosp_admissions",
            "weekly_hosp_admissions_per_million",
            "icu_patients_per_million",
            "hosp_patients_per_million",
            "continent"
        ]
    covid19 = pd.read_csv(url, sep=",", parse_dates=True, engine="c")
    covid19 = covid19.drop(columns=dataToRemove)
    column_values = covid19[["location"]].values.ravel()
    countries = pd.unique(column_values)
    statistics = [i for i in covid19.columns]
    statistics.remove("iso_code")
    statistics.remove("location")
    with open("covid19Data/Variables","wb") as f:
        pickle.dump(statistics,f)
    with open("covid19Data/Countries", "wb") as f:
        pickle.dump(countries,f)
    dataFrames = []
    for i in countries:
        # data cleaning
        Country = covid19[covid19["location"] == i].copy()
        # cases
        Country["total_cases"] = Country["total_cases"].fillna(method="ffill").fillna(0)
        Country["new_cases"] = Country["new_cases"].fillna(0)
        Country["total_cases_per_million"] = \
            Country["total_cases_per_million"].fillna(
                round(Country["total_cases"] / Country["population"] * 1000000, 3))
        # deaths
        Country["total_deaths"] = Country["total_deaths"].fillna(method="ffill").fillna(0)
        Country["new_deaths"] = Country["new_deaths"].fillna(0)
        Country["total_deaths_per_million"] = \
            Country["total_deaths_per_million"].fillna(
                round(Country["total_deaths"] / Country["population"] * 1000000, 3))
        # tests
        Country["total_tests"] = Country["total_tests"].fillna(method="ffill").fillna(0)
        Country["total_tests_per_thousand"] = \
            Country["total_tests_per_thousand"].fillna(round(Country["total_tests"] / Country["population"] * 1000, 3))
        Country["tests_per_case"] = \
            Country["tests_per_case"].fillna(round(Country["total_tests"] / Country["total_cases"], 3)).replace(np.inf,
                                                                                                                0).fillna(
                0)
        Country["positive_rate"] = Country["tests_per_case"].fillna(0)
        # hospital
        Country["icu_patients"] = Country["icu_patients"].fillna(method="ffill").fillna(0)
        Country["hosp_patients"] = Country["hosp_patients"].fillna(method="ffill").fillna(0)
        Country["new_tests"] = Country["new_tests"].fillna(0)
        # miscellaneous
        Country["extreme_poverty"] = Country["extreme_poverty"].fillna(0)
        Country["stringency_index"] = Country["stringency_index"].fillna(0)
        dataFrames.append(Country)
    dataFrames = pd.concat(dataFrames)
    dataFrames.date = pd.to_datetime(dataFrames.date)
    dataFrames.to_csv(r'D:\python\PycharmProjects\DataScienceAndMath\covid19Data\CovidData.csv', index=False,
                      header=True)
    writeSyncing(False)
    return


if __name__ == '__main__':
    sync()
    # print(covid19[covid19["location"] == "Serbia"][["date","total_cases","new_cases"]])
    # print(covid19['location'].unique(),len(covid19['location'].unique()))
