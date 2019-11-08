from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import csv

# Obtain start and end time

writeFile = open("security_heuristics_unix/", "a")
readFile = open("security_heuristics/", "r")

# Initialize Writer
csv_writer = csv.writer(writeFile)
# Initialize reader
csv_reader = csv.reader(readFile, delimiter=",")
count = 0

# bug2 = [['Id'], ['Start'], ['Date Fixed']]
# csv_writer.writerow(bug2)
status = True
statusFixed = True

for bug in csv_reader:


    url = "https://bugs.chromium.org/p/chromium/issues/detail_ezt?id=" + bug[0]
    urls = [url]
    visited = [url]

    while len(urls) > 0:

        try:
            htmltext = urllib.request.urlopen(urls[0]).read()
        except:
            print(urls[0])
        try:
            soup = BeautifulSoup(htmltext, features="lxml")
            urls.pop(0)
            # Find the sibling whose header is closed
            endDate = soup.find('th', text='Closed:').find_next_sibling('td').text
            startDateUnix = 0
            mydivsRepo = soup.find('chops-timestamp')  # reported date if  need be
            startDateRepo = mydivsRepo.get('timestamp')

            mydivs = soup.find(id='ezt-comments')

            content = mydivs.get('comment-list')
            # Date Started Key
            t = content.find("newOrDeltaValue\": \"Started")
            # Date Fixed Key
            f = content.find("newOrDeltaValue\": \"Fixed")

            t = content.find("newOrDeltaValue\": \"Started")
            if t == -1:
                t = content.find("newOrDeltaValue\": \"Assigned")
                if t == -1:
                    print("No  Assigned or Started Date. Report Date to be used")
                    startDateUnix = startDateRepo
                    status = False

            if f == -1:
                print("No Date Fixed using date on left panel")
                fixedDate = endDate
                statusFixed = False


            t2 = content.find("timestamp\": ", t)
            f2 = content.find("timestamp\": ", f)

            t4 = content.find("}", t2)
            f4 = content.find("}", f2)

            t3 = t2 + 12 #changed to +12 because of spaces in some instances

            f3 = f2 + 12

            if (status):
                startDateUnix = content[t3:t4]

            if (statusFixed):
                fixedDate = content[f3:f4]

            bugs = [bug[0], startDateUnix, fixedDate,endDate]
            csv_writer.writerow(bugs)
            print(bugs)

            #Reset Status Fixed
            status = True
            statusFixed = True
        except Exception as e:
            print(e)
readFile.close()
writeFile.close()

# mydivs = soup.find('div',{'id':'color_control'})
# date Reported mydivs = soup.find_all('chops-timestamp')
# mydivs = soup.find(id= 'ezt-comments')
#     list = mydivs.get('comment-list')
#     print(list)
