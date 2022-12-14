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
from pyparsing import condition_as_parse_action
from shapely.wkt import loads
from shapely.geometry import LineString
os.environ["SDL_VIDEO_CENTERED"] = '1'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ordem = 0
        self.nome = ""
        
    def defineNome(self, nome):
        self.nome = nome
        return self


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
    font = pygame.font.SysFont('bahnschrift', int(largura*0.025)) #fonte a ser usada nas variaveis
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
            textRect_iteracao.center = (largura*0.1, altura*0.02) # define a posição do centro do retangulo acima
            screen.blit(texto_iteracao, textRect_iteracao)
            
            
            texto_menorcaminho = font.render('iteração: '+str(record_cont)+' || distancia do menor caminho: '+str(record_distance), True, branco)
            textRect_menorcaminho = texto_menorcaminho.get_rect()
            textRect_menorcaminho.center = (largura*0.4, altura*0.94)
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




def algoritmoGenetico(pontos, distancia_gravada, menor_caminho, tela ,branco, verde, preto, run):
    
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
        #print("sorteio_pai: ",sorteio_pai," pai: ",pai)
        #print("sorteio_mae: ",sorteio_mae," mae: ",mae)
        return pai, mae
    
    def definePontosDeCrossover(df):
        
        a = random.randint(0, len(df['caminho'][0]))
        b = a
        while a == b:
            b = random.randint(0, len(df['caminho'][0]))
        if a<b:
            pontos = [a,b]
        elif a>b:
            pontos = [b,a]
            
        return pontos
     
    def definePontosDeCrossoverV2(lista):
        
        #f(x) = x^0.4
        taxa_de_crossover = 0.4
        print("qtes de pontos de cross", int(len(lista)**(taxa_de_crossover)))
        qtde = int(len(lista)**(taxa_de_crossover))
        qtde = 3
        pontos_de_crossover = [0 for i in range(qtde)]
    
        while len(set(pontos_de_crossover)) < len(pontos_de_crossover):
            pontos_de_crossover = [random.randint(0, len(lista)-1) for i in range(qtde)] 
        pontos_de_crossover = [None] + sorted(pontos_de_crossover) + [None]
        print(pontos_de_crossover)
        return pontos_de_crossover
        
           
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
        
        
        for i in range(len(df)):
            if df['id'][i] == pai:
                caminho_pai = df['caminho'][i]
            elif df['id'][i] == mae:
                caminho_mae = df['caminho'][i]
                
        caminho_mae = caminho_mae[:-1]
        caminho_pai = caminho_pai[:-1] 
          
        pontos_de_crossover = definePontosDeCrossover(df) # 2 pontos fixos
        #pontos_de_crossover = definePontosDeCrossoverV2(caminho_mae) # X pontos, de acordo com o tamanho do caminho
        #print("pontos de crossover", pontos_de_crossover)
        
        gameta_pai = caminho_pai[pontos_de_crossover[0]:pontos_de_crossover[1]]
        gameta_mae = caminho_mae[pontos_de_crossover[0]:pontos_de_crossover[1]]
        filho1 = list(dict.fromkeys(caminho_pai[:pontos_de_crossover[0]]+gameta_mae+caminho_pai[pontos_de_crossover[1]:]))
        filho2 = list(dict.fromkeys(caminho_mae[:pontos_de_crossover[0]]+gameta_pai+caminho_mae[pontos_de_crossover[1]:]))
        filho3 = list(dict.fromkeys(caminho_pai[:pontos_de_crossover[1]]+caminho_mae[pontos_de_crossover[1]:]))
        filho4 = list(dict.fromkeys(caminho_mae[:pontos_de_crossover[1]]+caminho_pai[pontos_de_crossover[1]:]))
        filho5 = list(dict.fromkeys(caminho_pai[:pontos_de_crossover[0]]+caminho_mae[pontos_de_crossover[0]:]))
        filho6 = list(dict.fromkeys(caminho_mae[:pontos_de_crossover[0]]+caminho_pai[pontos_de_crossover[0]:]))
    
        filhos = [filho1, filho2, filho3, filho4, filho5, filho6]
        for filho in filhos:    
            for i in range(len(caminho_pai)):
                p = caminho_pai[i]
                if p not in filho:
                    filho.append(p)
        for filho in filhos:         
            for i in range(len(caminho_mae)):
                p = caminho_mae[i]
                if p not in filho:
                    filho.append(p)                
        
        #mutação
        for filho in filhos:
            filho = mutacao(filho)
            filho.append(filho[0])
        
        
        return filhos
         
    def crossoverV2(df, pai, mae):
        
        for i in range(len(df)):
            if df['id'][i] == pai:
                caminho_pai = df['caminho'][i]
            elif df['id'][i] == mae:
                caminho_mae = df['caminho'][i]
                
        caminho_mae = caminho_mae[:-1]
        caminho_pai = caminho_pai[:-1] 
        
        
        
        pontos_de_crossover = definePontosDeCrossoverV2(caminho_mae) # X pontos, de acordo com o tamanho do caminho
        
        #print(pontos_de_crossover)

        filhos = {}
        pedaco_pai = {}
        pedaco_mae = {}
        
        for i in range(len(pontos_de_crossover)-1):
            pedaco_pai[i] = caminho_pai[pontos_de_crossover[i]:pontos_de_crossover[i+1]]
            pedaco_mae[i] = caminho_mae[pontos_de_crossover[i]:pontos_de_crossover[i+1]]
        
        #print(pedaco_mae)
        #print(pedaco_pai)
            
        filhos = [list(itertools.chain.from_iterable(i)) for i in itertools.product(*zip(pedaco_pai.values(), pedaco_mae.values()))]
        #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        #print(filhos[0])
        #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        
        for filho in filhos:
            for i in range(len(caminho_pai)):
                p = caminho_pai[i]
                if p not in filho:
                    filho.append(p)
        for filho in filhos:
            for i in range(len(caminho_mae)):
                p = caminho_mae[i]
                if p not in filho:
                    filho.append(p)
        
        #mutação
        #print(filhos)
        for filho in filhos:
            filho = mutacao(filho)
            filho.append(filho[0])
        #print("="*20)
        #print(filhos)
        return filhos
    
    def crossoverV3(df,pai,mae):
        
        #Simple inversion crossover (Holland) 
        
        for i in range(len(df)):
            if df['id'][i] == pai:
                caminho_pai = df['caminho'][i]
            elif df['id'][i] == mae:
                caminho_mae = df['caminho'][i]
                
        caminho_mae = caminho_mae[:-1]
        caminho_pai = caminho_pai[:-1] 
          
        pontos_de_crossover = definePontosDeCrossover(df) # 2 pontos fixos
        
        gameta_pai = caminho_pai[pontos_de_crossover[0]:pontos_de_crossover[1]]
        gameta_mae = caminho_mae[pontos_de_crossover[0]:pontos_de_crossover[1]]
        filho1 = list(dict.fromkeys(caminho_pai[:pontos_de_crossover[0]]+gameta_mae+caminho_pai[pontos_de_crossover[1]:]))
        filho2 = list(dict.fromkeys(caminho_mae[:pontos_de_crossover[0]]+gameta_pai+caminho_mae[pontos_de_crossover[1]:]))
        filho3 = list(dict.fromkeys(caminho_pai[:pontos_de_crossover[1]]+caminho_mae[pontos_de_crossover[1]:]))
        filho4 = list(dict.fromkeys(caminho_mae[:pontos_de_crossover[1]]+caminho_pai[pontos_de_crossover[1]:]))
        filho5 = list(dict.fromkeys(caminho_pai[:pontos_de_crossover[0]]+caminho_mae[pontos_de_crossover[0]:]))
        filho6 = list(dict.fromkeys(caminho_mae[:pontos_de_crossover[0]]+caminho_pai[pontos_de_crossover[0]:]))
        
        #V3
       
        filho7 = list(dict.fromkeys(caminho_pai[:pontos_de_crossover[0]]+list(reversed(gameta_pai))+caminho_pai[pontos_de_crossover[1]:]))
        filho8 = list(dict.fromkeys(caminho_mae[:pontos_de_crossover[0]]+list(reversed(gameta_mae))+caminho_mae[pontos_de_crossover[1]:]))
        filho9 = list(dict.fromkeys(caminho_pai[:pontos_de_crossover[0]]+list(reversed(gameta_mae))+caminho_pai[pontos_de_crossover[1]:]))
        filho10 = list(dict.fromkeys(caminho_mae[:pontos_de_crossover[0]]+list(reversed(gameta_pai))+caminho_mae[pontos_de_crossover[1]:]))
    
        filhos = [filho1, filho2, filho3, filho4, filho5, filho6, filho7, filho8, filho9, filho10]
        for filho in filhos:    
            for i in range(len(caminho_pai)):
                p = caminho_pai[i]
                if p not in filho:
                    filho.append(p)
        for filho in filhos:         
            for i in range(len(caminho_mae)):
                p = caminho_mae[i]
                if p not in filho:
                    filho.append(p)                
        
        #mutação
        for filho in filhos:
            filho = mutacao(filho)
            filho.append(filho[0])
        
        return filhos
    
    def addFilhosNaPopulacao(df, filhos):
        
        
        novos_caminhos = [filho for filho in filhos]
        novos_ids = [max(df['id'])+i for i in range(1,len(filhos)+1)]
        novas_distancias = [calcula_distancia(filho) for filho in filhos]
        novos_fitness = [0 for i in range(len(filhos))]
        novos_pedacos = [0 for i in range(len(filhos))]
        
        novo_df = pd.DataFrame(list(zip(novos_ids, novos_caminhos, novas_distancias, novos_fitness, novos_pedacos)), columns = ['id','caminho', 'distancias','fitness','pedaco'])
        
        df = pd.concat([df,novo_df], axis=0, ignore_index=True)
        
        return df
    
    
    def eliminaXpiores(df, filhos):
        
        X = len(filhos) #Numero de individuos a serem eliminados na seleção natural
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
        print("=============APOCALIPSE=============")
        #sobrevivente = df.head(1)
        #print(sobrevivente)
        populacao_nova = [geraCaminhoAleatorio(pontos) for i in range(nr_de_cromossomos)]
        distancias = [calcula_distancia(caminho) for caminho in populacao_nova]
        ids = [i for i in range(1,len(populacao_nova)+1)]
        df = pd.DataFrame(list(zip(ids, populacao_nova, distancias)), columns = ['id','caminho', 'distancias'])
        df = calculaFitness(df)
        #df = pd.concat([df,sobrevivente], ignore_index=True)
        #print("nova população\n",df)
        time.sleep(10)
        return df
    
    
    def verificaPoligonoSimples(df):
        caminho = df['caminho'][0]
        caminho = caminho[:-1]
        print(caminho)
        
        
        G = nx.Graph()
        for i in range(len(caminho)):
            G.add_node(i, pos=(caminho[i].x, -caminho[i].y))
            
        for i in range(len(caminho)-1):
            G.add_edge(i, i+1)
        G.add_edge(len(caminho)-1, 0)
    
            
        pontos=nx.get_node_attributes(G,'pos')
        #print(pontos)
        
        v = loads(LineString([pontos[i] for i in range(len(pontos))]).wkt)
        
        #print("v", v)
        if v.is_simple == True:
            nx.draw(G, pontos)
            plt.text(min([ponto.x for ponto in df['caminho'][0]]) - 10,  -(min([ponto.y for ponto in df['caminho'][0]]) - 10),'Solução ótima')
            plt.show()
            cond = True
            #time.sleep(10)
        else:
            df = apocalipse(df)
            cond = False
        
        return df, cond
    
    def verificaConvergencia(df):
        
        vec = []
        for i in range(len(df)):
            vec.append(int(df['distancias'][i]))
           
        #print("len(set(vec)): ",len(set(vec))) 
        
        if len(set(vec)) == 1:
            df, cond = verificaPoligonoSimples(df)
            
        else:
            cond = False
            pass
        
        return df, cond
        
    def novaGeracao(df):
        
        df = calculoDaPizza(df) #calculo da pizza
        pai, mae = selecaoDePais(df) #selecao de pais
        #filhos = crossover(df,pai,mae)#crossover entre pais
        #filhos = crossoverV2(df,pai,mae)
        filhos = crossoverV3(df,pai,mae)
        df = addFilhosNaPopulacao(df,filhos)#add filhos na população
        df = eliminaXpiores(df, filhos) #eliminar X piores
        #print("nova geração: \n",df)
         
        return df
    
    
    font = pygame.font.SysFont('bahnschrift', int(altura*0.025)) #fonte a ser usada nas variaveis
    distancia_gravada = np.inf
    

    nr_de_cromossomos = int(0.5*len(pontos))
    populacao_inicial = [geraCaminhoAleatorio(pontos) for i in range(nr_de_cromossomos)]
    distancias = [calcula_distancia(caminho) for caminho in populacao_inicial]
    ids = [i for i in range(1,len(populacao_inicial)+1)]
    df = pd.DataFrame(list(zip(ids, populacao_inicial, distancias)), columns = ['id','caminho', 'distancias'])
    df = calculaFitness(df)

    
    
    print(geracao,"\n", len(df))
    time.sleep(3)
    while run:
        df = calculaFitness(df)
        #print("geracao ",geracao,": \n",df)
        if len(df) < 100:
            for i in range(len(df)):
                tela.fill(preto)
                caminho = df['caminho'][i]
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                
                #desenha pontos
                
                for n in range(len(pontos)):
                    pygame.draw.circle(tela, branco, (pontos[n].x, pontos[n].y), 5)
                    texto_nome = font.render(''+str(pontos[n].nome), True, branco) # cria um objeto de superficie para a fonte
                    textRect_nome = texto_nome.get_rect() # cria uma superficie retangular para texto 
                    textRect_nome.center = (pontos[n].x, pontos[n].y - 20) # define a posição do centro do retangulo acima
                    tela.blit(texto_nome, textRect_nome)
                    
                for m in range(len(caminho)-1):
                    pygame.draw.line(tela, branco, (caminho[m].x, caminho[m].y), (caminho[m+1].x, caminho[m+1].y), 1)
                
                #Variaveis na tela
                texto_id = font.render('id cromossomo: '+str(df['id'][i]), True, branco) # cria um objeto de superficie para a fonte
                textRect_id = texto_id.get_rect() # cria uma superficie retangular para texto 
                textRect_id.center = (largura*0.2, altura*0.02) # define a posição do centro do retangulo acima
                tela.blit(texto_id, textRect_id)
                
                texto_dist = font.render('distancia: '+str(df['distancias'][i]), True, branco) # cria um objeto de superficie para a fonte
                textRect_dist = texto_dist.get_rect() # cria uma superficie retangular para texto 
                textRect_dist.center = (largura*0.2, altura*0.98) # define a posição do centro do retangulo acima
                tela.blit(texto_dist, textRect_dist)
                
                texto_dist = font.render('geração: '+str(geracao), True, branco) # cria um objeto de superficie para a fonte
                textRect_dist = texto_dist.get_rect() # cria uma superficie retangular para texto 
                textRect_dist.center = (largura*0.9, altura*0.02) # define a posição do centro do retangulo acima
                tela.blit(texto_dist, textRect_dist)
                
                texto_indiv = font.render('individuos diferentes: '+str(len(set([df['distancias'][i] for i in range(len(df))]))), True, branco) # cria um objeto de superficie para a fonte
                textRect_indiv = texto_indiv.get_rect() # cria uma superficie retangular para texto 
                textRect_indiv.center = (largura*0.8, altura*0.98) # define a posição do centro do retangulo acima
                tela.blit(texto_indiv, textRect_indiv)
                    
                
                pygame.display.update()
                #time.sleep(1)
        else:
            print(geracao,"\n", df)
            melhor_cromossomo = 0
            
        df, cond = verificaConvergencia(df)   
        distancia_gravada = min([d for d in df['distancias']])
        if cond == True: break 
        #print(df)
        df = novaGeracao(df)
        geracao+=1
            
    return distancia_gravada
       
         
       
       
