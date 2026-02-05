from .utils import read_datafile, csv_read_datafile, timing
import pandas as pd
import duckdb


@timing
def pandas_solution() -> str:
    users = read_datafile("users")
    usage = read_datafile("usage")
    df = pd.merge(left=users, right=usage, how="left", on="user_id")
    users_usage = (
        df[["username", "filesize"]]
        .groupby(
            by="username",
        )
        .agg("sum")
        .sort_values(by="filesize", ascending=False)
        .reset_index(drop=False)
    )
    top_user = users_usage["username"].loc[0]
    return top_user


@timing
def csv_solution() -> str:
    users = csv_read_datafile("users")[1:]
    usage = csv_read_datafile("usage")[1:]
    user_data = {x[0]: x[1] for x in users}
    user_usage = {}
    for x in usage:
        if x[0] in user_usage.keys():
            user_usage[x[0]] += int(x[-1])
        else:
            user_usage[x[0]] = int(x[-1])
    max_usage = max(user_usage.values())
    top_user_id = next(x for x, y in user_usage.items() if y == max_usage)
    return next(y for x, y in user_data.items() if x == top_user_id)


@timing
def duckdb_solution() -> str:
    users = read_datafile("users")
    usage = read_datafile("usage")
    users_usage = duckdb.query(
        """
        select users.username, sum(usage.filesize) as filesize
        from users
        left join usage on users.user_id = usage.user_id
        group by users.username
        order by sum(usage.filesize) desc
        """
    ).to_df()
    return users_usage["username"].loc[0]


def main() -> None:
    pandas_top_user = pandas_solution()
    csv_top_user = csv_solution()
    duckdb_top_user = duckdb_solution()
    print(f"Pandas method: User with most data used: {pandas_top_user}")
    print(f"csv method: user with most data used: {csv_top_user}")
    print(f"duckdb method: user with most data used: {duckdb_top_user}")


if __name__ == "__main__":
    main()
