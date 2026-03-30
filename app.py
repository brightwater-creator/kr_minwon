import pygame
import pymunk
import random

# 기본 설정
WIDTH, HEIGHT = 500, 800
FPS = 60

def create_ball(space, pos, color, number):
    mass = 1
    radius = 12
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.6  # 탄성
    shape.friction = 0.5
    shape.color = color
    shape.number = number
    space.add(body, shape)
    return shape

def setup_space():
    space = pymunk.Space()
    space.gravity = (0, 900)  # 아래로 떨어지는 중력

    # 장애물(핀) 생성
    for y in range(200, 600, 70):
        shift = 30 if (y // 70) % 2 == 0 else 0
        for x in range(50, WIDTH, 60):
            static_body = space.static_body
            shape = pymunk.Circle(static_body, 5, offset=(x + shift, y))
            shape.elasticity = 0.8
            space.add(shape)

    # 깔때기 라인 생성
    left_funnel = pymunk.Segment(space.static_body, (0, 650), (220, 750), 5)
    right_funnel = pymunk.Segment(space.static_body, (WIDTH, 650), (280, 750), 5)
    bottom_gate = pymunk.Segment(space.static_body, (220, 780), (280, 780), 2) # 골인 지점 근처
    
    for line in [left_funnel, right_funnel, bottom_gate]:
        line.elasticity = 0.5
        space.add(line)
        
    return space

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    space = setup_space()
    
    balls = []
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), 
              (0,255,255), (255,165,0), (128,0,128), (0,128,128), (128,128,0)]
    
    running = True
    started = False
    winner = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not started:
                    for i in range(10):
                        # 시작 위치에 약간의 변칙을 주어 겹치지 않게 투하
                        pos = (WIDTH//2 + random.uniform(-20, 20), 50 - (i * 30))
                        balls.append(create_ball(space, pos, colors[i], i+1))
                    started = True

        screen.fill((240, 240, 240))
        
        # 핀(장애물) 그리기
        for shape in space.shapes:
            if isinstance(shape, pymunk.Circle) and shape.body == space.static_body:
                pygame.draw.circle(screen, (100, 100, 100), shape.offset, 5)
            elif isinstance(shape, pymunk.Segment):
                pygame.draw.line(screen, (50, 50, 50), shape.a, shape.b, 5)

        # 공 그리기 및 승자 체크
        for ball in balls:
            pos = ball.body.position
            pygame.draw.circle(screen, ball.color, (int(pos.x), int(pos.y)), 12)
            
            # 깔때기 끝 통과 여부 확인 (y축 기준 750 이상)
            if winner is None and pos.y > 750:
                winner = ball.number

        if winner:
            font = pygame.font.SysFont("malgungothic", 40)
            txt = font.render(f"Winner: Player {winner}!", True, (0, 0, 0))
            screen.blit(txt, (WIDTH//2 - 100, 100))

        space.step(1/FPS)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
