from entidades.persona import Persona

class Cliente(Persona):
    def __init__(self, documento, nombre, apellido, email, telefono, fecha_ingreso, nacionalidad):
        super().__init__(documento, nombre, apellido, email, telefono, fecha_ingreso)
        self.__nacionalidad = nacionalidad
        self.__historial_de_vuelos = []
    
    @property
    def nacionalidad(self):
        return self.__nacionalidad
    
    @property
    def historial_de_vuelos(self):
        return self.__historial_de_vuelos
    
    def agregar_vuelo(self, vuelo):
        self.__historial_de_vuelos.append(vuelo)