class Aerolinea:
    def __init__(self, codigo, nombre, pais_origen):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__pais_origen = pais_origen
    
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def pais_origen(self):
        return self.__pais_origen

