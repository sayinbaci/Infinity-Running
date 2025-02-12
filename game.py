import pgzrun
from random import randint


# Pencere boyutları
WIDTH = 800
HEIGHT = 600

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Oyun durumları
MENU = 0
PLAYING = 1
game_state = MENU

# Müzik ve ses ayarları
music_on = True
sounds_on = True

# Karakter sınıfı
class Character:
    def __init__(self, x, y, images, speed):
        self.x = x
        self.y = y
        self.images = images
        self.speed = speed
        self.frame = 0
        self.is_moving = False

    def move(self):
        self.is_moving = True

    def stop(self):
        self.is_moving = False

    def update(self):
        if self.is_moving:
            self.frame = (self.frame + 0.2) % len(self.images)
        else:
            self.frame = 0

    def draw(self):
        image = self.images[int(self.frame)]
        screen.blit(image, (self.x, self.y))

# Düşman sınıfı
class Enemy(Character):
    def __init__(self, x, y, images, speed, min_x, max_x):
        super().__init__(x, y, images, speed)
        self.min_x = min_x
        self.max_x = max_x
        self.direction = 1

    def update(self):
        super().update()
        self.x += self.speed * self.direction
        if self.x <= self.min_x or self.x >= self.max_x:
            self.direction *= -1

# Oyun nesneleri
hero = Character(100, 400, ["player_walk1", "player_walk2", "player_hang"], 5)

# Zombiler rastgele y koordinatlarına yerleştirilecek ve yola yerleştirilecek
enemies = [
    Enemy(randint(200, 600), randint(300, 500), ["zombie_walk1", "zombie_walk2"], 3, 200, 600),
    Enemy(randint(200, 600), randint(300, 500), ["zombie_walk1", "zombie_walk2"], 2, 400, 700)
]

# Ana menü butonları
buttons = [
    {"text": "Play the Game", "pos": (WIDTH // 2, HEIGHT // 2 - 50), "action": "start"},
    {"text": "Sound On/Sound Of Music", "pos": (WIDTH // 2, HEIGHT // 2), "action": "toggle_music"},
    {"text": "Exit", "pos": (WIDTH // 2, HEIGHT // 2 + 50), "action": "quit"}
]

# Oyun başlatma
def start_game():
    global game_state
    game_state = PLAYING
    if music_on:
        music.play("mixkit-retro-game-emergency-alarm-1000.wav")

# Müzik aç/kapa
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.unpause()
    else:
        music.pause()

# Çıkış
def quit_game():
    exit()

# Fare tıklaması
def on_mouse_down(pos):
    global game_state
    if game_state == MENU:
        for button in buttons:
            x, y = button["pos"]
            if abs(pos[0] - x) < 100 and abs(pos[1] - y) < 20:
                if button["action"] == "start":
                    start_game()
                elif button["action"] == "toggle_music":
                    toggle_music()
                elif button["action"] == "quit":
                    quit_game()

# Klavye girişi
def on_key_down(key):
    if game_state == PLAYING:
        if key == keys.RIGHT:
            hero.x += hero.speed
        elif key == keys.LEFT:
            hero.x -= hero.speed
        if key == keys.SPACE:
            hero.move()
            sounds.jump.play()

# Oyun güncelleme
def update():
    if game_state == PLAYING:
        hero.update()

        # Zombilerin hareketi
        for enemy in enemies:
            enemy.update()

        # Zombiler yolun başlangıcına ulaştığında rastgele yeni bir y koordinatına yerleştirilecek
        for enemy in enemies:
            if enemy.x <= 200 or enemy.x >= 600:
                enemy.y = randint(300, 500)

# Oyun çizimi
def draw():
    screen.clear()

    # Yol çizimi
    screen.draw.rect(Rect((100, 300), (600, 10)), WHITE)

    if game_state == MENU:
        screen.draw.text("Infinity Running Game", center=(WIDTH // 2, HEIGHT // 2 - 150), fontsize=60, color=WHITE)
        for button in buttons:
            screen.draw.text(button["text"], center=button["pos"], fontsize=40, color=WHITE)
    elif game_state == PLAYING:
        hero.draw()

        # Zombileri çiz
        for enemy in enemies:
            enemy.draw()

# Pygame Zero başlatma
pgzrun.go()
