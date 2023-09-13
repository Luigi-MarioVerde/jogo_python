import pygame
import random
from pygame.locals import *

# Definição de cores e imagens
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)

cogumeload = pygame.image.load('play/monstro.png')
cogumelofigura = pygame.transform.scale(cogumeload, (120, 120))
miraload = pygame.image.load('play/mira.png')
mira = pygame.transform.scale(miraload, (30, 30))
cenario = pygame.image.load('play/cenario-r4.png')
personagemload = pygame.image.load('play/personagem.png')
personagem = pygame.transform.scale(personagemload, (200, 200))
personagem2load = pygame.image.load('play/personagem2.png')
personagem2 = pygame.transform.scale(personagem2load, (200, 200))

# Definição de texto, alvo cogumelo, função de clique e som de tiro
def texto(msg, cor, tam, x, y):
    font = pygame.font.SysFont(None, tam)
    texto1 = font.render(msg, True, cor)
    tela.blit(texto1, [x, y])

def cogumeloalvo(cogumelox, cogumeloy):
    cogumelo = cogumelofigura.get_rect()
    cogumelo.center = (cogumelox, cogumeloy)
    tela.blit(cogumelofigura, cogumelo)

def click(cogumelox, cogumeloy):
    mouse = pygame.mouse.get_pos()
    cogumelo_hitbox = cogumelofigura.get_rect()
    cogumelo_hitbox.center = (cogumelox, cogumeloy)
    return cogumelo_hitbox.collidepoint(mouse)

def tocar_som(som):
    pygame.mixer.music.load(som)
    pygame.mixer.music.play()

# Inicialização e demais configurações
pygame.init()
tela = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Teste sua mira')

clock = pygame.time.Clock()

DIREITA = 1
ESQUERDA = 0
FORA = 1
DENTRO = 0
contador = 10

sentido = DIREITA
status = FORA
cogumelox = 0
cogumeloy = random.randint(50, 500)
cogumelolargura, cogumeloaltura = 120, 120

armax = 10
armay = 10

# Ajuste das coordenadas para posicionar o personagem no canto inferior direito
armax = tela.get_width() - personagem.get_width() - 10
armay = tela.get_height() - personagem.get_height() - 10

vida_alvo = 100  # Vida inicial do alvo

atirando = False

# Velocidade do monstro
velocidade = 40

# Controle de movimento do monstro
movendo = True

# Loop principal do jogo - mouseclick, reiniciar e movimentação do alvo cogumelo
while True:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == MOUSEBUTTONDOWN and contador > 0:
            mouse_pos = pygame.mouse.get_pos()
            if movendo and click(cogumelox, cogumeloy):
                contador -= 1
                vida_alvo -= 20  # Diminui a vida do alvo em 20 quando acerta
                tocar_som('play/SOM DE TIRO.mp3')
            else:
                atirando = True
                tocar_som('play/SOM DE TIRO.mp3')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                contador = 10
                vida_alvo = 100
                movendo = True
                atirando = False

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:  # Botão esquerdo do mouse
                atirando = False

    if sentido == DIREITA and movendo:
        cogumelox += velocidade
    if sentido == ESQUERDA and movendo:
        cogumelox -= velocidade

    if cogumelox < -cogumelolargura or cogumelox > tela.get_width():
        sentido = random.randint(0, 1)
        if sentido == 0:
            sentido = ESQUERDA
            cogumelox = tela.get_width()
        elif sentido == 1:
            sentido = DIREITA
            cogumelox = -cogumelolargura
        cogumeloy = random.randint(50, 500)

    # Definições de exibição na tela
    pygame.mouse.set_visible(False)
    tela.blit(cenario, (0, 0))
    cogumeloalvo(cogumelox, cogumeloy)
    tela.blit(mira, pygame.mouse.get_pos())

    if atirando:
        tela.blit(personagem2, (armax, armay))
    else:
        tela.blit(personagem, (armax, armay))

    pygame.draw.rect(tela, preto, [145, 0, 310, 45])
    pygame.draw.rect(tela, branco, [150, 0, 300, 40])
    pygame.draw.rect(tela, vermelho, [150, 0, ((300) / 100) * vida_alvo, 40])  # Barra de vida proporcional à vida_alvo

    if contador <= 0:
        texto("Você venceu!", preto, 50, 200, 300)
        texto("Aperte R para reiniciar.", preto, 40, 140, 330)
        movendo = False

    pygame.display.update()
