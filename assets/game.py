# Lập trình game flappy bird
import pygame, sys
def draw_floor():
    screen.blit(floor,(floor_x_pos,600)) # Hiển thị Sàn trên màn hình
    screen.blit(floor,(floor_x_pos+432,600)) # Hiển thị Sàn thứ 2 kế tiếp sàn thứ nhất
pygame.init()
screen = pygame.display.set_mode((432, 768)) # Mở cửa sổ màn hình
clock = pygame.time.Clock() # Xét FPS
gravity = 0.25 # Thêm trọng lực.
bird_movement = 0
# Chèn background
bg = pygame.image.load('background-night.png').convert()
bg = pygame.transform.scale2x(bg) # background chiếm hết khung hình của pygame
# chèn sàn
floor = pygame.image.load('floor.png')
floor = pygame.transform.scale2x(floor) # Sàn chiếm hết khung hình của pygame
floor_x_pos = 0
# chèn con chim
bird = pygame.image.load('yellowbird-midflap.png')
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384)) # Con chim ở vị trí giữa, vị trí y = 1 nửa màn hình.
while True: # Vòng lặp thực hiện trong cửa sổ.
    for event in pygame.event.get(): # Vòng lặp sự kiện, lấy tất cả sự kiện diễn ea
        if event.type == pygame.QUIT: # Ấn phím thoát ra ngoài
            pygame.quit()
            sys.exit()
        if event == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Ấn phím space
                bird_movement = 0
                bird_movement = -11
    screen.blit(bg,(0,0)) # Hiển thị  background trên màn hình. 0, 0 ở vị trí góc trên bên trái. y tăng đi xuống.
    bird_movement += gravity # Con chim càng di chuyển trọng lực càng tăng
    bird_rect.centery += bird_movement # Di chuyển xuống dưới.
    screen.blit(bird,bird_rect)
    floor_x_pos -= 1
    draw_floor()
    # ĐỔi chổ vị trí 2 sàn
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120) #FPS = 120