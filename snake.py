import os
import random
import sys

import pygame as pg

pg.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pg.init()

board_width, board_height = 51, 51
scale = 10
screen_width, screen_height = (board_width * scale, board_height * scale)
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (int(pg.display.Info().current_w - screen_width) / 2,
                                                int(pg.display.Info().current_h - screen_height) / 3)
screen = pg.display.set_mode((screen_width, screen_height), 0, 32)
pg.display.set_caption('Snake')
clock = pg.time.Clock()
fps = 60

bg_colour = (25, 25, 25)
bg_images = [pg.image.load('Assets/snake_bg/snake_bg_0.png'), pg.image.load('Assets/snake_bg/snake_bg_1.png')]
base_colours = [(230, 230, 230), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
num_food_colours = 8
food_colours = [(195, 6, 6), (37, 124, 32), (20, 74, 135), (227, 90, 0), (57, 0, 126), (253, 246, 0),
                (0, 206, 79), (255, 0, 68)]
food_images = []
for n in range(num_food_colours):
    food_images.append(pg.image.load(f'Assets/snake_food/snake_food_{n}.png'))
snake_images = [pg.image.load('Assets/snake_body/snake_body_0.png').convert(),
                pg.image.load('Assets/snake_body/snake_body_1.png').convert()]
snake_start = [[25, 32], [25, 33], [25, 34], [25, 35], [25, 36]]
snake_head = [[23, 50], [27, 50], [23, 49], [27, 49], [23, 48], [27, 48], [22, 47], [28, 47], [22, 46], [28, 46],
              [21, 45], [29, 45], [21, 44], [29, 44], [21, 43], [29, 43], [23, 43], [27, 43], [21, 42], [29, 42],
              [22, 41], [28, 41], [22, 40], [28, 40], [23, 39], [27, 39], [24, 38], [26, 38], [25, 37]]
food_start = (25, 10)
title_start = (4, 10)
title_path = [(0, 0), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, -1), (-1, -1), (0, -1), (1, -1), (1, 0),
              (1, 1), (0, 1),  # S
              (2, 5), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 1), (0, 1), (0, 1),  # n
              (4, 0), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 0), (0, 1), (0, 1), (1, 1),  # a
              (2, 0), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (2, 2), (-1, 1), (1, 1), (0, 1),  # k
              (3, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (0, 1), (0, 1), (1, 0), (1, -1), (0, -1),  # e
              (0, 5), (0, -1), (-1, 0), (-1, 0), (-1, 0), (-1, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 1), (1, 0),
              (1, 0), (1, -1), (0, -1), (0, -1), (-1, 0),  # G
              (5, 0), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -3), (0, 1), (0, 1), (1, 1),  # a
              (2, 0), (0, -1), (0, -1), (1, -1), (1, 1), (0, -1), (1, 0), (1, 1), (0, 1), (0, 1),  # m
              (3, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 1), (0, 1), (0, 1), (1, 0), (1, -1), (0, -1),  # e
              (4, 3), (0, -5), (-1, 5), (0, -5), (-1, 5), (0, -5), (-1, 5), (0, -5), (-1, 6), (0, -7), (-1, 7),
              (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7),
              (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7),
              (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -8), (-1, 8), (1, -9),
              (-2, 9), (2, -10), (-3, 10), (3, -11), (-4, 11), (4, -12), (-5, 12), (5, -13), (-6, 13), (5, -14),
              (-6, 13), (5, -13), (-6, 12), (5, -13), (-5, 12), (4, -12), (-4, 11), (3, -11), (-3, 10), (2, -10),
              (-2, 9), (1, -9), (-1, 8), (0, -9), (-1, 8), (0, -9), (-1, 9), (0, -9), (-1, 9), (0, -9), (-1, 9),
              (0, -8), (-1, 8), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7),
              (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -7), (-1, 7), (0, -8), (-1, 8), (1, -9), (-2, 9),
              (1, -10), (-2, 10), (1, -11), (-2, 11), (1, -11), (-2, 11), (1, -11), (-1, 0), (-1, 10), (0, -9),
              (-1, 9), (0, -9), (-1, 9), (0, -9), (-1, 9), (0, -9)]  # border
title_master = []
title_pos = title_start
for direc in title_path:
    title_pos = (title_pos[0] + direc[0], title_pos[1] + direc[1])
    title_master.append([title_pos[0], title_pos[1], 0])
