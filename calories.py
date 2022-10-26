#!/usr/bin/env python3


import pandas as pd


def parse_foods():
    dct = {}
    with open("Calories - Foods.csv") as f:
        f.readline()  # throw away header
        for line in f:
            line = line.strip()
            split = line.split(",")
            dct[split[0]] = float(split[1])
    return dct


def main():
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
    daily_calories = journal.groupby("Date", as_index=False)["Subtotals"].sum()
    daily_calories.rename(
        columns={"Subtotals": "Daily Calories"}, inplace=True
    )
    return daily_calories


if __name__ == "__main__":
    print(main())
