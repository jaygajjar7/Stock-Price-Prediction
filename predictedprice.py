import csv
import sys

def getValuesFromCSV():
    try:
        f = open('Excel/Prediction.csv', 'rt')
        outputFile = open('Excel/OutputFile.csv', 'w', newline='')
        outputWriter = csv.writer(outputFile)
        reader = csv.reader(f)
        count = 0;
        for row in reader:
            if count==0:
                count+=1;
                #outputWriter.writerow(['Close','%change'])
                continue;
            else:
                #outputWriter.writerow([row[4],getRatio(row[5],853)]);
                print(row[2]);
        print('Next predictions for 10 days');
        print('File succesfully created!');
        f.close();
        outputFile.close();
    except:
        print("File not found!");
getValuesFromCSV();
