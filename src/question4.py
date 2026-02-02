from .utils import read_datafile, csv_read_datafile
import pandas as pd
import duckdb


def pandas_solution() -> str:
    usage = read_datafile("usage")
    users = read_datafile("users")
    df = pd.merge(left=users, right=usage, on="user_id", how="left")
    df = df[df["filetype"].isin([".xlsx", ".csv"])]
    df = (
        df.groupby(by="dept")
        .agg("count")
        .sort_values(by="filetype", ascending=False)
        .reset_index(drop=False)
    )
    top_dept = df["dept"].loc[0]
    return top_dept


def csv_solution() -> str:
    usage = csv_read_datafile("usage")[1:]
    users = csv_read_datafile("users")[1:]
    user_depts = {x[0]: x[-1] for x in users}
    dept_file_counts = {}
    for x in usage:
        user_id = x[0]
        dept = user_depts[user_id]
        filetype = x[2]
        if filetype in [".xlsx", ".csv"]:
            if dept in dept_file_counts.keys():
                dept_file_counts[dept] += 1
            else:
                dept_file_counts[dept] = 1
    top_dept = next(
        x for x, y in dept_file_counts.items() if y == max(dept_file_counts.values())
    )
    return top_dept


def duckdb_solution() -> str:
    usage = read_datafile("usage")
    users = read_datafile("users")
    df = duckdb.query(
        """
        select users.dept, count(*) as files
        from usage
        left join users on usage.user_id = users.user_id
        where usage.filetype in ('.xlsx', '.csv')
        group by users.dept
        order by count(*) desc
        """
    ).to_df()
    return df["dept"].loc[0]


def main() -> None:
    pandas_result = pandas_solution()
    csv_result = csv_solution()
    duckdb_result = duckdb_solution()
    print(f"Department with most data files: {pandas_result}")
    print(f"Department with most data files: {csv_result}")
    print(f"Department with most data files: {duckdb_result}")


if __name__ == "__main__":
    main()
