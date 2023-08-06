import socket, threading, logging
                    
encoding = 'utf-8'                            
logging.basicConfig(filename='log.log', encoding=encoding, filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', level=logging.DEBUG)
host = '127.0.0.1'                                                      
port = 7976                                                             

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              
server.bind((host, port))                                               
server.listen()

clients = []
nicknames = []

def broadcast(message):                                              
    for client in clients:
        try:
            client.send(message)
        except:
            continue

        

def handle(client):                                         
    while True:
        try:                                                           
            message = client.recv(1024)
            decodedmessage = message.decode(encoding)
            if (decodedmessage and decodedmessage.strip()): #checking if string is empty
                broadcast(message)
                logging.info(decodedmessage)

        except:                                                         
            index = clients.index(client)
            nickname = nicknames[index]
            client.close()
            clients.remove(client)
            nicknames.remove(nickname)
            broadcast('\nUser {} is left!'.format(nickname).encode(encoding))
            logging.info('User {} is left!'.format(nickname))
            break

def receive():                                                          
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))       
        client.send('NICKNAME'.encode(encoding))
        nickname = client.recv(1024).decode(encoding)
        nicknames.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode(encoding))
        logging.info("{} joined!".format(nickname))
        client.send('\nConnected to server!'.encode(encoding))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()