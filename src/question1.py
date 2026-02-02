from .utils import read_datafile, csv_read_datafile
import pandas as pd


def pandas_solution() -> pd.DataFrame:
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
    return users_usage


def csv_solution() -> None:
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


def main() -> None:
    users_usage = pandas_solution()
    top_user = users_usage["username"].loc[0]
    print(f"Pandas method: User with most data used: {top_user}")
    top_user_name = csv_solution()
    print(f"csv method: user with most data used: {top_user_name}")


if __name__ == "__main__":
    main()
