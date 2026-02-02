##2) Write a file to find out which department has stored the most files in the last 3 years

from .utils import read_datafile
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

usage = read_datafile("usage")
users = read_datafile("users")

usage["date_uploaded"] = pd.to_datetime(usage["date_uploaded"])
time = datetime.now() - relativedelta(months=36)
print(time)

users_usage = pd.merge(left=users, right=usage,on="user_id",how="left")
last_three_years = users_usage[users_usage["date_uploaded"]>=time]
print(last_three_years)

count = last_three_years.groupby(by="dept").count().sort_values(by="user_id",ascending=False)
print(count)

