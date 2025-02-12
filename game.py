import pgzrun
from random import randint
import time

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
GAME_OVER = 2
game_state = MENU

# Müzik ve ses ayarları
music_on = True
sounds_on = True

# Puan
score = 0

# Karakter sınıfı
class Character:
    def __init__(self, x, y, images, speed, idle_images):
        self.x = x
        self.y = y
        self.images = images
        self.idle_images = idle_images  
        self.speed = speed
        self.frame = 0
        self.idle_frame = 0 
        self.is_moving = {"left": False, "right": False, "up": False, "down": False}

    def move(self, direction, moving):
        self.is_moving[direction] = moving

    def update(self):
        if self.is_moving["right"]:
            self.x += self.speed
        if self.is_moving["left"]:
            self.x -= self.speed
        if self.is_moving["up"]:
            self.y -= self.speed
        if self.is_moving["down"]:
            self.y += self.speed
        
                # Eğer hareket ediyorsa, animasyonları güncelle
        if any(self.is_moving.values()):
            self.frame = (self.frame + 0.2) % len(self.images)  # Hareket animasyonu
        else:
            self.idle_frame = (self.idle_frame + 0.2) % len(self.idle_images)  # Sabit duruş animasyonu

    def draw(self):
        # Eğer hareket etmiyorsa, sabit duruş animasyonunu göster
        if not any(self.is_moving.values()):
            image = self.idle_images[int(self.idle_frame)]  # Sabit duruş için frame kullan
            screen.blit(image, (self.x, self.y))
        else:
            image = self.images[int(self.frame)]  # Hareket animasyonu
            screen.blit(image, (self.x, self.y))
    
    def collides_with(self, other):
        return abs(self.x - other.x) < 30 and abs(self.y - other.y) < 30

# Düşman sınıfı
class Enemy(Character):
    def __init__(self, x, y, images, speed, idle_images):
        super().__init__(x, y, images, speed, idle_images)
        self.direction_x = randint(-1, 1)
        self.direction_y = randint(-1, 1)

    def update(self):
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y
        if self.x <= 0 or self.x >= WIDTH:
            self.direction_x *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.direction_y *= -1
         # Hareket ettikleri zaman animasyonu güncelle
        if self.is_moving:
            self.frame = (self.frame + 0.1) % len(self.images)  # Zombi animasyonu
        else:
            self.idle_frame = (self.idle_frame + 0.2) % len(self.idle_images)

    def draw(self):
        # Eğer hareket etmiyorlarsa sabit duruşu göster
        if not any([self.direction_x, self.direction_y]):
            image = self.idle_images[int(self.idle_frame)]  # Sabit duruş animasyonu
        else:
            image = self.images[int(self.frame)]  # Hareket animasyonu
        screen.blit(image, (self.x, self.y))

# Oyun nesneleri
hero = Character(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), ["player_walk1", "player_walk2", "player_hang"], 5, ["player_idle","player_stand"])
coin = Actor("coin_01", (randint(50, WIDTH - 50), randint(50, HEIGHT - 50)))
coin.images = ["coin_01", "coin_02", "coin_03", "coin_04"]
coin.frame = 0

# Zombiler listesi
enemies = []

# Ana menü butonları
buttons = [
    {"text": "Play the Game", "pos": (WIDTH // 2, HEIGHT // 2 - 50), "action": "start"},
    {"text": "Sound On/Sound Off Music", "pos": (WIDTH // 2, HEIGHT // 2), "action": "toggle_music"},
    {"text": "Exit", "pos": (WIDTH // 2, HEIGHT // 2 + 50), "action": "quit"}
]

# Game over butonları
game_over_buttons = [
    {"text": "Restart", "pos": (WIDTH // 2, HEIGHT // 2 + 50), "action": "restart"},
    {"text": "Menu", "pos": (WIDTH // 2, HEIGHT // 2 + 100), "action": "go_to_menu"}
]


def start_game():
    global game_state, hero, enemies, score, coin
    game_state = PLAYING
    hero.x = randint(50, WIDTH - 50)
    hero.y = randint(50, HEIGHT - 50)
    hero.is_moving = {"left": False, "right": False, "up": False, "down": False}  # Hareketi durdur
    enemies.clear()
    score = 0
    coin.x = randint(50, WIDTH - 50)
    coin.y = randint(50, HEIGHT - 50)
    if music_on:
        play_music()

def play_music():
    if music_on:
        music.play("mixkit-retro-game-emergency-alarm-1000.wav")  # Müzik çal

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        play_music()  # Müzik çal
    else:
        music.stop()  # Müzik durdur

def quit_game():
    exit()

def go_to_menu():
    global game_state
    game_state = MENU  # Ana menüye dön

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
    elif game_state == GAME_OVER:
        for button in game_over_buttons:
            x, y = button["pos"]
            if abs(pos[0] - x) < 100 and abs(pos[1] - y) < 20:
                if button["action"] == "restart":
                    start_game()  # Game Over ekranında Restart butonuna tıklanınca oyun yeniden başlar
                elif button["action"] == "go_to_menu":
                    go_to_menu()  # Menu butonuna tıklayınca ana menüye yönlendirilir

def on_key_down(key):
    global game_state  # game_state değişkenini global olarak kullanıyoruz
    if game_state == PLAYING:
        if key == keys.RIGHT:
            hero.move("right", True)
        elif key == keys.LEFT:
            hero.move("left", True)
        elif key == keys.UP:
            hero.move("up", True)
        elif key == keys.DOWN:
            hero.move("down", True)
        
        # Coin ile çarpışma kontrolü
        if hero.collides_with(coin):
            global score
            score += 10
            coin.x = randint(50, WIDTH - 50)
            coin.y = randint(50, HEIGHT - 50)
            sounds.coin.play()  # Coin toplama sesi

        # Zombi ile çarpışma kontrolü
        for enemy in enemies:
            if hero.collides_with(enemy):
                game_state = GAME_OVER
                sounds.gameover.play()  # Yanma sesi
                return

def on_key_up(key):
    if game_state == PLAYING:
        if key == keys.RIGHT:
            hero.move("right", False)
        elif key == keys.LEFT:
            hero.move("left", False)
        elif key == keys.UP:
            hero.move("up", False)
        elif key == keys.DOWN:
            hero.move("down", False)

def update():
    global game_state
    if game_state == PLAYING:
        hero.update()
        coin.frame = (coin.frame + 0.2) % len(coin.images)
        coin.image = coin.images[int(coin.frame)]
        
        for enemy in enemies:
            enemy.update()
            if hero.collides_with(enemy):
                game_state = GAME_OVER
                sounds.gameover.play()  # Yanma sesi
                return

        # Her 30 puanda yeni bir zombi ekleyin
        if score % 30 == 0 and score > 0 and len([e for e in enemies if e]) < score // 30:
            enemies.append(Enemy(randint(0, WIDTH), randint(0, HEIGHT), ["zombie_walk1", "zombie_walk2", "zombie_hang"], 2,["zombie_idle","zombie_stand"]))

def draw():
    screen.clear()
    if game_state == MENU:
        screen.draw.text("Infinity Running Game", center=(WIDTH // 2, HEIGHT // 2 - 150), fontsize=60, color=WHITE)
        for button in buttons:
            screen.draw.text(button["text"], center=button["pos"], fontsize=40, color=WHITE)
    elif game_state == PLAYING:
        hero.draw()
        coin.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color=WHITE)
    elif game_state == GAME_OVER:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 150), fontsize=60, color=RED)
        for button in game_over_buttons:
            screen.draw.text(button["text"], center=button["pos"], fontsize=40, color=WHITE)

pgzrun.go()
