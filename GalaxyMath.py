import pygame, sys, random
pygame.init()
pygame.mixer.init()
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
width, height = 700, 600
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Galaxy Math")
FPS = pygame.time.Clock()
fondo = pygame.image.load("assets/space.jpg")
fondo_ts = pygame.transform.scale(fondo, (width, height))
y = 0
icon = pygame.image.load("assets/spacerock.png")
pygame.display.set_icon(icon)
#Musica de fondo
music = pygame.mixer.Sound("assets/music.mp3")
volumen = 0.15
music.set_volume(volumen)
music.play(1)

#Marcador (Score)
score = 0
highscore = 0
#Números Random
if score > 0:
    a = random.randint(-score, score)
    b = random.randint(-score, score)
else:
    a = random.randint(-10, 10)
    b = random.randint(-10, 10)
#Respuestas
r = a + b
if score > 0:
    n2 = random.randint(-score * 2, score * 2)
    n1 = random.randint(-score * 2, score * 2)
    if n2 == n1 or n2 == r:
        n2 = random.randint(-score * 2, score * 2)
    if n1 == r:
        n1 = random.randint(-score * 2, score * 2)
else:
    n2 = random.randint(-20, 20)
    n1 = random.randint(-20, 20)
    if n2 == n1 or n2 == r:
        n2 = random.randint(-20, 20)
    if n1 == r:
        n1 = random.randint(-20, 20)
lista = [n1, n2, r]
rd1 = random.choice(lista)
lista.remove(rd1)
rd2 = random.choice(lista)
lista.remove(rd2)
rd3 = random.choice(lista)

#Método para crear texto
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font("assets/Font.ttf", size)
    text_surface = font.render(text, True, (white))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_text2(surface, text, size, x, y):
    font = pygame.font.Font("assets/Font.ttf", size)
    text_surface = font.render(text, True, (black))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

