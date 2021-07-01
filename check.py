import os

action = 0

def run_check():
    os.system('sudo nvme smart-log /dev/nvme0 -H > smartLog.txt')
    os.system("sed -i '1,8d' smartLog.txt")

def extract_log():
    list_lines = []
    file = open("smartLog.txt","r")

    #Removes empty spaces and separates lines as list of key value pairs
    for line in file:
        stripped_line = line.strip()
        stripped_line = stripped_line.replace("\t", "")
        line_list = stripped_line.split(":") #list of key value pair
        list_lines.append(line_list) #list of list of key value pairs
    
    file.close()

    return list_lines

def write_header():
    l_lines = extract_log()
    global action
    file = open("test.txt","a")
    if action == 0:
        action += 1
        for line in l_lines:
            file.write(line[0] + ",")
    else:
        for line in l_lines:
            file.write(line[1] + ",")
    file.write("\n")
    file.close()

def check_errors():
    file = open("test.txt","r")
    

if __name__ == '__main__':
    run_check()
    write_header()
