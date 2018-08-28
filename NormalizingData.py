import csv
import sys

def getRatio(data,maximum):
    value = float(data);
    val2 = float(maximum)
    ratio = (((val2-value)*100)/val2);
    #ratio = round(ratio,2);
    return str(ratio);

def getRatio2(data,maximum):
    value = float(data);
    val2 = float(maximum)
    ratio = ((val2*value)/100);
    #ratio = round(ratio,2);
    return str(ratio);

def getPrediction(data,maximum):
    value = float(data);
    val2 = float(maximum)
    ratio = (val2*value)/100;
    ra = ratio+813;
    #ratio = round(ratio,2);
    return str(ra);

def getfinaldata(high,close):
    if(high>=close):
        return 0
    else:
        return 1
def getcolval():
     book = xlrd.open_workbook('Excel/Stockdata.csv')
     first_sheet = book.sheet_by_index(0)
     particular_cell_value = first_sheet.cell(2,3).value
     print(particular_cell_value);
       

def getValuesFromCSV():
    try:
        f = open('Excel/Stockdata.csv', 'rt')
        outputFile = open('Excel/OutputFile.csv', 'w', newline='')
        outputWriter = csv.writer(outputFile)
        reader = csv.reader(f)
        count = 0;
        for row in reader:
            if count==0:
                count+=1;
                outputWriter.writerow(['Close','%change'])
                continue;
            else:
                outputWriter.writerow([row[4],getRatio(row[5],843)]);
            
        print('File succesfully created!');
        f.close();
        outputFile.close();
    except:
        print("File not found!");
def predictdata():
    try:
        f1=open('Excel/OutputFile.csv','rt')
        OF = open('Excel/Prediction.csv','w', newline='')
        outputWriter = csv.writer(OF)
        reader = csv.reader(f1)
        count = 0;
        for row in reader:
            if count==0:
                count+=1;
                outputWriter.writerow(['result','%change','PredictedPrice'])
                continue;
            else:
                outputWriter.writerow([row[0],row[1],getPrediction(row[1],813)]);               
                print(row[1],'%');
        print('The stock price changes in percentage::');
        print('File succesfully created!');
        f.close();
        outputFile.close();
    except:
        print('nf');
getValuesFromCSV();
predictdata();
