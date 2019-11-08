import urllib.request
import urllib.parse
from selenium.common.exceptions import NoSuchElementException
import csv
from bs4 import BeautifulSoup
import re
# Might have to rewrite this to check if we need to append or write "a"


from selenium.webdriver import ChromeOptions, Chrome

options = ChromeOptions()
options.add_argument('--headless')
driver = Chrome(options=options)

writeFile = open("testMultipleLinks.csv", "w", newline="")
writeFile2 = open("testMultipleLinks_error.csv", "w")
readFile = open("all_security_emails.csv", "r")

# Initialize Writer
csv_writer = csv.writer(writeFile)
restricted_writer = csv.writer(writeFile2)
# Initialize reader
csv_reader = csv.reader(readFile, delimiter=",")
count = 0

bug2 = [['Id'], ['Date Started'], ['Fix Date']]
# csv_writer.writerow(bug2)
status = True

for bug in csv_reader:
    start = 0
    iterations = True
    totalAddedLoc = 0
    totalSubLoc = 0
    offset = 0
    gerList = []

    new_bug = re.sub("[^0-9]", "", bug[0])
    url = "https://bugs.chromium.org/p/chromium/issues/detail_ezt?id=" + new_bug
    urls = [url]

    while len(urls) > 0:
        try:
            print("Start", start)

            try:
                htmltext = urllib.request.urlopen(urls[0]).read()
            except:
                print(urls[0])

            soup = BeautifulSoup(htmltext, features="lxml")
            urls.pop(0)

            mydivs = soup.find(id='ezt-comments')

            content = mydivs.get('comment-list')
            # loop for multiple links
            while iterations == True:
                 #create a list to ensure no repeating ids are used
                offset = 0
                print("***********")
                print(start)
                newContent = content[start:len(content) - 1]

                t = newContent.find("chromium/src/+/")  # real
                # modified code
                s = newContent.find("codereview.chromium.org/")

                u = newContent.find("https://chromium-review.googlesource.com/")


                mylist = [u, s, t]
                mylist = [i for i in mylist if i != -1]  # remove everything = -1

                if len(mylist) == 0:
                    iterations = False
                else:
                    small = min(mylist)

                    if s != small:
                        s = -1
                    if t != small:
                        t = -1
                    if u != small:
                        u = -1



                # print("s", s)

                storeIDGerrit = 0
                leftURL = "https://chromium-review.googlesource.com/c/chromium/src/+/"  # type 1
                sleftURL = "https://codereview.chromium.org/"  # type 2
                uleftURL = "https://chromium-review.googlesource.com/"  # type 3

                if len(newContent) < u + 41:
                    print("Nothing left to Check")
                else:
                    if 'c' == newContent[u + 41]:
                        uleftURL = "https://chromium-review.googlesource.com/"
                        offset = 2

                if t != -1:
                    '''t1 is the starting point for the ID #
                        t2 is the starting point of the new line character \n
                         t3 gets rid of the \ from the \n
                     Then we print the ID from the range of t1 to t3
                    '''
                    # get us to the / after src
                    t1 = t + 15

                    t2 = content.find("n", t1)
                    # print(content.find(0,t1))
                    t3 = t2 - 1
                    # read next 7 numbers
                    t4 = t1 + 7

                    storeIDGerritA = newContent[t1:t4]
                    storeIDGerrit = re.sub("[^0-9]", "", storeIDGerritA)

                    # if not gerList.__contains__(storeIDGerrit):
                    if storeIDGerrit not in gerList:
                        gerList.append(storeIDGerrit)



                        URL = leftURL + storeIDGerrit

                        # urls2 = [URL]

                        urls2 = [URL]
                        driver.get(URL)
                        try:
                            input = driver.find_element_by_id("mainContent")

                            print("***********")
                            print("Type 1")  # first bugs dealt
                            # endDate = soup.find('th', text='Closed:').find_next_sibling('td').text

                            input2 = input.find_element_by_id('output')

                            if input2.text.__contains__('BUG=' + bug[0]) or input2.text.__contains__('Bug: ' + bug[0]):
                                bugIdExist = True
                            else:
                                bugIdExist = False

                            # bugIdExist = input2.text.__contains__('Bug: ' + bug[0])
                            # bugIdExist2 = input2.text.__contains__('BUG=' + bug[0])
                            # print(bugIdExist)
                            otherBugIdExist = input2.text.__contains__('Bug: ')
                            otherBugIdExist2 = input2.text.__contains__('BUG=')
                            if bugIdExist == False:
                                print("Other Bug Exist",otherBugIdExist)
                                print("Other Bug Exist 2",otherBugIdExist2)

                            # print("BUG= ", otherBugIdExist2)
                            # print("Bug: ", otherBugIdExist)

                            # if bugIdExist or bugIdExist2 == True or otherBugIdExist and otherBugIdExist2 == False:
                            if bugIdExist == True or otherBugIdExist and otherBugIdExist2 == False:
                                # print("We entered")
                                # print(input.find_elements_by_id("fileList")[0].text)
                                myInput = input.find_elements_by_id("fileList")[0].text
                                g = myInput.splitlines()
                                f = g[len(g) - 1].split(' ')

                                added = float(f[0])
                                subtracted = float(f[1])
                                print(str(added) + " two values " + str(subtracted))

                                print("***********************BEFORE")
                                print("BeforeAdded",totalAddedLoc,"BeforeSubtracted",totalSubLoc)

                                totalAddedLoc = added + totalAddedLoc
                                totalSubLoc = subtracted + totalSubLoc


                                print("***********************AFTER")
                                print("AddedSum: ", totalAddedLoc, "SubtractedSum: ", totalSubLoc)

                        except Exception as e1:
                            print("Error Occurred", str(e1))
                            restricted_writer.writerow([bug[0], str(e1)])
                    else:
                        print("Duplicate Gerrit ID Ignored")
                    start = start + t4
                    input = None # reset to prevent reuse of previous results

                if s != -1:

                    s1 = s + 24
                    # read next 7 numbers
                    s4 = s1 + 10

                    storeIDGerrit2b = newContent[s1:s4]
                    storeIDGerrit2 = re.sub("[^0-9]", "", storeIDGerrit2b)

                    if storeIDGerrit2 not in gerList:
                        gerList.append(storeIDGerrit2)

                        print("gId2: " + storeIDGerrit2)

                        URL = sleftURL + storeIDGerrit2

                        print("******************")
                        print("Type 2")  # second bugs dealt
                        print(URL)

                        urls2 = [URL]

                        driver.get(URL)
                        try:

                            input = driver.find_element_by_class_name("issue-list")
                            input2 = input.find_elements_by_tag_name("i")

                            out2 = driver.find_element_by_id("issue-description")
                            out3 = out2.text

                            if out3.__contains__('BUG=' + bug[0]) or out3.__contains__('Bug: ' + bug[0]):
                                bugIdExist = True
                            else:
                                bugIdExist = False

                            bugIdExist2 = out3.__contains__('BUG=chromium:' + bug[0])
                            print(bugIdExist)
                            otherBugIdExist = out3.__contains__('Bug: ')
                            otherBugIdExist2 = out3.__contains__('BUG=')
                            if bugIdExist == False:
                                print("Other Bug Exist",otherBugIdExist)
                                print("Other Bug Exist 2",otherBugIdExist2)

                            print(bugIdExist)

                            if bugIdExist or bugIdExist2 == True or otherBugIdExist and otherBugIdExist2 == False:
                                numbers = input2[1].text
                                print(numbers)

                                splitNum = numbers.split(",")
                                toAdd = splitNum[0].split(" ")[0]
                                toSub = splitNum[1].split(" ")[1]

                                print("total sub lines")
                                print(totalSubLoc)

                                print("toSub lines")
                                print(toSub)
                                try:
                                    print("AddedSum: ", totalAddedLoc, "SubtractedSum: ", totalSubLoc)
                                    print("***********************BEFORE")
                                    print("BeforeAdded",totalAddedLoc,"BeforeSubtracted",totalSubLoc)

                                    totalAddedLoc = totalAddedLoc + float(toAdd)
                                    totalSubLoc = totalSubLoc + float(toSub)

                                    print("***********************AFTER")
                                    print("AddedSum: ", totalAddedLoc, "SubtractedSum: ", totalSubLoc)

                                except ValueError:
                                    print("Value Error occured")
                                    restricted_writer.writerow([bug[0]])

                        except Exception as e2:
                            print("Error Occured", str(e2))
                            restricted_writer.writerow([bug[0], str(e2)])

                    else:
                        print("Duplicated Gerrit ID Ignored")

                    start = start + s4
                    input = None # reset to prevent reuse of previous results
                    print("Start" + str(start))

                if u != -1:
                    u1 = 41 + u + offset
                    # read next 7 numbers
                    u4 = u1 + 7

                    storeIDGerrit3c = newContent[u1:u4]
                    storeIDGerrit3 = re.sub("[^0-9]", "", storeIDGerrit3c)

                    if storeIDGerrit3 not in gerList:
                        gerList.append(storeIDGerrit3)

                        URL = uleftURL + storeIDGerrit3
                        print(URL)

                        # urls2 = [URL]

                        urls2 = [URL]
                        driver.get(URL)
                        try:

                            input = driver.find_element_by_id("mainContent")

                            print("***********")
                            print("Type 3")
                            # endDate = soup.find('th', text='Closed:').find_next_sibling('td').text

                            input2 = input.find_element_by_id('output')
                            print("GID",storeIDGerrit3)
                            print(input2.text)

                            # bugIdExist = input2.text.__contains__('Bug: ' + bug[0])
                            if input2.text.__contains__('BUG=' + bug[0]) or input2.text.__contains__('Bug: ' + bug[0]):
                                bugIdExist = True
                                print("We are here")
                            else:
                                bugIdExist = False
                                print("We said false")

                            bugIdExist2 = input2.text.__contains__('BUG=chromium:' + bug[0])
                            print(bugIdExist)
                            otherBugIdExist = input2.text.__contains__('Bug: ')
                            otherBugIdExist2 = input2.text.__contains__('BUG=')

                            if bugIdExist == False:
                                print("Other Bug Exist",otherBugIdExist)
                                print("Other Bug Exist 2",otherBugIdExist2)

                            if bugIdExist or bugIdExist2 == True or otherBugIdExist and otherBugIdExist2 == False:
                                # print(input.find_elements_by_id("fileList")[0].text)
                                myInput = input.find_elements_by_id("fileList")[0].text
                                g = myInput.splitlines()
                                f = g[len(g) - 1].split(' ')

                                added = float(f[0])
                                subtracted = float(f[1])
                                print(str(added) + " two values " + str(subtracted))
                                print("***********************BEFORE")
                                print("BeforeAdded",totalAddedLoc,"BeforeSubtracted",totalSubLoc)

                                totalAddedLoc = added + totalAddedLoc
                                totalSubLoc = subtracted + totalSubLoc

                                print("***********************AFTER")
                                print("AddedSum: ", totalAddedLoc, "SubtractedSum: ", totalSubLoc)

                        except Exception as e3:
                            print("Error Occured", str(e3))
                            restricted_writer.writerow([bug[0], str(e3)])

                    #execute always
                    else:
                        print("Duplicate Gerrit ID Ignored")
                    start = start + u4
                    input = None # reset to prevent reuse of previous results
            else:
                print("No Reviewed-On link found")
                linesOfCode = None
        except Exception as e:
            print("Error Occured" + bug[0])
            restricted_writer.writerow([bug[0], str(e)])


        csv_writer.writerow([bug[0], totalAddedLoc, totalSubLoc])

################################### repeating gerrit id trouble bug id 945650

readFile.close()
writeFile2.close()
writeFile.close()
