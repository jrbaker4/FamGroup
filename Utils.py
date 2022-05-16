import pandas as pd
from graph import *
import warnings
from ParseResponse import *
import matplotlib.pyplot as plt
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
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

def parse_survey_create_graph(survey_file, save_files=False):
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

#def parse_files_create_graph():
    #TODO read from files not survey!
    # students_df = pd.read_csv("students.csv")
    # conns_mat = pd.read_csv('conn_mat.csv')
    # for student in students_df

def create_age_demographic_figure(summit_college, fam_group):
    all_ages = []
    fam_ages = []
    for student in summit_college.get_all_students():
        all_ages.append(student.year)
    for student in fam_group.members:
        fam_ages.append(student.year)
    plt.hist(all_ages, bins=[.5,1.5,2.5,3.5,4.5,5.5], align='mid', density=True, ls='dotted',lw=3, alpha = 0.9, color='b', label="All Summit College")
    plt.hist(fam_ages, bins=[.5,1.5,2.5,3.5,4.5,5.5], align='mid', density=True, ls='dashed',lw=3, alpha = 0.9, color='r', label="Family Group")
    plt.legend()
    plt.xlabel('Years at State')
    plt.ylabel('Percent of students')
    plt.title("Demographics of Years at State", size=16)
    plt.show()

def create_maturity_demographic_figure(summit_college, fam_group):
    all_ages = []
    fam_ages = []
    for student in summit_college.get_all_students():
        all_ages.append(student.maturity)
    for student in fam_group.members:
        fam_ages.append(student.maturity)
    plt.hist(all_ages, bins=[.5,1.5,2.5,3.5,4.5,5.5, 6.5, 7.5, 8.5, 9.5, 10.5], align='mid', density=True, ls='dotted',lw=3, alpha = 0.9, color='b', label="All Summit College")
    plt.hist(fam_ages, bins=[.5,1.5,2.5,3.5,4.5,5.5, 6.5, 7.5, 8.5, 9.5, 10.5], align='mid', density=True, ls='dashed',lw=3, alpha = 0.9, color='r', label="Family Group")
    plt.legend()
    plt.xlabel('Maturity')
    plt.ylabel('Percent of students')
    plt.title("Demographics of Student Maturity", size=16)
    plt.show()

def create_gender_demographic_figure(summit_college, fam_group, ):
    all_genders = []
    fam_genders = []
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10,10))
    for student in summit_college.get_all_students():
        all_genders.append(int(student.female))
    total_percent_female = np.sum(all_genders)/len(all_genders)
    total_percent_male = 1.0- total_percent_female

    for student in fam_group.members:
        fam_genders.append(int(student.female))
    fam_percent_female = np.sum(fam_genders)/len(fam_genders)
    fam_percent_male = 1.0- fam_percent_female

    ax1.pie([fam_percent_female, fam_percent_male], explode = (.1,0), labels=["Female", "Male"], autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.set_title("Gender Percentage of Family Group")

    ax2.pie([total_percent_female, total_percent_male], explode = (.1,0), labels=["Female", "Male"], autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax2.set_title("Gender Percentage of Summit College")
    save_path = dir_path + "/report/" + "gender_fig_" + str(fam_group.fg_num) + ".png" 
    fig.savefig(save_path)
    plt.close(fig)
    return fig

def print_report(summit_college):
    for fam_group in summit_college.fam_groups:
        #age_fig = create_age_demographic_figure(fam_group, graph)
        gender_fig = create_gender_demographic_figure(summit_college, fam_group)
           # save the figure to file
        
        #maturity_fig = create_maturity_demographic_figure(fam_group, graph)
        #influence_fig = create_influential_figure(fam_group, graph)