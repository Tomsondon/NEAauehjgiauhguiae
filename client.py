import socket
import keyboard
import time

host = input("Enter host IP: ")
port = 2706
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))
movementKeys = ["w", "s", "a", "d"]
delay = 1/240

def checkInput():
    for key in movementKeys:
        if keyboard.is_pressed(key):
            inputDirection = movementKeys.index(key) + 1
            return inputDirection
    return 0


while True:
    if checkInput() != 0:
        messageToSend = str(f'{checkInput()}')
        socket.send(messageToSend.encode('ascii'))
        time.sleep(delay)

