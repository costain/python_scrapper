import csv
# This class merges Lines of Code with user responsible for them

writeFile = open("time_experience/user_days_input.csv", "w", newline="")
writeFile2 = open("time_experience/user_days_input_error.csv", "w")
bug_times_file = open("all_security_unix_input.csv", "r")
users_file = open("all_security_emails.csv", "r")
# loc_file = open("test.csv", "r")
# users_file = open("test2.csv", "r")

csv_writer = csv.writer(writeFile)
error_writer = csv.writer(writeFile2)

csv_reader = csv.reader(bug_times_file, delimiter=",")
csv_reader2 = csv.reader(users_file, delimiter=",")

for bug in csv_reader:
    user_id = None
    found = False
    try:
        for bug2 in csv_reader2:

            if bug[0] == bug2[0]:
                if len(bug2[5]) > 1:
                    csv_writer.writerow([bug[0], bug2[5], bug[1], bug[2]])
                    found = True
                    break
                else:
                    error_writer.writerow([bug[0], "User Not Found"])
                    found = True
                    break


        if found is False:
            print("User not Found")
            error_writer.writerow([bug[0], "User Not Found"])


    except Exception as e:
        print("Error occurred", bug[0])
        error_writer.writerow([bug[0], str(e)])

users_file.close()
bug_times_file.close()
writeFile.close()
writeFile2.close()
