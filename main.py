from turtle import update, width
import pygame
import random
import numpy as np
import pandas as pd
import time
import os
import math
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from shapely.wkt import loads
from shapely.geometry import LineString
os.environ["SDL_VIDEO_CENTERED"] = '1'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ordem = 0


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
            textRect_menorcaminho.center = (400, 940)
            screen.blit(texto_menorcaminho, textRect_menorcaminho)
            
            pygame.display.update()
            cont += 1
        print("Qtde de iterações", cont)
        time.sleep(10)
        run = False
        #pygame.display.quit()
        #pygame.quit()
        #sys.exit()
    return record_distance




def algoritmoGenetico(pontos, record_distance, menor_caminho, screen ,branco, verde, preto, run):
    
    geracao = 1
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
    
    
    def calculoDaPizza(df):
        pizza=[]
        soma = 0
        for i in range(len(df)):
            soma += df['fitness'][i]
            pizza.append(soma)
        
        df['pedaco'] = pizza
        return df
    
    
    def selecaoDePais(df):
        pai=0
        mae=0
        
        
        while pai == mae:
            sorteio_pai = random.random()
            sorteio_mae = random.random()
        
            for i in range(len(df)):
                if sorteio_pai < df['pedaco'][i]:
                    pai = df['id'][i]
                    break
                
            for i in range(len(df)):
                if sorteio_mae < df['pedaco'][i]:
                    mae = df['id'][i]
                    break
        print("sorteio_pai: ",sorteio_pai," pai: ",pai)
        print("sorteio_mae: ",sorteio_mae," mae: ",mae)
        return pai, mae
    
    def definePontosDeCrossover(df):
        
        a = random.randint(0, len(df['caminho'][0])-1)
        b = a
        while a == b:
            b = random.randint(0, len(df['caminho'][0])-1)
        if a<b:
            pontos = [a,b]
        elif a>b:
            pontos = [b,a]
            
        return pontos
        
    def mutacao(vec):
        
        taxa_de_mutacao = 0.01
        #10 pontos, tx = 0.8, geracao_convergente = não convergiu
        #10 pontos, tx = 0.5, geracao_convergente = não convergiu
        #10 pontos, tx = 0.25, geracao_convergente = 1100, solução não-planar
        #10 pontos, tx = 0.15, geracao_convergente = 715
        #10 pontos, tx = 0.10, geracao_convergente = 400
        #15 pontos, tx = 0.8, geracao_convergente = não convergiu
        #15 pontos, tx = 0.5, geracao_convergente = não convergiu
        #15 pontos, tx = 0.25, geracao_convergente = não convergiu, mas achou solução ótima na geração 28000
        #15 pontos, tx = 0.15, geracao_convergente = 3400
        #15 pontos, tx = 0.10, geracao_convergente = 1100
        iteracoes = taxa_de_mutacao*len(vec)
        if iteracoes < 1:
            iteracoes = 1
        for i in range(int(iteracoes)):
            a = random.randint(0, len(vec)-1)
            b = a
            while a == b:
                b = random.randint(0, len(vec)-1)
                
            aux = vec[a]
            vec[a] = vec[b]
            vec[b] = aux
         
         
        return vec
    
    def crossover(df, pai, mae):
        
        # 
        for i in range(len(df)):
            if df['id'][i] == pai:
                caminho_pai = df['caminho'][i]
            elif df['id'][i] == mae:
                caminho_mae = df['caminho'][i]
                
        caminho_mae = caminho_mae[:-1]
        caminho_pai = caminho_pai[:-1] 
          
        pontos_de_crossover = definePontosDeCrossover(df)
        print("pontos de crossover", pontos_de_crossover)
        
        gameta_pai = caminho_pai[pontos_de_crossover[0]:pontos_de_crossover[1]]
        gameta_mae = caminho_mae[pontos_de_crossover[0]:pontos_de_crossover[1]]
        filho = caminho_pai[:pontos_de_crossover[0]]+gameta_mae+caminho_pai[pontos_de_crossover[1]:]
        filha = caminho_mae[:pontos_de_crossover[0]]+gameta_pai+caminho_mae[pontos_de_crossover[1]:]
        
        filho = list(dict.fromkeys(filho))
        filha = list(dict.fromkeys(filha))
            
        for i in range(len(caminho_pai)):
            p = caminho_pai[i]
            if p not in filho:
                filho.append(p)
                
        for i in range(len(caminho_mae)):
            p = caminho_mae[i]
            if p not in filha:
                filha.append(p)                
        
        #mutação
        filho = mutacao(filho)
        filha = mutacao(filha)
        
        filho.append(filho[0])
        filha.append(filha[0])
        
        
        
        
        return filho, filha
         
        
    def addFilhosNaPopulacao(df, filho, filha):
        
        novos_caminhos = [filho, filha]
        novos_ids = [max(df['id'])+1, max(df['id'])+2]
        novas_distancias = [calcula_distancia(filho), calcula_distancia(filha)]
        novos_fitness = [0,0]
        novos_pedacos = [0,0]
        
        novo_df = pd.DataFrame(list(zip(novos_ids, novos_caminhos, novas_distancias, novos_fitness, novos_pedacos)), columns = ['id','caminho', 'distancias','fitness','pedaco'])
        
        df = pd.concat([df,novo_df], axis=0, ignore_index=True)
        
        return df
    
    
    def eliminaXpiores(df):
        
        X = 2 #Numero de individuos a serem eliminados na seleção natural
        for i in range(X):
            maior_distancia = 0
            for i in range(len(df)):
                if df['distancias'][i] > maior_distancia:
                    maior_distancia = df['distancias'][i]
                    id_maior_distancia = df['id'][i]
                    
            #print("1 maior distancia: ", id_maior_distancia)
            df = df[df.id != id_maior_distancia]
            df.reset_index(drop = True, inplace = True)
        
        return df
    
    
    def apocalipse(df):
        
        sobrevivente = df.head(1)
        print(sobrevivente)
        populacao_nova = [geraCaminhoAleatorio(pontos) for i in range(nr_de_cromossomos)]
        distancias = [calcula_distancia(caminho) for caminho in populacao_nova]
        ids = [i for i in range(1,len(populacao_nova)+1)]
        df = pd.DataFrame(list(zip(ids, populacao_nova, distancias)), columns = ['id','caminho', 'distancias'])
        df = calculaFitness(df)
        df = pd.concat([df,sobrevivente])
        plt.show()
        return df
    
    
    def verificaPoligonoSimples(df):
        caminho = df['caminho'][0]
        caminho = caminho[:-1]
        print(caminho)
        
        
        G = nx.Graph()
        for i in range(len(caminho)):
            G.add_node(i, pos=(caminho[i].x, caminho[i].y))
            
        for i in range(len(caminho)-1):
            G.add_edge(i, i+1)
        G.add_edge(len(caminho)-1, 0)
    
            
        pontos=nx.get_node_attributes(G,'pos')
        print(pontos)
        
        v = loads(LineString([pontos[i] for i in range(len(pontos))]).wkt)
        
        print("v", v)
        if v.is_simple == True:
            nx.draw(G, pontos)
            plt.text(30, 0,'Solução ótima')
            plt.show()
            time.sleep(10)
        else:
            apocalipse(df)
        
        return df
    
    def verificaConvergencia(df):
        
        vec = []
        for i in range(len(df)):
            vec.append(int(df['distancias'][i]))
           
        print("len(set(vec)): ",len(set(vec))) 
        if len(set(vec)) == 1:
            df = verificaPoligonoSimples(df)
            
        else:
            pass
        
        return df
        
    def novaGeracao(df):
        
        df = calculoDaPizza(df) #calculo da pizza
        pai, mae = selecaoDePais(df) #selecao de pais
        filho, filha = crossover(df,pai,mae)#crossover entre pais
        df = addFilhosNaPopulacao(df,filho, filha)#add 2 filhos na população
        df = eliminaXpiores(df) #eliminar X piores
        #print("nova geração: \n",df)
         
        return df
    
    
    font = pygame.font.SysFont('bahnschrift', 24) #fonte a ser usada nas variaveis
    record_distance = np.inf

    nr_de_cromossomos = 6
    populacao_inicial = [geraCaminhoAleatorio(pontos) for i in range(nr_de_cromossomos)]
    distancias = [calcula_distancia(caminho) for caminho in populacao_inicial]
    ids = [i for i in range(1,len(populacao_inicial)+1)]
    df = pd.DataFrame(list(zip(ids, populacao_inicial, distancias)), columns = ['id','caminho', 'distancias'])
    df = calculaFitness(df)

    
    

    while run:
        df = calculaFitness(df)
        print("geracao ",geracao,": \n",df)
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
            textRect_id.center = (largura*0.2, altura*0.02) # define a posição do centro do retangulo acima
            screen.blit(texto_id, textRect_id)
            
            texto_dist = font.render('distancia: '+str(df['distancias'][i]), True, branco) # cria um objeto de superficie para a fonte
            textRect_dist = texto_dist.get_rect() # cria uma superficie retangular para texto 
            textRect_dist.center = (largura*0.2, altura*0.98) # define a posição do centro do retangulo acima
            screen.blit(texto_dist, textRect_dist)
            
            texto_dist = font.render('geração: '+str(geracao), True, branco) # cria um objeto de superficie para a fonte
            textRect_dist = texto_dist.get_rect() # cria uma superficie retangular para texto 
            textRect_dist.center = (largura*0.9, altura*0.02) # define a posição do centro do retangulo acima
            screen.blit(texto_dist, textRect_dist)
                
            
            pygame.display.update()
            #time.sleep(1)
        
        verificaConvergencia(df)   
        df = novaGeracao(df)
        geracao+=1
            
    return record_distance
       
       
       
       
       
       
       
       
largura, altura = 1000, 1000
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
nr_de_pontos = 25

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
#record_distance = forcaBruta(pontos, record_distance, menor_caminho, screen ,branco, verde, preto, run)
algoritmoGenetico(pontos, record_distance, menor_caminho, screen ,branco, verde, preto, run)
    
 
    
print("A menor distancia é: ", record_distance)
