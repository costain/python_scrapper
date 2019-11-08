import csv
# This class merges Lines of Code with user responsible for them

writeFile = open("users_loc/security_all_locNoZero.txt", "w", newline="")
# writeFileP = open("users_loc/security_user_locP.txt", "w", newline="",)
# writeFileN = open("users_loc/security_user_locN.txt", "w", newline="")
writeFile2 = open("users_loc/security_all_loc_errorsNoZero.csv", "w")
loc_file = open("loc/sec_all_loc.csv", "r")
users_file = open("all_security_emails.csv", "r")
# loc_file = open("test.csv", "r")
# users_file = open("test2.csv", "r")

csv_writer = csv.writer(writeFile, delimiter='\t')
# csv_writerP = csv.writer(writeFileP, delimiter='\t')
# csv_writerN = csv.writer(writeFileN, delimiter='\t')
error_writer = csv.writer(writeFile2, delimiter='\t')

csv_reader = csv.reader(loc_file, delimiter=",")
csv_reader2 = csv.reader(users_file, delimiter=",")

for bug in csv_reader:
    user_id = None
    found = False
    try:
        for bug2 in csv_reader2:

            if bug[0] == bug2[0]:
                if bug[1] and bug[2] == "0":
                    print("zero removed")
                    error_writer.writerow([bug2[5], bug[1],bug[2]])
                    found = True
                    break

                elif len(bug2[5]) > 1:
                    # csv_writerP.writerow([bug2[5], bug[1]])
                    # csv_writerN.writerow([bug2[5], bug[2]])


                    csv_writer.writerow([bug2[5], bug[1],bug[2]])
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
loc_file.close()
writeFile.close()
# writeFileP.close()
# writeFileN.close()
writeFile2.close()
