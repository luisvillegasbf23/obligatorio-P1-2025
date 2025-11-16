from sistema import Sistema
from excepciones.error import OpcionInvalidaError, AerolineaNoRegistradaError, DatoDuplicadoError, PesoExcedidoError

if __name__ == "__main__":
    sistema = Sistema()
    
    sistema.limpiar_consola()
    sistema.menu_principal()
    while True:
        try:
            opcion = sistema.seleccionar_opcion()
            match opcion:
                case '0':
                    print("Saliendo...")
                    print("Nos vemos pronto!")
                    break
                case '1':
                    sistema.registrar_persona()
                case '2':
                    sistema.registrar_compania_aerea()
                case '3':
                    sistema.registrar_vuelo()
                case '4':
                    sistema.crear_ticket()
                case '5':
                    sistema.asignar_personal_vuelo()
                case '6':
                    sistema.registrar_equipaje()
                case '7':
                    sistema.visualizar_vuelos()
                case '8':
                    sistema.cancelar_ticket()
                case '9':
                    sistema.cancelar_vuelo()
                case '10':
                    sistema.menu_informes()
                case _:
                    sistema.limpiar_consola()
                    sistema.menu_principal()
                    raise OpcionInvalidaError("Opción inválida. Intente nuevamente.")
        except (OpcionInvalidaError, AerolineaNoRegistradaError, DatoDuplicadoError, PesoExcedidoError) as e:
            print(f"{e}")