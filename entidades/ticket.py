class Ticket:
    def __init__(self, numero, pasajero):
        self.__numero = numero
        self.__pasajero = pasajero
    
    @property
    def numero(self):
        return self.__numero
    
    @property
    def pasajero(self):
        return self.__pasajero

