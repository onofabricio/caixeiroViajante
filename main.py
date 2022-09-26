from turtle import update, width
import pygame
import random
import numpy as np
from points import Point
import time
import os
import matplotlib.pyplot as plt
import math
import itertools

os.environ["SDL_VIDEO_CENTERED"] = '1'


def DistanciaDe(a,b):
    return math.sqrt((b.x-a.x)**2 + (b.y-a.y)**2)

def SomaDistancias(pontos):
    s=0
    for i in range(len(pontos)):
        dist = DistanciaDe(pontos[i], pontos[(i+1) % len(pontos)])
 
def constroiCaminho(pontos):
    caminho = pontos.copy()
    caminho.append(pontos[0])
    return caminho
    
           
#calcula distancia usando teorema de pitagoras, construindo caminho euleriano
def calcula_distancia(caminho):
    total = 0
    for n in range(len(caminho)-1):
        distancia = ((caminho[n].x - caminho[n+1].x)**2 + (caminho[n].y - caminho[n+1].y)**2)**0.5
        total += distancia 
        
    return total



#embaralha a posição dos pontos da lista
def shuffle(pontos):
    a=0
    b=0
    while a == b:
        a = random.randint(0, len(pontos)-1)
        b = random.randint(0, len(pontos)-1)
        
    temp = pontos[a]
    pontos[a] = pontos[b]
    pontos[b] = temp
    
def forcaBruta(pontos, record_distance, menor_caminho, screen ,branco, verde, preto, run):
    
    
    cont=0
    caminhos_possiveis = itertools.permutations(pontos)
    while run:
        for pontos in caminhos_possiveis:
            pontos = list(pontos)
            screen.fill(preto)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
            #desenha pontos
            
            for n in range(len(pontos)):
                pygame.draw.circle(screen, branco, (pontos[n].x, pontos[n].y), 10)
            
            
            
            caminho = constroiCaminho(pontos)
            dist = calcula_distancia(caminho)
            
            if dist < record_distance:
                record_distance = dist
                menor_caminho = caminho.copy()
                
                print("iteração: ", cont,"|| distancia do menor caminho", record_distance)
            
            for m in range(len(menor_caminho)-1):
                pygame.draw.line(screen, verde, (menor_caminho[m].x, menor_caminho[m].y), (menor_caminho[m+1].x, menor_caminho[m+1].y), 5)  
                
            for m in range(len(caminho)-1):
                pygame.draw.line(screen, branco, (caminho[m].x, caminho[m].y), (caminho[m+1].x, caminho[m+1].y), 1)
            
            
            pygame.display.update()
            cont += 1
        print("Qtde de iterações", cont)
        time.sleep(3)
        pygame.display.update()
        run = False
    
    return pontos
       
largura, altura = 1000,1000
#cores
preto = (0,0,0)
branco = (255,255,255)
verde = (0,255,0)

#pygame settings
pygame.init()
pygame.display.set_caption("Problema do Caixeiro Viajante")
screen = pygame.display.set_mode((largura, altura))

#variaveis 
pontos = []
offset_screen = 50
menor_caminho = []
record_distance = 0
nr_de_pontos = 6

#gera pontos aleatorios na screen
for n in range(nr_de_pontos):
    x = random.randint(offset_screen, largura - offset_screen)
    y = random.randint(offset_screen, altura - offset_screen)
    
    point = Point(x,y)
    pontos.append(point)
    
    
caminho = constroiCaminho(pontos)
dist = calcula_distancia(caminho)
record_distance = dist
menor_caminho = pontos.copy()

run = True

#Exibição dos pontos
for n in range(len(pontos)):
        pygame.draw.circle(screen, branco, (pontos[n].x, pontos[n].y), 10)
pygame.display.update()
time.sleep(3)

#inicio das iterações por força bruta
forcaBruta(pontos, record_distance, menor_caminho, screen ,branco, verde, preto, run)
    
    
    
print("A menor distancia é: ", record_distance)
pygame.quit()