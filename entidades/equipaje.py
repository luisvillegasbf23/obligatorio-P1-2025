from excepciones.error import PesoExcedidoError

class Equipaje:
    PESO_MINIMO = 23
    PESO_MEDIO = 32
    PESO_MAXIMO = 45
 
    def __init__(self, codigo, pasajero, vuelo, peso):
        self.__codigo = codigo
        self.__pasajero = pasajero
        self.__vuelo = vuelo
        self.__peso = peso
        self.__precio = self.__calcular_precio()

    def __calcular_precio(self):
        if self.__peso > self.PESO_MAXIMO:
            raise PesoExcedidoError(f"No se admite equipaje de más de {self.PESO_MAXIMO} kg. Peso actual: {self.__peso} kg")

        es_internacional = self.__vuelo.tipo_vuelo == "internacional"

        match self.__peso:
            case peso if peso <= self.PESO_MINIMO:
                return 0
            case peso if peso <= self.PESO_MEDIO:
                return 100 if es_internacional else 30
            case peso if peso <= self.PESO_MAXIMO:
                return 200 if es_internacional else 60

    @property
    def codigo(self):
        return self.__codigo

    @property
    def pasajero(self):
        return self.__pasajero

    @property
    def vuelo(self):
        return self.__vuelo

    @property
    def peso(self):
        return self.__peso

    @property
    def precio(self):
        return self.__precio