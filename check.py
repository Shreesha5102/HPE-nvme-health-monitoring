#Importing the necessary libraries.
import os
import schedule 
import time
import datetime
import csv 
import json
from texttable import Texttable 


action = 0
main_counter=0
threshold_counter=0
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
    list_lines.clear()
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
                table.add_row([parameter,list_lines[x][1],parameters[parameter]["threshold"],"Device is running smoothly"])
        elif parameters[parameter]["comparison"] == "<":
            if int(list_lines[x][1]) < parameters[parameter]["threshold"]:
                table.add_row([parameter,list_lines[x][1],parameters[parameter]["threshold"],parameters[parameter]["comment"]])
            else:
                table.add_row([parameter,list_lines[x][1],parameters[parameter]["threshold"],"Device is running smoothly"])
        else:
            print("Invalid paramter")
            
#Code for Data Analysis - we check when the device has overheated. If temp drops below threshold for 1 minute reset the counters.
def data_analysis():
    start_timestamp=""
    end_timestamp=""
    global main_counter
    global threshold_counter

    if int(list_lines[0][1])>parameters["temperature"]["threshold"] and main_counter==0:
        main_counter+=1
        start_timestamp=datetime.datetime.now()
    if int(list_lines[0][1])<=parameters["temperature"]["threshold"] and (main_counter>=0 and threshold_counter <=2):
       threshold_counter+=1
    if int(list_lines[0][1])<=parameters["temperature"]["threshold"] and threshold_counter==2:
       end_timestamp=datetime.datetime.now()
       time=get_time_duration(main_counter)
       main_counter=0
       threshold_counter=0
       print("Device overheated from "+start_timestamp+" to " +end_timestamp+".\nTotal time Duration was"+ time +" .\nCheck the applications you were running at that given time") 

def get_time_duration(x):
    if(x>360):
       hours=x/360
       x=x/360
    if(x>6):
       minutes=x/6
       x=x/6
    seconds=x*10
    time=str(hours)+":"+str(minutes)+":"+str(seconds)
    return(time)
#Driver method
def driver():
    run_check()
    write_header()
    check_errors()
    data_analysis()
    print(table.draw())
    print("=================================================================================================================")
    table.reset()


schedule.every(10).seconds.do(driver)

if __name__ == '__main__':
    get_drive()
    while True:
        schedule.run_pending()
        time.sleep(1)
   
