import pygame
import numpy
import keyboard

(width, height) = (500, 500)
centro = [width / 2, height / 2]
screen = pygame.display.set_mode((width, height))

running = True

def mult_matrices_y_vector(mat, v, largo):
    NuevoVector = []

    for i in range(largo):
        NuevoVector.append(0)
        for ii in range(largo):
            NuevoVector[i] += mat[i][ii] * v[ii]

    return NuevoVector


def sum_matrices(mat,mat2,largo):
    NuevaMatriz = []

    for i in range(largo):
        Vector = [0, 0, 0]
        for ii in range(largo):
            Vector[ii] += mat2[i][ii] * mat[i][ii]
        NuevaMatriz.append(Vector)

    return NuevaMatriz


def mult_matrices(mat, mat2, largo):
    NuevaMatriz = []

    for i in range(largo):
        Vector = [0, 0, 0]
        for ii in range(largo):
            for iii in range(largo):
                Vector[ii] += mat2[iii][ii] * mat[i][iii]
        NuevaMatriz.append(Vector)

    return NuevaMatriz


def suma_vec(v1,v2,largo):
    Vector = [0,0,0]
    for i in range(largo):
        Vector[i] = v1[i] + v2[i]
    return Vector

def dibujar_linea(punto1, punto2, color):
    vector = [punto2[0] - punto1[0], punto2[1]-punto1[1], punto2[2]-punto1[2]]

    for i in range(10):

        puntoM = [punto1[0] + i * vector[0]/10,punto1[1] + i*vector[1]/10, punto1[2]+i*vector[2]/10]
        puntoM = mult_matrices_y_vector(MatrizCamara, suma_vec(puntoM, VecMov, 3), 3)
        puntoM = [puntoM[0], puntoM[1] / (puntoM[0] / 200) + centro[0], puntoM[2] / (puntoM[0] / 200) + centro[1]]

        if width > puntoM[1] > 0 and height > puntoM[2] > 0 and puntoM[0] > 0:
            pygame.draw.circle(screen, color, (puntoM[1].__int__(), puntoM[2].__int__()),1)

    #pygame.draw.line(screen, color, (punto1[1]/(punto1[0]/200) + centro[0], punto1[2]/(punto1[0]/200) + centro[1]),
    #                 (punto2[1]/(punto2[0]/200) + centro[0], punto2[2]/(punto2[0]/200) + centro[1]), 2)


def rotate_matrix(eje, derecha, matriz):
    matrizRotacion = []

    A = .01
    if derecha:
        A = -.01

    if eje == 0:
        matrizRotacion = [[numpy.cos(A), -numpy.sin(A), 0],
                          [numpy.sin(A), numpy.cos(A), 0],
                          [0, 0, 1]]
    if eje == 1:
        matrizRotacion = [[1, 0, 0],
                          [0, numpy.cos(A), -numpy.sin(A)],
                          [0, numpy.sin(A), numpy.cos(A)]]
    if eje == 2:
        matrizRotacion = [[numpy.cos(A), 0, numpy.sin(A)],
                          [0, 1, 0],
                          [-numpy.sin(A), 0, numpy.cos(A)]]
    return mult_matrices(matriz, matrizRotacion, 3)


def rotate_matrix_Prueba(AnguloX, AnguloZ):
    MatrizCamara = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    MatrizGiro = [[numpy.cos(AnguloX), 0, numpy.sin(AnguloX)],
                  [0, 1, 0],
                  [-numpy.sin(AnguloX), 0, numpy.cos(AnguloX)]]

    MatrizCamara = mult_matrices(MatrizCamara, MatrizGiro, 3)

    MatrizGiro = [[numpy.cos(AnguloZ), -numpy.sin(AnguloZ), 0],
                  [numpy.sin(AnguloZ), numpy.cos(AnguloZ), 0],
                  [0, 0, 1]]
    MatrizCamara = mult_matrices(MatrizCamara, MatrizGiro, 3)

    return MatrizCamara


