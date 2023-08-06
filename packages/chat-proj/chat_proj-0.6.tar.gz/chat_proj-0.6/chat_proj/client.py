import socket, threading
nickname = input("Choose your nickname: ")

encoding = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      
client.connect(('127.0.0.1', 7976))                             

def receive():
    while True:                                                 
        try:
            message = client.recv(1024).decode(encoding)
            if message == 'NICKNAME':
                client.send(nickname.encode(encoding))
            else:
                print(message)
        except:                                                 
            print("Something went wrong! Please, contact with developer - @emonakov (telegram)")
            client.close()
            break
def write():
    while True:                                                 
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode(encoding))

receive_thread = threading.Thread(target=receive)               
receive_thread.start()
write_thread = threading.Thread(target=write)                  
write_thread.start()
