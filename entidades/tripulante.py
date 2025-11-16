from enum import Enum
from entidades.persona import Persona
from excepciones.error import RolInvalidoError

class Rol(Enum):
    PILOTO = "piloto"
    COPILOTO = "copiloto"
    AZAFATA = "azafata"
    
    @classmethod
    def validar_rol(cls, rol_str):
        rol_lower = rol_str.lower()
        for rol in cls:
            if rol.value == rol_lower:
                return rol
        raise RolInvalidoError(f"Rol inválido: {rol_str}. Debe ser uno de: piloto, copiloto, azafata")


class Tripulante(Persona):
    def __init__(self, documento, nombre, apellido, email, telefono, fecha_ingreso, rol, horas_de_vuelo=0):
        super().__init__(documento, nombre, apellido, email, telefono, fecha_ingreso)
        self.__rol = rol
        self.__horas_de_vuelo = horas_de_vuelo
    
    @property
    def rol(self):
        return self.__rol
    
    @property
    def horas_de_vuelo(self):
        return self.__horas_de_vuelo
    
    @horas_de_vuelo.setter
    def horas_de_vuelo(self, horas):
        self.__horas_de_vuelo += horas