largura, altura = 1600, 900
#cores
preto = (0,0,0)
branco = (255,255,255)
verde = (0,255,0)

#pygame settings
pygame.init()
pygame.display.set_caption("Problema do Caixeiro Viajante") 
tela = pygame.display.set_mode((largura, altura))

#variaveis
pontos = []
margem = 50
menor_caminho = []
distancia_gravada = 0
nr_de_pontos = 60

#gera pontos aleatorios na tela
for n in range(nr_de_pontos):
    x = random.randint(margem, largura - margem)
    y = random.randint(margem, altura - margem)
    
    point = Point(x,y)
    pontos.append(point)
    
    
caminho = constroiCaminho(pontos)
dist = calcula_distancia(caminho)
distancia_gravada = dist
menor_caminho = pontos.copy()
run = True

#capitais 
capitais = {'AC': [ -8.77, -70.55]  , 'AL': [ -9.71, -35.73], 'AM': [ -3.07, -61.66]  , 
            'AP': [  1.41, -51.77]  , 'BA': [-12.96, -38.51]  , 'CE': [ -3.71, -38.54]  , 
            'DF': [-15.83, -47.86]  , 'ES': [-19.19, -40.34]  , 'GO': [-16.64, -49.31]  , 
            'MA': [ -2.55, -44.30]  , 'MT': [-12.64, -55.42]  , 'MS': [-20.51, -54.54]  , 
            'MG': [-18.10, -44.38]  , 'PA': [ -5.53, -52.29]  , 'PB': [ -7.06, -35.55]  , 
            'PR': [-24.89, -51.55]  , 'PE': [ -8.28, -35.07]  , 'PI': [ -8.28, -43.68]  , 
            'RJ': [-22.84, -43.15]  , 'RN': [ -5.22, -36.52]  , 'RO': [-11.22, -62.80]  , 
            'RS': [-30.01, -51.22]  , 'RR': [  1.89, -61.22]  , 'SC': [-27.33, -49.44]  , 
            'SE': [-10.90, -37.07] , 'SP': [-23.55, -46.64]  , 'TO': [-10.25, -48.25]}
pontos=[]
for estado in capitais:
    capitais[estado] = (np.array(capitais[estado])*18)
    capitais[estado][1] = capitais[estado][1]+1700
    capitais[estado][0] = capitais[estado][0]*-1
    capitais[estado][0] = capitais[estado][0]+250
for estado in capitais:
    x = capitais[estado][1]
    y = capitais[estado][0]
    nome = estado
    point = Point(x,y).defineNome(nome)
    pontos.append(point)
    
caminho = constroiCaminho(pontos)
dist = calcula_distancia(caminho)
distancia_gravada = dist
menor_caminho = pontos.copy()

#Exibição dos pontos
for n in range(len(pontos)):
        pygame.draw.circle(tela, branco, (pontos[n].x, pontos[n].y), 5)
pygame.display.update()
time.sleep(3)

agr = time.time()
#inicio das iterações por força bruta
#distancia_gravada = forcaBruta(pontos, distancia_gravada, menor_caminho, tela ,branco, verde, preto, run)
distancia_gravada = algoritmoGenetico(pontos, distancia_gravada, menor_caminho, tela ,branco, verde, preto, run)
    
dps = time.time() - agr
print("tempo de execução: ", dps)    
    
print("A menor distancia é: ", distancia_gravada)
