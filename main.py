import csv
import sys
from os import path, listdir

defDir = 'C:\\FIXMLK\\'


def zAdd(input):
    if len(input) < 2:
        return "0" + input
    return input


def strToSec(input):
    return (int(input[0:2]) * 3600 + int(input[2:4]) * 60 + int(input[4:6]))


def secToStr(input):
    outH = (input // 3600)
    outM = (input - (3600 * outH)) // 60
    outS = (input - (3600 * outH) - (60 * outM))
    # return zAdd(str(outH)) + ":" + zAdd(str(outM)) + ":" + zAdd(str(outS))
    return zAdd(str(outH)) + zAdd(str(outM)) + zAdd(str(outS))


def openFile(fName):
    output = ""
    print(f'    Process file: {fName}')
    with open(fName, 'r', encoding='UTF-8') as f:
        i = 0
        data = csv.reader(f)
        for row in data:
            cowDetach = strToSec(row[0][0:6])
            cowAttach = strToSec(row[0][44:51])
            milkTime = float(row[0][31:35].lstrip()) * 60
            idTime = strToSec(row[0][37:44])
            # print ("IDTIME",idTime,"Converted",secToStr(idTime))
            if cowAttach == 0 & idTime == 0:
                i += 1
                cowAttach = cowDetach - int(milkTime)
                idTime = cowAttach - 60
                if idTime < 0: idTime = idTime + 86400
                if cowAttach < 0: cowAttach = cowAttach + 86400

            # Вывод данных
            out = secToStr(cowDetach) + row[0][6:37] + secToStr(idTime) + "  " + secToStr(cowAttach) + row[0][51:-1]
            output += out + "\n"
        print(f'         fixed - {i} lines')

        return (output)


def fileOutput(fName, str):
    try:
        print(f'         file: {fName} - [Fixed]')
        f = open(fName, 'w')
        f.write(str)
        f.close()
    except:
        print("Error")
    return "Ok"


if __name__ == '__main__':
    print("-" * 46, "\n.mlk Converter v0.18 @DigiFarm software 2022\n" + "-" * 46)
    print(f'    Default work dis is {defDir}')
    print(f'    Custom dir lunch: "mlkConv.exe x:\\youdir\\"\n' + "-" * 46+'\n')
    workDir = defDir
    #print(f'LEN: {len(sys.argv)} -0-  {sys.argv[0]}  -1- {sys.argv[1]}')
    if len(sys.argv) > 1:
        workDir = path.normpath(sys.argv[1])+'\\'
    print(f'Work dir is: {workDir}')
    if path.isdir(workDir):
        for fileInput in listdir(workDir):
            fullFileName = workDir + fileInput
            if path.isfile(fullFileName) and path.splitext(fullFileName)[1].lower() == '.mlk':
                #print(f'ext of file is: {path.splitext(fullFileName)[1]}')
                fileOutput(fullFileName, openFile(fullFileName))
    else: print (f'Directory {workDir} is not found...')

