from tabula.io import read_pdf, convert_into
import json
import csv
from collections import OrderedDict
import numpy as np

def convert_to_csv(filepath):

    df = read_pdf(filepath, pages='all')[0]

    filename = filepath.split(".")[0]
    convert_into(filepath, f"{filename}.csv", output_format="csv", pages='all')
    print(df)

def get_data():
    with open("data.json","r") as f:
        user = json.load(f)

    return user



def find_line(file, content):
    file = open(file)
    lines = file.readlines()
    line_num = 0
    for line_number, line in enumerate(lines, 1):
        if content.lower() in line.lower():
            line_num = line_number
            break

    return (line_num - 1)

def find_importance(thelist):
    correct_index = 1000
    print(thelist)
    for i in range(len(thelist)):
        if any(item in thelist[i] for item in ["x", "X", "☒"]) and i != 0:
            correct_index = i
            break

    return correct_index


def input_data_from_csv(filepath):
    file = open(filepath)
    content = file.readlines()

    data = get_data()



    uni_name = filepath.split('.')[0]

    data[uni_name] = {}
    data[uni_name]["Location"] = {}
    data[uni_name]["Location"]["State"] = ""

    data[uni_name]["RaceGender"] = {}

    try:
        data[uni_name]["RaceGender"]["M"] = ((next(csv.reader([content[find_line(filepath,"Total all students")]])))[1]).replace("\n", '')
    except:
        data[uni_name]["RaceGender"]["M"] = 0

    try:
        data[uni_name]["RaceGender"]["F"] = ((next(csv.reader([content[find_line(filepath,"Total all students")]])))[2]).replace("\n", '')
    except:
        data[uni_name]["RaceGender"]["F"] = 0


    try:
        data[uni_name]["RaceGender"]["NonRes"] = ((next(csv.reader([content[find_line(filepath,"Nonresidents")]])))[1]).replace("\n", '')

        if " " in data[uni_name]["RaceGender"]["NonRes"]:
            data[uni_name]["RaceGender"]["NonRes"] = (data[uni_name]["RaceGender"]["NonRes"].split(" "))[1]


        data[uni_name]["RaceGender"]["Hispanic"] = ((next(csv.reader([content[find_line(filepath,"Hispanic/Latino")]])))[1]).replace("\n", '')

        if " " in data[uni_name]["RaceGender"]["Hispanic"]:
            data[uni_name]["RaceGender"]["Hispanic"] = (data[uni_name]["RaceGender"]["Hispanic"].split(" "))[1]

        data[uni_name]["RaceGender"]["Black"] = ((next(csv.reader([content[find_line(filepath,"Black or African American")]])))[1]).replace("\n", '')

        if " " in data[uni_name]["RaceGender"]["Black"]:
            data[uni_name]["RaceGender"]["Black"] = (data[uni_name]["RaceGender"]["NonRes"].split(" "))[1]

        data[uni_name]["RaceGender"]["White"] = ((next(csv.reader([content[find_line(filepath,"White")]])))[1]).replace("\n", '')

        if " " in data[uni_name]["RaceGender"]["White"]:
            data[uni_name]["RaceGender"]["White"] = (data[uni_name]["RaceGender"]["White"].split(" "))[1]

        data[uni_name]["RaceGender"]["Native"] = ((next(csv.reader([content[find_line(filepath,"American Indian")]])))[1]).replace("\n", '')

        if " " in data[uni_name]["RaceGender"]["Native"]:
            data[uni_name]["RaceGender"]["Native"] = (data[uni_name]["RaceGender"]["Native"].split(" "))[1]

        data[uni_name]["RaceGender"]["Asian"] = ((next(csv.reader([content[find_line(filepath,"Asian")]])))[1]).replace("\n", '')

        if " " in data[uni_name]["RaceGender"]["Asian"]:
            data[uni_name]["RaceGender"]["Asian"] = (data[uni_name]["RaceGender"]["Asian"].split(" "))[1]

        data[uni_name]["RaceGender"]["TwoMoreNonHispanic"] = ((next(csv.reader([content[find_line(filepath,"Two or more races")]])))[1]).replace("\n", '')

        if " " in data[uni_name]["RaceGender"]["TwoMoreNonHispanic"]:
            data[uni_name]["RaceGender"]["TwoMoreNonHispanic"] = (data[uni_name]["RaceGender"]["TwoMoreNonHispanic"].split(" "))[1]

        data[uni_name]["RaceGender"]["Unknown"] = ((next(csv.reader([content[find_line(filepath,"Race and/or ethnicity unknown")]])))[1]).replace("\n", '')

        if " " in data[uni_name]["RaceGender"]["Unknown"]:
            data[uni_name]["RaceGender"]["Unknown"] = (data[uni_name]["RaceGender"]["Unknown"].split(" "))[1]

    except:
        data[uni_name]["RaceGender"]["NonRes"] = 0
        data[uni_name]["RaceGender"]["Hispanic"] = 0
        data[uni_name]["RaceGender"]["Black"] = 0
        data[uni_name]["RaceGender"]["White"] = 0
        data[uni_name]["RaceGender"]["Native"] = 0
        data[uni_name]["RaceGender"]["Asian"] = 0
        data[uni_name]["RaceGender"]["TwoMoreNonHispanic"] = 0
        data[uni_name]["RaceGender"]["Unknown"] = 0




    data[uni_name]["Importance"] = {}
    data[uni_name]["Importance"]["GPA"] = find_importance(content[find_line(filepath,"Academic GPA")].split(","))
    data[uni_name]["Importance"]["Standardized"] = find_importance(content[find_line(filepath,"Standardized test scores")].split(","))
    data[uni_name]["Importance"]["Essay"] = find_importance(content[find_line(filepath,"Application Essay")].split(","))
    data[uni_name]["Importance"]["LORS"] = find_importance(content[find_line(filepath,"Recommendation")].split(","))
    data[uni_name]["Importance"]["EC"] = find_importance(content[find_line(filepath,"Extracurricular")].split(","))
    data[uni_name]["Importance"]["FirstGen"] = find_importance(content[find_line(filepath,"First generation")].split(","))
    data[uni_name]["Importance"]["Legacy"] = find_importance(content[find_line(filepath,"Alumni")].split(","))
