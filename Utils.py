import pandas as pd
from graph import *
def calculate_edge_cut_loss(original_graph, cuts):
    cost = 0
    for cut in cuts:
        cost += cut.weight

def parse_spread_sheet_create_graph(student_csv_file, conn_matrix_csv):
    students_df = pd.read_csv(student_csv_file, index_col=0)
    student_dict = {}
    for index, student in students_df.iterrows():
        new_student = Student(index, student['name'],student['year'], bool(student['sc_leader']), student['maturity'], student['fg_num'], bool(student['female']))
        student_dict[index] = new_student

    conns_df = pd.read_csv(conn_matrix_csv)
    sc_graph = {}
    for indx, row in conns_df.iterrows():
        things_to_add = []
        for idx, value in row.iteritems():
            if value == 1:
                things_to_add.append(student_dict[int(idx)])
        sc_graph[student_dict[int(indx)]] = things_to_add
    return sc_graph
#graph = parse_spread_sheet_create_graph('students.csv', 'conn_matrix.csv')
