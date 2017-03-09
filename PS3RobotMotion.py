#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

os.sys.path.append('dynamixel_functions_py')                # Path setting

import dynamixel_functions as dynamixel                     # Uses Dynamixel SDK library

# -------------------Conexion del control y funciones de pygame----------------- #
import pygame
from pygame.locals import *

pygame.init()

pygame.joystick.init()

#----------------------------------------------------------------------------#

ADDR_MX_GOAL_POSITION       = 30                            # Direccion de posicion objetivo
PROTOCOL_VERSION            = 1                             # Version del Protocolo de los motores

# Ajustes por defecto
DXL_ID                      = 1                             # ID del motor Dynamixel: 1 (para maquina de estados)
BAUDRATE                    = 1000000                       # Tasa de transmision
DEVICENAME                  = "/dev/ttyUSB0".encode('utf-8')# Revisar el puerto de transmision que se esta usando
                                                            # Linux: "/dev/ttyUSB0", RPi: "/dev/ttyAMA0"

# Inicializar las estructuras de PortHandler
# Establecer la ruta del puerto
# Obtener métodos y miembros de PortHandlerLinux

port_num = dynamixel.portHandler(DEVICENAME)

# Inicializar las estructuras de PacketHandler
dynamixel.packetHandler()

# Abrir Puerto
if dynamixel.openPort(port_num):
    print("Succeeded to open the port!")
else:
    print("Failed to open the port!")
    print("Press any key to terminate...")
    getch()
    quit()

vector_pos=[]

while 1:

    joystick = pygame.joystick.Joystick(0)              # Crea un nuevo objeto Joystick
    joystick.init()                                     # Inicializa el objeto Joystick
    evento = pygame.event.wait()                        # Espera un solo evento de la cola
    
    if joystick.get_button(0):                          # Obtiene el estado actual del boton()
        print ("Ha terminado la teleoperación del Robot")
        break
        #raise SystemExit
    
    if joystick.get_axis(0):                            # Obtiene el valor de la posicion actual del eje()
        vector_pos.append(joystick.get_axis(0))
        pos=int((int(vector_pos[-1]*127))*(2.68503937)) # Transformacion del valor del eje a valor
        pos=512-pos                                     # comprensible por el motor AX-12A
    else:
        pos=512
    dynamixel.write2ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_MX_GOAL_POSITION, pos)

## Copia guarda en un vector los valores recibidos por el
## control ordenados de menor a mayor sin repetirlos
copia = []

for i in vector_pos:
    if i not in copia:
        copia.append(i)

copia.sort()        # Sort organiza el vector de menor a mayor

"""---------------------------------------------------------
## Funcion para transformar a decimal los valores
## leidos por el control: Factor de transf = int(x*127)
## x corresponde al valor que envia el control

for i in copia:
    p=int(i*127)
    print(p)

## Transformacion de valores decimales a valores de angulo
## comprensibles por el motor AX-12A:
## factor = 682/254 -> 682 es el rango de movimiento
## de los limites del motor (de 171(50°)->853(250°))
## 254 -> rango de los ejes del control (-127 -> 126)

for i in copia:
    q=int(i*127)
    p=int(q*(2.68503937))
    r=512-p
    print(r)
-------------------------------------------------------------"""

# Cerrar puerto
dynamixel.closePort(port_num)
