import csv
from datetime import date, datetime

# open the file in the write mode
f = open('logbook.csv', 'a', newline='')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
today = date.today()
start = datetime.now().replace(microsecond=0)
items = input("What did you work on?: ")
end = datetime.now().replace(microsecond=0)
writer.writerow([today, end - start, items])

# close the file
f.close()