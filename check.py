#Importing the necessary libraries.
import os
import subprocess
import schedule #For checking the NVME Drive periodically.
import time
import datetime
import csv 
import json #To access Threshold values.
from texttable import Texttable #Create an output table. 


action = 0
list_lines = []
drive_to_check = ''
#Loading the Threshold Parameters.
j = open('threshold.json') 
parameters = json.load(j)

#Creating a table that compares current value of NVME drive parameters with threshold values.
table = Texttable()

def get_drive():
    os.system("sudo nvme list")
    print('These are the available NVME Drives. Which one will you like to check?') #Asking the user which NVME drive he wants to check.
    global drive_to_check
    drive_to_check =input() #Taking user input.
    print('Checking for Drive', drive_to_check)

#This function obtains the SMART LOG for the given NVME device. 
def run_check():
    
    table.add_rows([['Parameter','Current Value','Threshold Value','Comments']])
    os.system('sudo nvme smart-log /dev/' + drive_to_check + ' -H > smartLog.txt') #Running the SMART log command for the given NVME drive and storing it in smartLog.txt.
    os.system("sed -i '1,8d' smartLog.txt") 

#This function extracts the SMART log file and pre-processes it so that it can be used for inferences.
def extract_log():
    global list_lines
    file = open("smartLog.txt","r") #Obtaining the SMART log file.

    #Removes empty spaces and separates lines as list of key value pairs
    for line in file:
        stripped_line = line.strip()
        stripped_line = stripped_line.replace("\t", "")
        stripped_line = stripped_line.replace("C", "")
        stripped_line = stripped_line.replace("%", "")
        stripped_line = stripped_line.replace(",", "")
        line_list = stripped_line.split(":") #list of key value pair
        list_lines.append(line_list) #list of list of key value pairs
    
    file.close()

#Function to write headers.
def write_header():
    global action
    extract_log()
    file = open("log.csv","a")
    writer = csv.writer(file)
    key = []
    value = []
    for line in list_lines:
        key.append(line[0])
        value.append(line[1])
    key.append('Timestamp') #adding timestamp column
    value.append(datetime.datetime.now()) #adding timestamp value
    if action == 0:
        action += 1
        writer.writerow(key)
        writer.writerow(value)
    else:
        writer.writerow(value)
    file.close()

#Function to check for errors in NVME drive. 5 Parameters are compared against their thresholds.
def check_errors():
    pos = [0,2,11,12,14]

    for parameter,x in zip(parameters,pos):
        if parameters[parameter]["comparison"] == ">":
            if int(list_lines[x][1]) > parameters[parameter]["threshold"]:
                table.add_row([parameter,list_lines[x][1],parameters[parameter]["threshold"],parameters[parameter]["comment"]])
            else:
                table.add_row([parameter,list_lines[x][1],parameters[parameter]["threshold"],"Device is running smooth"])
        elif parameters[parameter]["comparison"] == "<":
            if int(list_lines[x][1]) < parameters[parameter]["threshold"]:
                table.add_row([parameter,list_lines[x][1],parameters[parameter]["threshold"],parameters[parameter]["comment"]])
            else:
                table.add_row([parameter,list_lines[x][1],parameters[parameter]["threshold"],"Device is running smooth"])
        else:
            print("Invalid paramter")
       
#Driver method
def driver():
    run_check()
    write_header()
    check_errors()
    print(table.draw())
    print("=================================================================================================================")
    table.reset()


schedule.every(10).seconds.do(driver)

if __name__ == '__main__':
    get_drive()
    while True:
        schedule.run_pending()
        time.sleep(1)
   