title_master = title_master + [ele + [0] for ele in snake_head] \
               + [ele + [0] for ele in reversed(snake_start)]  # includes snake in title screen
main_font = pg.font.SysFont('Consolas', 15)  # main font
small_font = pg.font.SysFont('Consolas', 10)  # smaller font
rules = {
    'Rules': [320, 26],
    'Collect food to': [320, 28],
    'increase score': [320, 30],
    'Reach 25 score to win': [320, 32]
}
controls = {
    'Controls': [320, 37],
    'WASD - move': [320, 39],
    'SPACE - play/ pause/': [320, 41],
    'skip intro': [384, 43],
    'ESC - return/ quit': [320, 45],
    'MB - change options': [320, 47]
}
rules_controls = {**rules, **controls}  # combines rules and controls dictionaries
options = {
    0: ['base Colour: ', ['White', 'Red', 'Green', 'Blue', 'Yellow', 'Pink', 'Teal'], 0,
        'Colour of most things in game', 20],
    1: ['Background: ', ['Style 1', 'Style 2', 'Style 3'], 0, 'Toggles background style', 40],
    2: ['added Particles: ', ['True', 'False'], 0, 'Additional particles effects', 36],
    3: ['Number of wraps: ', ['Unlimited', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 6,
        'Available screen wraps', 24],
    4: ['Visual style: ', ['Blocks', 'Pixel Art', 'Particles'], 0, 'Visual style of snake and food', 32],
    5: ['Tail style: ', ['Base Colour', 'Background Fade', 'Food Colour'], 0, 'How new tail colour is determined', 28],
    6: ['Mute audio: ', ['True', 'False'], 1, 'Toggles game audio', 44]
}  # options information dictionary (index: text, options, current option, tooltip, height)

# sounds
pg.mixer.music.load('Assets/Audio/theme.wav')  # theme
pg.mixer.music.set_volume(0.05)  # lowers volume
pg.mixer.music.play(-1)  # play theme music continuously
sound_list = [['menu_click', 0.5], ['pause', 0.5], ['esc', 0.5], ['snake_move', 0.05], ['snake_eat', 0.2],
              ['win', 0.25], ['lose', 0.1], ['snake_edge', 0.5], ['borders', 0.5], ['start', 0.1]]
sounds = {}
for sound in sound_list:
    sfx = pg.mixer.Sound(f'Assets/Audio/{sound[0]}.wav')
    sfx.set_volume(sound[1])
    sounds[sound[0]] = sfx


def menu():  # menu control
    global button_collide
    reset = True
    animate = True
    title = title_master.copy()
    title_speed_name = 50
    title_speed_snake = 20
    title_speed = title_speed_name
    title_counter = 0
    menu_text_fade = 0
    menu_text_fade_time = 150
    pg.mouse.set_visible(False)
    while True:
        if reset:  # resets certain variables
            title_timer = 0
            start = title_start
            reset = False
            particles = []
            food_colour = random.randint(0, num_food_colours - 1)
            button_collide = [0] * len(options)

        dt = clock.tick(fps)
        title_timer += dt
        if title_timer >= title_speed:
            title_counter += 1
            if title_counter > 100:
                title_speed = title_speed_snake
                menu_text_fade += 1
                if menu_text_fade > menu_text_fade_time:
                    menu_text_fade = menu_text_fade_time
            title.append(title.pop(0))

            temp = title_path.pop(0)
            start = (start[0] + temp[0], start[1] + temp[1])
            title_path.append(temp)
            title_timer = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                keys_pressed = pg.key.get_pressed()
                if keys_pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if keys_pressed[pg.K_SPACE]:
                    if animate:
                        for pos in snake_start:
                            try:
                                title.remove(pos + [0])
                            except ValueError:
                                pass
                            try:
                                title.remove(pos + [1])
                            except ValueError:
                                pass
                        animate = False
                        menu_text_fade = True
                        buttons = []  # options
                        for option in range(len(options)):
                            temp_text = main_font.render(options[option][0] + options[option][1][options[option][2]],
                                                         True, convert_colours(options[0][1][options[0][2]]))
                            temp_button = pg.Rect(scale * 2, scale * options[option][4], temp_text.get_width() + scale,
                                                  temp_text.get_height() + int(scale / 2))
                            temp_tooltip = main_font.render(options[option][3], True,
                                                            convert_colours(options[0][1][options[0][2]]))
                            buttons.append([temp_text, temp_button, temp_tooltip])
                        sounds['esc'].play()
                        pg.mouse.set_visible(True)

                    else:
                        sounds['start'].play()
                        reset = game(options, food_colour, particles)
                if not animate:  # option key binds
                    option_index = -1
                    if keys_pressed[pg.K_c]:
                        option_index = 0
                    if keys_pressed[pg.K_b]:
                        option_index = 1
                    if keys_pressed[pg.K_p]:
                        option_index = 2
                    if keys_pressed[pg.K_n]:
                        option_index = 3
                    if keys_pressed[pg.K_v]:
                        option_index = 4
                    if keys_pressed[pg.K_t]:
                        option_index = 5
                    if keys_pressed[pg.K_m]:
                        option_index = 6

                    if option_index != -1:
                        new_index = options[option_index][2] + 1
                        if new_index > len(options[option_index][1]) - 1:  # wrap index value
                            new_index = 0
                        options[option_index][2] = new_index
                        sounds['menu_click'].play()

            if not animate:
                mouse_pos = pg.mouse.get_pos()  # gets mouse position
                button_collide = [int(buttons[index][1].collidepoint(mouse_pos)) for index
                                  in range(len(button_collide))]  # checks for collision between mouse and all buttons
                if 1 in button_collide:  # if mouse is colliding with a button
                    button = button_collide.index(1)  # gets collided button index
                    if event.type == pg.MOUSEMOTION:
                        particles.append(Particle(mouse_pos[0],
                                                  mouse_pos[1],
                                                  random.randint(-10, 10) / 10,
                                                  random.randint(-5, 5) / 10,
                                                  0,
                                                  0.2,
                                                  convert_colours(options[0][1][options[0][2]]),
                                                  random.randint(1, 2),
                                                  0.1))
                    if event.type == pg.MOUSEBUTTONUP:  # if mouse button depressed
                        if event.button == 1 or event.button == 3:  # if left or right mouse button clicked
                            cur_index = options[button][2]  # current index
                            if event.button == 1:  # increment index with left click
                                new_index = cur_index + 1
                                if new_index > len(options[button][1]) - 1:  # wrap index value
                                    new_index = 0
                            elif event.button == 3:  # decrement index with right click
                                new_index = cur_index - 1
                                if new_index < 0:  # wrap index value
                                    new_index = len(options[button][1]) - 1
                            options[button][2] = new_index  # new index
                            sounds['menu_click'].play()

        if title[5][-1] == 1 and animate:
            del title[0:5]  # deletes snake from title array
            animate = False
            pg.mouse.set_visible(True)
            buttons = []  # options
            for option in range(len(options)):
                temp_text = main_font.render(options[option][0] + options[option][1][options[option][2]],
                                             True, convert_colours(options[0][1][options[0][2]]))
                temp_button = pg.Rect(scale * 2, scale * options[option][4], temp_text.get_width() + scale,
                                      temp_text.get_height() + int(scale / 2))
                temp_tooltip = main_font.render(options[option][3], True, convert_colours(options[0][1][options[0][2]]))
                buttons.append([temp_text, temp_button, temp_tooltip])
        snake_colours = [convert_colours(options[0][1][options[0][2]])] * len(snake_start)
        buttons = draw_menu(options, title, animate, food_colour, snake_colours, particles, menu_text_fade,
                            menu_text_fade_time, button_collide)
        if options[6][1][options[6][2]] == 'True':
            pg.mixer.music.set_volume(0)  # mutes musics
            for key in sounds:  # mutes sound effects
                sounds[key].set_volume(0)
        else:
            pg.mixer.music.set_volume(0.05)  # un mute
            for index, key in enumerate(sounds):
                sounds[key].set_volume(sound_list[index][1])


# draws menu screen
def draw_menu(options, title, animate, food_colour, snake_colours, particles, menu_text_fade,
              menu_text_fade_time, button_collide):
    base_colour = options[0][1][options[0][2]]
    bg_style = options[1][1][options[1][2]]
    visual_style = options[4][1][options[4][2]]
    screen.fill(bg_colour)
    draw_title(title, animate, bg_style, base_colour)
    if menu_text_fade > 0:
        buttons = draw_menu_text(base_colour, animate, menu_text_fade, menu_text_fade_time, button_collide)
    else:
        buttons = []
    if not animate:
        particles = draw_snake(visual_style, snake_start, snake_colours, particles)
        draw_food(visual_style, food_start, food_colour, particles, False)
        draw_particles(particles)
    pg.display.update()
    return buttons


def draw_title(title, animate, bg_style, base_colour):  # draws title text with snaking effect
    if not animate:
        if bg_style == 'Style 2':
            screen.blit(bg_images[0], (0, 0))
        elif bg_style == 'Style 3':
            screen.blit(bg_images[1], (0, 0))
    for index, pos in enumerate(title):
        outline = 0
        if animate:
            if index == 4:
                outline = 2
                pos[2] = 1
            elif index == 3:
                outline = -4
                pos[2] = 1
            elif index == 2:
                outline = -3
                pos[2] = 1
            elif index == 1:
                outline = -2
                pos[2] = 1
            elif index == 0:
                outline = -1
                pos[2] = 1
            elif pos[2] == 0:
                outline = 2
        rect = pg.Rect(pos[0] * scale, pos[1] * scale, scale, scale)
        pg.draw.rect(screen, convert_colours(base_colour), rect)
        pg.draw.rect(screen, bg_colour, rect, 2 - outline)


def convert_colours(name):
    if name == 'White':
        colour = (230, 230, 230)
    elif name == 'Red':
        colour = (255, 0, 0)
    elif name == 'Green':
        colour = (0, 255, 0)
    elif name == 'Blue':
        colour = (0, 0, 255)
    elif name == 'Yellow':
        colour = (255, 255, 0)
    elif name == 'Pink':
        colour = (255, 0, 255)
    elif name == 'Teal':
        colour = (0, 255, 255)
    else:
        colour = (230, 230, 230)
    return colour


def draw_menu_text(base_colour, animate, menu_text_fade, menu_text_fade_time, button_collide):  # draws game controls
    if animate:
        colour_dif = ((convert_colours(base_colour)[0] - bg_colour[0]) / menu_text_fade_time,
                      (convert_colours(base_colour)[1] - bg_colour[1]) / menu_text_fade_time,
                      (convert_colours(base_colour)[2] - bg_colour[2]) / menu_text_fade_time)
        colour = (bg_colour[0] + colour_dif[0] * menu_text_fade,
                  bg_colour[1] + colour_dif[1] * menu_text_fade,
                  bg_colour[2] + colour_dif[2] * menu_text_fade)
    else:
        colour = convert_colours(base_colour)

    for key in rules:
        pass

    for key in rules_controls:  # controls
        pos = rules_controls[key]
        text = main_font.render(key, True, colour)
        screen.blit(text, (pos[0], pos[1] * scale))

    buttons = []  # options
    temp_text = main_font.render('Options', True, colour)
    screen.blit(temp_text, (20, 180))
    for option in range(len(options)):
        temp_text = main_font.render(options[option][0] + options[option][1][options[option][2]], True, colour)
        temp_button = pg.Rect(scale * 2, scale * options[option][4], temp_text.get_width() + scale,
                              temp_text.get_height() + int(scale / 2))
        temp_tooltip = small_font.render(options[option][3], True, colour)
        buttons.append([temp_text, temp_button, temp_tooltip])
    for index, button in enumerate(buttons):
        screen.blit(button[0], (button[1][0] + int(scale / 2), button[1][1] + int(scale / 4)))
        pg.draw.rect(screen, colour, button[1], 1 + button_collide[index])
        if button_collide[index]:  # tooltip
            screen.blit(button[2], (20, int((options[index][4] + 2.5) * scale)))
    return buttons


# game control
def game(options, food_colour, particles):
    # player options
    base_colour = options[0][1][options[0][2]]
    bg_style = options[1][1][options[1][2]]
    added_particles = options[2][1][options[2][2]] == 'True'
    wrap_uses = options[3][1][options[3][2]]
    if wrap_uses == 'Unlimited':
        wrap_uses = 1000000
    else:
        wrap_uses = int(wrap_uses)
    visual_style = options[4][1][options[4][2]]
    tail_style = options[5][1][options[5][2]]
    snake_colours = [convert_colours(base_colour)] * len(snake_start)

    run = True
    running, pause = 0, 1
    state = running
    pg.mouse.set_visible(False)
    snake = snake_start.copy()
    snake_dir = (0, -1)
    new_dir = snake_dir
    food = food_start
    grow = False
    border = False
    snake_speed = 50
    snake_timer = 0
    border_size = 0
    wrap_counter = 0
    score = 0
    score_win = 25
    won = False
    lost = False
    particle_speed = 250
    particle_timer = 0
    fade_start = 5
    fade_length = 15

    while run:
        if state == running:
            if added_particles:
                if particle_timer >= particle_speed:
                    for _ in range(score):
                        particles.append(Particle(screen_width / 2,
                                                  -150,
                                                  random.randint(-50, 50) / 10,
                                                  random.randint(-10, 10) / 10,
                                                  0,
                                                  0.2,
                                                  convert_colours(base_colour),
                                                  random.randint(1, 3),
                                                  random.randint(0, 25) / 100))
                    particle_timer = 0

            # snake control
            if snake_timer >= snake_speed and not won and not lost:
                if snake_dir != new_dir:
                    sounds['snake_move'].play()
                snake_dir = new_dir  # snake direction
                new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])  # new head position

                if new_head in snake:  # if snake hits its tail
                    lost = True
                    lost_counter = 0
                    sounds['lose'].play()

                if wrap_counter < wrap_uses:  # wraps snake to opposite side of board
                    if new_head[0] == -1:  # left side
                        new_head = (board_width - 1, new_head[1])
                        wrap_counter += 1
                        sounds['snake_edge'].play()
                    elif new_head[0] == board_width:  # right side
                        new_head = (0, new_head[1])
                        wrap_counter += 1
                        sounds['snake_edge'].play()
                    elif new_head[1] == -1:  # top side
                        new_head = (new_head[0], board_height - 1)
                        wrap_counter += 1
                        sounds['snake_edge'].play()
                    elif new_head[1] == board_height:  # bottom side
                        new_head = (new_head[0], 0)
                        wrap_counter += 1
                        sounds['snake_edge'].play()
                else:
                    if new_head[0] == 0 or new_head[0] == board_width - 1 or new_head[1] == 0 \
                            or new_head[1] == board_height - 1:
                        lost = True
                        lost_counter = 0
                        sounds['lose'].play()

                if not border and wrap_counter == wrap_uses:
                    border = True
                    border_size = 10
                    sounds['borders'].play()
                if border_size > 0:
                    border_size -= 1  # animates border

                if new_head == food:  # if snake eats food
                    while food in snake or food == new_head:
                        # spawns new food
                        food = (random.randint(1, board_width - 2), random.randint(1, board_height - 2))
                    grow = True  # snake grows
                    snake_speed -= 1  # snake speed increases
                    score += 1  # increments scored
                    sounds['snake_eat'].play()
                    if score == score_win:
                        won = True
                        won_counter = 0
                        sounds['win'].play()
                    if added_particles:
                        for _ in range(5 * score):  # spawns flurry of particles
                            particles.append(Particle(new_head[0] * scale + int(scale / 2),
                                                      new_head[1] * scale + int(scale / 2),
                                                      random.randint(-50, 50) / 10,
                                                      random.randint(-50, 50) / 10,
                                                      0,
                                                      0.1,
                                                      food_colours[food_colour],
                                                      random.randint(1, 3),
                                                      random.randint(0, 25) / 100))
                    b_colour = convert_colours(base_colour)
                    if tail_style == 'Base Colour':  # default colour
                        snake_colours.append(b_colour)
                    elif tail_style == 'Background Fade':  # background fade
                        index = len(snake)
                        if index < fade_start:
                            colour = b_colour
                        elif index < fade_start + fade_length:
                            fade_scale = (int((bg_colour[0] - b_colour[0]) / fade_length),
                                          int((bg_colour[1] - b_colour[1]) / fade_length),
                                          int((bg_colour[2] - b_colour[2]) / fade_length))
                            colour = (b_colour[0] + fade_scale[0] * (index - fade_start),
                                      b_colour[1] + fade_scale[1] * (index - fade_start),
                                      b_colour[2] + fade_scale[2] * (index - fade_start))
                        else:
                            colour = bg_colour
                        snake_colours.append(colour)
                    elif tail_style == 'Food Colour':  # food colour
                        snake_colours.append(food_colours[food_colour])
                    food_colour = random.randint(0, num_food_colours - 1)  # new food colour

                # moves snake
                snake.insert(0, new_head)  # adds new head to snake
                if grow:
                    grow = False  # snake grows in length
                else:
                    snake.pop(-1)  # remove end tail
                snake_timer = 0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    keys_pressed = pg.key.get_pressed()
                    if keys_pressed[pg.K_ESCAPE]:
                        pg.mixer.pause()
                        sounds['esc'].play()
                        pg.mouse.set_visible(True)
                        return True

                    # snake movement
                    if keys_pressed[pg.K_w] and snake_dir != (0, -1) and snake_dir != (0, 1):
                        new_dir = (0, -1)
                    elif keys_pressed[pg.K_s] and snake_dir != (0, 1) and snake_dir != (0, -1):
                        new_dir = (0, 1)
                    elif keys_pressed[pg.K_a] and snake_dir != (-1, 0) and snake_dir != (1, 0):
                        new_dir = (-1, 0)
                    elif keys_pressed[pg.K_d] and snake_dir != (1, 0) and snake_dir != (-1, 0):
                        new_dir = (1, 0)

                    if keys_pressed[pg.K_SPACE] and not won and not lost:
                        state = pause
                        sounds['pause'].play()

            draw_game(visual_style, bg_style, snake, food, food_colour, snake_colours, score, particles,
                      base_colour, border, border_size, state == pause, won, lost)
            dt = clock.tick(fps)
            snake_timer += dt
            particle_timer += dt
            if won:
                for _ in range(3):
                    particles.append(Particle(screen_width / 2,
                                              screen_height + 25,
                                              random.randint(-30, 30) / 10,
                                              random.randint(-125, 0) / 10,
                                              random.randint(-1, 1) / 100,
                                              0.2,
                                              random.choice(base_colours),
                                              random.randint(1, 5),
                                              0.025))
                won_counter += 1
                if won_counter > fps * 10:  # 3 second timer
                    pg.mouse.set_visible(True)
                    return True
            if lost:
                particles.append(Particle(random.randint(0, screen_width),
                                          -10,
                                          0,
                                          random.randint(0, 10) / 10,
                                          0,
                                          0.2,
                                          (0, 0, random.randint(0, 255)),
                                          random.randint(1, 2),
                                          0.005))
                lost_counter += 1
                if lost_counter > fps * 5:  # 3 second timer
                    pg.mouse.set_visible(True)
                    return True
        elif state == pause:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    keys_pressed = pg.key.get_pressed()
                    if keys_pressed[pg.K_ESCAPE]:
                        sounds['esc'].play()
                        return True
                    if keys_pressed[pg.K_SPACE]:
                        state = running
                        sounds['pause'].play()


