import pygame
import numpy as np

pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Audio Rendering")

# 사운드 생성 함수
def generate_sound(freq, duration=1.0, volume=0.5):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    samples = (volume * 32767.0 * np.sin(2 * np.pi * freq * t)).astype(np.int16)
    return pygame.mixer.Sound(buffer=samples)

# 캐릭터 초기 위치와 이동 속도
character_x, character_y = WIDTH // 2, HEIGHT // 2
character_speed = 0.1

# 캐릭터 이미지
character_img = pygame.Surface((10, 10))
character_img.fill((255, 0, 0))  # 빨간색

# 초기 사운드 생성
sound_freq = 44  # 기본 주파수 설정
base_volume = 0.5  # 기본 볼륨 설정
sound_effect = generate_sound(sound_freq, volume=base_volume)  # 초기 볼륨 조절

# 게임 루프
running = True
max_distance = 500  # 최대 거리 설정
while running:
    win.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 캐릭터 이동 로직
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x += character_speed
    if keys[pygame.K_UP]:
        character_y -= character_speed
    if keys[pygame.K_DOWN]:
        character_y += character_speed

    # 캐릭터 경계 제한
    if character_x < 0:
        character_x = 0
    elif character_x > WIDTH - 50:
        character_x = WIDTH - 50
    if character_y < 0:
        character_y = 0
    elif character_y > HEIGHT - 50:
        character_y = HEIGHT - 50

    # 캐릭터와 음원 사이의 거리 계산
    character_position = pygame.math.Vector2(character_x + 25, character_y + 25)
    sound_position = pygame.math.Vector2(WIDTH // 2 - 10, HEIGHT // 2 - 10)  # 음원 위치
    listener_distance = sound_position.distance_to(character_position)

    # Doppler 효과 모의 - 소리의 주파수 변화
    doppler_freq = sound_freq * (1 + (character_speed / max_distance))

    # 대기 흡수 모의 - 거리에 따른 볼륨 감소
    if listener_distance > max_distance:
        distance_volume = 0.1  # 최대 거리를 넘어가면 소리가 감쇠됨
    else:
        distance_volume = max(0.1, 1 - listener_distance / max_distance)

    # 캐릭터 그리기
    win.blit(character_img, (character_x, character_y))

    # 음원 위치에 음원 모양 그리기
    sound_img = pygame.Surface((10, 10))
    sound_img.fill((0, 255, 0))  # 초록색
    win.blit(sound_img, sound_position)

    # Doppler 효과 및 대기 흡수 모의를 반영한 소리 재생
    sound_effect = generate_sound(doppler_freq, volume=base_volume * distance_volume)
    sound_effect.play()

    pygame.display.update()

pygame.quit()
