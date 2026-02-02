from .utils import read_datafile, csv_read_datafile
import pandas as pd


def pandas_solution() -> pd.DataFrame:
    users = read_datafile("users")
    usage = read_datafile("usage")
    costs = read_datafile("costs")
    df = pd.merge(left=usage, right=costs, on="filetype", how="left")
    df["file_cost"] = df["filesize"].astype(int) * df["cost_per_unit"].astype(int)
    df = (
        df.groupby(by="user_id")
        .agg("sum")
        .sort_values("file_cost", ascending=False)
        .reset_index(drop=False)
    )
    users_df = pd.merge(left=df, right=users, on="user_id", how="left")
    results = users_df[["username", "file_cost"]]
    return results


def csv_solution() -> list[tuple]:
    users = csv_read_datafile("users")[1:]
    usage = csv_read_datafile("usage")[1:]
    costs = csv_read_datafile("costs")[1:]
    user_spends = {}
    for x in usage:
        user_id = x[0]
        username = next(y[1] for y in users if y[0] == user_id)
        filetype = x[2]
        cost_per_unit = next(y[1] for y in costs if y[0] == filetype)
        filesize = x[-1]
        cost_of_file = int(filesize) * int(cost_per_unit)
        if username in user_spends.keys():
            user_spends[username] += cost_of_file
        else:
            user_spends[username] = cost_of_file
    results = [(k, v) for k, v in user_spends.items()]
    results.sort(key=lambda x: -x[1])
    return results


def main() -> None:
    pandas_result = pandas_solution()
    csv_result = csv_solution()
    print(f"Users with highest spend:\n {pandas_result}")
    print(f"User with highest spend: {csv_result}")


if __name__ == "__main__":
    main()