MatrizCamara = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

Ax = 0
Ay = 0

VecMov = [0, 0, 0]

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if keyboard.is_pressed('esc'):
        running = False

    screen.fill((0, 0, 0))

    mov = pygame.mouse.get_rel()
    Ay -= mov[0] / 50
    Ax += mov[1] / 50

    if Ax > numpy.pi / 2:
        Ax = numpy.pi / 2
    if Ax < -numpy.pi / 2:
        Ax = -numpy.pi / 2
    MatrizCamara = rotate_matrix_Prueba(Ax, Ay)

    MatrizGiroX = rotate_matrix_Prueba(0,-Ay)


    if keyboard.is_pressed('w'):
        VecMov = suma_vec(VecMov,mult_matrices_y_vector(MatrizGiroX,[-1,0,0],3),3)
    if keyboard.is_pressed('s'):
        VecMov = suma_vec(VecMov,mult_matrices_y_vector(MatrizGiroX,[1,0,0],3),3)
    if keyboard.is_pressed('a'):
        VecMov = suma_vec(VecMov,mult_matrices_y_vector(MatrizGiroX,[0,1,0],3),3)
    if keyboard.is_pressed('d'):
        VecMov = suma_vec(VecMov, mult_matrices_y_vector(MatrizGiroX, [0, -1, 0], 3), 3)
    if keyboard.is_pressed(' '):
        VecMov = suma_vec(VecMov,[0,0, 1],3)
    if keyboard.is_pressed('shift'):
        VecMov = suma_vec(VecMov,[0,0, -1],3)

    # DIRECCIONES [x,y,z] o sea [adentro afuera, izq der, arriba abajo]
    punto1 = [200, -50, -50]
    punto2 = [200, -50, 50]
    punto3 = [200, 50, 50]
    punto4 = [200, 50, -50]

    punto5 = [300, -50, -50]
    punto6 = [300, -50, 50]
    punto7 = [300, 50, 50]
    punto8 = [300, 50, -50]

    """punto1 = mult_matrices_y_vector(MatrizCamara, suma_vec([200, -50, -50],VecMov,3), 3)
    punto2 = mult_matrices_y_vector(MatrizCamara, suma_vec([200, -50, 50],VecMov,3), 3)
    punto3 = mult_matrices_y_vector(MatrizCamara, suma_vec([200, 50, 50],VecMov,3), 3)
    punto4 = mult_matrices_y_vector(MatrizCamara, suma_vec([200, 50, -50],VecMov,3), 3)

    punto5 = mult_matrices_y_vector(MatrizCamara, suma_vec([300, -50, -50],VecMov,3), 3)
    punto6 = mult_matrices_y_vector(MatrizCamara, suma_vec([300, -50, 50],VecMov,3), 3)
    punto7 = mult_matrices_y_vector(MatrizCamara, suma_vec([300, 50, 50],VecMov,3), 3)
    punto8 = mult_matrices_y_vector(MatrizCamara, suma_vec([300, 50, -50],VecMov,3), 3)"""

    dibujar_linea(punto1, punto2, (255, 0, 0))
    dibujar_linea(punto2, punto3, (255, 0, 0))
    dibujar_linea(punto3, punto4, (255, 0, 0))
    dibujar_linea(punto4, punto1, (255, 0, 0))

    dibujar_linea(punto5, punto6, (0, 255, 0))
    dibujar_linea(punto6, punto7, (0, 255, 0))
    dibujar_linea(punto7, punto8, (0, 255, 0))
    dibujar_linea(punto8, punto5, (0, 255, 0))

    dibujar_linea(punto1, punto5, (0, 0, 255))
    dibujar_linea(punto2, punto6, (0, 0, 255))
    dibujar_linea(punto3, punto7, (0, 0, 255))
    dibujar_linea(punto4, punto8, (0, 0, 255))

    pygame.display.update()
