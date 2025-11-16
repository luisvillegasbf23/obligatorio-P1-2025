import os
from datetime import datetime
from entidades.cliente import Cliente
from entidades.tripulante import Tripulante, Rol
from entidades.aerolinea import Aerolinea
from entidades.vuelo import Vuelo, PAISES
from entidades.ticket import Ticket
from entidades.equipaje import Equipaje
from entidades.vuelo_cancelado import VueloCancelado
from excepciones.error import OpcionInvalidaError, DatoDuplicadoError, DatoVacioError, AerolineaNoRegistradaError, PesoExcedidoError
from seed import CLIENTES, TRIPULANTES, AEROLINEAS, VUELOS_PRECARGADOS


class Sistema:
    def __init__(self):
        self.__clientes = []
        self.__vuelos = []
        self.__equipajes = []
        self.__tripulantes = []
        self.__aerolineas = []
        self.__tickets_cancelados = []
        self.__vuelos_cancelados_info = []
        self._precargar_datos()

    def _precargar_datos(self):
        self.__clientes.extend(CLIENTES)
        self.__tripulantes.extend(TRIPULANTES)
        self.__aerolineas.extend(AEROLINEAS)
        self.__vuelos.extend(VUELOS_PRECARGADOS)

    # MENÚES
    def menu_principal(self):
        self._encabezado("MENÚ PRINCIPAL")
        print("1. Registrar persona")
        print("2. Registrar compañía aérea")
        print("3. Crear vuelo")
        print("4. Crear ticket")
        print("5. Asignar personal a vuelo")
        print("6. Registrar equipaje en bodega")
        print("7. Visualizar vuelos")
        print("8. Cancelar ticket")
        print("9. Cancelar vuelo")
        print("10. Informes")
        print("0. Salir")
        self._separador()

    def _menu_registrar_persona(self):
        self._encabezado("REGISTRAR PERSONA")
        print("1. Pasajero")
        print("2. Tripulante")
        self._separador()

    def _menu_seleccionar_rol(self):
        self._encabezado("SELECCIONAR ROL")
        print("1. Piloto")
        print("2. Copiloto")
        print("3. Azafata")
        self._separador()

    def _menu_seleccionar_pais(self, texto="SELECCIONAR PAÍS"):
        self._encabezado(texto)
        for i, pais in enumerate(PAISES, 1):
            print(f"{i}. {pais}")
        self._separador()

    def _menu_seleccionar_tipo_vuelo(self):
        self._encabezado("TIPO DE VUELO")
        print("1. Nacional")
        print("2. Internacional")
        self._separador()

    def _encabezado_datos_personales(self):
        self._encabezado("DATOS PERSONALES")

    def _encabezado_registrar_aerolinea(self, pais_origen):
        self._encabezado("REGISTRAR AEROLÍNEA")
        print(f"País de origen: {pais_origen}")

    def _encabezado_crear_vuelo(self):
        self._encabezado("CREAR VUELO")

    def _mostrar_aerolineas_disponibles(self):
        self.limpiar_consola()
        self._encabezado_crear_vuelo()
        print("Aerolíneas disponibles:")
        for i, aerolinea in enumerate(self.__aerolineas, 1):
            print(f"{i}. {aerolinea.nombre} ({aerolinea.codigo}) - {aerolinea.pais_origen}")
        self._separador()

    # UTILS
    def limpiar_consola(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def seleccionar_opcion(self):
        return input(": ").strip()

    def _separador(self):
        print("=" * 50)

    def _encabezado(self, titulo):
        self._separador()
        print(titulo)
        self._separador()

    # Colores ANSI para terminal
    def _verde(self, texto):
        """Retorna el texto en color verde"""
        return f"\033[92m{texto}\033[0m"
    
    def _imprimir_exito(self, mensaje):
        """Imprime un mensaje de éxito en verde"""
        print(self._verde(mensaje))

    def _solicitar_dato(self, nombre_campo):
        while True:
            dato = input(f"{nombre_campo}: ").strip()
            try:
                if not dato:
                    raise DatoVacioError(f"El campo {nombre_campo} no puede estar vacío")
                return dato
            except DatoVacioError as e:
                print(f"{e}")

    # VALIDACIONES
    def _validar_documento_duplicado(self, documento):
        todas_las_personas = [*self.__clientes, *self.__tripulantes]
        for persona in todas_las_personas:
            if persona.documento == documento:
                raise DatoDuplicadoError(f"Ya existe una persona con el documento {documento}. Por favor, ingrese un documento diferente.")

    def _validar_codigo_aerolinea_duplicado(self, codigo):
        for aerolinea in self.__aerolineas:
            if aerolinea.codigo == codigo:
                raise DatoDuplicadoError(f"Ya existe una aerolínea con el código {codigo}. Por favor, ingrese un código diferente.")

    def _validar_codigo_vuelo_duplicado(self, codigo):
        for vuelo in self.__vuelos:
            if vuelo.codigo == codigo:
                raise DatoDuplicadoError(f"Ya existe un vuelo con el código {codigo}. Por favor, ingrese un código diferente.")

    def _buscar_aerolinea_por_codigo(self, codigo):
        for aerolinea in self.__aerolineas:
            if aerolinea.codigo == codigo:
                return aerolinea
        return None

    # REGISTRAR PERSONA
    def registrar_persona(self):
        self.limpiar_consola()
        self._menu_registrar_persona()

        while True:
            try:
                match self.seleccionar_opcion():
                    case "1":
                        self._registrar_pasajero()
                        break
                    case '2':
                        self._registrar_tripulante()
                        break
                    case _:
                        self.limpiar_consola()
                        self._menu_registrar_persona()
                        raise OpcionInvalidaError("Opción inválida. Debe ser 1 o 2")
            except OpcionInvalidaError as e:
                print(f"{e}")

    def _registrar_persona(self):
        self.limpiar_consola()
        self._encabezado_datos_personales()
        while True:
            documento = self._solicitar_dato("Documento")
            try:
                self._validar_documento_duplicado(documento)
                break
            except DatoDuplicadoError as e:
                self.limpiar_consola()
                self._encabezado_datos_personales()
                print(f"{e}")

        nombre = self._solicitar_dato("Nombre")
        apellido = self._solicitar_dato("Apellido")
        email = self._solicitar_dato("Email")
        telefono = self._solicitar_dato("Teléfono")
        fecha_ingreso = datetime.now()
        return documento, nombre, apellido, email, telefono, fecha_ingreso

    def _registrar_pasajero(self):
        documento, nombre, apellido, email, telefono, fecha_ingreso = self._registrar_persona()
        nacionalidad = self._solicitar_dato("Nacionalidad")
        cliente = Cliente(documento, nombre, apellido, email, telefono, fecha_ingreso, nacionalidad)
        self.__clientes.append(cliente)
        self.limpiar_consola()
        self.menu_principal()
        self._imprimir_exito(f"Pasajero {nombre} {apellido} registrado con éxito!")
        self._separador()

    def _registrar_tripulante(self):
        documento, nombre, apellido, email, telefono, fecha_ingreso = self._registrar_persona()
        self._menu_seleccionar_rol()

        while True:
            opcion_rol = self.seleccionar_opcion()
            try:
                match opcion_rol:
                    case "1":
                        rol = Rol.PILOTO
                        break
                    case '2':
                        rol = Rol.COPILOTO
                        break
                    case '3':
                        rol = Rol.AZAFATA
                        break
                    case _:
                        self.limpiar_consola()
                        self._menu_seleccionar_rol()
                        raise OpcionInvalidaError("Opción inválida. Debe ser 1, 2 o 3")
            except OpcionInvalidaError as e:
                print(f"{e}")

        self.limpiar_consola()
        self._encabezado_datos_personales()
        print(f"Rol: {rol.value.capitalize()}")
        self._separador()
        
        while True:
            try:
                horas_str = self._solicitar_dato("Horas de vuelo acumuladas")
                horas_de_vuelo = float(horas_str)
                if horas_de_vuelo < 0:
                    self.limpiar_consola()
                    self._encabezado_datos_personales()
                    print(f"Rol: {rol.value.capitalize()}")
                    self._separador()
                    raise OpcionInvalidaError("Las horas de vuelo deben ser un número mayor o igual a 0")
                break
            except ValueError:
                self.limpiar_consola()
                self._encabezado_datos_personales()
                print(f"Rol: {rol.value.capitalize()}")
                self._separador()
                print("Debe ingresar un número válido")
            except OpcionInvalidaError as e:
                print(f"{e}")

        tripulante = Tripulante(documento, nombre, apellido, email, telefono, fecha_ingreso, rol, horas_de_vuelo)
        self.__tripulantes.append(tripulante)
        self.limpiar_consola()
        self.menu_principal()
        self._imprimir_exito(f"Tripulante {nombre} {apellido} registrado con éxito!")
        self._separador()

    # REGISTRAR AEROLÍNEA
    def registrar_compania_aerea(self):
        self.limpiar_consola()
        self._menu_seleccionar_pais()

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(PAISES)):
                    self.limpiar_consola()
                    self._menu_seleccionar_pais()
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(PAISES)}")
                opcion_pais = int(opcion)
                pais_origen = PAISES[opcion_pais - 1]
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        self.limpiar_consola()
        self._encabezado_registrar_aerolinea(pais_origen)

        nombre = self._solicitar_dato("Nombre")
        codigo = self._generar_codigo_aerolinea(nombre)

        aerolinea = Aerolinea(codigo, nombre, pais_origen)
        self.__aerolineas.append(aerolinea)
        self.limpiar_consola()
        self.menu_principal()
        self._imprimir_exito(f"Aerolínea {nombre} ({codigo}) registrada con éxito!")
        self._separador()

    def _generar_codigo_aerolinea(self, nombre):
        nombre_limpio = ''.join(c for c in nombre.upper() if c.isalpha())[:3]
        if len(nombre_limpio) < 3:
            nombre_limpio = nombre_limpio.ljust(3, 'X')

        numero = len(self.__aerolineas) + 1
        codigo = f"{nombre_limpio}{numero:03d}"

        return codigo

    def _generar_codigo_vuelo(self, codigo_aerolinea):
        vuelos_de_aerolinea = [v for v in self.__vuelos if v.aerolinea.codigo == codigo_aerolinea]
        codigo = f"{codigo_aerolinea}-{(len(vuelos_de_aerolinea) + 1):03d}"
        return codigo

    def _mostrar_contexto_vuelo(self, aerolinea, codigo, origen=None, destino=None, duracion=None, fecha=None):
        self.limpiar_consola()
        self._encabezado_crear_vuelo()
        print(f"Aerolínea: {aerolinea.nombre} ({aerolinea.codigo})")
        print(f"Código de vuelo: {codigo}")
        if origen:
            print(f"Origen: {origen}")
        if destino:
            print(f"Destino: {destino}")
        if duracion:
            print(f"Duración: {duracion} horas")
        if fecha:
            print(f"Fecha: {fecha.strftime('%Y-%m-%d')}")

    def _solicitar_duracion(self, aerolinea, codigo, origen, destino):
        self._mostrar_contexto_vuelo(aerolinea, codigo, origen, destino)
        while True:
            try:
                return float(self._solicitar_dato("Duración de vuelo (en horas)"))
            except ValueError:
                self._mostrar_contexto_vuelo(aerolinea, codigo, origen, destino)
                print("Debe ingresar un número válido")

    def _solicitar_fecha(self, aerolinea, codigo, origen, destino, duracion):
        self._mostrar_contexto_vuelo(aerolinea, codigo, origen, destino, duracion)
        while True:
            try:
                fecha_str = self._solicitar_dato("Fecha (YYYY-MM-DD)")
                return datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                self._mostrar_contexto_vuelo(aerolinea, codigo, origen, destino, duracion)
                print("Formato de fecha inválido. Use YYYY-MM-DD")

    def _solicitar_cantidad_asientos(self, aerolinea, codigo, origen, destino, duracion, fecha):
        self._mostrar_contexto_vuelo(aerolinea, codigo, origen, destino, duracion, fecha)
        while True:
            try:
                return int(self._solicitar_dato("Cantidad de asientos"))
            except ValueError:
                self._mostrar_contexto_vuelo(aerolinea, codigo, origen, destino, duracion, fecha)
                print("Debe ingresar un número válido")

    def _seleccionar_pais(self, texto_menu):
        self._menu_seleccionar_pais(texto_menu)
        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(PAISES)):
                    self.limpiar_consola()
                    self._menu_seleccionar_pais(texto_menu)
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(PAISES)}")
                return PAISES[int(opcion) - 1]
            except OpcionInvalidaError as e:
                print(f"{e}")

    def _seleccionar_origen(self, aerolinea, codigo):
        self._mostrar_contexto_vuelo(aerolinea, codigo)
        self._menu_seleccionar_pais("SELECCIONAR ORIGEN")
        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(PAISES)):
                    self._mostrar_contexto_vuelo(aerolinea, codigo)
                    self._menu_seleccionar_pais("SELECCIONAR ORIGEN")
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(PAISES)}")
                return PAISES[int(opcion) - 1]
            except OpcionInvalidaError as e:
                print(f"{e}")

    def _seleccionar_destino(self, aerolinea, codigo, origen):
        self._mostrar_contexto_vuelo(aerolinea, codigo, origen)
        self._menu_seleccionar_pais("SELECCIONAR DESTINO")
        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(PAISES)):
                    self._mostrar_contexto_vuelo(aerolinea, codigo, origen)
                    self._menu_seleccionar_pais("SELECCIONAR DESTINO")
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(PAISES)}")
                return PAISES[int(opcion) - 1]
            except OpcionInvalidaError as e:
                print(f"{e}")

    # REGISTRAR VUELO
    def registrar_vuelo(self):
        if not self.__aerolineas:
            self.limpiar_consola()
            self.menu_principal()
            raise AerolineaNoRegistradaError("No hay aerolíneas registradas. Debe registrar al menos una aerolínea primero.")

        self._mostrar_aerolineas_disponibles()
        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(self.__aerolineas)):
                    self._mostrar_aerolineas_disponibles()
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(self.__aerolineas)}")
                aerolinea = self.__aerolineas[int(opcion) - 1]
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        codigo = self._generar_codigo_vuelo(aerolinea.codigo)

        origen = self._seleccionar_origen(aerolinea, codigo)
        destino = self._seleccionar_destino(aerolinea, codigo, origen)
        duracion = self._solicitar_duracion(aerolinea, codigo, origen, destino)
        fecha = self._solicitar_fecha(aerolinea, codigo, origen, destino, duracion)
        cantidad_asientos = self._solicitar_cantidad_asientos(aerolinea, codigo, origen, destino, duracion, fecha)

        # Determinar automáticamente el tipo de vuelo basado en origen y destino
        tipo_vuelo = "nacional" if origen == destino else "internacional"

        vuelo = Vuelo(codigo, origen, destino, duracion, fecha, aerolinea, cantidad_asientos, tipo_vuelo)
        self.__vuelos.append(vuelo)
        self.limpiar_consola()
        self.menu_principal()
        self._imprimir_exito(f"Vuelo {codigo} creado con éxito!")
        self._separador()

    # CREAR TICKET
    def _encabezado_crear_ticket(self):
        self._encabezado("CREAR TICKET")

    def _mostrar_vuelos_disponibles(self):
        self.limpiar_consola()
        self._encabezado_crear_ticket()
        vuelos_activos = [v for v in self.__vuelos if v.estado == "activo"]
        if not vuelos_activos:
            return None

        print("Vuelos disponibles:")
        for i, vuelo in enumerate(vuelos_activos, 1):
            asientos_disponibles = vuelo.cantidad_asientos - len(vuelo.tickets)
            print(f"{i}. {vuelo.codigo} - {vuelo.origen} → {vuelo.destino} ({vuelo.fecha.strftime('%Y-%m-%d')}) - Asientos disponibles: {asientos_disponibles}/{vuelo.cantidad_asientos}")
        self._separador()
        return vuelos_activos

    def _mostrar_vuelos_para_personal(self):
        self.limpiar_consola()
        self._encabezado_asignar_personal()
        vuelos_activos = [v for v in self.__vuelos if v.estado == "activo"]
        if not vuelos_activos:
            return None

        vuelos_sin_tripulacion_completa = []
        for vuelo in vuelos_activos:
            tiene_piloto = any(t.rol == Rol.PILOTO for t in vuelo.tripulantes)
            tiene_copiloto = any(t.rol == Rol.COPILOTO for t in vuelo.tripulantes)
            tiene_azafata = any(t.rol == Rol.AZAFATA for t in vuelo.tripulantes)
            if not (tiene_piloto and tiene_copiloto and tiene_azafata):
                vuelos_sin_tripulacion_completa.append(vuelo)

        if not vuelos_sin_tripulacion_completa:
            return None

        print("Vuelos disponibles:")
        for i, vuelo in enumerate(vuelos_sin_tripulacion_completa, 1):
            asientos_disponibles = vuelo.cantidad_asientos - len(vuelo.tickets)
            print(f"{i}. {vuelo.codigo} - {vuelo.origen} → {vuelo.destino} ({vuelo.fecha.strftime('%Y-%m-%d')})")
        self._separador()
        return vuelos_sin_tripulacion_completa

    def _mostrar_pasajeros_disponibles(self, vuelo):
        if not self.__clientes:
            print("No hay pasajeros registrados.")
            return None

        pasajeros_en_vuelo = {ticket.pasajero.documento for ticket in vuelo.tickets}
        pasajeros_disponibles = [c for c in self.__clientes if c.documento not in pasajeros_en_vuelo]

        if not pasajeros_disponibles:
            print("No hay pasajeros disponibles. Todos los pasajeros registrados ya tienen ticket en este vuelo.")
            return None

        print("Pasajeros disponibles:")
        for i, cliente in enumerate(pasajeros_disponibles, 1):
            print(f"{i}. {cliente.nombre} {cliente.apellido} ({cliente.documento}) - {cliente.nacionalidad}")
        self._separador()
        return pasajeros_disponibles

    def _validar_disponibilidad_vuelo(self, vuelo):
        if len(vuelo.tickets) >= vuelo.cantidad_asientos:
            raise OpcionInvalidaError(f"El vuelo {vuelo.codigo} está completo. No hay asientos disponibles.")

    def _generar_numero_ticket(self, vuelo):
        numeros_ocupados = {ticket.numero for ticket in vuelo.tickets}
        for numero in range(1, vuelo.cantidad_asientos + 1):
            if numero not in numeros_ocupados:
                return numero
        raise OpcionInvalidaError("No hay números de ticket disponibles.")

    def crear_ticket(self):
        if not self.__vuelos or not any(v.estado == "activo" for v in self.__vuelos):
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay vuelos activos disponibles. Debe crear al menos un vuelo primero.")

        if not self.__clientes:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay pasajeros registrados. Debe registrar al menos un pasajero primero.")

        vuelos_activos = self._mostrar_vuelos_disponibles()

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(vuelos_activos)):
                    self._mostrar_vuelos_disponibles()
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(vuelos_activos)}")
                vuelo = vuelos_activos[int(opcion) - 1]
                self._validar_disponibilidad_vuelo(vuelo)
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        self.limpiar_consola()
        self._encabezado_crear_ticket()
        print(f"Vuelo seleccionado: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
        self._separador()

        pasajeros = self._mostrar_pasajeros_disponibles(vuelo)
        if not pasajeros:
            self.limpiar_consola()
            self.menu_principal()
            return

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(pasajeros)):
                    self.limpiar_consola()
                    self._encabezado_crear_ticket()
                    print(f"Vuelo seleccionado: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
                    self._separador()
                    self._mostrar_pasajeros_disponibles(vuelo)
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(pasajeros)}")
                pasajero = pasajeros[int(opcion) - 1]
                break
            except OpcionInvalidaError as e:
                self.limpiar_consola()
                self._encabezado_crear_ticket()
                print(f"Vuelo seleccionado: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
                self._separador()
                self._mostrar_pasajeros_disponibles(vuelo)
                print(f"{e}")

        numero_ticket = self._generar_numero_ticket(vuelo)
        ticket = Ticket(numero_ticket, pasajero)
        vuelo.tickets.append(ticket)
        pasajero.agregar_vuelo(vuelo)

        self.limpiar_consola()
        self.menu_principal()
        self._imprimir_exito(f"Ticket #{numero_ticket} creado con éxito para {pasajero.nombre} {pasajero.apellido} en el vuelo {vuelo.codigo}!")
        self._separador()

    # ASIGNAR PERSONAL A VUELO
    def _encabezado_asignar_personal(self):
        self._encabezado("ASIGNAR PERSONAL A VUELO")

    def _mostrar_contexto_asignar_personal(self, vuelo):
        self.limpiar_consola()
        self._encabezado_asignar_personal()
        print(f"Vuelo seleccionado: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
        if vuelo.tripulantes:
            print("Tripulación asignada:")
            for tripulante in vuelo.tripulantes:
                rol_capitalizado = tripulante.rol.value.capitalize()
                print(f"- {rol_capitalizado}: {tripulante.nombre} {tripulante.apellido}")

    def _mostrar_tripulantes_disponibles(self, vuelo, rol):
        tripulantes_en_vuelo = {t.documento for t in vuelo.tripulantes}
        tripulantes_filtrados = [t for t in self.__tripulantes if t.documento not in tripulantes_en_vuelo and t.rol == rol]

        if not tripulantes_filtrados:
            return None

        print(f"Tripulantes disponibles ({rol.value}):")
        for i, tripulante in enumerate(tripulantes_filtrados, 1):
            print(f"{i}. {tripulante.nombre} {tripulante.apellido} ({tripulante.documento}) - {tripulante.horas_de_vuelo} horas de vuelo")
        self._separador()
        return tripulantes_filtrados

    def _validar_tripulacion_minima(self, vuelo):
        tiene_piloto = any(t.rol == Rol.PILOTO for t in vuelo.tripulantes)
        tiene_copiloto = any(t.rol == Rol.COPILOTO for t in vuelo.tripulantes)
        tiene_azafata = any(t.rol == Rol.AZAFATA for t in vuelo.tripulantes)

        if not tiene_piloto:
            raise OpcionInvalidaError("El vuelo debe tener al menos un piloto asignado.")
        if not tiene_copiloto:
            raise OpcionInvalidaError("El vuelo debe tener al menos un copiloto asignado.")
        if not tiene_azafata:
            raise OpcionInvalidaError("El vuelo debe tener al menos una azafata asignada.")

    def asignar_personal_vuelo(self):
        if not self.__vuelos or not any(v.estado == "activo" for v in self.__vuelos):
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay vuelos activos disponibles. Debe crear al menos un vuelo primero.")

        if not self.__tripulantes:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay tripulantes registrados. Debe registrar al menos un tripulante primero.")

        vuelos_activos = self._mostrar_vuelos_para_personal()
        if not vuelos_activos:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("Todos los vuelos activos ya tienen la tripulación mínima asignada.")

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(vuelos_activos)):
                    self._mostrar_vuelos_para_personal()
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(vuelos_activos)}")
                vuelo = vuelos_activos[int(opcion) - 1]
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        roles_requeridos = [Rol.PILOTO, Rol.COPILOTO, Rol.AZAFATA]
        for rol in roles_requeridos:
            tripulantes_rol = [t for t in vuelo.tripulantes if t.rol == rol]
            if not tripulantes_rol:
                self._mostrar_contexto_asignar_personal(vuelo)
                tripulantes_disponibles = self._mostrar_tripulantes_disponibles(vuelo, rol)
                if not tripulantes_disponibles:
                    self.limpiar_consola()
                    self.menu_principal()
                    print(f"No hay {rol.value}s disponibles para asignar.")
                    return

                while True:
                    try:
                        opcion = self.seleccionar_opcion()
                        if not opcion.isdigit() or not (1 <= int(opcion) <= len(tripulantes_disponibles)):
                            self._mostrar_contexto_asignar_personal(vuelo)
                            self._mostrar_tripulantes_disponibles(vuelo, rol)
                            raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(tripulantes_disponibles)}")
                        tripulante = tripulantes_disponibles[int(opcion) - 1]
                        vuelo.tripulantes.append(tripulante)
                        break
                    except OpcionInvalidaError as e:
                        print(f"{e}")

        self._validar_tripulacion_minima(vuelo)

        self.limpiar_consola()
        self.menu_principal()
        self._imprimir_exito(f"Personal asignado con éxito al vuelo {vuelo.codigo}!")
        self._separador()

    # REGISTRAR EQUIPAJE
    def _encabezado_registrar_equipaje(self):
        self._encabezado("REGISTRAR EQUIPAJE")

    def _mostrar_vuelos_con_tickets(self):
        self.limpiar_consola()
        self._encabezado_registrar_equipaje()
        vuelos_activos = [v for v in self.__vuelos if v.estado == "activo" and v.tickets]
        if not vuelos_activos:
            return None

        print("Vuelos disponibles:")
        for i, vuelo in enumerate(vuelos_activos, 1):
            print(f"{i}. {vuelo.codigo} - {vuelo.origen} → {vuelo.destino} ({vuelo.fecha.strftime('%Y-%m-%d')})")
        self._separador()
        return vuelos_activos

    def _mostrar_tickets_vuelo(self, vuelo):
        if not vuelo.tickets:
            return None

        print(f"Tickets del vuelo {vuelo.codigo}:")
        tickets_sin_equipaje = []
        for ticket in vuelo.tickets:
            tiene_equipaje = any(e.pasajero.documento == ticket.pasajero.documento for e in vuelo.equipajes)
            if not tiene_equipaje:
                tickets_sin_equipaje.append(ticket)
        
        if not tickets_sin_equipaje:
            print("Todos los tickets ya tienen equipaje registrado.")
            return None

        for i, ticket in enumerate(tickets_sin_equipaje, 1):
            print(f"{i}. Ticket #{ticket.numero} - {ticket.pasajero.nombre} {ticket.pasajero.apellido} ({ticket.pasajero.documento})")

        self._separador()
        return tickets_sin_equipaje

    def _mostrar_contexto_equipaje(self, vuelo, ticket):
        self.limpiar_consola()
        self._encabezado_registrar_equipaje()
        print(f"Vuelo seleccionado: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
        print(f"Ticket seleccionado: #{ticket.numero} - {ticket.pasajero.nombre} {ticket.pasajero.apellido} ({ticket.pasajero.documento})")
        self._separador()

    def _solicitar_peso(self, vuelo, ticket):
        self._mostrar_contexto_equipaje(vuelo, ticket)
        while True:
            try:
                peso_str = self._solicitar_dato("Peso del equipaje (kg)")
                peso = float(peso_str)
                if peso <= 0:
                    self._mostrar_contexto_equipaje(vuelo, ticket)
                    raise OpcionInvalidaError("El peso debe ser mayor a 0")
                if peso > 45:
                    self._mostrar_contexto_equipaje(vuelo, ticket)
                    raise OpcionInvalidaError(f"No se admite equipaje de más de 45 kg. Peso actual: {peso} kg")
                return peso
            except ValueError:
                self._mostrar_contexto_equipaje(vuelo, ticket)
                raise OpcionInvalidaError("Debe ingresar un número válido")
            except OpcionInvalidaError as e:
                print(f"{e}")

    def registrar_equipaje(self):
        if not self.__vuelos or not any(v.estado == "activo" and v.tickets for v in self.__vuelos):
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay vuelos activos con tickets. Debe crear al menos un vuelo con tickets primero.")

        vuelos_activos = self._mostrar_vuelos_con_tickets()
        if not vuelos_activos:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay vuelos activos con tickets disponibles.")

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(vuelos_activos)):
                    self._mostrar_vuelos_con_tickets()
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(vuelos_activos)}")
                vuelo = vuelos_activos[int(opcion) - 1]
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        self.limpiar_consola()
        self._encabezado_registrar_equipaje()
        print(f"Vuelo seleccionado: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
        self._separador()

        tickets_disponibles = self._mostrar_tickets_vuelo(vuelo)
        if not tickets_disponibles:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("Todos los pasajeros de este vuelo ya tienen equipaje registrado.")

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(tickets_disponibles)):
                    self.limpiar_consola()
                    self._encabezado_registrar_equipaje()
                    print(f"Vuelo seleccionado: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
                    self._separador()
                    self._mostrar_tickets_vuelo(vuelo)
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(tickets_disponibles)}")
                ticket = tickets_disponibles[int(opcion) - 1]
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        codigo_equipaje = f"{vuelo.codigo}-{ticket.numero}"

        peso = self._solicitar_peso(vuelo, ticket)

        equipaje = Equipaje(codigo_equipaje, ticket.pasajero, vuelo, peso)
        vuelo.equipajes.append(equipaje)
        self.limpiar_consola()
        self.menu_principal()
        costo_texto = f"USD {equipaje.precio}" if equipaje.precio > 0 else "sin cargo adicional"
        self._imprimir_exito(f"Equipaje registrado con éxito!")
        print(f"Código: {codigo_equipaje}")
        print(f"Peso: {peso} kg")
        print(f"Costo ({vuelo.tipo_vuelo}): {costo_texto}")
        self._separador()

    # VISUALIZAR VUELOS
    def _encabezado_visualizar_vuelos(self):
        self._encabezado("VISUALIZAR VUELOS")

    def visualizar_vuelos(self):
        if not self.__vuelos:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay vuelos registrados en el sistema.")

        self.limpiar_consola()
        self._encabezado_visualizar_vuelos()

        for vuelo in self.__vuelos:
            print(f"\nVuelo: {vuelo.codigo}")
            print(f"Aerolínea: {vuelo.aerolinea.nombre} ({vuelo.aerolinea.codigo})")
            print(f"Ruta: {vuelo.origen} → {vuelo.destino}")
            print(f"Fecha: {vuelo.fecha.strftime('%Y-%m-%d')}")
            print(f"Duración: {vuelo.duracion} horas")
            print(f"Tipo: {vuelo.tipo_vuelo}")
            print(f"Estado: {vuelo.estado.upper()}")
            print(f"Asientos: {len(vuelo.tickets)}/{vuelo.cantidad_asientos} ocupados")

            print("\nPersonal asignado:")
            if vuelo.tripulantes:
                pilotos = [t for t in vuelo.tripulantes if t.rol == Rol.PILOTO]
                copilotos = [t for t in vuelo.tripulantes if t.rol == Rol.COPILOTO]
                azafatas = [t for t in vuelo.tripulantes if t.rol == Rol.AZAFATA]

                if pilotos:
                    for piloto in pilotos:
                        print(f"  - Piloto: {piloto.nombre} {piloto.apellido} ({piloto.documento})")
                else:
                    print("  - Piloto: No asignado")

                if copilotos:
                    for copiloto in copilotos:
                        print(f"  - Copiloto: {copiloto.nombre} {copiloto.apellido} ({copiloto.documento})")
                else:
                    print("  - Copiloto: No asignado")

                if azafatas:
                    for azafata in azafatas:
                        print(f"  - Azafata: {azafata.nombre} {azafata.apellido} ({azafata.documento})")
                else:
                    print("  - Azafata: No asignada")
            else:
                print("  - No hay personal asignado")

            print("\nPasajeros registrados:")
            if vuelo.tickets:
                for ticket in vuelo.tickets:
                    print(f"  - Ticket #{ticket.numero}: {ticket.pasajero.nombre} {ticket.pasajero.apellido} ({ticket.pasajero.documento})")
            else:
                print("  - No hay pasajeros registrados")

            self._separador()

        input("\nPresione Enter para volver al menú principal...")
        self.limpiar_consola()
        self.menu_principal()

    # CANCELAR TICKET
    def _encabezado_cancelar_ticket(self):
        self._encabezado("CANCELAR TICKET")

    def _mostrar_vuelos_con_tickets_para_cancelar(self):
        self.limpiar_consola()
        self._encabezado_cancelar_ticket()
        vuelos_activos = [v for v in self.__vuelos if v.estado == "activo" and v.tickets]
        if not vuelos_activos:
            return None

        print("Vuelos disponibles:")
        for i, vuelo in enumerate(vuelos_activos, 1):
            print(f"{i}. {vuelo.codigo} - {vuelo.origen} → {vuelo.destino} ({vuelo.fecha.strftime('%Y-%m-%d')})")
        self._separador()
        return vuelos_activos

    def _mostrar_tickets_para_cancelar(self, vuelo):
        if not vuelo.tickets:
            return None

        print(f"Tickets del vuelo {vuelo.codigo}:")
        for i, ticket in enumerate(vuelo.tickets, 1):
            print(f"{i}. Ticket #{ticket.numero} - {ticket.pasajero.nombre} {ticket.pasajero.apellido} ({ticket.pasajero.documento})")
        self._separador()
        return vuelo.tickets

    def cancelar_ticket(self):
        if not self.__vuelos or not any(v.estado == "activo" and v.tickets for v in self.__vuelos):
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay vuelos activos con tickets. No se puede cancelar ningún ticket.")

        vuelos_activos = self._mostrar_vuelos_con_tickets_para_cancelar()
        if not vuelos_activos:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay vuelos activos con tickets disponibles para cancelar.")

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(vuelos_activos)):
                    self._mostrar_vuelos_con_tickets_para_cancelar()
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(vuelos_activos)}")
                vuelo = vuelos_activos[int(opcion) - 1]
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        self.limpiar_consola()
        self._encabezado_cancelar_ticket()
        print(f"Vuelo seleccionado: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
        self._separador()

        tickets = self._mostrar_tickets_para_cancelar(vuelo)
        if not tickets:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay tickets disponibles para cancelar en este vuelo.")

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(tickets)):
                    self.limpiar_consola()
                    self._encabezado_cancelar_ticket()
                    print(f"Vuelo seleccionado: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
                    self._separador()
                    self._mostrar_tickets_para_cancelar(vuelo)
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(tickets)}")
                ticket = tickets[int(opcion) - 1]
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        vuelo.tickets.remove(ticket)

        equipajes_a_remover = [e for e in vuelo.equipajes if e.pasajero.documento == ticket.pasajero.documento]
        for equipaje in equipajes_a_remover:
            vuelo.equipajes.remove(equipaje)

        self.__tickets_cancelados.append(ticket)

        self.limpiar_consola()
        self.menu_principal()
        self._imprimir_exito(f"Ticket #{ticket.numero} cancelado con éxito para {ticket.pasajero.nombre} {ticket.pasajero.apellido}")
        if equipajes_a_remover:
            print(f"Equipaje del pasajero también ha sido removido del vuelo.")
        self._separador()

    # CANCELAR VUELO
    def _encabezado_cancelar_vuelo(self):
        self._encabezado("CANCELAR VUELO")

    def _mostrar_vuelos_activos_para_cancelar(self):
        self.limpiar_consola()
        self._encabezado_cancelar_vuelo()
        vuelos_activos = [v for v in self.__vuelos if v.estado == "activo"]
        if not vuelos_activos:
            return None

        print("Vuelos activos disponibles para cancelar:")
        for i, vuelo in enumerate(vuelos_activos, 1):
            print(f"{i}. {vuelo.codigo} - {vuelo.origen} → {vuelo.destino} ({vuelo.fecha.strftime('%Y-%m-%d')})")
        self._separador()
        return vuelos_activos

    def _mostrar_vuelos_para_reasignar(self, vuelo_a_cancelar):
        self.limpiar_consola()
        self._encabezado_cancelar_vuelo()
        print(f"Vuelo a cancelar: {vuelo_a_cancelar.codigo} - {vuelo_a_cancelar.origen} → {vuelo_a_cancelar.destino}")
        self._separador()
        vuelos_activos = [v for v in self.__vuelos if v.estado == "activo" and v.codigo != vuelo_a_cancelar.codigo]
        if not vuelos_activos:
            return None

        print("Vuelos disponibles para reasignar pasajeros, personal y equipaje:")
        for i, vuelo in enumerate(vuelos_activos, 1):
            asientos_disponibles = vuelo.cantidad_asientos - len(vuelo.tickets)
            print(f"{i}. {vuelo.codigo} - {vuelo.origen} → {vuelo.destino} ({vuelo.fecha.strftime('%Y-%m-%d')}) - Asientos disponibles: {asientos_disponibles}/{vuelo.cantidad_asientos}")
        self._separador()
        return vuelos_activos

    def _solicitar_causa_cancelacion(self, vuelo_a_cancelar):
        self.limpiar_consola()
        self._encabezado_cancelar_vuelo()
        print(f"Vuelo a cancelar: {vuelo_a_cancelar.codigo} - {vuelo_a_cancelar.origen} → {vuelo_a_cancelar.destino}")
        self._separador()
        return self._solicitar_dato("Causa de cancelación")

    def cancelar_vuelo(self):
        if not self.__vuelos or not any(v.estado == "activo" for v in self.__vuelos):
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay vuelos activos disponibles. No se puede cancelar ningún vuelo.")

        vuelos_activos = self._mostrar_vuelos_activos_para_cancelar()
        if not vuelos_activos:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay vuelos activos disponibles para cancelar.")

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(vuelos_activos)):
                    self._mostrar_vuelos_activos_para_cancelar()
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(vuelos_activos)}")
                vuelo_a_cancelar = vuelos_activos[int(opcion) - 1]
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        vuelos_para_reasignar = self._mostrar_vuelos_para_reasignar(vuelo_a_cancelar)
        if not vuelos_para_reasignar:
            self.limpiar_consola()
            self.menu_principal()
            raise OpcionInvalidaError("No hay otros vuelos activos disponibles para reasignar pasajeros, personal y equipaje. Debe haber al menos otro vuelo activo.")

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(vuelos_para_reasignar)):
                    self._mostrar_vuelos_para_reasignar(vuelo_a_cancelar)
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(vuelos_para_reasignar)}")
                vuelo_destino = vuelos_para_reasignar[int(opcion) - 1]
                
                tickets_a_reasignar = len(vuelo_a_cancelar.tickets)
                asientos_disponibles = vuelo_destino.cantidad_asientos - len(vuelo_destino.tickets)
                if tickets_a_reasignar > asientos_disponibles:
                    self._mostrar_vuelos_para_reasignar(vuelo_a_cancelar)
                    raise OpcionInvalidaError(f"El vuelo destino no tiene suficientes asientos disponibles. Necesita {tickets_a_reasignar} asientos pero solo tiene {asientos_disponibles} disponibles.")
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        causa = self._solicitar_causa_cancelacion(vuelo_a_cancelar)
        fecha_cancelacion = datetime.now()

        cantidad_tickets = len(vuelo_a_cancelar.tickets)
        cantidad_tripulantes = len(vuelo_a_cancelar.tripulantes)
        cantidad_equipajes = len(vuelo_a_cancelar.equipajes)

        tickets_a_reasignar = list(vuelo_a_cancelar.tickets)
        for ticket in tickets_a_reasignar:
            vuelo_a_cancelar.tickets.remove(ticket)
            vuelo_destino.tickets.append(ticket)
            if vuelo_a_cancelar in ticket.pasajero.historial_de_vuelos:
                ticket.pasajero.historial_de_vuelos.remove(vuelo_a_cancelar)
            ticket.pasajero.agregar_vuelo(vuelo_destino)

        tripulantes_a_reasignar = list(vuelo_a_cancelar.tripulantes)
        for tripulante in tripulantes_a_reasignar:
            vuelo_a_cancelar.tripulantes.remove(tripulante)
            if tripulante not in vuelo_destino.tripulantes:
                vuelo_destino.tripulantes.append(tripulante)

        equipajes_a_reasignar = list(vuelo_a_cancelar.equipajes)
        for equipaje in equipajes_a_reasignar:
            vuelo_a_cancelar.equipajes.remove(equipaje)
            vuelo_destino.equipajes.append(equipaje)

        vuelo_a_cancelar.estado = "cancelado"

        vuelo_cancelado = VueloCancelado(
            vuelo_a_cancelar.codigo,
            vuelo_a_cancelar.origen,
            vuelo_a_cancelar.destino,
            causa,
            fecha_cancelacion,
            cantidad_tickets
        )
        self.__vuelos_cancelados_info.append(vuelo_cancelado)

        self.limpiar_consola()
        self.menu_principal()
        self._imprimir_exito(f"Vuelo {vuelo_a_cancelar.codigo} cancelado con éxito.")
        print(f"Causa: {causa}")
        print(f"Fecha de cancelación: {fecha_cancelacion.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Pasajeros reasignados: {cantidad_tickets}")
        print(f"Personal reasignado: {cantidad_tripulantes}")
        print(f"Equipajes reasignados: {cantidad_equipajes}")
        print(f"Todo ha sido reasignado al vuelo {vuelo_destino.codigo}.")
        self._separador()

    # INFORMES
    def _menu_informes(self):
        self._encabezado("MENÚ DE INFORMES")
        print("1. Informe de pasajeros por vuelo")
        print("2. Informe de personal asignado")
        print("3. Informe de vuelos por compañía")
        print("4. Informe de vuelos cancelados")
        print("0. Volver al menú principal")
        self._separador()

    def _mostrar_vuelos_para_informe(self, encabezado_func):
        self.limpiar_consola()
        encabezado_func()
        vuelos_activos = [v for v in self.__vuelos if v.estado == "activo"]
        if not vuelos_activos:
            return None

        print("Vuelos disponibles:")
        for i, vuelo in enumerate(vuelos_activos, 1):
            print(f"{i}. {vuelo.codigo} - {vuelo.origen} → {vuelo.destino} ({vuelo.fecha.strftime('%Y-%m-%d')})")
        self._separador()
        return vuelos_activos

    def informe_pasajeros_por_vuelo(self):
        if not self.__vuelos or not any(v.estado == "activo" for v in self.__vuelos):
            self.limpiar_consola()
            self._menu_informes()
            raise OpcionInvalidaError("No hay vuelos activos disponibles.")

        def encabezado():
            self._encabezado("INFORME DE PASAJEROS POR VUELO")

        vuelos_activos = self._mostrar_vuelos_para_informe(encabezado)
        if not vuelos_activos:
            self.limpiar_consola()
            self._menu_informes()
            raise OpcionInvalidaError("No hay vuelos activos disponibles.")

        while True:
            try:
                opcion = self.seleccionar_opcion()
                if not opcion.isdigit() or not (1 <= int(opcion) <= len(vuelos_activos)):
                    self._mostrar_vuelos_para_informe(encabezado)
                    raise OpcionInvalidaError(f"Opción inválida. Debe ser un número entre 1 y {len(vuelos_activos)}")
                vuelo = vuelos_activos[int(opcion) - 1]
                break
            except OpcionInvalidaError as e:
                print(f"{e}")

        self.limpiar_consola()
        encabezado()
        print(f"Vuelo: {vuelo.codigo} ")
        print(f"Ruta: {vuelo.origen} → {vuelo.destino}")
        print(f"Fecha: {vuelo.fecha.strftime('%Y-%m-%d')}")
        self._separador()
        print(f"{'Nombre':<25} {'Cédula':<15} {'Nacionalidad':<15} {'Equipaje':<10}")
        self._separador()

        if vuelo.tickets:
            for ticket in vuelo.tickets:
                cantidad_equipaje = len([e for e in vuelo.equipajes if e.pasajero.documento == ticket.pasajero.documento])
                nombre_completo = f"{ticket.pasajero.nombre} {ticket.pasajero.apellido}"
                print(f"{nombre_completo:<25} {ticket.pasajero.documento:<15} {ticket.pasajero.nacionalidad:<15} {cantidad_equipaje:<10}")
        else:
            print("No hay pasajeros registrados en este vuelo.")

        self._separador()
        input("\nPresione Enter para volver al menú de informes...")
        self.menu_informes()

    def informe_personal_asignado(self):
        if not self.__vuelos or not any(v.estado == "activo" for v in self.__vuelos):
            self.limpiar_consola()
            self._menu_informes()
            raise OpcionInvalidaError("No hay vuelos activos disponibles.")

        self.limpiar_consola()
        self._encabezado("INFORME DE PERSONAL ASIGNADO")

        vuelos_activos = [v for v in self.__vuelos if v.estado == "activo"]
        if not vuelos_activos:
            self.limpiar_consola()
            self._menu_informes()
            raise OpcionInvalidaError("No hay vuelos activos disponibles.")

        for vuelo in vuelos_activos:
            print(f"\nVuelo: {vuelo.codigo} - {vuelo.origen} → {vuelo.destino}")
            print(f"Fecha: {vuelo.fecha.strftime('%Y-%m-%d')}")
            self._separador()

            pilotos = [t for t in vuelo.tripulantes if t.rol == Rol.PILOTO]
            copilotos = [t for t in vuelo.tripulantes if t.rol == Rol.COPILOTO]
            azafatas = [t for t in vuelo.tripulantes if t.rol == Rol.AZAFATA]

            if pilotos:
                print("Piloto(s):")
                for piloto in pilotos:
                    print(f"  - {piloto.nombre} {piloto.apellido} ({piloto.documento})")
            else:
                print("Piloto: No asignado")

            if copilotos:
                print("Copiloto(s):")
                for copiloto in copilotos:
                    print(f"  - {copiloto.nombre} {copiloto.apellido} ({copiloto.documento})")
            else:
                print("Copiloto: No asignado")

            if azafatas:
                print("Azafata(s):")
                for azafata in azafatas:
                    print(f"  - {azafata.nombre} {azafata.apellido} ({azafata.documento})")
            else:
                print("Azafata: No asignada")

            self._separador()

        input("\nPresione Enter para volver al menú de informes...")
        self.menu_informes()

    def informe_vuelos_por_compania(self):
        if not self.__aerolineas:
            self.limpiar_consola()
            self._menu_informes()
            raise OpcionInvalidaError("No hay aerolíneas registradas.")

        self.limpiar_consola()
        self._encabezado("INFORME DE VUELOS POR COMPAÑÍA")
        print(f"{'Aerolínea':<30} {'Código':<15} {'Vuelos Activos':<15} {'Vuelos Cancelados':<15} {'Total':<10}")
        self._separador()

        for aerolinea in self.__aerolineas:
            vuelos_aerolinea = [v for v in self.__vuelos if v.aerolinea.codigo == aerolinea.codigo]
            vuelos_activos = len([v for v in vuelos_aerolinea if v.estado == "activo"])
            vuelos_cancelados = len([v for v in vuelos_aerolinea if v.estado == "cancelado"])
            total = len(vuelos_aerolinea)

            print(f"{aerolinea.nombre:<30} {aerolinea.codigo:<15} {vuelos_activos:<15} {vuelos_cancelados:<15} {total:<10}")

        self._separador()
        input("\nPresione Enter para volver al menú de informes...")
        self.menu_informes()

    def informe_vuelos_cancelados(self):
        if not self.__vuelos_cancelados_info:
            self.limpiar_consola()
            self._menu_informes()
            raise OpcionInvalidaError("No hay vuelos cancelados registrados.")

        self.limpiar_consola()
        self._encabezado("INFORME DE VUELOS CANCELADOS")
        print(f"{'Vuelo':<15} {'Ruta':<25} {'Fecha Cancelación':<20} {'Pasajeros Afectados':<20} {'Causa':<30}")
        self._separador()

        for vuelo_cancelado in self.__vuelos_cancelados_info:
            ruta = f"{vuelo_cancelado.origen} → {vuelo_cancelado.destino}"
            fecha_cancel = vuelo_cancelado.fecha.strftime('%Y-%m-%d %H:%M')
            pasajeros = vuelo_cancelado.pasajeros_afectados
            causa = vuelo_cancelado.causa[:28] + "..." if len(vuelo_cancelado.causa) > 30 else vuelo_cancelado.causa

            print(f"{vuelo_cancelado.codigo:<15} {ruta:<25} {fecha_cancel:<20} {pasajeros:<20} {causa:<30}")

        self._separador()
        input("\nPresione Enter para volver al menú de informes...")
        self.menu_informes()

    def menu_informes(self):
        self.limpiar_consola()
        self._menu_informes()
        while True:
            try:
                opcion = self.seleccionar_opcion()
                match opcion:
                    case '0':
                        self.limpiar_consola()
                        self.menu_principal()
                        break
                    case '1':
                        self.informe_pasajeros_por_vuelo()
                    case '2':
                        self.informe_personal_asignado()
                    case '3':
                        self.informe_vuelos_por_compania()
                    case '4':
                        self.informe_vuelos_cancelados()
                    case _:
                        self.limpiar_consola()
                        self._menu_informes()
                        raise OpcionInvalidaError("Opción inválida. Debe ser un número entre 0 y 4")
            except OpcionInvalidaError as e:
                print(f"{e}")
        