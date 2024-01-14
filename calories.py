#!/usr/bin/env python3


import pandas as pd
import numpy as np


def parse_foods():
    dct = {}
    with open(
        "/Users/kyle/Documents/calorie-count/Calories Per Gram-Table 1.csv"
    ) as f:
        f.readline()  # throw away header
        for line in f:
            line = line.strip()
            split = line.split(",")
            dct[split[0]] = float(split[1])
    return dct


def get_journal():
    foods = parse_foods()
    journal = pd.read_csv(
        "/Users/kyle/Documents/calorie-count/Calorie Tracking-Table 1.csv"
    )

    def calc_calories(row):
        if row.Food not in foods:
            raise Exception(
                f"food: '{row.Food}' does not have an entry in the Foods table"
            )
        return row["Quantity (g)"] * foods[row.Food]

    journal["Subtotals"] = journal.apply(calc_calories, axis=1)
    return journal


def calc_rolling_avg(daily_calories, days):
    rolling_avg_values = daily_calories["Daily Calories"].iloc[1 : 1 + days]
    days = min(len(rolling_avg_values), days)
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
    daily_calories = daily_calories.iloc[::-1].reset_index(drop=True)
    return daily_calories


def main():
    journal = get_journal()
    daily = get_daily(journal)
    calc_rolling_avg(daily, 7)
    calc_rolling_avg(daily, 10)
    # calc_rolling_avg(daily, 30)
    # calc_rolling_avg(daily, 365)
    # calc_rolling_avg(daily, 2 * 365)
    print(daily.to_string(index=False))


if __name__ == "__main__":
    main()
