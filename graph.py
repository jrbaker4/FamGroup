import random
import numpy as np
from numpy.lib.function_base import average
import pygame
from pygame.display import update

class Student():
    def __init__(self, id = 0, name = "", year = 0, dg_leader_bool = False, maturity = 1, fg_num =0, female = True, xpos = None, ypos = None):
        if xpos is None:
            xpos = random.random()
        if ypos is None:
            ypos = random.random()
        self.id = id
        self.name = name
        self.year = year
        self.dg_leader_bool = dg_leader_bool
        self.maturity = maturity
        self.fg_num = fg_num
        self.female = female
        self.xpos = xpos
        self.ypos = ypos

class Fam_Group():
    def __init__(self, fg_num = 0, color=pygame.Color(), male_leader = None, female_leader = None, members = [], ave_maturity=0.0, ave_age=0.0, percent_male=0.0, connection_cost = 0.0, age_diversity = 0.0):
        self.fg_num = fg_num
        self.color = color
        self.members = members
        self.male_leader = male_leader
        self.female_leader = female_leader
        self.ave_maturity = ave_maturity
        self.ave_age =ave_age
        self.percent_female = percent_male
        self.connection_cost = connection_cost
        self.age_diversity = age_diversity

    def add_member(self, member, summit_college, update_statistics=True):
        self.members.append(member)
        if update_statistics:
            self.update_statistics(summit_college)

    def remove_member(self, old_member, summit_college, update_statistics=True):
        self.members.remove(old_member)
        if update_statistics:
            self.update_statistics(summit_college)

    def update_statistics(self, summit_college):
        self.update_connection_loss(summit_college)
        self.update_percent_female()
        self.update_age_diversity()
        self.update_average_age()
        
    def update_connection_loss(self, summit_college):
        cuts = 0
        for student in self.members:
            for friend in summit_college[student]:
                if friend.fg_num != self.fg_num:
                    cuts +=1
        self.connection_cost = cuts

    def update_average_age(self):
        age_sum = 0
        for student in self.members:
            age_sum += student.year 
        self.ave_age = (age_sum/len(self.members))

    def update_percent_female(self):
        num_females = 0
        for student in self.members:
            if student.female == 1:
                num_females += 1
        self.percent_female = num_females/(len(self.members))

    def update_age_diversity(self):
        #TODO FIGURE THIS OUT
        self.age_diversity = 0.0

class Summit_College():
    def __init__(self, node_dict = {}, fam_groups = []):
        self.node_dict = node_dict
        self.num_fgs = max([i.fg_num for i in node_dict.keys()]) 
        self.fam_groups = fam_groups
        for i in range(self.num_fgs +1):
            self.fam_group_colors.append(pygame.Color(  np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)))
    def get_all_students(self):
        return self.node_dict.keys
    

john = Student(0, "John", 2, "Logan", True, 6, "Logan")
john1 = Student(1, "Baker", 2, "Logan", True, 6, "Logan")
john2 = Student(2, "Randall", 3, "Logan", True, 6, "Logan")

test_dict = {
    john: [john1, john2],
    john1: [john],
    john2: [john]
    }

summit_college = Graph(test_dict)