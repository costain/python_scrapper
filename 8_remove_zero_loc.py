import csv
from datetime import datetime


writeFile = open("time_out/all_security.csv", "w", newline="")
writeFile2 = open("time_error/all_security_error.csv", "w")
readFile = open("all_security_unix_input.csv", "r")

csv_writer = csv.writer(writeFile)
csv_reader = csv.reader(readFile, delimiter=",")
error_writer = csv.writer(writeFile2)

for bug in csv_reader:

    try:
        startDate = int(bug[1])
        endDate = int(bug[2])

        datetimeFormat = '%m-%d-%Y %H'
        endDateFormat = datetime.utcfromtimestamp(endDate).strftime('%m-%d-%Y %H')
        print(endDateFormat)
        startDateFormat = datetime.utcfromtimestamp(startDate).strftime('%m-%d-%Y %H')
        print(startDateFormat)

        diff = datetime.strptime(endDateFormat, datetimeFormat) \
               - datetime.strptime(startDateFormat, datetimeFormat)

        dayRange = diff.days
        hourRange = diff.seconds/3600

        csv_writer.writerow([bug[0], dayRange, hourRange])
    except Exception as e:
        print("Error occured", bug[0])
        error_writer.writerow([bug[0], str(e)])

readFile.close()
writeFile.close()
writeFile2.close()
