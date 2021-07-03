import os
import schedule
import time
import json
from texttable import Texttable

action = 0
list_lines = []

#loading the parameters
j = open('threshold.json')
parameters = json.load(j)

#creating and adding the headers
table = Texttable()
table.add_rows([['Parameter','Current Value','Threshold Value','Comments']])

def run_check():
    os.system('sudo nvme smart-log /dev/nvme0 -H > smartLog.txt')
    os.system("sed -i '1,8d' smartLog.txt")

def extract_log():
    global list_lines
    file = open("smartLog.txt","r")

    #Removes empty spaces and separates lines as list of key value pairs
    for line in file:
        stripped_line = line.strip()
        stripped_line = stripped_line.replace("\t", "")
        line_list = stripped_line.split(":") #list of key value pair
        list_lines.append(line_list) #list of list of key value pairs
    
    file.close()

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

def check_errors():

    if int(list_lines[0][1][:-1]) >= parameters["temperature"]:
        table.add_row(["Temperature",list_lines[0][1],"35 C","NVME Overheating"])

    if int(list_lines[2][1][:-1]) < parameters["available_spare_threshold"] :
        table.add_row(["Available Spare",list_lines[2][1],"10%","NVME is running out of storage"])
    
    if int(list_lines[11][1].replace(",","")) > parameters["power_on_hours"]:
        table.add_row(["Power On hours",list_lines[11][1]+" hours","44000 hours","NVME is turning old"])

    if int(list_lines[12][1]) > parameters["unsafe_shutdowns"]:
        table.add_row(["Unsafe Shutdowns",list_lines[12][1],"1000","NVME is facing unsafe shutdowns.\n Please take care !!!\n :)"])

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
