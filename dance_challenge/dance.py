import pygame
import sys
from random import randint
import pgzrun

WIDTH = 1401
HEIGHT = 800
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

move_list = []
display_list = []
confetti_list = []
balloon_list = []

score = 0
current_move = 0
count = 4
dance_length = 4

say_dance = False
show_countdown = True
moves_complete = False
game_over = False
game_started = False  # Track whether the title screen has been passed

dancer = Actor("dancer_start")
dancer.pos = CENTER_X + 5, CENTER_Y - 40

up = Actor("up")
up.pos = CENTER_X, CENTER_Y + 110
right = Actor("right")
right.pos = CENTER_X + 60, CENTER_Y + 170
down = Actor("down")
down.pos = CENTER_X, CENTER_Y + 230
left = Actor("left")
left.pos = CENTER_X - 60, CENTER_Y + 170

# Setup confetti particles
for i in range(60):
    confetti_list.append({
        "x": randint(0, WIDTH),
        "y": randint(0, HEIGHT),
        "speed": randint(2, 6),
        "size": randint(4, 9),
        "color": (randint(150, 255), randint(100, 255), randint(100, 255))
    })

# Setup floating balloon particles
for i in range(8):
    balloon_list.append({
        "x": randint(50, WIDTH - 50),
        "y": randint(0, HEIGHT),
        "speed": randint(1, 3),
        "radius": randint(15, 25),
        "color": (randint(100, 220), randint(100, 220), 255)
    })

def draw():
    global game_over, score, say_dance, game_started
    global count, show_countdown
    
    current_width = screen.width
    current_height = screen.height
    center_x = current_width / 2
    center_y = current_height / 2

    # 1. TITLE SCREEN
    if not game_started:
        screen.clear()
        scaled_stage = pygame.transform.scale(images.stage, (current_width, current_height))
        screen.blit(scaled_stage, (0, 0))
        
        # Draw confetti & balloons on the title screen
        for p in confetti_list:
            screen.draw.filled_circle((p["x"], p["y"]), p["size"], p["color"])
        for b in balloon_list:
            screen.draw.filled_circle((b["x"], b["y"]), b["radius"], b["color"])
            screen.draw.line((b["x"], b["y"] + b["radius"]), (b["x"], b["y"] + b["radius"] + 20), (255, 255, 255))

        # Title text
        screen.draw.text("HAPPY BIRTHDAY!", color="black", center=(center_x, center_y - 60), fontsize=65)
        screen.draw.text("Press ENTER to Start Dancing!", color="white", center=(center_x, center_y + 10), fontsize=35)
        return

    # 2. GAMEPLAY SCREEN
    if not game_over:
        screen.clear()
        
        scaled_stage = pygame.transform.scale(images.stage, (current_width, current_height))
        screen.blit(scaled_stage, (0, 0))
        
        for p in confetti_list:
            screen.draw.filled_circle((p["x"], p["y"]), p["size"], p["color"])
        for b in balloon_list:
            screen.draw.filled_circle((b["x"], b["y"]), b["radius"], b["color"])
            screen.draw.line((b["x"], b["y"] + b["radius"]), (b["x"], b["y"] + b["radius"] + 20), (255, 255, 255))
        
        dancer.draw()
        up.draw()
        down.draw()
        right.draw()
        left.draw()
        
        screen.draw.text("Score: " + str(score), color="white", topleft=(20, 20))
        
        if say_dance:
            screen.draw.text("Dance!", color="black", center=(center_x, 150), fontsize=60)
        if show_countdown:
            screen.draw.text(str(count), color="black", center=(center_x, 150), fontsize=60)
            
    # 3. GAME OVER SCREEN
    else:
        screen.clear()
        
        scaled_stage = pygame.transform.scale(images.stage, (current_width, current_height))
        screen.blit(scaled_stage, (0, 0))
        
        screen.draw.text("Score: " + str(score), color="black", topleft=(10, 10))
        screen.draw.text("GAME OVER!", color="black", center=(center_x, 220), fontsize=60)
    return

