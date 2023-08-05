import os
import pygame
print("ezgame.py loaded")

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

def window_size(width, height):
    screen = pygame.display.set_mode((width, height))
    return screen

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', name)
        raise SystemExit(message)
    return sound

def load_music(name):
    class NoneMusic:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneMusic()
    fullname = os.path.join('data', name)
    try:
        music = pygame.mixer.music.load(fullname)
    except pygame.error as message:
        print('Cannot load music:', name)
        raise SystemExit(message)
    return music

def load_font(name, size):
    fullname = os.path.join('data', name)
    try:
        font = pygame.font.Font(fullname, size)
    except pygame.error as message:
        print('Cannot load font:', name)
        raise SystemExit(message)
    return font

def load_text(font, text, color):
    text = font.render(text, 1, color)
    return text, text.get_rect()

def pew(screen,img,pos=(0,0)):
    screen.blit(img, pos)

def pew_all(screen,imgs,pos=(0,0)):
    for img in imgs:
        screen.blit(img, pos)

def exit_handler():
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()