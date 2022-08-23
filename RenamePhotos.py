from audioop import reverse
from heapq import nsmallest
import os
import argparse
import timeit
import glob
import csv
from tkinter import NS
import openpyxl


def get_args():
    '''Get arguements from user'''
    parser = argparse.ArgumentParser(description='STAIR Generic File Renamer')
    parser.add_argument(
        '-d', '--directory', metavar='directory', default=os.path.dirname(__file__), help='The directory that has the items to be renamed.'
    )
    parser.add_argument(
        '-r', '--reverse', action='store_true', help='Reverse the order of the renaming.'
    )
    return parser.parse_args()


def countWork(workingDir):
    osSep = os.sep

    jpgList = glob.glob(workingDir + osSep + '*.jpg')
    nefList = glob.glob(workingDir + osSep + '.nef')
    csvList = glob.glob(workingDir + osSep + '*.csv')
    xlsxList = glob.glob(workingDir + osSep + '*.xlsx')

    return jpgList, nefList, csvList, xlsxList


def readCsv(csvFile):
    filenameDict = {}

    for file in csvFile:
        dataFileNames = csv.reader(open(file, newline=''))
        for sourceFilename, destFilename in dataFileNames:
            filenameDict[sourceFilename] = destFilename

    return filenameDict


def readXlsx(xlsxList):

    for file in xlsxList:
        pass


def renameFiles(workingDir, fileNames, reverse):

    osSep = os.sep

    for filename in fileNames:
        if (reverse):
            try:
                os.rename(workingDir + osSep + fileNames[filename],
                        workingDir + osSep + filename)
                print(f'''Filename: {fileNames[filename]} ==> {filename}''')
            except FileNotFoundError:
                print(f'''File Not Found: {filename}''')
        else:    
            try:
                os.rename(workingDir + osSep + filename,
                        workingDir + osSep + fileNames[filename])
                print(f'''Filename: {filename} ==> {fileNames[filename]}''')
            except FileNotFoundError:
                print(f'''File Not Found: {fileNames[filename]}''')


def main():
    args = get_args()

    jpgList, nefList, csvList, xlsxList = countWork(args.directory)

    renameFiles(args.directory, readCsv(csvList), args.reverse)

    print(f'''
    Current working directory {args.directory}
    Discovered {len(jpgList)} jpgs.
    Discovered {len(nefList)} Nikon RAW files.
    Discovered {len(csvList)} CSV files.
    Discovered {len(xlsxList)} Excel spreadsheets.
    ''')


if __name__ == '__main__':
    main()
