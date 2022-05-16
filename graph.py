import random
import numpy as np
from numpy.lib.function_base import average
import pygame
from pygame.display import update

class Student():
    def __init__(self, id = 0, name = "", year = 0, sc_leader = False, maturity = 1, fg_num =0, female = True, discipler = -1, xpos = None, ypos = None):
        if xpos is None:
            xpos = random.random()
        if ypos is None:
            ypos = random.random()
        self.id = id
        self.name = name
        self.year = year
        self.sc_leader = sc_leader
        self.maturity = maturity
        self.fg_num = fg_num
        self.female = female
        self.discipler = discipler
        self.xpos = xpos
        self.ypos = ypos

class Fam_Group():
    def __init__(self, fg_num = -1, color=None, male_leader = None, female_leader = None, members = [], ave_maturity=0.0, ave_age=0.0, percent_female=0.0, connection_cost = 0.0, age_diversity = 0.0, x = None, y =None):
        self.fg_num = fg_num
        self.color = color
        self.members = members
        self.male_leader = male_leader
        self.female_leader = female_leader
        self.ave_maturity = ave_maturity
        self.ave_age =ave_age
        self.percent_female = percent_female
        self.connection_cost = connection_cost
        self.age_diversity = age_diversity
        if x is None:
            x = random.random()
        if y is None:
            y = random.random()
        self.centroid = (x, y)

    def __eq__(self, other):
        return self.fg_num == other.fg_num
    def __ne__(self, other):
        return self.fg_num != other.fg_num

    def add_member(self, member, summit_college, update_statistics=True):
        member.fg_num = self.fg_num
        self.members.append(member)
        if update_statistics:
            self.update_statistics(summit_college)

    def remove_member(self, old_member, summit_college, update_statistics=True):
        #old_member.fg_num = -1
        self.members.remove(old_member)
        if update_statistics:
            self.update_statistics(summit_college)

    def update_statistics(self, summit_college):
        self.update_connection_loss_per_student(summit_college)
        self.update_percent_female()
        self.update_age_diversity()
        self.update_average_age()
        self.update_average_maturity()

    def update_average_maturity(self):
        tot_mat = 0
        for student in self.members:
            tot_mat += student.maturity
        if len(self.members) != 0:
            self.ave_maturity = tot_mat/len(self.members)
        else:
            self.ave_maturity = 0.0
        
    def update_connection_loss_per_student(self, summit_college):
        cuts = 0
        for student in self.members:
            for friend in summit_college.node_dict[student]:
                if friend.fg_num != self.fg_num:
                    cuts +=1
        if len(self.members) != 0:
            self.connection_cost = cuts/len(self.members)
        else:
            self.connection_cost = 0

    def update_average_age(self):
        age_sum = 0
        for student in self.members:
            age_sum += student.year 
        if len(self.members) != 0:
            self.ave_age = (age_sum/len(self.members))
        else:
            self.ave_age = 0.0

    def update_percent_female(self):
        num_females = 0
        for student in self.members:
            if student.female == 1:
                num_females += 1
        if len(self.members) != 0:
            self.percent_female = num_females/(len(self.members))
        else:
            self.percent_female = 0.0

    def update_age_diversity(self):
        #TODO FIGURE THIS OUT
        self.age_diversity = 0.0

class Summit_College():
    def __init__(self, node_dict = {}, fam_groups = []):
        self.node_dict = node_dict
        num_fgs = len(set([x.fg_num for x in self.node_dict.keys()]))
        self.fam_groups = fam_groups

        #Create list of appropriate size to hold all the fam groups
        if len(fam_groups) == 0:
            self.fam_groups = [None]*num_fgs
        #Create fam groups and add students to correct fam groups
        for student in self.node_dict.keys():
            new_fam_group = None
            fg = None
            if student not in self.fam_groups:
                new_fam_group = Fam_Group(fg_num=student.fg_num, color = pygame.Color(  np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)), members=[])
                student.xpos =  min(abs(np.random.normal(new_fam_group.centroid[0], .05)), .95)
                student.ypos =  min(abs(np.random.normal(new_fam_group.centroid[1], .05)), .8)
                new_fam_group.add_member(student, self, False)
                self.fam_groups[student.fg_num -1] = new_fam_group
            else:
                fg = self.fam_groups[self.fam_groups.index(student)]
                student.xpos = min(abs(np.random.normal(fg.centroid[0], .05)), .95)
                student.ypos = min(abs(np.random.normal(fg.centroid[1], .05)), .8)
                fg.add_member(student, self, False)
        #calc all statistics for the FGs
        for fg in self.fam_groups:
            fg.update_statistics(self)
        
    def get_all_students(self):
        return self.node_dict.keys()
    
    def gather_fam_group_stats(self):
        fg_stats = {}
        for fg in self.fam_groups:
            fg_stats[fg.fg_num] = vars(fg)
        return fg_stats
# john = Student(0, "John", 2, "Logan", True, 0, "Logan")
# john1 = Student(1, "Baker", 2, "Logan", True, 1, "Logan")
# john2 = Student(2, "Randall", 3, "Logan", True, 1, "Logan")

# test_dict = {
#     john: [john1, john2],
#     john1: [john],
#     john2: [john]
#     }

# summit_college = Summit_College(test_dict)