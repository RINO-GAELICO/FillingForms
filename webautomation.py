from selenium import webdriver 
from selenium.webdriver.chrome.options import Options   
from selenium.webdriver.common.by import By
import time
import csv
import sys

f = open('./infoUscis.csv', 'w')

# create the csv writer
csvwriter = csv.writer(f)

firstrow = ['CASE NUMBER', 'STATUS MESSAGE', 'FORM', 'MONTH', 'DAY', 'YEAR']
months = ['December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']

csvwriter.writerow(firstrow)

options = Options()
options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
driver_path = '/usr/local/bin/chromedriver'
drvr = webdriver.Chrome(options = options, executable_path = driver_path)
startingPoint = int(sys.argv[2])

drvr.get('https://egov.uscis.gov/casestatus/landing.do')
for index in range(int(sys.argv[1])):

    # if(drvr.find_element(by=By.XPATH, value='//*[@id="popupDialogArea"]')):
    #     errorButton = drvr.find_element(by=By.XPATH, value='ui-button-text')
    #     errorButton.click()
    number = index+startingPoint
    receiptNumber = "IOE091371"+str(number)
    receiptToFill = drvr.find_element(by=By.XPATH, value='//*[@id="receipt_number"]')
    receiptToFill.send_keys(receiptNumber)
    if index == 0:
        checkButton = drvr.find_element(by=By.XPATH, value='//*[@id="landingForm"]/div/div[1]/div/div[1]/fieldset/div[2]/div[2]/input')
    else:
        checkButton = drvr.find_element(by=By.XPATH, value='//*[@id="caseStatusSearchBtn"]')
    checkButton.click()

    textToScan = drvr.find_element(by=By.CSS_SELECTOR, value='.text-center')
    textToScan = textToScan.text
    # print(textToScan)
    tokenizedTextStart = textToScan.split('\n')
    statusMessage = tokenizedTextStart[0]

    # open the file in the write mode

    # write a row to the csv file
    tokenizedText = tokenizedTextStart[1].split()

    # getting length of list
    length = len(tokenizedText)
    form = ' '
    # Iterating the index
    # same as 'for i in range(len(list))'
    for i in range(length):
        if tokenizedText[i] in months:
            month = tokenizedText[i]
            day = tokenizedText[i+1]
            year = tokenizedText[i+2]
            continue
        elif tokenizedText[i] == 'Form':
            form = tokenizedText[i+1]

    
    oneRow = [receiptNumber, statusMessage, form[:-1], month,day[:-1],year[:-1]]
    
    csvwriter.writerow(oneRow)



# close the file
f.close()


