import socket
import threading

class ServidorChat:
    def __init__(self):
        # Configuración de conexión (IP local y Puerto 5555)
        self.host = '127.0.0.1'
        self.port = 5555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        
        # Diccionarios para guardar quién está en cada sala
        self.clientes = {}      # {socket: nombre}
        self.salas = {}         # {nombre_sala: [lista_de_sockets]}
        self.donde_esta = {}    # {socket: nombre_sala}
        
        print(f"[*] Servidor encendido en el puerto {self.port}...")

    def difundir(self, mensaje, sala):
        """Envía el mensaje solo a las personas de la misma sala."""
        if sala in self.salas:
            for cliente in self.salas[sala]:
                try:
                    cliente.send(mensaje.encode('utf-8'))
                except:
                    self.cerrar_conexion(cliente)

    def manejar_cliente(self, cliente):
        """Hilo dedicado para cada usuario conectado."""
        while True:
            try:
                mensaje = cliente.recv(1024).decode('utf-8')
                
                # Comando para unirse a una sala
                if mensaje.startswith('/join '):
                    nueva_sala = mensaje.split(' ')[1]
                    self.unir_a_sala(cliente, nueva_sala)
                
                # Si no es comando, es un mensaje para la sala actual
                elif cliente in self.donde_esta:
                    sala_actual = self.donde_esta[cliente]
                    nombre = self.clientes[cliente]
                    self.difundir(f"[{nombre}]: {mensaje}", sala_actual)
                else:
                    cliente.send("[!] Primero únete a una sala con: /join nombre".encode('utf-8'))
            except:
                break
        self.cerrar_conexion(cliente)

    def unir_a_sala(self, cliente, nombre_sala):
        # Sacarlo de la sala vieja si ya estaba en una
        if cliente in self.donde_esta:
            self.salas[self.donde_esta[cliente]].remove(cliente)
        
        # Meterlo a la nueva sala
        if nombre_sala not in self.salas:
            self.salas[nombre_sala] = []
        
        self.salas[nombre_sala].append(cliente)
        self.donde_esta[cliente] = nombre_sala
        cliente.send(f"[*] Te has unido a la sala: {nombre_sala}".encode('utf-8'))

    def cerrar_conexion(self, cliente):
        if cliente in self.clientes:
            del self.clientes[cliente]
        cliente.close()

    def iniciar(self):
        while True:
            cliente, _ = self.server.accept()
            cliente.send("NICK".encode('utf-8'))
            nombre = cliente.recv(1024).decode('utf-8')
            self.clientes[cliente] = nombre
            
            # Crear un hilo para este nuevo cliente
            threading.Thread(target=self.manejar_cliente, args=(cliente,)).start()

if __name__ == "__main__":
    ServidorChat().iniciar()