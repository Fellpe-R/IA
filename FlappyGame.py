import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

# Almenta a escala de uma imagem: pygame.transform.scale2x()
# Localiza arquivos: os.path.join('dir', 'file')
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'pipe.png')))
IMGBASE = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bg.png')))

# lista de imagens do personagem
IMAGEM_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird3.png'))),
]

# iniciando e passando paramentros para uma clase fonte
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


class Person:
    IMGS = IMAGEM_PASSARO
    # ANIMAÇÕES DE ROTAÇÃO
    ROT_MAX = 25
    ROT_VELO = 20
    ANIM_TIME = 5

    # Método construtor da class
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ang = 0
        self.velo = 0
        self.alt = self.y
        self.temp = 0
        self.img_cont = 0
        self.img = self.IMGS[0]

    def jump(self):
        # Formula do movimento uniforme (S = So + vot + at^2/2)
        # S = Posição final; So = Posição inicial; v = Velocidade; t = Tempo;
        self.velo = -10.5
        self.temp = 0
        self.alt = self.y

    def move(self):
        # calcula o deslocamento
        self.temp += 1
        desloc = 1.5 * (self.temp ** 2) + self.velo * self.temp

        # limites de deslocamento
        if desloc > 16:
            desloc = 16
        elif desloc < 0:
            # ganho no salto
            desloc -= 2

        # aplicação do movimento
        self.y += desloc

        # angulo de rotação da animação
        if desloc < 0 or self.y < (self.alt + 50):
            if self.ang < self.ROT_MAX:
                self.ang = self.ROT_MAX
        else:
            if self.ang > -90:
                self.ang -= self.ROT_VELO

    def print(self, tela):
        # Definindo img
        self.img_cont += 1
        if self.img_cont < self.ANIM_TIME:
            self.img = self.IMGS[0]
        elif self.img_cont < self.ANIM_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_cont < self.ANIM_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_cont < self.ANIM_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_cont < self.ANIM_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_cont = 0

        # Desativa movimento das asas
        if self.ang <= -80:
            self.img = self.IMGS[1]
            self.img_cont = self.ANIM_TIME * 2

        # print
        img_rotate = pygame.transform.rotate(self.img, self.ang)
        pos_cent_img = self.img.get_rect(topleft=(self.x, self.y)).center
        person = img_rotate.get_rect(center=pos_cent_img)
        tela.blit(img_rotate, person.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Cano:
    DISTAN = 200
    VELO = 5

    def __init__(self, x):
        self.x = x
        self.alt = 0
        self.posTop = 0
        self.posBase = 0
        self.CANOTOP = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANOBASE = IMAGEM_CANO
        self.passou = False
        self.defAlt()

    # Definindo a altura do obstaculo
    def defAlt(self):
        self.alt = random.randrange(50, 450)
        self.posTop = self.alt - self.CANOTOP.get_height()
        self.posBase = self.alt + self.DISTAN

    def move(self):
        self.x -= self.VELO

    def print(self, tela):
        tela.blit(self.CANOTOP, (self.x, self.posTop))
        tela.blit(self.CANOBASE, (self.x, self.posBase))

    def colisao(self, person):
        personMask = person.get_mask()
        topMask = pygame.mask.from_surface(self.CANOBASE)
        baseMask = pygame.mask.from_surface(self.CANOTOP)

        distTop = (self.x - person.x, self.posTop - round(person.y))
        distBase = (self.x - person.x, self.posBase - round(person.y))

        topColi = personMask.overlap(topMask, distTop)
        baseColi = personMask.overlap(baseMask, distBase)

        if baseColi or topColi:
            return True
        else:
            return False


class Base:
    VEL = 5
    LARG = IMGBASE.get_width()
    IMG = IMGBASE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARG

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.LARG < 0:
            self.x1 = self.x1 + self.LARG
        if self.x2 + self.LARG < 0:
            self.x2 = self.x2 + self.LARG

    def print(self, tela):
        tela.blit(self.IMG, (self.x1, self.y))
        tela.blit(self.IMG, (self.x2, self.y))


def screen(tela, persons, canos, base, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for person in persons:
        person.print(tela)
    for cano in canos:
        cano.print(tela)

    texto = FONTE_PONTOS.render(f"pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    base.print(tela)
    pygame.display.update()


def main():
    persons = [Person(230, 350)]
    base = Base(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    run = True
    while run:
        relogio.tick(30)

        # interação com usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for person in persons:
                        person.jump()

        # Movimentação do ambiente
        for person in persons:
            person.move()
        base.move()

        addCano = False
        rmCanos = []
        for cano in canos:
            # pegando posição na lista:
            for i, person, in enumerate(persons):
                if cano.colisao(person):
                    persons.pop(i)
                if not cano.passou and person.x > cano.x:
                    cano.passou = True
                    addCano = True

            cano.move()

            if cano.x + cano.CANOTOP.get_width() < 0:
                rmCanos.append(cano)

        if addCano:
            pontos += 1
            canos.append(Cano(600))

        for cano in rmCanos:
            canos.remove(cano)

        for i, person in enumerate(persons):
            if (person.y + person.img.get_height()) > base.y or person.y < 0:
                persons.pop(i)

        screen(tela, persons, canos, base, pontos)


if __name__ == '__main__':
    main()
