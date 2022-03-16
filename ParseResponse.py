from cmath import nan
import pandas as pd
import sys
from graph import *

FG_MAP = {"Andrew Baker":0,
            "Vivian and Silas":1,
            "Mikato and Nicole":2,
            "Andrew W. and Mara":3,
            "Kandis and Kobe":4,
            "Michael Smith and Emma S.":5,
            "Tripp, Trey, and Claire":6,
            "Campbell and Adah":7,
            "Michael H. and Aidan":8}


def parse_spread_sheet_create_dicts(student_csv_file):
    students_df = pd.read_csv(student_csv_file, index_col=0)
    student_dict = {}
    friends_dict = {}

    for index, student in students_df.iterrows():
        #Create Student objects
        name = student['Name']
        year = student['At the end of this year, how many years will you have been at NC State?']
        if year == "5+":
            year = 5
        sc_leader = (student['Do you lead a D-Group?'] == "Yes")
        fg_num = FG_MAP[student['Who are your family group leaders?']]
        new_student = Student(index, name=name, year=year, sc_leader=sc_leader, maturity = -1, fg_num=fg_num, female=(student['Gender'] == "Female"), discipler=student['Who is your D-Group Leader? If you have multiple, only choose one.'])
        student_dict[name] = new_student

        #Create Connection Matrix
        friends = []
        i = 23
        end = False
        while i < 33 and end is False:
            column_name = "Unnamed: " + str(i)
            i += 1
            friend = student[column_name]
            if not pd.isna(friend):
                friends.append(friend)
        friends_dict[name] = friends
    return student_dict, friends_dict
def match_name_to_student(name, student_dict):
    for key in student_dict:
        if name == key:
            return student_dict[key]

def create_conn_mat(student_dict, friends_dict):
    for name in friends_dict:
        for name in friends_dict[name]:
            match_name_to_student(name, student_dict)


student_dict, friends_dict = parse_spread_sheet_create_dicts("SurveyResponse_3_15.csv")
create_conn_mat(student_dict, friends_dict)