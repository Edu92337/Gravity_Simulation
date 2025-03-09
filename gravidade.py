import pygame,math
import numpy as np
from pygame.locals import *

simulacao_ativa = True
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulação")
clock = pygame.time.Clock()
running = True
dt = 1/60

G = 600
M = 400
m = 40

class Particula():
    def __init__(self):
        self.cores = ['blue', 'orange', 'purple', 'yellow', 'green']
        self.cor_inicial = self.cores[np.random.randint(0, 5)]
        self.cor = self.cor_inicial
        self.raio = 10
        self.posicao = pygame.Vector2(np.random.randint(screen.get_width() // 3, 2 * screen.get_width() // 3))
        self.velocidade = pygame.Vector2(np.random.randint(-20, 20), np.random.randint(-20, 20))
        self.aceleracao = pygame.Vector2(0, 0)
        self.tempo_vermelho = 0
    
    def draw(self):
        return pygame.draw.circle(screen, self.cor, self.posicao, self.raio)

    
    def movimento(self):
        v_meio_passo = self.velocidade + self.aceleracao * dt / 2
        self.posicao = self.posicao + v_meio_passo * dt
        self.velocidade = v_meio_passo + self.aceleracao * dt / 2
        
        #COLISÕES COM A JANELA
        if self.posicao.y + self.raio >= screen.get_height() or self.posicao.y <= self.raio:
            self.cor = 'red'
            self.tempo_vermelho = 10  # Partícula fica vermelha por 10 frames
            self.velocidade.y = - self.velocidade.y
            
        if self.posicao.x - self.raio <= 0 or self.posicao.x + self.raio >= screen.get_width():
            self.cor = 'red'
            self.tempo_vermelho = 10  # Partícula fica vermelha por 10 frames
            self.velocidade.x = - self.velocidade.x
        
        # Se o tempo for maior que 0, conta regressiva até voltar à cor original
        if self.tempo_vermelho > 0:
            self.tempo_vermelho -= 1
        else:
            self.cor = self.cor_inicial
        

def verifica_colisao(p1, p2, coef_rest=1.0):
    distancia = math.dist(p1.posicao, p2.posicao)
    if distancia <= (p1.raio + p2.raio):
        if p1.posicao - p2.posicao != 0:
            delta_posicao = p1.posicao - p2.posicao
            if delta_posicao.length() > 0:  # Verifica se o vetor não é nulo
                normal = delta_posicao.normalize()
            else:
                normal = pygame.Vector2(0, 0)
            tangencial = pygame.Vector2(-normal.y, normal.x)

            v1n = normal.dot(p1.velocidade)
            v1t = tangencial.dot(p1.velocidade)
            v2n = normal.dot(p2.velocidade)
            v2t = tangencial.dot(p2.velocidade)

            
            m1, m2 = 1, 1  
            v1n_nova = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2) * coef_rest
            v2n_nova = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2) * coef_rest

            
            p1.velocidade = tangencial * v1t + normal * v1n_nova
            p2.velocidade = tangencial * v2t + normal * v2n_nova

            # Reajuste de posições
            ajuste = (p1.raio + p2.raio - distancia) / 2
            p1.posicao += normal * ajuste
            p2.posicao -= normal * ajuste

def gravidade(pos1, pos2, massa=m, epsilon=1e-2):
    
    r = math.dist(pos1, pos2)
    if r < epsilon:
        return pygame.Vector2(0, 0)
    direcao = (pos2 - pos1).normalize()
    forca = G * M / (r**2)
    aceleracao = direcao * forca
    
    return aceleracao


#SIMULAÇÃO
n = np.random.randint(1,21)
particulas =[]

for _ in range(n):
    p = Particula()
    particulas.append(p)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    
    if simulacao_ativa:
        screen.fill("black")
            
        for particula in particulas:
            particula.draw()
            particula.movimento()
        for i in range(len(particulas)):
            for j in range(i+1,len(particulas)):
                verifica_colisao(particulas[i],particulas[j])
        
        
        mouse_clicked = pygame.mouse.get_pressed()
        if mouse_clicked[0] == True:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            for particula in particulas:
                # Verifica se a partícula está perto do ponto de gravidade
                if math.dist(particula.posicao, mouse_pos) < 25:  # Raio de tolerância
                    particula.velocidade = pygame.Vector2(0, 0)
                    particula.aceleracao = pygame.Vector2(0, 0)
                    particula.posicao = pygame.Vector2((mouse_pos.x+2*particula.raio,mouse_pos.y+2*particula.raio))
                else:
                    particula.aceleracao = gravidade(particula.posicao, mouse_pos)
        elif mouse_clicked[2] == True:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            for particula in particulas:
                # Verifica se a partícula está perto do ponto de gravidade
                if math.dist(particula.posicao, mouse_pos) < 25:  # Raio de tolerância
                    particula.velocidade = pygame.Vector2(0, 0)
                    particula.aceleracao = pygame.Vector2(0, 0)
                    particula.posicao = pygame.Vector2((mouse_pos.x+2*particula.raio,mouse_pos.y+2*particula.raio))
                else:
                    particula.aceleracao = -gravidade(particula.posicao, mouse_pos)
        else:
            for particula in particulas:
                particula.aceleracao = pygame.Vector2(0, 0)
                    


    
        pygame.display.flip()
        dt = clock.tick(60) / 1000

pygame.quit()