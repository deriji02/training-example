#1) Write a file to find out the name of the user who has stored the most data by filesize

from .utils import read_datafile
users = read_datafile("users")
print(users)

usage = read_datafile("usage")
total_data = usage.groupby('user_id')['filesize'].sum() #.sort_values(by="filesize",ascending=False)
print(total_data)
top_user = total_data.idxmax()
print(top_user)

top_user_name = users["username"][users["user_id"]==top_user]
print(top_user_name)