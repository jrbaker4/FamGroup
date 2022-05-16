import networkx as nx
import csv
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import blackman
import pygame
from pygame.locals import *
import sys

from sqlalchemy import true
from graph import *
from Utils import *

WHITE = pygame.Color(255, 255, 255) 
BLACK = pygame.Color(0, 0, 0)

def display_graph(screen, graph):
    #Draw nodes
    screen.fill(pygame.Color(255, 255, 255))
    #display_student_info_rect(screen)
    for student in graph.node_dict:
        x = (student.xpos*screen.get_width())
        y = (student.ypos*screen.get_height())
        pygame.draw.circle(screen, graph.fam_groups[student.fg_num].color, (x,y),10)
    #Draw edges
    for student in graph.node_dict:
        friends = graph.node_dict[student]
        for friend in friends:
            pygame.draw.line(screen, pygame.Color(0, 0, 0), (student.xpos*screen.get_width(), student.ypos*screen.get_height()), (friend.xpos*screen.get_width(), friend.ypos*screen.get_height()), 1)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def display_student_info_rect(screen, box_width, box_height):
    pygame.draw.rect(screen, BLACK, pygame.Rect((screen.get_width()/2)-box_width/2, 0,box_width, box_height), 2)

def display_cost_rect(screen, box_width, box_height):
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, screen.get_height() - 250, box_width, box_height), 2)
    pygame.display.update()

def clear_student_info(screen, box_width, box_height):
    screen.fill(WHITE, pygame.Rect((screen.get_width()/2)-box_width/2, 0, box_width, box_height))

def centered_text_display(text, screen, x, y, font_size):
    largeText = pygame.font.Font('freesansbold.ttf',font_size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def left_text_display(text, screen, x, y, font_size):
    largeText = pygame.font.Font('freesansbold.ttf',font_size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.topleft = (x,y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def display_student_info(student, screen):
    box_height = 50
    box_width = 250
    clear_student_info(screen, box_width, box_height)
    display_student_info_rect(screen, box_width, box_height)
    centered_text_display(student.name, screen, screen.get_width()/2, box_height/2, 20)

def display_total_cost(screen, graph):
    box_height = 50
    box_width = 800
    display_cost_rect(screen, box_width, box_height)
    #centered_text_display("Total Cost", screen, box_width/2, screen.get_height() - 260, 20)
    total_cost, cut_cost, gender_cost, number_of_members_cost, maturity_cost = calculate_total_cost(graph)
    cost_string = "Total Cost: " + str(round(total_cost,2)) + ", Cut Cost: " + str(round(cut_cost,2)) + ", Gender Cost: " + str(round(gender_cost,2)) + ", Numbers Cost: " + str(round(number_of_members_cost,2))+ ", Maturity Cost: " + str(round(maturity_cost,2))
    centered_text_display(cost_string, screen, box_width/2, screen.get_height() - (250 - box_height/2), 15)

def convert_fg_stats_to_text(fg_stats):
    text_blocks = []
    text_blocks.append('Family Group Number: ' + str(fg_stats['fg_num'])) 
    text_blocks.append('Number of Students: ' + str(len(fg_stats['members'])))
    text_blocks.append('Average Maturity: ' + str(round(fg_stats['ave_maturity'], 2)))
    text_blocks.append("Average Age: " + str(round(fg_stats['ave_age'], 2)))
    text_blocks.append("Percent Female: " + str(round(fg_stats['percent_female'], 2)))
    text_blocks.append("Connection Cost per Student: " + str(round(fg_stats['connection_cost'], 2)))
    return text_blocks

def display_fam_group_stats(screen, graph):
    box_width = screen.get_width()
    box_height = 200
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, screen.get_height() - box_height,box_width, box_height), 2)
    stats = graph.gather_fam_group_stats()
    for i in range(len(graph.fam_groups)):
        fg_stats = stats[i]
        color = fg_stats['color']
        x_loc = (i)*(box_width/len(graph.fam_groups))
        y_loc = screen.get_height() - box_height
        pygame.draw.rect(screen, color, pygame.Rect(x_loc, y_loc, 30, 30))
        texts = convert_fg_stats_to_text(fg_stats)
        for count, text in enumerate(texts):
            left_text_display(text, screen, x_loc + 30, y_loc +5 + 15*count, 12)

def find_nearest_node(mouse_x, mouse_y, graph, screen):
    min_dist = 1000000000
    nearest_student = Student()
    for student in graph.node_dict:
        dist = np.sqrt((student.xpos*screen.get_width() - mouse_x)**2 + (student.ypos*screen.get_height() - mouse_y)**2)
        if dist <= min_dist:
            nearest_student = student
            min_dist = dist
    return nearest_student

def main_display(graph):
    pygame.init()
    #screen=pygame.display.set_mode([1500, 800])
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill(WHITE)

    display_graph(screen, graph)
    x = 0
    y = 0
    newx_pos = 0
    newy_pos = 0
    drawing = False
    mainloop = True
    active_student = Student()
    while mainloop:
        pygame.display.update()
        x, y = pygame.mouse.get_pos()
        hover_student = find_nearest_node(x, y, graph, screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False  # Set running to False to end the while loop.
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                x, y = pygame.mouse.get_pos()
                active_student = find_nearest_node(x, y, graph, screen)
                drawing=True
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_p] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    print_reports(graph)
            elif event.type == MOUSEMOTION:
                if drawing:
                    newx_pos, newy_pos =  pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP:
                if drawing:
                    newx_pos, newy_pos =  pygame.mouse.get_pos()
                if button==1:
                    active_student.xpos = newx_pos/screen.get_width()
                    active_student.ypos = newy_pos/screen.get_height()
                elif button==3: #Change Fam Group
                    
                    old_fam_group = graph.fam_groups[active_student.fg_num]
                    old_fam_group.remove_member(active_student, graph)
                    fam_groups_to_update = []
                    for friend in graph.node_dict[active_student]:
                        fam_groups_to_update.append(friend.fg_num)
                    active_student.fg_num = (active_student.fg_num + 1) % len(graph.fam_groups)
                    new_fam_group = graph.fam_groups[active_student.fg_num]
                    new_fam_group.add_member(active_student, graph)

                    for fg in set(fam_groups_to_update):
                        graph.fam_groups[fg].update_connection_loss_per_student(graph)

                drawing=False
                display_graph(screen, graph)
                display_fam_group_stats(screen, graph)
                display_total_cost(screen, graph)
        display_student_info(hover_student, screen)
                
graph = parse_survey_create_graph("SurveyResponse_3_21.csv", true)
#graph = parse_files_create_graph()
summit_college = Summit_College(graph)
#print_report(summit_college)
main_display(summit_college)
