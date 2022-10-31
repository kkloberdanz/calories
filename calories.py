#!/usr/bin/env python3


import pandas as pd
import numpy as np


def parse_foods():
    dct = {}
    with open("Calories - Foods.csv") as f:
        f.readline()  # throw away header
        for line in f:
            line = line.strip()
            split = line.split(",")
            dct[split[0]] = float(split[1])
    return dct


def get_journal():
    foods = parse_foods()
    journal = pd.read_csv("Calories - Journal.csv")

    def calc_calories(row):
        if row.Food not in foods:
            raise Exception(
                f"food: '{row.Food}' does not have an entry in the Foods table"
            )
        return row["Number of Units"] * foods[row.Food]

    journal["Subtotals"] = journal.apply(
        lambda row: calc_calories(row), axis=1
    )
    return journal


def calc_rolling_avg(daily_calories, days):
    rolling_avg_values = daily_calories["Daily Calories"][:days]
    rolling_avg = round(rolling_avg_values.sum() / len(rolling_avg_values))
    print(f"{days} day rolling average = {rolling_avg}")


def get_daily(journal):
    daily_calories = (
        journal.groupby("Date", as_index=False)["Subtotals"].sum().round()
    )
    daily_calories.rename(
        columns={"Subtotals": "Daily Calories"}, inplace=True
    )
    daily_calories["Daily Calories"] = (
        daily_calories["Daily Calories"].round().astype(np.int64)
    )
    calc_rolling_avg(daily_calories, 5)
    calc_rolling_avg(daily_calories, 30)
    calc_rolling_avg(daily_calories, 365)
    calc_rolling_avg(daily_calories, 2 * 365)
    return daily_calories


def main():
    journal = get_journal()
    daily = get_daily(journal)
    return daily


if __name__ == "__main__":
    print(main())
