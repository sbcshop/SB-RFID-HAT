import csv
import os

class CSVFile:
    def Write(name, Data, overwrte = False):
        if(overwrte == True):
            mode = 'w'
        else:
            mode = 'a'
        with open(name, mode, newline='') as file:
            writer = csv.writer(file)
            writer.writerow(Data)
            file.close()

    def Read(name):
        try:
            with open(name, 'r') as file:
                reader = csv.reader(file)
                rows = []
                for row in reader: 
                    rows.append(row) 
                return rows
        except:
            pass
    def remove(name):
        os.remove(name)
