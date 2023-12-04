import pygame
import numpy as np
from numpy.linalg import det
import math

# Colors' initialization
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (230, 231, 232)
RED = (255, 0, 0)

# There are parameters of our window (initialization)
WIDTH = 600
HEIGHT = 600
# Set title
pygame.display.set_caption("Fifth lab (group: 0323, team: 4)")
# Set window's parameters
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Scale of object's vertices
scale = 100

# Set position of the object
position = [WIDTH / 2, HEIGHT / 2]

xAngle = 0
yAngle = 0
zAngle = 0

# Initialize cube vertices
points = []
points.append(np.matrix([0, 0, 0, 1]))
points.append(np.matrix([1, 0, 0, 1]))
points.append(np.matrix([1, 1, 0, 1]))
points.append(np.matrix([0, 1, 0, 1]))
points.append(np.matrix([0, 1, 1, 1]))
points.append(np.matrix([0, 0, 1, 1]))
points.append(np.matrix([1, 0, 1, 1]))
points.append(np.matrix([1, 1, 1, 1]))

edges = []
edges.append([0, 1, 2, 3, 4])
edges.append([0, 3, 4, 5, 6])
edges.append([0, 1, 6, 5, 7])
edges.append([1, 2, 7, 6, 0])
edges.append([7, 4, 5, 6, 0])
edges.append([7, 4, 3, 2, 0])


projectionMatrix = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0]
])

projectedPoints = [
    [n, n] for n in range(len(points))
]

def connectPoints(i, j, points):
    pygame.draw.line(window, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

def displayCube():
    i = 0
    # Display object's vertices & their rotation
    rotated2DList = list()
    for point in points:
        rotated2D = np.dot(yRotation, np.transpose(point))
        rotated2D = np.dot(xRotation, rotated2D)
        rotated2D = np.dot(zRotation, rotated2D)

        rotated2DList.append(rotated2D)

        projected2D = np.dot(projectionMatrix, rotated2D)

        x = int(projected2D[0][0] * scale) + position[0]
        y = int(projected2D[1][0] * scale) + position[1]

        projectedPoints[i] = [x, y]
        #pygame.draw.circle(window, RED, (x, y), 2)
        i += 1

    # Link cube's vertices
    for edge in edges:
        if (ifEdgeVisible(rotated2DList[edge[0]], rotated2DList[edge[1] % 8], rotated2DList[edge[2] % 8], rotated2DList[edge[4] % 8])):
            connectPoints(edge[0], edge[1], projectedPoints)
            connectPoints(edge[1], edge[2], projectedPoints)
            connectPoints(edge[2], edge[3], projectedPoints)
            connectPoints(edge[3], edge[0], projectedPoints)

def ifEdgeVisible(first, second, third, test):
    o = (first + second + third + test) / 4
    functionO = surfaceFunction(first, second, third, o)
    functionH = surfaceFunction(first, second, third, [[0], [0], [10], [1]])
    return (functionO * functionH < 0)

def surfaceFunction(first, second, third, point):
    testFunction = list()
    testFunction.append([point[0]- first[0], point[1] - first[1], point[2] - first[2]])
    testFunction.append([second[0] - first[0], second[1] - first[1], second[2] - first[2]])
    testFunction.append([third[0] - first[0], third[1] - first[1], third[2] - first[2]])
    return det(np.matrix(np.array(testFunction)))

clock = pygame.time.Clock()
while True:

    clock.tick(60)

    xRotation = np.matrix([
        [1, 0, 0, 0],
        [0, math.cos(xAngle), -math.sin(xAngle), 0],
        [0, math.sin(xAngle), math.cos(xAngle), 0],
        [0, 0, 0, 1],
    ])

    yRotation = np.matrix([
        [math.cos(yAngle), 0, math.sin(yAngle), 0],
        [0, 1, 0, 0],
        [-math.sin(yAngle), 0, math.cos(yAngle), 0],
        [0, 0, 0, 1],
    ])

    zRotation = np.matrix([
        [math.cos(zAngle), -math.sin(zAngle), 0, 0],
        [math.sin(zAngle), math.cos(zAngle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                yAngle -= 0.1
            if event.key == pygame.K_UP:
                yAngle += 0.1
            if event.key == pygame.K_RIGHT:
                xAngle -= 0.1
            if event.key == pygame.K_LEFT:
                xAngle += 0.1
            if event.key == pygame.K_1:
                zAngle += 0.1
            if event.key == pygame.K_2:
                zAngle -= 0.1

    # Make window's color white
    window.fill(WHITE)
    displayCube()

    pygame.display.update()