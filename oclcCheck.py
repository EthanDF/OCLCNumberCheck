import requests
import csv
import tkinter

# r = requests(testurl)

root = tkinter.Tk()
root.withdraw()
# oclc = 13755345

def checkURL(oclcNum):
    # url = 'http://xisbn.worldcat.org/webservices/xid/oclcnum/'+str(oclcNum)+'?method=getMetadata&format=xml&fl=*'
    url = 'http://www.worldcat.org/search?q=no%3A'+str(oclcNum)+'&qt=advanced&dblist=638'
    r = requests.get(url)

    ##convert response to text
    rt = r.text

    ##split the text up so that we can find the OCLC Number returned
    # a = rt.split('"')

    ##cycle through the lists to find the place where the result is
    buzzWord = 'oclc/'

    oclcMaster = rt[rt.find(buzzWord)+len(buzzWord):rt.find('"',rt.find(buzzWord))]

    try:
        int(oclcMaster)
    except ValueError:
        oclcMaster = -1


    # counter = 0
    # counterResult = 0

    # for x in a:
    #     # print(str(counter),":", x)
    #     if buzzWord in x:
    #         counterResult = counter
    #         # print("found!")
    #         # print('counterResult is: '+str(counterResult))
    #     counter += 1


    # if counterResult == 0:
    #     oclcMaster = oclcNum
    # else:
    #     oclcMaster = (a[counterResult+1])

    # print(oclcMaster)

    return int(oclcMaster)

def checkFLVC(goodOCLCNum):
    url = 'http://union.catalog.fcla.edu/ux.jsp?fl=bo&st='+str(goodOCLCNum)+'&ix=nu&S=0921439321283054&fl=bo'
    r = requests.get(url)

    ##convert response to text
    rt = r.text

    hasResultsKey = 'Results/page'

    foundInResults = [False, -1]
    if hasResultsKey in rt:
        bibIDgiveaway = 'sysnum%3D'
        try:
            bibID = int(rt[rt.find(bibIDgiveaway)+len(bibIDgiveaway):rt.find(bibIDgiveaway)+9+len(bibIDgiveaway)])
            foundInResults = [True, bibID]
        except ValueError:
            foundInResults = [False, -1]

    return foundInResults

def printResults(results, logFile):

    # logFile = 'oclcLogResults.csv'


    rows = []
    rows.append(results)

    with open(logFile, 'a', newline='') as out:
        a = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL)
        a.writerows(rows)



def validateOCLC(ocl):

    #check if ocl is still a valid OCLC Number

    ##results = [inputocl, foundocl, good (logical), Duplicate Aleph]
    results = []
    goodOCL = checkURL(ocl)
    if goodOCL == ocl:
        results = [ocl, goodOCL, 0, 0]
    elif goodOCL == -1:
        results = [ocl, 'invalid oclc number', 0, 0]
    else:
        inFLVC = checkFLVC(goodOCL)
        if inFLVC[0]:
            results = [ocl, goodOCL, 1, inFLVC[1]]
        else:
            results = [ocl, goodOCL, 1, 0]

    # printResults(results)

    return results

def runValidation():

    oclList = []
    from tkinter import filedialog

    input("press any key to choose a Input File\n")
    marcPath = tkinter.filedialog.askopenfile()
    oclcNumberFile = marcPath.name

    input("thanks! press any key to choose a results log\n")
    logPath = tkinter.filedialog.askopenfile()
    logFile = logPath.name
    # oclcNumberFile = 'oclcList.csv'

    print("thanks... checking...")

    with open(oclcNumberFile, 'r') as f:
        reader = csv.reader(f)
        oclList = list(reader)

    for row in oclList:
        results = []
        try:
            int(row[1])
            tempresults = validateOCLC(int(row[1]))
        except ValueError:
            tempresults = ['invalid OCLC Number', -1, -1]


        # tempresults = validateOCLC(int(row[1]))
        results.append(row[0])
        for r in tempresults:
            results.append(r)

        printResults(results, logFile)

        stop = 'n'
        # stop = input("stop?")
        if stop == 'y':
            break

runValidation()