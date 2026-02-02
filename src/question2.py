from .utils import read_datafile, csv_read_datafile
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import duckdb


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
        .sort_values("filename", ascending=False)
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
        dept = next(y[-1] for y in users if y[0] == user)
        filter_date = datetime.now() - relativedelta(months=36)
        date_uploaded_parts = x[3].split("-")
        date_uploaded = datetime(
            int(date_uploaded_parts[0]),
            int(date_uploaded_parts[1]),
            int(date_uploaded_parts[2]),
        )
        if date_uploaded >= filter_date:
            if dept in results.keys():
                results[dept] += 1
            else:
                results[dept] = 1
    return next(x for x, y in results.items() if y == max(results.values()))


def duckdb_solution() -> str:
    usage = read_datafile("usage")
    users = read_datafile("users")
    users_usage = duckdb.query(
        """
        select users.dept, count(filename) as files
        from users
        left join usage on users.user_id = usage.user_id
        where cast(usage.date_uploaded as date) >= current_date - interval 36 month
        group by users.dept
        order by count(filename) desc
        """
    ).to_df()
    return users_usage["dept"].loc[0]


def main() -> None:
    pd_top_dept = pandas_solution()
    csv_top_dept = csv_solution()
    duckdb_top_dept = duckdb_solution()
    print(f"Department with most files in the last 3 years: {pd_top_dept}")
    print(f"Department with most files in the last 3 years: {csv_top_dept}")
    print(f"Department with most files in the last 3 years: {duckdb_top_dept}")


if __name__ == "__main__":
    main()
