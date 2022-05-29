import play
import pygame
from random import randint


pip_list = []

def draw_pip(top_height, pip_list):
    tot_ver_pix = play.screen.top - play.screen.bottom
    pixel_gap = 190
    bot_height = tot_ver_pix - pixel_gap - 40 - top_height

    pip_body_up = play.new_box(width=100, height=top_height, color = 'green', border_color='black', border_width=4, y = play.screen.top - top_height / 2, x = play.screen.right + 80)
    pip_head_up = play.new_box(width=130, height=40, color='green', border_color='black', border_width=4, y=play.screen.top - top_height, x=  play.screen.right + 80)
    pip_body_down = play.new_box(width=100, height=bot_height, color = 'green', border_color='black', border_width=4, y = play.screen.bottom + bot_height / 2, x =  play.screen.right + 80)
    pip_head_down = play.new_box(width=130, height=40, color='green', border_color='black', border_width=4, y=play.screen.bottom + bot_height, x=  play.screen.right + 80)
    pip_list.append(pip_body_down)
    pip_list.append(pip_body_up)
    pip_list.append(pip_head_down)
    pip_list.append(pip_head_up)
    draw_coins(bot_height - 210, play.screen.right + 80)




coin_sound = pygame.mixer.Sound('coin.wav')
sea_sound = pygame.mixer.Sound('OH NO.wav')
pygame.mixer.Sound.set_volume(sea_sound, 0.08)
pygame.display.set_caption('Platformer: cel mai greu joc din toate timpurile!')
soundtrack = pygame.mixer.Sound('soundtrack.mp3')

#sprite = play.new_image(image = 'bird.png', x= - 50, y=0, size = 5)
sprite = play.new_circle(color='light grey', x= -50, y=0, border_color='grey', border_width=3, radius=15)
platforms = []
coins = []
vol = []
vol_image = play.new_image(image = 'volume.png', x = play.screen.left + 40, y = play.screen.top - 40, size = 12)
for i in range(4):
    change_vol_b = play.new_box(y = play.screen.top - 40, x = play.screen.left + 90 + i * 35 , color= 'red', border_color= 'black', border_width= 6, width= 30, height=15 + i * 15)
    vol.append(change_vol_b)



def draw_coins(y_loc, x_loc):
    coin = play.new_circle(
        color='yellow', x= x_loc, y=y_loc, radius=10
    )
    coins.append(coin)






score_txt = play.new_text(words='Score:', x=play.screen.right-100, y=play.screen.top-30, size=70)
score = play.new_text(words='0', x=play.screen.right-30, y=play.screen.top-30, size=70)

@play.when_program_starts
def start():
    pygame.mixer.Sound.set_volume(soundtrack, 0.1)
    soundtrack.play()
    sprite.start_physics(can_move=True, stable=False, obeys_gravity=True, mass=10, friction=1.0, bounciness=0.5)

    
@play.repeat_forever
async def game():
    for c in coins:
        if c.is_touching(sprite):
            coin_sound.play()
            coins.remove(c)
            c.hide()
            score.words=str(int(score.words) + 1)
    for pip1 in pip_list:
        
        if sprite.is_touching(pip1) or sprite.y <= play.screen.bottom + 5:
            sea_sound.play()
            await play.timer(seconds=0.5)
            for pip in pip_list:
                pip.hide()
            for coin in coins:
                coin.hide()
            coins.clear()
            pip_list.clear()
            sprite.y = 0
            sprite.x = 0
            sprite.physics.x_speed = 0
            score.words = '0'
            
        
            

    await play.timer(seconds=1/120)



@play.when_key_pressed('q')
async def attack(key_press):
    if True:
        start_pos_y = sprite.y
        start_pos_x = sprite.x
        attacking = play.new_circle(color = 'red', border_color='grey', border_width=3, radius=6, y = start_pos_y, x = start_pos_x)
        attacking.start_physics(obeys_gravity=False, can_move=True, mass = 100, friction=0.0, x_speed= 30)
        await play.timer(seconds = 2)
        attacking.remove()


@play.repeat_forever
async def jump():
    if play.key_is_pressed('w', 'W', "'"):
        sprite.physics.y_speed = 38
        await play.timer(seconds=0.5)

@play.repeat_forever
async def move_objects():
    global pip_list
    last_hieght = 200
    draw_pip(last_hieght, pip_list)
    timer_ = 0
    while True:
        timer_ += 1
        for pip in pip_list:
            pip.x = pip.x - 4
        for coin in coins:
            coin.x = coin.x - 4
        await play.timer(seconds = 0.01)
        if timer_ >= 60:
            timer_ = 0
            up_or_down_num = randint(1, 10)
            if (up_or_down_num > 5 and last_hieght > 60) or last_hieght > 290 :
                last_hieght = last_hieght - randint(1, 50)
            else:
                last_hieght += randint(1, 50)
            draw_pip(last_hieght, pip_list)


@play.repeat_forever
def vol_cont():
    for i in range(4):
        if vol[i].is_clicked:
            pygame.mixer.Sound.set_volume(soundtrack, 0.05 + 0.25 * i)
            for j in range(4):
                if j > i:
                    vol[j].color = 'grey'
                else:
                    vol[j].color = 'red'



play.start_program()
