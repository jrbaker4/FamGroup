import networkx as nx
import csv
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import blackman
import pygame
from pygame.locals import *
import sys
from graph import *
from Utils import *

WHITE = pygame.Color(255, 255, 255) 
BLACK = pygame.Color(0, 0, 0)

def display_graph(screen, graph):
    #Draw nodes
    screen.fill(pygame.Color(255, 255, 255))
    display_student_info_rect(screen)
    for student in graph.node_dict:
        x = (student.xpos*screen.get_width())
        y = (student.ypos*screen.get_height())
        pygame.draw.circle(screen, graph.fam_group_colors[student.fg_num], (x,y),10)
    #Draw edges
    for student in graph.node_dict:
        friends = graph.node_dict[student]
        for friend in friends:
            pygame.draw.line(screen, pygame.Color(0, 0, 0), (student.xpos*screen.get_width(), student.ypos*screen.get_height()), (friend.xpos*screen.get_width(), friend.ypos*screen.get_height()), 1)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def display_student_info_rect(screen):
    box_width = 100
    box_height = 50
    pygame.draw.rect(screen, BLACK, pygame.Rect((screen.get_width()/2)-box_width/2,0,box_width, box_height), 2)

def message_display(text, screen, x, y, font_size):
    largeText = pygame.font.Font('freesansbold.ttf',font_size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def display_student_info(student, screen):
    box_height = 50
    display_student_info_rect(screen)
    message_display(student.name, screen, screen.get_width()/2, box_height/2, 20)
    
def find_nearest_node(mouse_x, mouse_y, graph, screen):
    min_dist = 1000000000
    nearest_student = Student()
    for student in graph.node_dict:
        dist = np.sqrt((student.xpos*screen.get_width() - mouse_x)**2 + (student.ypos*screen.get_height() - mouse_y)**2)
        if dist <= min_dist:
            nearest_student = student
            min_dist = dist
    return nearest_student

def display_fam_group_stats(screen, graph):
    box_width = 300
    box_height = 300
    pygame.draw.rect(screen, BLACK, pygame.Rect(0,screen.get_height() - box_height,box_width, box_height), 2)
    stats = graph.gather_fam_group_stats()
def main_display(graph):
    pygame.init()
    screen=pygame.display.set_mode([1500, 800])
    screen.fill(WHITE)

    display_graph(screen, graph)
    x = 0
    y = 0
    newx_pos = 0
    newy_pos = 0
    drawing = False
    active_student = Student()
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            active_student = find_nearest_node(x, y, graph, screen)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                drawing=True
            elif event.type == MOUSEMOTION:
                if drawing:
                    newx_pos, newy_pos =  pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP:
                if drawing:
                    newx_pos, newy_pos =  pygame.mouse.get_pos()
                if button==1:
                    active_student.xpos = newx_pos/screen.get_width()
                    active_student.ypos = newy_pos/screen.get_height()
                elif button==3:
                    active_student.fg_num = (active_student.fg_num + 1) % 3
                display_graph(screen, graph)
                display_fam_group_stats(screen, graph)
                display_student_info(active_student, screen)
                drawing=False


graph = parse_spread_sheet_create_graph('students.csv', 'conn_matrix.csv')
summit_college = Summit_College(graph)

main_display(summit_college)
