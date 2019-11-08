import csv
from datetime import datetime
#

writeFile = open("time_experience/time_experience.csv", "w", newline="")

writeFile2 = open("time_experience/time_experience_error.csv", "w")
loop1_file = open("time_experience/user_days_input.csv", "r")



csv_writer = csv.writer(writeFile)
error_writer = csv.writer(writeFile2)

csv_reader = csv.reader(loop1_file, delimiter=",")
# csv_reader2 = csv.reader(loop2_file, delimiter=",")
email_list = []
for bug in csv_reader:
    start = 1556236800
    end = 0
    number_bugs = 0

    if bug[1] not in email_list:
        email_list.append(bug[1])
        loop2_file = open("time_experience/user_days_input.csv", "r")
        csv_reader2 = csv.reader(loop2_file, delimiter=",")
        try:

            for bug2 in csv_reader2:
                # print(bug[1],bug[2])
                if bug2[1] == bug[1]:
                    # print("are we here")
                    number_bugs = number_bugs + 1
                    if start > int(bug2[2]):
                        start = int(bug2[2])


                    if end < int(bug2[3]):
                        end = int(bug2[3])


            # csv_writer.writerow([bug[1], start, end, number_bugs])

            datetimeFormat = '%m-%d-%Y %H'
            endDateFormat = datetime.utcfromtimestamp(end).strftime('%m-%d-%Y %H')
            # print(endDateFormat)
            startDateFormat = datetime.utcfromtimestamp(start).strftime('%m-%d-%Y %H')
            # print(startDateFormat)

            diff = datetime.strptime(endDateFormat, datetimeFormat) \
                   - datetime.strptime(startDateFormat, datetimeFormat)

            dayRange = diff.days
            hourRange = diff.seconds/3600
            csv_writer.writerow([bug[1], dayRange, number_bugs])
            loop2_file.close()

        except Exception as e:
            print("Error occurred", bug[0])
            error_writer.writerow([bug[0], str(e)])

loop1_file.close()

writeFile.close()
writeFile2.close()
