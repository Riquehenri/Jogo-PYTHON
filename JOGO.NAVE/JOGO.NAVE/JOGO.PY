from random import randint
import pygame
from pygame import font
from pygame import display
from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import event
from pygame.locals import QUIT, KEYUP, K_SPACE, K_r, K_q
from pygame.time import Clock

pygame.init()

tamanho = 800, 600
fonte = font.SysFont('comicsans', 50)
fonte_perdeu = font.SysFont('comicsans', 100)

superficie = display.set_mode(size=tamanho)
display.set_caption('Destruidor de aliens')

fundo = scale(load('images/space.jpg'), tamanho)

class Nave(Sprite):
    def __init__(self, tiros):
        super().__init__()
        self.image = load('images/pixels.png')
        self.image = pygame.transform.scale(self.image, (130, 130)) 
        self.rect = self.image.get_rect(center=(80, 300))
        self.tiros = tiros
        self.velocidade = 5
        self.ultimo_tiro = pygame.time.get_ticks()
        self.delay_tiro = 300  
    
    def tacar_bala(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.delay_tiro:
            if len(self.tiros) < 15:
                self.tiros.add(Tiro(*self.rect.center))
            self.ultimo_tiro = agora

    def update(self):
        keys = pygame.key.get_pressed()

        tiros_fonte = fonte.render(f'Tiros: {15 - len(self.tiros)}', True, (255, 255, 255))
        superficie.blit(tiros_fonte, (20, 20))

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > tamanho[0]:
            self.rect.right = tamanho[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > tamanho[1]:
            self.rect.bottom = tamanho[1]

class Tiro(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load('images/tiroo.png')
        self.image = pygame.transform.scale(self.image, (120, 45)) 
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += 10
        if self.rect.x > tamanho[0]:
            self.kill()

class Virus(Sprite):
    def __init__(self):
        super().__init__()
        self.image = load('images/inimigo_1.png')
        self.image = pygame.transform.scale(self.image, (50, 50))  
        self.rect = self.image.get_rect(center=(800, randint(20, 580)))

    def update(self):
        self.rect.x -= 3
        if self.rect.x < 0:
            self.kill()
            global perdeu
            perdeu = True

class Fantasma(Sprite):
    def __init__(self):
        super().__init__()
        self.image = load('images/inimigo_2.png')
        self.image = pygame.transform.scale(self.image, (50, 50))  
        self.rect = self.image.get_rect(center=(800, randint(20, 580)))

    def update(self):
        self.rect.x -= 3
        if self.rect.x < 0:
            self.kill()
            global perdeu
            perdeu = True

class NaveMae(Sprite):
    def __init__(self):
        super().__init__()
        self.image = load('images/inimigo_3.png')
        self.image = pygame.transform.scale(self.image, (150, 80))  
        self.rect = self.image.get_rect(center=(800, randint(20, 580)))

    def update(self):
        self.rect.x -= 3
        if self.rect.x < 0:
            self.kill()
            global perdeu
            perdeu = True

def mostrar_quadro_final(mortes, tempo_de_sobrevivencia):
    superficie.fill((0, 0, 0))
    pygame.draw.rect(superficie, (255, 255, 255), (100, 50, 600, 500), 5)
    pygame.draw.rect(superficie, (50, 50, 50), (110, 60, 580, 480))

    texto_perdeu = fonte_perdeu.render('VOCÊ PERDEU', True, (255, 0, 0))
    texto_perdeu_rect = texto_perdeu.get_rect(center=(tamanho[0] // 2, 120))
    superficie.blit(texto_perdeu, texto_perdeu_rect)

    texto_mortes = fonte.render(f'Aliens mortos: {mortes}', True, (255, 255, 255))
    texto_mortes_rect = texto_mortes.get_rect(center=(tamanho[0] // 2, 220))
    superficie.blit(texto_mortes, texto_mortes_rect)

    texto_tempo = fonte.render(f'Tempo de sobrevivência: {tempo_de_sobrevivencia} s', True, (255, 255, 255))
    texto_tempo_rect = texto_tempo.get_rect(center=(tamanho[0] // 2, 320))
    superficie.blit(texto_tempo, texto_tempo_rect)

    texto_reiniciar = fonte.render('Pressione R para reiniciar', True, (0, 255, 0))
    texto_reiniciar_rect = texto_reiniciar.get_rect(center=(tamanho[0] // 2, 420))
    superficie.blit(texto_reiniciar, texto_reiniciar_rect)

    texto_sair = fonte.render('Pressione Q para sair', True, (255, 0, 0))
    texto_sair_rect = texto_sair.get_rect(center=(tamanho[0] // 2, 520))
    superficie.blit(texto_sair, texto_sair_rect)

    display.update()

grupo_inimigos = Group()
grupo_tiros = Group()
nave = Nave(grupo_tiros)
grupo_nave = GroupSingle(nave)

clock = Clock()
mortes = 0
round = 0
perdeu = False
tempo_de_sobrevivencia = 0

while True:
    for evento in event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                nave.tacar_bala()

            if perdeu and evento.key == K_r:
                grupo_inimigos.empty()
                grupo_tiros.empty()
                nave.rect.center = (400, 300)
                mortes = 0
                round = 0
                perdeu = False
                tempo_de_sobrevivencia = 0

            if perdeu and evento.key == K_q:
                pygame.quit()
                exit()

    if perdeu:
        mostrar_quadro_final(mortes, round // 60)
        continue

    clock.tick(60)
    tempo_de_sobrevivencia = round // 60

    if round % 60 == 0:
        if mortes < 10:
            grupo_inimigos.add(Virus())
        elif mortes < 20:
            grupo_inimigos.add(Fantasma())
        elif mortes < 30:
            grupo_inimigos.add(NaveMae())
        else:
            grupo_inimigos.add(Virus())
            grupo_inimigos.add(Fantasma())
            grupo_inimigos.add(NaveMae())

    if groupcollide(grupo_tiros, grupo_inimigos, True, True):
        mortes += 1

    
    superficie.blit(fundo, (0, 0))

    fonte_mortes = fonte.render(f'Mortes: {mortes}', True, (255, 255, 255))
    superficie.blit(fonte_mortes, (20, 70))

    fonte_tempo = fonte.render(f'Tempo: {tempo_de_sobrevivencia} s', True, (255, 255, 255))
    superficie.blit(fonte_tempo, (20, 130))

    grupo_nave.draw(superficie)
    grupo_inimigos.draw(superficie)
    grupo_tiros.draw(superficie)

    grupo_nave.update()
    grupo_inimigos.update()
    grupo_tiros.update()

    round += 1
    display.update()
