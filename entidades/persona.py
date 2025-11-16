from abc import ABC

class Persona(ABC):
    def __init__(self, documento, nombre, apellido, email, telefono, fecha_ingreso):
        self.__documento = documento
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__telefono = telefono
        self.__fecha_ingreso = fecha_ingreso
      
    @property
    def documento(self):
        return self.__documento
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def apellido(self):
        return self.__apellido
    
    @property
    def email(self):
        return self.__email
      
    @property
    def telefono(self):
        return self.__telefono
    
    @property
    def fecha_ingreso(self):
        return self.__fecha_ingreso
 