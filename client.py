import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

nickname = input('Введите ваш ник: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(msg)
        except:
            print('Ошибка соединения!')
            client.close()
            break

def write():
    while True:
        msg = f'{nickname}: {input()}'
        client.send(msg.encode('utf-8'))

if __name__ == '__main__':
    threading.Thread(target=receive).start()
    threading.Thread(target=write).start()
