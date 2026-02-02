from .utils import read_datafile, csv_read_datafile
import pandas as pd
import duckdb


def pandas_join_datasets() -> pd.DataFrame:
    users = read_datafile("users")
    usage = read_datafile("usage")
    costs = read_datafile("costs")
    usage_costs = pd.merge(left=usage, right=costs, on="filetype", how="left")
    usage_costs["file_cost"] = usage_costs["filesize"] * usage_costs["cost_per_unit"]
    usage_costs_users = pd.merge(
        left=usage_costs, right=users, on="user_id", how="left"
    )
    usage_costs_users = (
        usage_costs_users.groupby("dept").agg("sum").reset_index(drop=False)
    )
    return usage_costs_users


def pandas_calculate_spends() -> dict[str, str]:
    usage_costs_users = pandas_join_datasets()
    budgets = read_datafile("budgets")
    dept_spends = {
        k: v for k, v in zip(usage_costs_users["dept"], usage_costs_users["file_cost"])
    }
    dept_results = {}
    budgets_dict = {k: v for k, v in zip(budgets["dept"], budgets["budget"])}
    for k, v in dept_spends.items():
        if v > budgets_dict[k]:
            dept_results[k] = "Over"
        elif v < budgets_dict[k]:
            dept_results[k] = "Under"
        else:
            dept_results[k] = "Equal"
    return dept_results


def csv_solution() -> dict[str, str]:
    users = csv_read_datafile("users")[1:]
    usage = csv_read_datafile("usage")[1:]
    budgets = csv_read_datafile("budgets")[1:]
    costs = csv_read_datafile("costs")[1:]
    costs_dict = {x[0]: x[1] for x in costs}
    budgets_dict = {x[0]: int(x[1]) for x in budgets}
    depts_spend = {}
    for x in usage:
        user_id = x[0]
        dept = next(y[-1] for y in users if y[0] == user_id)
        filetype = x[2]
        filesize = x[-1]
        cost_per_unit = costs_dict[filetype]
        file_cost = int(filesize) * int(cost_per_unit)
        if dept in depts_spend.keys():
            depts_spend[dept] += file_cost
        else:
            depts_spend[dept] = file_cost
    dept_results = {}
    for k, v in depts_spend.items():
        if v > budgets_dict[k]:
            dept_results[k] = "Over"
        elif v < budgets_dict[k]:
            dept_results[k] = "Under"
        else:
            dept_results[k] = "Equal"
    return dept_results


def duckdb_solution() -> dict[str, str]:
    users = read_datafile("users")
    usage = read_datafile("usage")
    costs = read_datafile("costs")
    budgets = read_datafile("budgets")
    usage_costs = duckdb.query(
        """
        select users.dept
            ,case when sum(usage.filesize * costs.cost_per_unit) > budgets.budget then 'Over'
                when sum(usage.filesize * costs.cost_per_unit) < budgets.budget then 'Under'
                else 'Equal' end as flag
        from usage
        left join costs on usage.filetype = costs.filetype
        left join users on usage.user_id = users.user_id
        left join budgets on users.dept = budgets.dept
        group by users.dept, budgets.budget
        """
    ).to_df()
    results = {k: v for k, v in zip(usage_costs["dept"], usage_costs["flag"])}
    return results


def main() -> None:
    pandas_results = pandas_calculate_spends()
    csv_results = csv_solution()
    duck_db_results = duckdb_solution()
    print(f"Pandas results: {pandas_results}")
    print(f"csv results: {csv_results}")
    print(f"duckdb results: {duck_db_results}")


if __name__ == "__main__":
    main()
