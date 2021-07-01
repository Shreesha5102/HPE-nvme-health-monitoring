import os

action = 0
list_lines = []

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

    if list_lines[0][1] >= 65:
        print("NVME Device is Overheating")

    if list_lines[2][1] < 10 :
        print("NVME is running out of storage")
    
    if list_lines[11][1] > 44000:
        print("NVME Device is turning old")

    if list_lines[12][1] > 1000:
        print("NVME is facing unsafe shutdowns.\n Please take care !!!\n :) ")


if __name__ == '__main__':
    run_check()
    write_header()
