import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from dto.sensor_data import SensorData
from receiver.kafka_receiver import KafkaReceiver

verticies = (
    (0.5, -1, -0.1),
    (0.5, 1, -0.1),
    (-0.5, 1, -0.1),
    (-0.5, -1, -0.1),
    (0.5, -1, 0.1),
    (0.5, 1, 0.1),
    (-0.5, -1, 0.1),
    (-0.5, 1, 0.1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def rotate(x: float, y: float):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glRotatef(x, 1, 0, 0)
    glRotatef(y, 0, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Cube()
    pygame.display.flip()
    pygame.time.wait(10)


def main():
    consumer = KafkaReceiver.create_consumer('my-test-11', bootstrap_server='192.168.2.108:9092')
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    old_x_rot = 0.
    old_y_rot = 0.

    for message in consumer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        data = message.value
        data = SensorData.from_json(data)
        data.print_log()
        new_x_rot = data.get_x_rotation()
        new_y_rot = data.get_y_rotation()

        glRotatef(new_x_rot-old_x_rot, 1, 0, 0)
        glRotatef(new_y_rot-old_y_rot, 0, 1, 0)

        old_x_rot = new_x_rot
        old_y_rot = new_y_rot

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(50)
    return

if __name__ == "__main__":
    main()
