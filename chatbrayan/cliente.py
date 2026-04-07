import socket
import threading

# Pedimos el nombre al usuario
nombre = input("¿Cuál es tu nombre?: ")

# Conectamos al servidor local
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 5555))

def recibir_mensajes():
    """Esta función corre en un hilo para escuchar lo que llega."""
    while True:
        try:
            msg = cliente.recv(1024).decode('utf-8')
            if msg == "NICK":
                cliente.send(nombre.encode('utf-8'))
            else:
                print(msg)
        except:
            print("[!] Conexión cerrada.")
            cliente.close()
            break

def enviar_mensajes():
    """Esta función permite escribir mensajes en cualquier momento."""
    while True:
        msg = input("")
        cliente.send(msg.encode('utf-8'))

# Lanzamos los dos hilos (escuchar y hablar al mismo tiempo)
threading.Thread(target=recibir_mensajes).start()
threading.Thread(target=enviar_mensajes).start()