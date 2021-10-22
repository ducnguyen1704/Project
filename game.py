# Lập trình game flappy bird
import pygame, sys, random

from pygame.mixer import Channel
# Hàm cho trò chơi
def draw_floor():
    screen.blit(floor,(floor_x_pos,650)) # Hiển thị Sàn trên màn hình
    screen.blit(floor,(floor_x_pos+432,650)) # Hiển thị Sàn thứ 2 kế tiếp sàn thứ nhất

# Hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height) # Chọn chiều cao ngẫu nhiên tạo ống
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos)) # Tọa độ bằng nửa màn hình, nằm xa phía bên phải. # Tọa độ ống dưới
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos-650))
    return bottom_pipe, top_pipe

# Hàm di chuyển ống
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5 # Lấy những ống đươc tạo ra di chuyển về bên trái
    return pipes

# Hàm  vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >=500: # Điều kiện quay ngược ống
            screen.blit(pipe_surface, pipe) 
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) # False là trục x, True là trục Y --> Lật ngược hình
            screen.blit(flip_pipe,pipe)

#Hàm xử lý va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False # Nếu va chạm sẽ kết thúc trò chơi
    if bird_rect.top <= 0 or bird_rect.bottom >= 720:
        return False # Trò chơi kết thúc
    return True

# Hàm xoay
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, - bird_movement * 3, 1)
    return new_bird

# Hàm đập cánh
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

# Hàm hiển thị điểm:
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255)) # Xuất ra màn hình font chữ, màu chữ.
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255)) # Xuất ra màn hình font chữ, màu chữ.
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,630))
        screen.blit(high_score_surface, high_score_rect)

# Cập nhập high score
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency=44100, size = 16, channels = 2, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((432, 768)) # Mở cửa sổ màn hình
clock = pygame.time.Clock() # Xét FPS
game_font = pygame.font.Font('04B_19.ttf', 40)

# Tạo biến cho trò chơi
gravity = 0.15 # Thêm trọng lực.
bird_movement = 0
game_active = True # Game hoạt động --> False thì trò chơi kết thúc.
# Tạo điểm
score = 0
high_score = 0
# Chèn background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg) # background chiếm hết khung hình của pygame

# chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor) # Sàn chiếm hết khung hình của pygame
floor_x_pos = 0

# chèn con chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up] # 0,1,2 -->index
bird_index = 0
bird = bird_list[bird_index] # Cánh hướng xuống
# bird = pygame.image.load('assets/yellowbird-midflap.png')
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384)) # Con chim ở vị trí giữa, vị trí y = 1 nửa màn hình.

# Tạo timer cho bird
birdflap = pygame.USEREVENT + 1 # event cho con chim
pygame.time.set_timer(birdflap,200)

# Tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# Tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200) # Sau 1200s sẽ tạo chướng ngại vật mới
pipe_height = [100,200,300]

# Tạo màn hình kết thúc:
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216,384))

# Chèn âm thanh:
flap_sound = pygame.mixer.Sound('Sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('Sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('Sound/sfx_point.wav')
score_sound_countdow = 100
while True: # Vòng lặp thực hiện trong cửa sổ.
    for event in pygame.event.get(): # Vòng lặp sự kiện, lấy tất cả sự kiện diễn ea
        if event.type == pygame.QUIT: # Ấn phím thoát ra ngoài
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active: # Ấn phím space và khi game hoạt động
                bird_movement = 0
                bird_movement = -8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False: # Khi game kết thúc
                game_active = True # Nhấn phím space sẽ chơi lại từ đầu.
                pipe_list.clear() # Xóa những ống đã chơi
                bird_rect.center = (100,384) # reset lại con chim
                bird_movement = 0 # reset lại chuyển động
                score = 0 # reset điểm
        if event.type == spawnpipe: 
            pipe_list.extend(create_pipe()) # Thêm ống vào list.

        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg,(0,0)) # Hiển thị  background trên màn hình. 0, 0 ở vị trí góc trên bên trái. y tăng đi xuống.
    if game_active:
        # chim
        bird_movement += gravity # Con chim càng di chuyển trọng lực càng tăng
        rotated_bird = rotate_bird(bird) # Hàm Xoay bird
        bird_rect.centery += bird_movement # Di chuyển xuống dưới.
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list) # Xử lý va chạm 

        # Ống
        pipe_list = move_pipe(pipe_list) # Lấy ống di chuyển sau đó trả lại list mới
        draw_pipe(pipe_list) # Vẽ ống lên màn hình
        score += 0.01
        score_display('main game') # điểm số
        score_sound_countdow -= 1
        if score_sound_countdow <= 0:
            score_sound.play()  
            score_sound_countdow = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)  
        score_display('game_over') # điểm số +  điểm cao nhất

    #Sàn
    floor_x_pos -= 1
    draw_floor()
    # ĐỔi chổ vị trí 2 sàn
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120) #FPS = 120