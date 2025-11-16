PAISES = ["Argentina", "Bolivia", "Brasil", "Chile", "Colombia", "Ecuador", "Paraguay", "Perú", "Uruguay", "Venezuela"]

class Vuelo:
    def __init__(self, codigo, origen, destino, duracion, fecha, aerolinea, cantidad_asientos, tipo_vuelo):
        self.__codigo = codigo
        self.__origen = origen
        self.__destino = destino
        self.__duracion = duracion
        self.__fecha = fecha
        self.__aerolinea = aerolinea
        self.__cantidad_asientos = cantidad_asientos
        self.__tipo_vuelo = tipo_vuelo
        self.__estado = "activo"
        self.__tickets = []
        self.__equipajes = []
        self.__tripulantes = []
        
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def origen(self):
        return self.__origen
    
    @property
    def destino(self):
        return self.__destino
    
    @property
    def duracion(self):
        return self.__duracion
    
    @property
    def fecha(self):
        return self.__fecha
    
    @property
    def aerolinea(self):
        return self.__aerolinea
    
    @property
    def cantidad_asientos(self):
        return self.__cantidad_asientos
    
    @property
    def tipo_vuelo(self):
        return self.__tipo_vuelo
    
    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, nuevo_estado):
        self.__estado = nuevo_estado
    
    @property
    def tickets(self):
        return self.__tickets
    
    @property
    def equipajes(self):
        return self.__equipajes
    
    @property
    def tripulantes(self):
        return self.__tripulantes