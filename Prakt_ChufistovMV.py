import pygame as pg

pg.init()

screen_width, screen_height = 800, 600

FPS = 24
clock = pg.time.Clock()

# Изображения
bg_img = pg.image.load('src/background.png')
icon_img = pg.image.load('src/ufo.png')

display = pg.display.set_mode((screen_width, screen_height))
pg.display.set_icon(icon_img)
pg.display.set_caption('Starfield')

sys_font = pg.font.SysFont('arial', 35)
font = pg.font.Font('src/04B_19.TTF', 100)


# display.fill('blue', (0, 0, screen_width, screen_height))
display.blit(bg_img, (0, 0))

text_img = sys_font.render(f'Score 357', True, 'yellow')
display.blit(text_img, (350, 50))

game_over_text = font.render('Game over', True, 'yellow')
w, h = game_over_text.get_size()
display.blit(game_over_text, (screen_width/2 - w/2, screen_height/2 - h/2))

# игрок
player_img = pg.image.load('src/player.png')
player_width, player_height = player_img.get_size()

running = True
flag = True
while running:
    pg.display.update()
    for event in pg.event.get():
        # нажали крестик на окне
        if event.type == pg.QUIT:
            running = False
        # тут нажимаем на клавиши
        if event.type == pg.KEYDOWN:
            # нажали на q - qlose
            if event.key == pg.K_q:
                running = False
            if event.key == pg.K_SPACE:
                display.blit(bg_img, (0, 0))
            if event.key == pg.K_F5:
                if flag:
                    flag = False
                    snapshot = display.copy()
                    player_name_text = sys_font.render("Матвей", True, 'yellow')
                    a = display.blit(player_name_text, (350, 500))
                else:
                    flag = True
                    display.blit(snapshot, a, a)

    clock.tick(FPS)

pg.quit()