#Crear clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player00.png")
        self.image = pygame.transform.scale(self.image, (110,110))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height -10
        self.speed_x = 0
        self.vidas = 3

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speed_x = -5
        if keys[pygame.K_d]:
            self.speed_x = 5
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        #Evitar salir de la ventana
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Balas(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

#Crear clase Balas
class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = balas_anim[0]
        self.image = pygame.transform.scale(self.image, (25,25))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 40 #Velocidad de la bala
        self.frame = 0
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -5
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 3:
                self.frame = 0
            if self.frame == len(balas_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = balas_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#Animacion balas
balas_anim = []
for i in range(4):
    file = "assets/balas0{}.png".format(i)
    img = pygame.image.load(file)
    img.set_colorkey(black)
    img_scale = pygame.transform.scale(img, (25, 25))
    balas_anim.append(img_scale)

#Crear clase Explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explo_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75 #Velocidad de la explosion
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explo_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explo_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#Animacion explosion
explo_anim = []
for i in range(7):
    file = "assets/explo0{}.png".format(i)
    img = pygame.image.load(file)
    img.set_colorkey(black)
    img_scale = pygame.transform.scale(img, (150, 150))
    explo_anim.append(img_scale)

#Crear clase Meteorito01
class Meteorito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/spacerock.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width * 0.25
        self.rect.y = -100
        self.speedy = 2
        self.valor = rd1

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height + 100:
            self.rect.centerx = width * 0.25
            self.rect.y = -100
            self.speedy = 2

#Crear clase Meteorito02
class Meteorito2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/spacerock.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width * 0.5
        self.rect.y = -100
        self.speedy = 2
        self.valor = rd2
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height + 100:
            self.rect.centerx = width * 0.5
            self.rect.y = -100
            self.speedy = 2

#Crear clase Meteorito03
class Meteorito3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/spacerock.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width * 0.75
        self.rect.y = -100
        self.speedy = 2
        self.valor = rd3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height + 100:
            self.rect.centerx = width * 0.75
            self.rect.y = 100
            self.speedy = 2

#Crear Radio
class Radio(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/radio.png")
        self.image = pygame.transform.scale(self.image, (90,68))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width * 0.92
        self.rect.centery = height * 0.92

#Crear Globo de Texto
class Globo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/globo.png")
        self.image.set_colorkey(red)
        self.rect = self.image.get_rect()
        self.rect.centerx = width * 0.81
        self.rect.centery = height * 0.805

#Cargar Sonido
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
laser_sound.set_volume(volumen)
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
explosion_sound.set_volume(volumen)
def show_go_screen():
    screen.blit(fondo_ts, [0, 0])
    draw_text(screen, "Galaxy Math", 65 , width // 2, height * 0.2)
    draw_text(screen, "Instrucciones:", 27 , width // 2, height * 0.4)
    draw_text(screen, "Mover a la izquierda: '<-' ó 'A'", 22 , width // 2, height * 0.47)
    draw_text(screen, "Mover a la derecha: '->' ó 'D'", 22 , width // 2, height * 0.53)
    draw_text(screen, "Disparar: 'Espacio'", 22 , width // 2, height * 0.59)
    draw_text(screen, "Pulsa cualquier tecla", 27 , width // 2, height * 3/4)

    pygame.display.flip()
    waiting = True
    while waiting:
        FPS.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

game_over = True
running = True
#Bucle del juego
while running:
    if game_over:
        show_go_screen()
        game_over = False
        #Grupo de juego
        all_sprites = pygame.sprite.Group()
        meteoritos_list = pygame.sprite.Group()
        globo = Globo()
        radio = Radio()
        player = Jugador()
        all_sprites.add(radio, globo, player)
        bullets = pygame.sprite.Group()
        #Obtener meteoritos
        meteorito = Meteorito()
        meteorito2 = Meteorito2()
        meteorito3 = Meteorito3()
        all_sprites.add(meteorito, meteorito2, meteorito3)
        meteoritos_list.add(meteorito, meteorito2, meteorito3)
    
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over = True
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #Colision (Jugador - Meteoros)
    hits = pygame.sprite.spritecollide(player, meteoritos_list, True)
    for hit in hits:
        score -= 30
        player.vidas -= 1
        meteorito.kill()
        meteorito2.kill()
        meteorito3.kill()
        meteorito = Meteorito()
        meteorito2 = Meteorito2()
        meteorito3 = Meteorito3()
        all_sprites.add(meteorito, meteorito2, meteorito3)
        meteoritos_list.add(meteorito, meteorito2, meteorito3)
        explosion_sound.play()
        explo = Explosion(hit.rect.center)
        all_sprites.add(explo)
        if player.vidas == 2:
            player.vidas = 2
        if player.vidas == 1:
            player.vidas = 1
        if score > 0:
            a = random.randint(-score, score)
            b = random.randint(-score, score)
        else:
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
        r = a + b
        if score > 0:
            n2 = random.randint(-score * 2, score * 2)
            n1 = random.randint(-score * 2, score * 2)
            if n2 == n1 or n2 == r:
                n2 = random.randint(-score * 2, score * 2)
            if n1 == r:
                n1 = random.randint(-score * 2, score * 2)
        else:
            n2 = random.randint(-20, 20)
            n1 = random.randint(-20, 20)
            if n2 == n1 or n2 == r:
                n2 = random.randint(-20, 20)
            if n1 == r:
                n1 = random.randint(-20, 20)
        lista = [n1, n2 ,r]
        rd1 = random.choice(lista)
        lista.remove(rd1)
        rd2 = random.choice(lista)
        lista.remove(rd2)
        rd3 = random.choice(lista)
    #Colision (Laser - Meteoros)
    hits = pygame.sprite.spritecollide(meteorito, bullets, True)
    for hit in hits:
        meteorito.kill()
        meteorito2.kill()
        meteorito3.kill()
        meteorito = Meteorito()
        meteorito2 = Meteorito2()
        meteorito3 = Meteorito3()
        all_sprites.add(meteorito, meteorito2, meteorito3)
        meteoritos_list.add(meteorito, meteorito2, meteorito3)
        explosion_sound.play()
        explo = Explosion(hit.rect.center)
        all_sprites.add(explo)
        if meteorito.valor == r:
            score += 10
        else:
            player.vidas -= 1
            score -= 30
        if highscore < score:
            highscore = score
        if score > 0:
            a = random.randint(-score, score)
            b = random.randint(-score, score)
        else:
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
        r = a + b
        if score > 0:
            n2 = random.randint(-score * 2, score * 2)
            n1 = random.randint(-score * 2, score * 2)
            if n2 == n1 or n2 == r:
                n2 = random.randint(-score * 2, score * 2)
            if n1 == r:
                n1 = random.randint(-score * 2, score * 2)
        else:
            n2 = random.randint(-20, 20)
            n1 = random.randint(-20, 20)
            if n2 == n1 or n2 == r:
                n2 = random.randint(-20, 20)
            if n1 == r:
                n1 = random.randint(-20, 20)
        lista = [n1, n2 ,r]
        rd1 = random.choice(lista)
        lista.remove(rd1)
        rd2 = random.choice(lista)
        lista.remove(rd2)
        rd3 = random.choice(lista)

    hits = pygame.sprite.spritecollide(meteorito2, bullets, True)
    for hit in hits:
        meteorito.kill()
        meteorito2.kill()
        meteorito3.kill()
        meteorito = Meteorito()
        meteorito2 = Meteorito2()
        meteorito3 = Meteorito3()
        all_sprites.add(meteorito, meteorito2, meteorito3)
        meteoritos_list.add(meteorito, meteorito2, meteorito3)
        explosion_sound.play()
        explo = Explosion(hit.rect.center)
        all_sprites.add(explo)
        if meteorito2.valor == r:
            score += 10
        else:
            player.vidas -= 1
            score -= 30
        if highscore < score:
            highscore = score
        if score > 0:
            a = random.randint(-score, score)
            b = random.randint(-score, score)
        else:
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
        r = a + b
        if score > 0:
            n2 = random.randint(-score * 2, score * 2)
            n1 = random.randint(-score * 2, score * 2)
            if n2 == n1 or n2 == r:
                n2 = random.randint(-score * 2, score * 2)
            if n1 == r:
                n1 = random.randint(-score * 2, score * 2)
        else:
            n2 = random.randint(-20, 20)
            n1 = random.randint(-20, 20)
            if n2 == n1 or n2 == r:
                n2 = random.randint(-20, 20)
            if n1 == r:
                n1 = random.randint(-20, 20)
        lista = [n1, n2 ,r]
        rd1 = random.choice(lista)
        lista.remove(rd1)
        rd2 = random.choice(lista)
        lista.remove(rd2)
        rd3 = random.choice(lista)

    hits = pygame.sprite.spritecollide(meteorito3, bullets, True)
    for hit in hits:
        meteorito.kill()
        meteorito2.kill()
        meteorito3.kill()
        meteorito = Meteorito()
        meteorito2 = Meteorito2()
        meteorito3 = Meteorito3()
        all_sprites.add(meteorito, meteorito2, meteorito3)
        meteoritos_list.add(meteorito, meteorito2, meteorito3)
        explosion_sound.play()
        explo = Explosion(hit.rect.center)
        all_sprites.add(explo)
        if meteorito3.valor == r:
            score += 10
        else:
            player.vidas -= 1
            score -= 30
        if highscore < score:
            highscore = score
        if score > 0:
            a = random.randint(-score, score)
            b = random.randint(-score, score)
        else:
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
        r = a + b
        if score > 0:
            n2 = random.randint(-score * 2, score * 2)
            n1 = random.randint(-score * 2, score * 2)
            if n2 == n1 or n2 == r:
                n2 = random.randint(-score * 2, score * 2)
            if n1 == r:
                n1 = random.randint(-score * 2, score * 2)
        else:
            n2 = random.randint(-20, 20)
            n1 = random.randint(-20, 20)
            if n2 == n1 or n2 == r:
                n2 = random.randint(-20, 20)
            if n1 == r:
                n1 = random.randint(-20, 20)
        lista = [n1, n2 ,r]
        rd1 = random.choice(lista)
        lista.remove(rd1)
        rd2 = random.choice(lista)
        lista.remove(rd2)
        rd3 = random.choice(lista)

    #Visualizar en pantalla
    all_sprites.update()
    y_relativa = y % fondo_ts.get_rect().height
    screen.blit(fondo_ts, [0, y_relativa - fondo_ts.get_rect().height])
    if y_relativa < height:
        screen.blit(fondo_ts, (0, y_relativa))

    y += 1
    all_sprites.draw(screen)
    draw_text(screen, "High Score:", 20, width * 0.89, height * 0.02)
    draw_text(screen, str(highscore), 20, width * 0.89, height * 0.06)
    draw_text(screen, "Score:", 20, width * 0.89, height * 0.1)
    draw_text(screen, str(score), 20, width * 0.89, height * 0.14)
    draw_text(screen, "Vidas:", 20, width * 0.07, height * 0.02)
    draw_text2(screen, "¡Meteoro Detectado!", 17, globo.rect.centerx, globo.rect.centery - 50)
    draw_text2(screen, "Calcular:", 17, globo.rect.centerx, globo.rect.centery - 25)
    if a >= 0 and b >= 0:
        draw_text2(screen, str(a)+" + "+str(b)+" = ¿?", 17, globo.rect.centerx, globo.rect.centery)
    if a >= 0 and b < 0:
        draw_text2(screen, str(a)+" + ("+str(b)+") = ¿?", 17, globo.rect.centerx, globo.rect.centery)
    if a < 0 and b >= 0:
        draw_text2(screen, "("+str(a)+") + "+str(b)+" = ¿?", 17, globo.rect.centerx, globo.rect.centery)
    if a < 0 and b < 0:
        draw_text2(screen, "("+str(a)+") + ("+str(b)+") = ¿?", 17, globo.rect.centerx, globo.rect.centery)
    draw_text(screen, str(rd1), 45, meteorito.rect.centerx, meteorito.rect.y + 50)
    draw_text(screen, str(rd2), 45, meteorito2.rect.centerx, meteorito2.rect.y + 50)
    draw_text(screen, str(rd3), 45, meteorito3.rect.centerx, meteorito3.rect.y + 50)

    if  149 < score:
        meteorito.speedy = 3.5
        meteorito2.speedy = 3.5
        meteorito3.speedy = 3.5
    if  99 < score < 151:
        meteorito.speedy = 3
        meteorito2.speedy = 3
        meteorito3.speedy = 3
    if  49 < score < 101:
        meteorito.speedy = 2.5
        meteorito2.speedy = 2.5
        meteorito3.speedy = 2.5
    if score < 0:
        meteorito.speedy = 1.5
        meteorito2.speedy = 1.5
        meteorito3.speedy = 1.5

    #Vidas
    cora = pygame.image.load("assets/player00.png").convert()
    cora.set_colorkey(black)
    muerte = pygame.transform.scale(cora, (30, 30))
    muerte_2 = screen.blit(muerte, (width * 0.02, height * 0.07))
    muerte_1 = screen.blit(muerte, (width * 0.07, height * 0.07))
    dead = pygame.image.load("assets/dead.png").convert()
    dead.set_colorkey(black)
    death = pygame.transform.scale(dead, (30, 30))
    if player.vidas == 2:
        muerte_1 = screen.blit(death, (width * 0.07, height * 0.07))
        player.image = pygame.image.load("assets/player01.png")
        player.image = pygame.transform.scale(player.image, (110,110))
    if player.vidas == 1:
        muerte_2 = screen.blit(death, (width * 0.02, height * 0.07))
        muerte_1 = screen.blit(death, (width * 0.07, height * 0.07))
        player.image = pygame.image.load("assets/player02.png")
        player.image = pygame.transform.scale(player.image, (110,110))
    if player.vidas <= 0:
        show_go_screen()
        score = 0
        player.vidas = 3
        explo.kill()
        player.kill()
        player = Jugador()
        all_sprites.add(player)
    pygame.display.flip()
#Salir del juego
pygame.quit()