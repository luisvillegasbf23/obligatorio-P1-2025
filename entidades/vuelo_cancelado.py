
class VueloCancelado:
    def __init__(self, codigo, origen, destino, causa, fecha, pasajeros_afectados):
        self.__codigo = codigo
        self.__origen = origen
        self.__destino = destino
        self.__causa = causa
        self.__fecha = fecha
        self.__pasajeros_afectados = pasajeros_afectados

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
    def causa(self):
        return self.__causa

    @property
    def fecha(self):
        return self.__fecha

    @property
    def pasajeros_afectados(self):
        return self.__pasajeros_afectados