#    data[uni_name]["Importance"]["InState"] = find_importance(content[244].split(","))
    data[uni_name]["Importance"]["Volunteering"] = find_importance(content[find_line(filepath,"Volunteer")].split(","))

    data[uni_name]["Testing"] = {}
    data[uni_name]["Testing"]["Optional"] = True

    try:
        if (content[find_line(filepath,"SAT or ACT")].split(","))[1] != "":
            data[uni_name]["Testing"]["Optional"] = False

    except:
        pass

    try:
        data[uni_name]["Testing"]["LowSAT"] = [(content[find_line(filepath,"SAT Evidence-Based")].split(","))[1], (content[find_line(filepath,"SAT Math")].split(","))[1], (next(csv.reader([content[find_line(filepath,"SAT Composite")]])))[1]]
        data[uni_name]["Testing"]["MidSAT"] = [(content[find_line(filepath,"SAT Evidence-Based")].split(","))[2], (content[find_line(filepath,"SAT Math")].split(","))[2], (next(csv.reader([content[find_line(filepath,"SAT Composite")]])))[2]]
        data[uni_name]["Testing"]["TopSAT"] = [(content[find_line(filepath,"SAT Evidence-Based")].split(","))[3], (content[find_line(filepath,"SAT Math")].split(","))[3], (next(csv.reader([content[find_line(filepath,"SAT Composite")]])))[3]]
    
    except:
        data[uni_name]["Testing"]["LowSAT"] = 0
        data[uni_name]["Testing"]["MidSAT"] = 0
        data[uni_name]["Testing"]["TopSAT"] = 0

    try:
        data[uni_name]["Testing"]["LowACT"] = [(content[find_line(filepath,"ACT Math")].split(","))[1], (content[find_line(filepath,"ACT English")].split(","))[1], (content[find_line(filepath,"ACT Writing")].split(","))[1], (content[find_line(filepath,"ACT Science")].split(","))[1], (content[find_line(filepath,"ACT Reading")].split(","))[1], (content[find_line(filepath,"ACT Composite")].split(","))[1]]
        data[uni_name]["Testing"]["MidACT"] = [(content[find_line(filepath,"ACT Math")].split(","))[2], (content[find_line(filepath,"ACT English")].split(","))[2], (content[find_line(filepath,"ACT Writing")].split(","))[2], (content[find_line(filepath,"ACT Science")].split(","))[2], (content[find_line(filepath,"ACT Reading")].split(","))[2], (content[find_line(filepath,"ACT Composite")].split(","))[2]]
        data[uni_name]["Testing"]["TopACT"] = [(content[find_line(filepath,"ACT Math")].split(","))[3], (content[find_line(filepath,"ACT English")].split(","))[3], (content[find_line(filepath,"ACT Writing")].split(","))[3], (content[find_line(filepath,"ACT Science")].split(","))[3], (content[find_line(filepath,"ACT Reading")].split(","))[3], (content[find_line(filepath,"ACT Composite")].split(","))[3]]
    
    except:
        data[uni_name]["Testing"]["LowACT"] = 0
        data[uni_name]["Testing"]["MidACT"] = 0
        data[uni_name]["Testing"]["TopACT"] = 0

    try:
        data[uni_name]["Testing"]["AvgGPA"] = (content[find_line(filepath,"Average high school GPA")].split(","))[1]
    except:
        data[uni_name]["Testing"]["AvgGPA"] = 0

    data[uni_name]["Finances"] = {}
    try:
        data[uni_name]["Finances"]["Tuition"] = (next(csv.reader([content[find_line(filepath,"Tuition")]])))[2]

        if data[uni_name]["Finances"]["Tuition"] == '':
            data[uni_name]["Finances"]["Tuition"] = (next(csv.reader([content[find_line(filepath,"Tuition: Out-of-state")]])))[1]
    
    except:
        data[uni_name]["Finances"]["Tuition"] = 0

    try:
        data[uni_name]["Finances"]["RoomBoard"] = (next(csv.reader([content[find_line(filepath,"Room and board")]])))[2]
    except:
        data[uni_name]["Finances"]["RoomBoard"] = 0

    try:
        data[uni_name]["Finances"]["AvgAid"] = (next(csv.reader([content[find_line(filepath,"The average financial aid")]])))[2]

    except:
        data[uni_name]["Finances"]["AvgAid"] = 0


    with open("data.json", "w") as f:
        json.dump(data,f, indent=4)


def run_system(cdspath):
    convert_to_csv(cdspath)
    filename = cdspath.split(".")[0]
    input_data_from_csv(f"{filename}.csv")


"""
{
    "Univerity":{
        "Location":{
            "State": ""
        },
        "RaceGender":{
            "M": 0,
            "F": 0,
            "NonRes": 0,
            "Hispanic": 0,
            "Black": 0,
            "White":0,
            "Native":0,
            "Asian": 0,
            "PacIslander": 0,
            "TwoMoreNonHispanic": 0,
            "Unknown": 0
        },
        "Importance":{
            "GPA": 0,
            "Standardized": 0,
            "Essay": 0,
            "LORS": 0,
            "EC": 0,
            "FirstGen": 0,
            "Legacy": 0,
            "InState": 0,
            "Volunteering": 0
        },
        "Testing":{
            "Optional": false,
            "LowSAT": [],
            "MidSAT": [],
            "TopSAT": [],
            "LowACT": [],
            "MidACT": [],
            "TopACT": [], 
            "AvgGPA": 0
        },
        "Finances":{
            "Tuition": 0,
            "RoomBoard": 0,
            "AvgAid": 0
        },
        "Staff":{
            "StudentStaffRatio": 0
        }
    }
}
"""