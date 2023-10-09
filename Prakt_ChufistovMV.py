import pygame as pg
import random

pg.init()

screen_width, screen_height = 800, 600

FPS = 24    # frame per second
clock = pg.time.Clock()

# изображения
bg_img = pg.image.load('src/background.png')
icon_img = pg.image.load('src/ufo.png')

display = pg.display.set_mode((screen_width, screen_height))
pg.display.set_icon(icon_img)
pg.display.set_caption('Космическое вторжение')

sys_font = pg.font.SysFont('arial', 34)
font = pg.font.Font('src/04B_19.TTF', 48)
font_big = pg.font.Font('src/04B_19.TTF', 72)

# # display.fill('blue', (0, 0, screen_width, screen_height))
# display.blit(bg_img, (0, 0))        # image.tr
#
# text_img = sys_font.render('Score 123', True, 'white')
# # display.blit(text_img, (100, 50))
#
# game_over_text = font.render('Game Over', True, 'red')
# w, h = game_over_text.get_size()
# # display.blit(game_over_text, (screen_width/2 - w/2, screen_height / 2 - h/2))

#player
player_img = pg.image.load('src/player.png')
player_width, player_height = player_img.get_size()
player_gap = 10
player_velocity = 10
player_dx = 0
player_x = screen_width/2 - player_width/2
player_y = screen_height - player_height - player_gap
player_alive = True

#bullet
bullet_img = pg.image.load('src/bullet.png')
bullet_width, bullet_height = bullet_img.get_size()
bullet_dy = -10
bullet_x = player_x - player_width / 4     # микро дз - пускать из середины
bullet_y = player_y - bullet_height
bullet_alive = False    # есть пуля?

#enemy
enemy_img = pg.image.load('src/enemy.png')
enemy_width, enemy_height = enemy_img.get_size()
enemy_dx = 0
enemy_dy = 5
enemy_x = 0
enemy_y = 0

#score
score = 0
game_over = False
paused = False
# pause_img = pg.image.load('')
# pause_w, pause_h = pause_img.get_size()

def model_update():
    if paused == False:
        player_model()
        bullet_model()
        enemy_model()

def enemy_create():
    global enemy_y, enemy_x
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = 0
    print(f"CREATE{enemy_x = }")

def enemy_model():
    """ Изменение положения противника, рассчет поражений."""
    global enemy_y, enemy_x, bullet_alive, player_alive, score
    if player_alive:
        enemy_x += enemy_dx
        enemy_y += enemy_dy
    if enemy_y > screen_height:
        enemy_create()

    # пересечение с пулей
    if bullet_alive:
        re = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rb = pg.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
        is_crossed = re.colliderect(rb)
        # попал!
        if is_crossed:
            print('BANG!')
            enemy_create()
            bullet_alive = False

    # пересечение с игроком
    if player_alive:
        pr = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rp = pg.Rect(player_x, player_y, player_width, player_height)
        pereseklis = pr.colliderect(rp)
        if pereseklis:
            print('Game over')
            player_alive = False
def player_model():
    if player_alive == True:
        global player_x
        player_x += player_dx
        if player_x < 0:
            player_x = 0
        elif player_x > screen_width - player_width:
            player_x = screen_width - player_width

def bullet_model():
    """ Изменяется положение пули.
    """
    global bullet_y, bullet_alive
    bullet_y += bullet_dy
    # пуля улетела за верх экрана
    if bullet_y < 0:
        bullet_alive = False

def bullet_create():
    global bullet_y, bullet_x, bullet_alive
    if player_alive:
        bullet_alive = True
        bullet_x = player_x - player_width / 10  # микро дз - пускать из середины
        bullet_y = player_y - bullet_height

def menu_game_over():
    global game_over
    if not player_alive:
        text_game_over = font_big.render('Game over', True, 'yellow')
        w_go, h_go = text_game_over.get_size()
        display.blit(text_game_over, (screen_width / 2 - w_go / 2, screen_height / 2 - h_go / 2))
        game_over = True

def display_redraw():
    display.blit(bg_img, (0, 0))
    display.blit(player_img, (player_x, player_y))
    display.blit(enemy_img, (enemy_x, enemy_y))
    if bullet_alive:
        display.blit(bullet_img, (bullet_x, bullet_y))
    pg.display.update()

def event_processing():
    global player_dx
    running = True
    for event in pg.event.get():
        # нажали крестик на окне
        if event.type == pg.QUIT:
            running = False
        # тут нажимаем на клавиши
        if event.type == pg.KEYDOWN:
            # нажали на q - quit
            if event.key == pg.K_q:
                running = False
        # движение игрока
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                player_dx = -player_velocity
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                player_dx = player_velocity
        if event.type == pg.KEYUP:
            player_dx = 0

        # по левому клику мыши стреляем
        if event.type == pg.MOUSEBUTTONDOWN:
            key = pg.mouse.get_pressed()    # key[0] - left, key[2] - right
            print(f'{key[0]=} {bullet_alive=}')
            if not bullet_alive:
                bullet_create()


    clock.tick(FPS)
    return running


enemy_create()
running = True
while running:
    model_update()
    display_redraw()
    running = event_processing()

pg.quit()