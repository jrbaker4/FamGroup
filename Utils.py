import pandas as pd
from graph import *
import warnings
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
