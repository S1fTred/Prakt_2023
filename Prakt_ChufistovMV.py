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

display.blit(bg_img, (0, 0))
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
player_live = True

#bullet
bullet_img = pg.image.load('src/bullet.png')
bullet_width, bullet_height = bullet_img.get_size()
bullet_dy = -10
bullet_x = player_x + player_width / 4     # микро дз - пускать из середины
bullet_y = player_y - bullet_height
bullet_live = False    # есть пуля?

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
pause_img = pg.image.load('src/pause-icon-30.png')
pause_w, pause_h = pause_img.get_size()

def update_model():
    if paused == False:
        model_player()
        model_bullet()
        model_enemy()

def redraw_display():
    if player_live == True:
        display.blit(bg_img, (0, 0))
        display.blit(player_img, (player_x, player_y))
        display.blit(enemy_img, (enemy_x, enemy_y))
        if bullet_live:
            display.blit(bullet_img, (bullet_x, bullet_y))
        write_score()
        menu_game_over()
        pg.display.update()
    else:
        display.blit(bg_img, (0, 0))
        menu_game_over()
        write_score()
        pg.display.update()
    if paused == True:
        display.blit(pause_img, (screen_width / 2 - pause_w / 2, screen_height / 2 - pause_h / 2))
        pg.display.update()

def create_enemy():
    global enemy_y, enemy_x
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = 0
    print(f"CREATE{enemy_x = }")

def model_enemy():
    """ Изменение положения противника, рассчет поражений."""
    global enemy_y, enemy_x, bullet_live, player_live, score
    if player_live:
        enemy_x += enemy_dx
        enemy_y += enemy_dy
    if enemy_y > screen_height:
        create_enemy()

    # пересечение с пулей
    if bullet_live:
        re = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rb = pg.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
        is_crossed = re.colliderect(rb)
        # попал!
        if is_crossed:
            print('BANG!')
            score += 1
            create_enemy()
            bullet_live = False

    # пересечение с игроком
    if player_live:
        pr = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rp = pg.Rect(player_x, player_y, player_width, player_height)
        peresek = pr.colliderect(rp)
        if peresek:
            print('Game over')
            player_live = False
def model_player():
    if player_live == True:
        global player_x
        player_x += player_dx
        if player_x < 0:
            player_x = 0
        elif player_x > screen_width - player_width:
            player_x = screen_width - player_width

def model_bullet():
    global bullet_y, bullet_live
    bullet_y += bullet_dy
    # пуля улетела за верх экрана
    if bullet_y < 0:
        bullet_live = False

def create_bullet():
    global bullet_y, bullet_x, bullet_live
    if player_live:
        bullet_live = True
        bullet_x = player_x + player_width / 4  # микро дз - пускать из середины
        bullet_y = player_y - bullet_height

def write_score():
    text_score = font.render("Score: " + str(score), True, 'yellow')
    w_gs, h_gs = text_score.get_size()
    if player_live:
        display.blit(text_score,(600,10))
    elif not player_live:
        display.blit(text_score, (screen_width / 2 - w_gs / 2, (screen_height / 2) + h_gs * 1.5))

def menu_game_over():
    global game_over
    if not player_live:
        text_game_over = font_big.render('Game over', True, 'yellow')
        w_go, h_go = text_game_over.get_size()
        display.blit(text_game_over, (screen_width / 2 - w_go / 2, screen_height / 2 - h_go / 2))
        game_over = True

def event_processing():
    global player_dx, paused, game_over, player_live, score
    running = True
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_q:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_p:
            paused = not paused
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            game_over = False
            player_live = True
            score = 0
            create_enemy()
            running = True
            while running:
                running = event_processing()
                update_model()
                redraw_display()

        # движение игрока
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                player_dx = -player_velocity
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                player_dx = player_velocity
        if event.type == pg.KEYUP:
            player_dx = 0


        # по клику мыши стреляем
        if event.type == pg.MOUSEBUTTONDOWN:
            key = pg.mouse.get_pressed()
            print(f'{key[0]=} {bullet_live=}')
            if not bullet_live:
                create_bullet()


    clock.tick(FPS)
    return running


create_enemy()
running = True
while running:
    update_model()
    redraw_display()
    running = event_processing()

pg.quit()