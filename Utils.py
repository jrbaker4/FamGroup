import pandas as pd
from graph import *
import warnings
from ParseResponse import *
warnings.filterwarnings("ignore", message="divide by zero encountered in log")
warnings.filterwarnings("ignore", message="invalid value encountered in multiply")
def calculate_total_cost(summit_college):
    A=1
    total_cut_cost = calculate_cut_loss(summit_college)
    B=1
    total_gender_cost = calculate_gender_cost(summit_college)
    C=1
    number_of_members_cost = fam_size_cost(summit_college)
    D=1
    total_maturity_cost = maturity_cost(summit_college)
    
    #TODO AGE COST
    total_cost = A*total_cut_cost + B*total_gender_cost + C*number_of_members_cost + D*total_maturity_cost
    
    return total_cost, A*total_cut_cost, B*total_gender_cost, C*number_of_members_cost, D*total_maturity_cost
def calculate_cut_loss(summit_college):
    total_cut_cost = 0
    for fam_group in summit_college.fam_groups:
        total_cut_cost += fam_group.connection_cost*len(fam_group.members)
    return total_cut_cost

def calculate_gender_cost(summit_college):
    total_gender_loss = 0
    #Max loss per fam group is 2.5
    for fam_group in summit_college.fam_groups:
        total_gender_loss += 10*(fam_group.percent_female - .5)**2 #parabola loss
    return total_gender_loss

def fam_size_cost(summit_college):
    fam_sizes = []
    for fam_group in summit_college.fam_groups:
        fam_sizes.append(len(fam_group.members))
    np_fam_sizes = np.array(fam_sizes)

    #standard deviation normalized by mean
    return np.std(np_fam_sizes)/np.mean(np_fam_sizes)

def KL_div(p,q):
    new_p = p[q!=0]
    new_q = q[q!=0]
    poop = np.where(new_p!=0, new_p * np.log(new_p / new_q), 0) #Silenced a ton of warnings. Could be broken....
    return np.sum(poop)

def maturity_cost(summit_college):
    mat_cost = 0
    all_mats = []
    for student in summit_college.get_all_students():
        all_mats.append(student.maturity)
    all_mat_distr, _ = np.histogram(all_mats, bins=10, range=[0,10])
    norm_all_dist = (all_mat_distr/len(all_mats))
    for fam_group in summit_college.fam_groups:
        fam_group_mats = []
        if len(fam_group.members) == 0:
            continue
        for student in fam_group.members:
            fam_group_mats.append(student.maturity)
        fam_mats_distr, _ = np.histogram(fam_group_mats, bins=10, range=[0,10])
        norm_fam_dist = (fam_mats_distr/len(fam_group_mats))
        KL_div_score = KL_div(norm_fam_dist, norm_all_dist)
        mat_cost += KL_div_score
    return mat_cost

def save_student_files(student_dict, conns_df):
    conns_df.to_csv('conn_mat.csv')
    students_data = []
    for student_id in student_dict:
        student = student_dict[student_id]
        student_data = [student.id, student.name, student.year, student.sc_leader, student.maturity, student.fg_num, student.female, student.discipler, student.xpos, student.ypos]
        students_data.append(student_data)
    student_df = pd.DataFrame(students_data, columns=["id", "name", "year", "sc_leader", "maturity", "fg_num", "Female", "discipler", "x_pos", "y_pos"])
    student_df.to_csv("students.csv")

def parse_spread_sheet_create_graph(survey_file, save_files=False):
    student_name_dict, friends_dict = parse_spread_sheet_create_dicts(survey_file)
    matched_students = create_conn_mat(student_name_dict, friends_dict)
    conns_df = pd.DataFrame(matched_students)
    #Student dict is a dic where name is the key, we need to change it to index being the key cause I'm too lazy to make better code
    student_dict = {}
    for stud in student_name_dict:
        id = student_name_dict[stud].id
        student_dict[id] = student_name_dict[stud]

    sc_graph = {}
    for indx, row in conns_df.iterrows():
        things_to_add = []
        for idx, value in row.iteritems():
            if value == 1:
                things_to_add.append(student_dict[int(idx)])
        sc_graph[student_dict[int(indx)]] = things_to_add

    if save_files:
        save_student_files(student_dict, conns_df)
        
    return sc_graph 