def reset_dancer():
    global game_over
    if not game_over:
        dancer.image = "dancer_start"
        up.image = "up"
        right.image = "right"
        down.image = "down"
        left.image = "left"
    return

def update_dancer(move):
    global game_over
    if not game_over:
        if move == 0:
            up.image = "up_lit"
            dancer.image = "dancer_up"
            clock.schedule(reset_dancer, 0.5)
        elif move == 1:
            right.image = "right_lit"
            dancer.image = "dancer_right"
            clock.schedule(reset_dancer, 0.5)
        elif move == 2:
            down.image = "down_lit"
            dancer.image = "dancer_down"
            clock.schedule(reset_dancer, 0.5)
        else:
            left.image = "left_lit"
            dancer.image= "dancer_left"
            clock.schedule(reset_dancer, 0.5)
    return

def display_moves():
    global move_list, display_list, dance_length
    global say_dance, show_countdown, current_move
    if display_list:
        this_move = display_list[0]
        display_list = display_list[1:]
        if this_move == 0:
            update_dancer(0)
            clock.schedule(display_moves, 1)
        elif this_move == 1:
            update_dancer(1)
            clock.schedule(display_moves, 1)
        elif this_move == 2:
            update_dancer(2)
            clock.schedule(display_moves, 1)
        elif this_move == 3:
            update_dancer(3)
            clock.schedule(display_moves, 1)
    else:
        say_dance = True
        show_countdown = False
    return            

def generate_moves():
    global move_list, dance_length, count
    global show_countdown, say_dance, moves_complete
    count = 4
    move_list = []
    moves_complete = False
    say_dance = False
    for move in range(0, dance_length):
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)
    show_countdown = True
    countdown()
    return

def countdown():
    global count, game_over, show_countdown
    if count > 1:
        count = count - 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()
    return

def next_move():
    global dance_length, current_move, moves_complete
    if current_move < dance_length - 1:
        current_move = current_move + 1
    else:
        moves_complete = True
    return

def on_key_up(key):
    global score, game_over, move_list, current_move, game_started
    
    # If we are on the title screen, start the game and switch music to dance on ENTER
    if not game_started:
        if key == keys.RETURN:
            game_started = True
            music.play("dance")  # Switches from title music to dance music!
            generate_moves()
        return

    # Normal gameplay controls once started
    if not game_over:
        if key == keys.UP:
            update_dancer(0)
            if move_list[current_move] == 0:
                score = score + 1
                next_move()
            else:
                game_over = True
        elif key == keys.RIGHT:
            update_dancer(1)
            if move_list[current_move] == 1:
                score = score + 1
                next_move()
            else:
                game_over = True
        elif key == keys.DOWN:
            update_dancer(2)
            if move_list[current_move] == 2:
                score = score + 1
                next_move()
            else:
                game_over = True
        elif key == keys.LEFT:
            update_dancer(3)
            if move_list[current_move] == 3:
                score = score + 1
                next_move()
            else:
                game_over = True
    return

# Play the title music as soon as the game opens
music.play("title")

def update():
    global game_over, current_move, moves_complete, game_started
    
    # Animate confetti falling down
    for p in confetti_list:
        p["y"] += p["speed"]
        if p["y"] > HEIGHT:
            p["y"] = 0
            p["x"] = randint(0, WIDTH)
            
    # Animate balloons floating up
    for b in balloon_list:
        b["y"] -= b["speed"]
        if b["y"] < -50:
            b["y"] = HEIGHT + 50
            b["x"] = randint(50, WIDTH - 50)

    # Only run game logic if the game has actually started
    if game_started:
        if not game_over:
            if moves_complete:
                generate_moves()
                current_move = 0
        else:
            music.stop()
            
pgzrun.go()
