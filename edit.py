import pandas as pd

def write_columns(ll,file):
    for line in ll:
        file.write(line[0] + ",")


def write_data(ll,file):
    for line in ll:
        file.write(line[1] + ",")


def con_t_C():
    d1 = pd.read_csv("test.txt")
    d1.to_csv("log.csv", index= None)


if __name__=="__main__":
    list_lines = []
    file = open("smartLog.txt","r")

    #Removes empty spaces and separates lines as list of key value pairs
    for line in file:
        stripped_line = line.strip()
        stripped_line = stripped_line.replace("\t", "")
        line_list = stripped_line.split(":") #list of key value pair
        list_lines.append(line_list) #list of list of key value pairs
    
    file.close()

    for line in list_lines:
        line[0].strip()
        line[1].strip()
        line[1] = line[1].replace(",", "")
        line[1] = line[1].replace(" ", "")

    file = open("test.txt","w")
    for line in list_lines:
        file.write(line[0] + ",")
    file.write("\n")



    for line in list_lines:
        file.write(line[1] + ",")

    d1 = pd.read_csv("test.txt")
    d1.to_csv("log.csv", index= None)
