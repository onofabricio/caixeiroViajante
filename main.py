from turtle import update, width
import pygame
import random
import numpy as np
from points import Point
import time
import os
import matplotlib.pyplot as plt

os.environ["SDL_VIDEO_CENTERED"] = '1'

largura, altura = 1000,1000
#cores
preto = (0,0,0)
branco = (255,255,255)
verde = (0,255,0)

#pygame settings
pygame.init()
pygame.display.set_caption("Problema do Caixeiro Viajante")
screen = pygame.display.set_mode((largura, altura))

#variables 
pontos = []
offset_screen = 50
menor_caminho = []
record_distance = 0
nr_de_pontos = 100

#gera pontos aleatorios na screen
for n in range(nr_de_pontos):
    x = random.randint(offset_screen, largura - offset_screen)
    y = random.randint(offset_screen, altura - offset_screen)
    
    point = Point(x,y)
    pontos.append(point)
    
#embaralha a posição dos pontos da lista
def shuffle(a, b, c):
    temp = a[b]
    a[b] = a[c]
    a[c] = temp
    
#distance between point using pythagorean theorem
def calcula_distancia(pontos):
    total = 0
    for n in range(len(pontos)-1):
        distancia = ((pontos[n].x - pontos[n+1].x)**2 + (pontos[n].y - pontos[n+1].y)**2)**0.5
        total += distancia 
    return total

dist = calcula_distancia(pontos)
record_distance = dist
menor_caminho = pontos.copy()

run = True

#Exibição dos pontos
for n in range(len(pontos)):
        pygame.draw.circle(screen, branco, (pontos[n].x, pontos[n].y), 10)
pygame.display.update()
time.sleep(3)

#inicio das iterações por força bruta
cont=1
while run:
    cont += 1
    screen.fill(preto)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    #desenha linhas e pontos
    
    for n in range(len(pontos)):
        pygame.draw.circle(screen, branco, (pontos[n].x, pontos[n].y), 10)
    
    a = random.randint(0, len(pontos)-1)
    b = random.randint(0, len(pontos)-1)
    shuffle(pontos, a, b)
    dist = calcula_distancia(pontos)
    if dist < record_distance:
        record_distance = dist
        menor_caminho = pontos.copy()
        
        print("iteração: ", cont,"|| distancia do menor caminho", record_distance)
        
    for m in range(len(pontos)-1):
        pygame.draw.line(screen, branco, (pontos[m].x, pontos[m].y), (pontos[m+1].x, pontos[m+1].y), 2)
    
    for m in range(len(menor_caminho)-1):
        pygame.draw.line(screen, verde, (menor_caminho[m].x, menor_caminho[m].y), (menor_caminho[m+1].x, menor_caminho[m+1].y), 2)
    
    pygame.display.update()
    cont += 1
    
    
print("A menor distancia é: ", record_distance)
pygame.quit()