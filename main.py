import pygame as pg
import random, time
pg.init()
clock = pg.time.Clock()

black = (0, 0, 0)

win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris')

font = pg.font.Font(None, 30)
speed = 10
score = 0
lives = 3
running = True

player_size = 70
player_pos = [win_width / 2, win_height - player_size]  
player_image = pg.image.load('./assets/images/Screenshot 2025-07-29 144049.png')
player_image = pg.transform.scale(player_image, (player_size, player_size)) 

obj_size = 60
obj_data = []     
obj = pg.image.load('./assets/images/Screenshot 2025-07-29 144431.png')
obj = pg.transform.scale(obj, (obj_size, obj_size))

heart_size = 60
heart_data = []     
heart = pg.image.load('./assets/images/Screenshot 2025-07-29 144530.png')
heart = pg.transform.scale(heart, (heart_size, heart_size))

apple_size = 60
apple_data = []     
apple = pg.image.load('./assets/images/Screenshot 2025-07-29 144305.png')
apple = pg.transform.scale(apple, (apple_size, apple_size))

bg_image = pg.image.load('./assets/images/Screenshot 2025-07-29 141243.png')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))


def create_object(obj_data):
    if len(obj_data) < 10 and random.random() < 0.1:            
        x = random.randint(0, win_width - obj_size)
        y = 0                                         
        obj_data.append([x, y, obj])

def create_heart(heart_data):
    if len(heart_data) < 1 and random.random() < 0.1:            
        x = random.randint(0, win_width - heart_size)
        y = 0                                         
        heart_data.append([x, y, heart])

def create_apple(apple_data):
    if len(apple_data) < 10 and random.random() < 0.1:            
        x = random.randint(0, win_width - apple_size)
        y = 0                                         
        apple_data.append([x, y, apple])


def update_objects(obj_data):
    global score

    for object in obj_data:
        x, y, image_data = object
        if y < win_height:
            y += speed
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            score += 1

def update_heart(heart_data):
    global score
    for heart in heart_data:
        x, y, image_data = heart
        if y < win_height:
            y += speed
            heart[1] = y
            screen.blit(image_data, (x, y))
            score += 1
        else:
            heart_data.remove(heart)

def update_apple(apple_data):
    global score
    for apple in apple_data:
        x, y, image_data = apple
        if y < win_height:
            y += speed
            apple[1] = y
            screen.blit(image_data, (x, y))
            
        else:
            apple_data.remove(apple)

def collision_check(obj_data, player_pos):
    global running, lives

    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            obj_data.remove(object)
            lives -= 1
            if lives == 0:
                text = f'Oh no!Game over!'
                text = font.render(text, 10, black)
                screen.blit(text, (player_x-50, player_y-40))
                pg.display.update()
                time.sleep(2)
                running = False
            break

def heart_collision_check(heart_data, player_pos):
    global running, lives

    for heart in heart_data:
        xh, yh, image_data = heart
        player_x, player_y = player_pos[0], player_pos[1]
        heart_rect = pg.Rect(xh, yh, heart_size, heart_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(heart_rect):
            heart_data.remove(heart)
            lives += 1
            break


def apple_collision_check(apple_data, player_pos):
    global running, lives, score

    for apple in apple_data:
        x, y, image_data = apple
        player_x, player_y = player_pos[0], player_pos[1]
        apple_rect = pg.Rect(x, y, apple_size, apple_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(apple_rect):
            apple_data.remove(apple)
            score += 1
            break
            
def main():

    global running, player_pos

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                x, y = player_pos[0], player_pos[1]
                if event.key == pg.K_LEFT:
                    x -= 20
                elif event.key == pg.K_RIGHT:
                    x += 20
                player_pos = [x, y]

        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Score: {score}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 60))
        text = f'Lives: {lives}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 40))

        create_object(obj_data)
        update_objects(obj_data)
        collision_check(obj_data, player_pos)

        create_heart(heart_data)
        update_heart(heart_data)
        heart_collision_check(heart_data, player_pos)

        create_apple(apple_data)
        update_apple(apple_data)
        apple_collision_check(apple_data, player_pos)

        clock.tick(25)
        pg.display.flip()

main()