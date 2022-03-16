import pandas as pd
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
def parse_spread_sheet_create_graph(student_csv_file):
    students_df = pd.read_csv(student_csv_file, index_col=0)
    student_dict = {}


    for index, student in students_df.iterrows():
        name = student['name']
        year = student['At the end of this year, how many years will you have been at NC State?']
        if year == "5+":
            year = 5
        sc_leader = (student['Do you lead a D-Group?'] == "Yes")
        fg_num = FG_MAP[student['Who are your family group leaders?']]
        new_student = Student(index, name=name, year=year, sc_leader=sc_leader, maturity = -1, fg_num=fg_num, female=(student['Gender'] == "Female"), discipler=student['Who is your D-Group Leader? If you have multiple, only choose one.'])
        student_dict[index] = new_student

    
    return student_dict