import csv
from pathlib import Path
from random import choice, randint
from datetime import date

USER_NAMES = [
    "Alice",
    "Layla",
    "Kassandra",
    "Amelia",
    "Sam",
    "Alistair",
    "Romesh",
    "Havi",
    "Kya",
    "Charlotte",
]
USERS = {k: v for k, v in zip(list(range(len(USER_NAMES))), USER_NAMES)}
DEPTS = ["IT", "Finance", "Sales"]


def write_users_data() -> None:
    filepath = Path(__file__).parent.parent / "data" / "users.csv"
    columns = ["user_id", "username", "dept"]
    with open(filepath, "w") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for k, v in USERS.items():
            user_dept = choice(DEPTS)
            writer.writerow([k, v, user_dept])


def write_usage_data() -> None:
    filepath = Path(__file__).parent.parent / "data" / "usage.csv"
    columns = ["user_id", "filename", "filetype", "date_uploaded", "filesize"]
    filetypes = [".csv", ".xlsx", ".jpeg", ".mp4", ".pdf"]
    with open(filepath, "w") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for _ in range(10000):
            user_id = randint(0, 9)
            filename = "example"
            filetype = choice(filetypes)
            date_uploaded = date(randint(2015, 2026), randint(1, 12), randint(1, 28))
            filesize = randint(100, 100000)
            row = [user_id, filename, filetype, date_uploaded, filesize]
            writer.writerow(row)


def write_budgets_data() -> None:
    filepath = Path(__file__).parent.parent / "data" / "budgets.csv"
    dept_budgets = {k: v for k, v in zip(DEPTS, [1000000000, 10000000, 50000000])}
    columns = ["dept", "budget"]
    with open(filepath, "w") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for k, v in dept_budgets.items():
            writer.writerow([k, v])


def write_costs_data() -> None:
    filepath = Path(__file__).parent.parent / "data" / "costs.csv"
    columns = ["filetype", "cost_per_unit"]
    filetypes = {".csv": 5, ".xlsx": 10, ".jpeg": 25, ".mp4": 50, ".pdf": 35}
    with open(filepath, "w") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for k, v in filetypes.items():
            writer.writerow([k, v])


def main() -> None:
    write_users_data()
    write_usage_data()
    write_budgets_data()
    write_costs_data()


if __name__ == "__main__":
    main()
