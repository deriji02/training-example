from .utils import read_datafile, csv_read_datafile
import pandas as pd


def pandas_solution() -> str:
    users = read_datafile("users")
    usage = read_datafile("usage")
    pdf_data = usage[usage["filetype"] == ".pdf"]
    user_totals = (
        pdf_data.groupby(by="user_id")
        .agg("sum")
        .sort_values(by="filesize", ascending=False)
        .reset_index(drop=False)
    )
    df = pd.merge(left=user_totals, right=users, on="user_id", how="left")
    top_user = df["username"].loc[0]
    return top_user


def csv_solution() -> str:
    users = csv_read_datafile("users")[1:]
    usage = csv_read_datafile("usage")[1:]
    usernames = {x[0]: x[1] for x in users}
    results = {}
    for x in usage:
        user_id = x[0]
        username = usernames[user_id]
        filetype = x[2]
        filesize = int(x[-1])
        if filetype == ".pdf":
            if username in results.keys():
                results[username] += filesize
            else:
                results[username] = filesize
    return next(x for x, y in results.items() if y == max(results.values()))


def main() -> None:
    pandas_result = pandas_solution()
    csv_result = csv_solution()
    print(f"User with most data stored as .pdf files: {pandas_result}")
    print(f"User with most data stored as .pdf files: {csv_result}")


if __name__ == "__main__":
    main()
