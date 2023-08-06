import pandas as pd
from pathlib import Path
from readcsvturbo import read_csv_head, read_csv_headtail, read_csv_line, read_csv_tail

path = Path("/home/donjor/5mSalesRecords.csv")

df = read_csv_head(path)
print(df)
df = read_csv_headtail(path)
print(df)
df = read_csv_line(path,100)
print(df)
df = read_csv_tail(path)
print(df)

df = read_csv_head(path,False)
print(df)
df = read_csv_headtail(path,False)
print(df)
df = read_csv_line(path,100,False)
print(df)
df = read_csv_tail(path,False)
print(df)

df = read_csv_headtail(path)

number = df['Total Profit'].iloc[0]
number2 = df['Total Profit'].iloc[1]

sum = number + number2
print(sum)