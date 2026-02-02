from .utils import read_datafile, csv_read_datafile
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def pandas_solution() -> str:
    usage = read_datafile("usage")
    users = read_datafile("users")
    df = pd.merge(left=users, right=usage, on="user_id", how="left")
    filter_date = datetime.now() - relativedelta(months=36)
    df["date_uploaded"] = pd.to_datetime(df["date_uploaded"])
    last_3_years = df[df["date_uploaded"] >= filter_date]
    last_3_years = (
        df.groupby(by="dept")
        .agg("count")
        .sort_values("filename")
        .reset_index(drop=False)
    )
    dept = last_3_years["dept"].loc[0]
    return dept


def csv_solution() -> str:
    usage = csv_read_datafile("usage")[1:]
    users = csv_read_datafile("users")[1:]
    results = {}
    for x in usage:
        user = x[0]
        dept = next(y[-1] for y in users if x[0] == user)
        if dept in results.keys():
            results[dept] += 1
        else:
            results[dept] = 1
    return next(x for x, y in results.items() if y == max(results.values()))


def main() -> None:
    pd_top_dept = pandas_solution()
    print(f"Department with most files in the last 3 years: {pd_top_dept}")
    csv_top_dept = csv_solution()
    print(f"Department with most files in the last 3 years: {csv_top_dept}")


if __name__ == "__main__":
    main()
