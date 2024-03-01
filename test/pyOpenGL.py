import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# 初始化Pygame
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# 设置视口和投影
glViewport(0, 0, width, height)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# 启用混合
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# 设置混合颜色
glColor4f(0.5, 0.5, 0.5, 0.5)
# 设置场景和对象
def draw_cube():
    glBegin(GL_QUADS)
    glColor3fv((1, 0, 0))
    glVertex3fv((-1, -1, -1))
    glVertex3fv((-1, 1, -1))
    glVertex3fv((1, 1, -1))
    glVertex3fv((1, -1, -1))

    glColor3fv((0, 1, 0))
    glVertex3fv((-1, -1, 1))
    glVertex3fv((-1, 1, 1))
    glVertex3fv((1, 1, 1))
    glVertex3fv((1, -1, 1))

    glColor3fv((0, 0, 1))
    glVertex3fv((-1, -1, -1))
    glVertex3fv((-1, 1, -1))
    glVertex3fv((-1, 1, 1))
    glVertex3fv((-1, -1, 1))

    glColor3fv((1, 1, 0))
    glVertex3fv((1, -1, -1))
    glVertex3fv((1, 1, -1))
    glVertex3fv((1, 1, 1))
    glVertex3fv((1, -1, 1))

    glColor3fv((0, 1, 1))
    glVertex3fv((-1, -1, -1))
    glVertex3fv((-1, -1, 1))
    glVertex3fv((1, -1, 1))
    glVertex3fv((1, -1, -1))

    glColor3fv((1, 0, 1))
    glVertex3fv((-1, 1, -1))
    glVertex3fv((-1, 1, 1))
    glVertex3fv((1, 1, 1))
    glVertex3fv((1, 1, -1))
    glEnd()

# 渲染场景
# 初始化旋转角度和旋转速度
rotation_angle = 0
rotation_speed = 0.01

# 渲染场景
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # 设置相机位置和朝向
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    # 根据旋转角度旋转对象
    glRotatef(rotation_angle, 0, 1, 0)
    draw_cube()
    pygame.display.flip()

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 按下左箭头键，减小旋转速度
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            rotation_speed -= 0.1
        # 按下右箭头键，增加旋转速度
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            rotation_speed += 0.1

    # 根据旋转速度更新旋转角度
    rotation_angle += rotation_speed
    render()

# 保存渲染的图像
glReadBuffer(GL_FRONT)
data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
image = pygame.image.fromstring(data, (width, height), 'RGB')
# pygame.image.save(image, 'rendered_image.png')

pygame.quit()
