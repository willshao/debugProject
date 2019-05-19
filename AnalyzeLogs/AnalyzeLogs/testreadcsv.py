import csv

def readcsvtoDict(filePath):
    f_data=[]
    with open(filePath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            f_data.append(row)
    return f_data

def main():
    readcsvtoDict('C:/test/_all_data.csv')


if __name__ == "__main__":
    main()