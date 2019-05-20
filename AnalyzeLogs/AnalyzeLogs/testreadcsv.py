import csv
from pykd import *
def readcsvtoDict(filePath):
    f_data=[]
    with open(filePath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            f_data.append(row)
    return f_data

def main():
    #readcsvtoDict('C:/test/_all_data.csv')
    stack=pykd.dbgCommand("!gcroot {}".format('0000004d643c0f78'))
    print(stack)
    print(stack.gettype())
if __name__ == "__main__":
    main()