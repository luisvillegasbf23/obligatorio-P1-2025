from datetime import datetime, timedelta
from entidades.cliente import Cliente
from entidades.tripulante import Tripulante, Rol
from entidades.aerolinea import Aerolinea
from entidades.vuelo import Vuelo
from entidades.ticket import Ticket
from entidades.equipaje import Equipaje

CLIENTES = [
    Cliente("12345678", "Juan", "Pérez", "juan@email.com", "099123456", datetime.now(), "Argentina"),
    Cliente("87654321", "María", "González", "maria@email.com", "099654321", datetime.now(), "Uruguay"),
    Cliente("11223344", "Carlos", "Rodríguez", "carlos@email.com", "099112233", datetime.now(), "Brasil"),
]

TRIPULANTES = [
    Tripulante("11111111", "Pedro", "Martínez", "pedro@email.com", "099111111", datetime.now(), Rol.PILOTO, 5000),
    Tripulante("22222222", "Ana", "López", "ana@email.com", "099222222", datetime.now(), Rol.COPILOTO, 3000),
    Tripulante("33333333", "Laura", "Fernández", "laura@email.com", "099333333", datetime.now(), Rol.AZAFATA, 2000),
    Tripulante("44444444", "Roberto", "Sánchez", "roberto@email.com", "099444444", datetime.now(), Rol.PILOTO, 6000),
    Tripulante("55555555", "Sofía", "García", "sofia@email.com", "099555555", datetime.now(), Rol.AZAFATA, 1500),
    Tripulante("66666666", "Miguel", "Torres", "miguel@email.com", "099666666", datetime.now(), Rol.COPILOTO, 4000),
]

AEROLINEAS = [
    Aerolinea("AER001", "Aerolíneas Argentinas", "Argentina"),
    Aerolinea("GOL001", "GOL", "Brasil"),
    Aerolinea("LAT001", "LATAM", "Chile"),
]

VUELOS_PRECARGADOS = [
    Vuelo(
        "AER001-001",
        "Argentina",
        "Uruguay",
        2.5,
        datetime.now() + timedelta(days=7),
        AEROLINEAS[0],
        150,
        "internacional",
    ),
    Vuelo(
        "GOL001-001",
        "Brasil",
        "Argentina",
        3.0,
        datetime.now() + timedelta(days=10),
        AEROLINEAS[1],
        180,
        "internacional",
    ),
    Vuelo("LAT001-001", "Chile", "Perú", 4.0, datetime.now() + timedelta(days=15), AEROLINEAS[2], 200, "internacional"),
]

VUELOS_PRECARGADOS[0].tickets.append(Ticket(1, CLIENTES[0]))
VUELOS_PRECARGADOS[0].tickets.append(Ticket(2, CLIENTES[1]))
CLIENTES[0].agregar_vuelo(VUELOS_PRECARGADOS[0])
CLIENTES[1].agregar_vuelo(VUELOS_PRECARGADOS[0])

VUELOS_PRECARGADOS[1].tickets.append(Ticket(1, CLIENTES[2]))
CLIENTES[2].agregar_vuelo(VUELOS_PRECARGADOS[1])

VUELOS_PRECARGADOS[2].tickets.append(Ticket(1, CLIENTES[0]))
CLIENTES[0].agregar_vuelo(VUELOS_PRECARGADOS[2])

VUELOS_PRECARGADOS[0].tripulantes.append(TRIPULANTES[0])  # PILOTO
VUELOS_PRECARGADOS[0].tripulantes.append(TRIPULANTES[1])  # COPILOTO
VUELOS_PRECARGADOS[0].tripulantes.append(TRIPULANTES[2])  # AZAFATA

VUELOS_PRECARGADOS[1].tripulantes.append(TRIPULANTES[3])  # PILOTO
VUELOS_PRECARGADOS[1].tripulantes.append(TRIPULANTES[5])  # COPILOTO
VUELOS_PRECARGADOS[1].tripulantes.append(TRIPULANTES[4])  # AZAFATA

VUELOS_PRECARGADOS[0].equipajes.append(Equipaje("AER001-001-1", CLIENTES[0], VUELOS_PRECARGADOS[0], 20.0))
VUELOS_PRECARGADOS[0].equipajes.append(Equipaje("AER001-001-2", CLIENTES[1], VUELOS_PRECARGADOS[0], 28.5))

VUELOS_PRECARGADOS[1].equipajes.append(Equipaje("GOL001-001-1", CLIENTES[2], VUELOS_PRECARGADOS[1], 35.0))