def is_edge(width, height, pos):
    if 0 <= pos[0] < width and 0 <= pos[1] < height:
        return False
    else:
        return True


# draws game screen
def draw_game(visual_style, bg_style, snake, food, food_colour, snake_colours, score, particles,
              base_colour, border, border_size, pause, won, lost):
    screen.fill(bg_colour)
    if bg_style == 'Style 2':
        screen.blit(bg_images[0], (0, 0))
    elif bg_style == 'Style 3':
        screen.blit(bg_images[1], (0, 0))
    particles = draw_snake(visual_style, snake, snake_colours, particles)
    particles = draw_food(visual_style, food, food_colour, particles, won)
    if border:
        draw_border(base_colour, border_size)
    draw_score(score, base_colour)
    draw_particles(particles, not pause)
    if pause:
        draw_text('Paused', base_colour)
    if won:
        draw_text('You Won!', base_colour)
    if lost:
        draw_text('You Lost!', base_colour)
    pg.display.update()


def draw_snake(visual_style, snake, snake_colours, particles):  # draws snake
    for pos, col in zip(snake, snake_colours):
        if visual_style == 'Blocks':  # blocks
            rect = pg.Rect(pos[0] * scale, pos[1] * scale, scale, scale)
            pg.draw.rect(screen, col, rect)
            pg.draw.rect(screen, bg_colour, rect, 2)
        elif visual_style == 'Pixel Art':  # pixel art
            if snake.index(pos) == 0:
                image = palette_swap(snake_images[0], (230, 230, 230), col)
            else:
                image = palette_swap(snake_images[1], (230, 230, 230), col)
            screen.blit(image, (pos[0] * scale, pos[1] * scale))
        elif visual_style == 'Particles':  # particles
            particles.append(Particle(pos[0] * scale + scale / 2,
                                      pos[1] * scale + scale / 2,
                                      random.randint(-5, 5) / 10,
                                      random.randint(-5, 5) / 10,
                                      0,
                                      0,
                                      col,
                                      random.randint(0, 2),
                                      0.075))
    return particles


