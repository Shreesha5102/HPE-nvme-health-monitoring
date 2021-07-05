#Importing the necessary libraries.
import os
import subprocess
import schedule #For checking the NVME Drive periodically.
import time 
import json #To access Threshold values.
from texttable import Texttable #Create an output table. 

action = 0
list_lines = []

#Loading the Threshold Parameters.
j = open('threshold.json') 
parameters = json.load(j)

#Creating a table that compares current value of NVME drive parameters with threshold values.
table = Texttable()
table.add_rows([['Parameter','Current Value','Threshold Value','Comments']]) 

#This function obtains the SMART LOG for the given NVME device. 
def run_check():
    nvme_list = subprocess.check_output("sudo nvme-list", shell=True); #Obtaining the list of NVME drives in the system.
    print('These are the available NVME Drives. Which one will you like to check?\n', nvme_list) #Asking the user which NVME drive he wants to check.      
    drive_to_check=input() #Taking user input.
    print('Checking for Drive', drive_to_check)
    os.system('sudo nvme smart-log /dev/'+drive_to_check+' -H > smartLog.txt') #Running the SMART log command for the given NVME drive and storing it in smartLog.txt.
    os.system("sed -i '1,8d' smartLog.txt") 

#This function extracts the SMART log file and pre-processes it so that it can be used for inferences.
def extract_log():
    global list_lines
    file = open("smartLog.txt","r") #Obtaining the SMART log file.

    #Removes empty spaces and separates lines as list of key value pairs
    for line in file:
        stripped_line = line.strip()
        stripped_line = stripped_line.replace("\t", "")
        line_list = stripped_line.split(":") #list of key value pair
        list_lines.append(line_list) #list of list of key value pairs
    
    file.close()

#Function to write headers.
def write_header():
    global action
    extract_log()
    file = open("test.txt","a")
    if action == 0:
        action += 1
        for line in list_lines:
            file.write(line[0] + ",")
    else:
        for line in list_lines:
            file.write(line[1] + ",")
    file.write("\n")
    file.close()
#Function to check for errors in NVME drive. 5 Parameters are compared against their thresholds.
def check_errors():
    #Temperature shouldn't cross 70 C
    if int(list_lines[0][1][:-1]) >= parameters["temperature"]:
        table.add_row(["Temperature",list_lines[0][1],"70 C","NVME Drive is overheating. \n Please backup your files to prevent data loss.\n Get your disk checked or replaced!\n "])
    #Avaliable Spare should not drop below 10%
    if int(list_lines[2][1][:-1]) < parameters["available_spare_threshold"] :
        table.add_row(["Available Spare",list_lines[2][1],"10%","NVME drive is running out of storage. \n Please backup your files to prevent data loss.\n Get your disk checked or replaced!\n "])
    #Power On Hours for an NVME Drive is rated at 44000. Above this value there are risks of failure. 
    if int(list_lines[11][1].replace(",","")) > parameters["power_on_hours"]:
        table.add_row(["Power On hours",list_lines[11][1]+" hours","44000 hours","NVME is reaching end of rated lifespan. \n Please backup your files to prevent data loss.\n Get your disk checked or replaced!\n"])
    #There should not be too many unsafe shutdowns
    if int(list_lines[12][1]) > parameters["unsafe_shutdowns"]:
        table.add_row(["Unsafe Shutdowns",list_lines[12][1],"1000","There are an abnormal number of unsafe shutdowns. \n Please backup your files to prevent data loss.\n Get your disk checked or replaced!\n"])
    #Media errors should not cross a certain range, or there is a high chance that the drive will fail.    
    if int(list_lines[14][1]) > parameters["media_errors"]:
        table.add_row(["Media Errors",list_lines[14][1],"100000","There are a lot of media errors.\n Please backup your files to prevent data loss.\n Get your disk checked or replaced!\n :)"])

#Driver method
def driver():
    run_check()
    write_header()
    write_header()
    check_errors()
    print(table.draw())

schedule.every(10).seconds.do(driver)

while True:
        schedule.run_pending()
        time.sleep(1)

# if __name__ == '__main__':
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
    # driver()
    # print(table.draw())
