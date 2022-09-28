from turtle import update, width
import pygame
import random
import numpy as np
import pandas as pd
from points import Point
import time
import os
import math
import itertools
import sys
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
    font = pygame.font.SysFont('bahnschrift', 24) #fonte a ser usada nas variaveis
    record_distance = np.inf
    record_cont = 0

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
                record_cont = cont
                
                print("iteração: ", record_cont,"|| distancia do menor caminho", record_distance)
                
                
            
            for m in range(len(menor_caminho)-1):
                pygame.draw.line(screen, verde, (menor_caminho[m].x, menor_caminho[m].y), (menor_caminho[m+1].x, menor_caminho[m+1].y), 5)  
                
            for m in range(len(caminho)-1):
                pygame.draw.line(screen, branco, (caminho[m].x, caminho[m].y), (caminho[m+1].x, caminho[m+1].y), 1)
            
            #Variaveis na tela
            texto_iteracao = font.render(str(cont+1)+'/'+str(np.math.factorial(len(pontos))), True, branco) # cria um objeto de superficie para a fonte
            textRect_iteracao = texto_iteracao.get_rect() # cria uma superficie retangular para texto 
            textRect_iteracao.center = (100, 20) # define a posição do centro do retangulo acima
            screen.blit(texto_iteracao, textRect_iteracao)
            
            
            texto_menorcaminho = font.render('iteração: '+str(record_cont+1)+' || distancia do menor caminho: '+str(record_distance), True, branco)
            textRect_menorcaminho = texto_menorcaminho.get_rect()
            textRect_menorcaminho.center = (400, 670)
            screen.blit(texto_menorcaminho, textRect_menorcaminho)
            
            pygame.display.update()
            cont += 1
        print("Qtde de iterações", cont)
        time.sleep(1000)
        run = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()
    return record_distance




def algoritmoGenetico(pontos, record_distance, menor_caminho, screen ,branco, verde, preto, run):
    
    def geraCaminhoAleatorio(pontos):
        caminho = np.random.permutation(pontos)
        caminho = list(caminho)
        caminho.append(caminho[0])
        return caminho        
    
    def calculaFitness(df):
        soma=0
        for i in range(len(df)):
            distancia = df['distancias'][i]
            soma = soma + (1/distancia)
        vec_fitness = []
        for i in range(len(df)):
            vec_fitness.append((1/df['distancias'][i])/soma)
        df['fitness'] = vec_fitness
            
        return df 
    
    def novaGeracao(df):
        
        #calculo da pizza
        #selecao de pais
        #crossover entre pais
        #https://www.youtube.com/watch?v=lcS-fv8tiEA
        #add 3 filhos na população
        #eliminar 3 piores
         
        return df
    
    cont=0
    caminhos_possiveis = itertools.permutations(pontos)
    font = pygame.font.SysFont('bahnschrift', 24) #fonte a ser usada nas variaveis
    record_distance = np.inf
    record_cont = 0
    nr_de_cromossomos = 6
    populacao_inicial = [geraCaminhoAleatorio(pontos) for i in range(nr_de_cromossomos)]
    distancias = [calcula_distancia(caminho) for caminho in populacao_inicial]
    ids = [i for i in range(1,len(populacao_inicial)+1)]
    df = pd.DataFrame(list(zip(ids, populacao_inicial, distancias)), columns = ['id','caminho', 'distancias'])
    df = calculaFitness(df)
    print(df)
    
    

    while run:
        for i in range(len(df)):
            screen.fill(preto)
            caminho = df['caminho'][i]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            #desenha pontos
            
            for n in range(len(pontos)):
                pygame.draw.circle(screen, branco, (pontos[n].x, pontos[n].y), 10)
                
            for m in range(len(caminho)-1):
                pygame.draw.line(screen, branco, (caminho[m].x, caminho[m].y), (caminho[m+1].x, caminho[m+1].y), 1)
            
            #Variaveis na tela
            texto_id = font.render('id cromossomo: '+str(df['id'][i]), True, branco) # cria um objeto de superficie para a fonte
            textRect_id = texto_id.get_rect() # cria uma superficie retangular para texto 
            textRect_id.center = (100, 20) # define a posição do centro do retangulo acima
            screen.blit(texto_id, textRect_id)
            
            texto_dist = font.render('distancia: '+str(df['distancias'][i]), True, branco) # cria um objeto de superficie para a fonte
            textRect_dist = texto_dist.get_rect() # cria uma superficie retangular para texto 
            textRect_dist.center = (200, 670) # define a posição do centro do retangulo acima
            screen.blit(texto_dist, textRect_dist)
            
                
            
            pygame.display.update()
            time.sleep(2)
            
    return record_distance
       
       
       
       
       
       
       
       
largura, altura = 700, 700
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
nr_de_pontos = 10

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
record_distance = forcaBruta(pontos, record_distance, menor_caminho, screen ,branco, verde, preto, run)
#algoritmoGenetico(pontos, record_distance, menor_caminho, screen ,branco, verde, preto, run)
    
 
    
print("A menor distancia é: ", record_distance)