def palette_swap(surf, old_c, new_c):
    surf.set_colorkey(old_c)
    img_copy = pg.Surface(surf.get_size())
    img_copy.fill(new_c)
    img_copy.blit(surf, (0, 0))
    img_copy.set_colorkey((25, 25, 25))
    return img_copy


def draw_food(visual_style, food, food_colour, particles, won):  # draws food
    if not won:
        if visual_style == 'Blocks':  # blocks
            rect = pg.Rect(food[0] * scale, food[1] * scale, scale, scale)
            pg.draw.rect(screen, food_colours[food_colour], rect)
            pg.draw.rect(screen, bg_colour, rect, 2)
        elif visual_style == 'Pixel Art':  # pixel art
            screen.blit(food_images[food_colour], (food[0] * scale, food[1] * scale))
        elif visual_style == 'Particles':  # particles
            for _ in range(5):
                particles.append(Particle(food[0] * scale + scale / 2,
                                          food[1] * scale + scale / 2,
                                          random.randint(-10, 10) / 10,
                                          random.randint(-20, 10) / 10,
                                          0,
                                          0.1,
                                          food_colours[food_colour],
                                          random.randint(0, 2),
                                          0.075))
    return particles


def draw_score(score, base_colour):  # draws score
    text = main_font.render('Score: ' + str(score), True, convert_colours(base_colour))
    screen.blit(text, (int((screen_width - text.get_width()) / 2), scale))


