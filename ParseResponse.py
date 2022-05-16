from cmath import nan
import pandas as pd
from graph import *
from difflib import SequenceMatcher
import numpy as np

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
    students_df = pd.read_csv(student_csv_file, index_col=False)
    student_dict = {}
    friends_dict = {}
    idxy = 0
    for index, student in students_df.iterrows():
        #Create Student objects
        name = student['Name']
        year = student['At the end of this year, how many years will you have been at NC State?']
        if year == "5+":
            year = 5
        year = int(year)
        sc_leader = (student['Do you lead a D-Group?'] == "Yes")
        fg_num = int(student['Future Fam group'])
        if fg_num ==-1:
            continue
        
        new_student = Student(idxy, name=name, year=year, sc_leader=sc_leader, maturity = -1, fg_num=(fg_num-1), female=(student['Gender'] == "Female"), discipler=student['Who is your D-Group Leader? If you have multiple, only choose one.'])
        student_dict[name] = new_student
        idxy +=1

        #Create Connection Matrix
        friends = []
        i = 24
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
    strictness = .8
    for key in student_dict:
        similarity = SequenceMatcher(None, name, key)
        if similarity.ratio() > strictness:
            return student_dict[key]
    return None

def create_conn_mat(student_dict, friends_dict):
    matched_students = np.zeros((len(student_dict.keys()), len(student_dict.keys())))
    for student in friends_dict:
        for name in friends_dict[student]:
            student_match = match_name_to_student(name, student_dict)
            if student_match is not None:
                matched_students[student_dict[student].id, student_match.id] = 1.0
            # else:
            #     print(name)
    return matched_students

# student_dict, friends_dict = parse_spread_sheet_create_dicts("SurveyResponse_3_21.csv")
# matched_students = create_conn_mat(student_dict, friends_dict)
# conn_mat = pd.DataFrame(matched_students)
