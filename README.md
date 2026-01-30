# Example project

This repo is being used to provide a training exercise for data analysis using python and/or sql. The repo consists of a data folder which contains 4 csv files and a src folder where you will write your code. When working with this repo, please make sure to create a new branch and carry out your work on your branch.

# Data
Users: user data detailing user names, user IDs and their department
Usage: records of files being stored by each user including the filename, filetype, user_id, filesize and date the file was uploaded on
Budgets: records of each department's budget
Costs: records of how much each unit of filesize costs for each filetype

# Guidance
Each question can be solved using python or sql. It is advised that you create a new file per question though where code is being reused, it may be helpful to store the code as functions in the utils module so that it can be imported into other files. There is already a function in the utils module for loading the data files in as pandas dataframes.
The data can be manipulated using the csv module, pandas or duckdb. Any choice is correct though it may be helpful to try all three to understand the differences between them.

# Questions
1) Write a file to find out the name of the user who has stored the most data by filesize
2) Write a file to find out which department has stored the most files in the last 3 years
3) Write a file to find out whether departments are over or under budget
4) Write a file to find out which department has stored the most data files (.csv & .xlsx)
5) Write a file to find out the name of the user who has stored the most data files PDF files by how much they have spent storing PDF files
6) Write a file to find out how much each user has spent and rank users by spend in descending order