def draw_border(base_colour, border_size):
    for x_pos in range(board_width):
        rect_top = pg.Rect(x_pos * scale, 0, scale, scale)  # top border
        pg.draw.rect(screen, convert_colours(base_colour), rect_top)
        pg.draw.rect(screen, bg_colour, rect_top, 2 + border_size)
        rect_bot = pg.Rect(x_pos * scale, (board_height - 1) * scale, scale, scale)  # bottom border
        pg.draw.rect(screen, convert_colours(base_colour), rect_bot)
        pg.draw.rect(screen, bg_colour, rect_bot, 2 + border_size)
    for y_pos in range(1, board_height - 1):
        rect_top = pg.Rect(0, y_pos * scale, scale, scale)  # top border
        pg.draw.rect(screen, convert_colours(base_colour), rect_top)
        pg.draw.rect(screen, bg_colour, rect_top, 2 + border_size)
        rect_bot = pg.Rect((board_width - 1) * scale, y_pos * scale, scale, scale)  # bottom border
        pg.draw.rect(screen, convert_colours(base_colour), rect_bot)
        pg.draw.rect(screen, bg_colour, rect_bot, 2 + border_size)


def draw_text(text, base_colour):
    text = main_font.render(f'{text}', True, convert_colours(base_colour))
    screen.blit(text, (int((screen_width - text.get_width()) / 2), int(screen_height / 3)))


class Particle:  # particle control
    def __init__(self, x_pos, y_pos, x_vel, y_vel, x_acc, y_acc, colour, size, shrink):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.colour = colour
        self.size = size
        self.shrink = shrink

    def draw(self, update):
        pg.draw.circle(screen, self.colour, (int(self.x_pos), int(self.y_pos)), int(self.size))  # draw particle
        if update:
            self.x_pos += self.x_vel  # x position + velocity
            self.y_pos += self.y_vel  # y position + velocity
            self.x_vel += self.x_acc  # x velocity + acceleration
            self.y_vel += self.y_acc  # y velocity + acceleration
            self.size -= self.shrink  # adjust particle size


def draw_particles(particles, update=True):  # draws particles
    for _, particle in sorted(enumerate(particles), reverse=True):
        if particle.size <= 0 or (not -screen_width <= particle.x_pos <= screen_width * 2) \
                or (not -screen_height <= particle.y_pos <= screen_height * 2):
            particles.remove(particle)
        else:
            particle.draw(update)  # draws particle


menu()
