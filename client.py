import socket
import select
import errno
import time

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username (equipe_role ex: 1_p1): ")
start = 0

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)



################################################################# code à modifier ######################################################################

########################### attendre le start ##########################

#while start == 0:
#    message_header = client_socket.recv(HEADER_LENGTH)
#    if len(message_header):
#        message_length = int(message_header.decode('utf-8').strip())
#        start = client_socket.recv(message_length).decode('utf-8')


########################################################################

#nombre d'envoi de données par seconde afin de calculer la vitesse
EPS = int(input("Entrez le nombre d'envoi de coordonnées par seconde : "))

#Coordonnés arbitraires pour l'instant
coords = [[260,160],[270,153],[395,146],[330,139],[365,133],[395,126],[420,120],[450,111],[478,100],[505,95],[530,98],[555,107],[580,115],[600,120],[566,124],[532,128],[498,132],[464,136],[430,140],[396,144],[362,148],[284,155]]

i = 0
last1 = 0
last2 = 0 #les deux derniers coordonnées stockées
nbEnvoi = 0 #nb de renvois depuis le dernier top

while True:

    for i in range (len(coords)):
        print(coords[i][0], coords[i][1], sep=",")
        if coords[i][1] > last1 and last1 < last2:
            print('TOP  ', 'Vitesse =', EPS/nbEnvoi, ' coup de rame/seconde')
            message = 'TOP'
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            #send message
            client_socket.send(message_header + message)
            nbEnvoi = 0
        last2 = last1
        last1 = coords[i][1]
        nbEnvoi = nbEnvoi + 1
        time.sleep(0.04)