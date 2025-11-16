# Sistema de Gestión de Vuelos Turísticos - Aeropuerto MERCOSUR

## 📋 Descripción General

Este sistema permite modelar, registrar y gestionar los elementos clave involucrados en la operación de vuelos turísticos del aeropuerto regional "MERCOSUR". El sistema gestiona vuelos directos (sin escalas) hacia países limítrofes de la región, incluyendo la interacción entre clientes, vuelos, compañías aéreas y equipaje en bodega.

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8 o superior
- No se requieren librerías externas (solo usa librerías estándar de Python)

### Ejecución
```bash
python main.py
```

El sistema iniciará con un menú principal interactivo donde podrás seleccionar las diferentes opciones disponibles.

## 📁 Estructura del Proyecto

```
entregable/
├── main.py                      # Punto de entrada del programa
├── sistema.py                   # Clase principal que gestiona toda la lógica del sistema
├── seed.py                      # Datos precargados para pruebas
├── entidades/                   # Clases que representan las entidades del dominio
│   ├── __init__.py
│   ├── persona.py               # Clase abstracta Persona
│   ├── cliente.py               # Clase Cliente (hereda de Persona)
│   ├── tripulante.py            # Clase Tripulante (hereda de Persona)
│   ├── aerolinea.py             # Clase Aerolinea
│   ├── vuelo.py                 # Clase Vuelo
│   ├── ticket.py                # Clase Ticket
│   ├── equipaje.py              # Clase Equipaje
│   └── vuelo_cancelado.py       # Clase VueloCancelado
└── excepciones/                 # Excepciones personalizadas
    ├── __init__.py
    └── error.py                 # Definición de excepciones
```

## 🏗️ Arquitectura del Sistema

### Clases Principales

#### 1. **Persona** (Clase Abstracta)
Clase base que contiene los atributos comunes entre clientes y tripulantes:
- `documento`: Documento de identidad
- `nombre`: Nombre
- `apellido`: Apellido
- `email`: Correo electrónico
- `telefono`: Teléfono/celular
- `fecha_ingreso`: Fecha de ingreso al sistema

#### 2. **Cliente** (Hereda de Persona)
Representa a los pasajeros del sistema:
- `nacionalidad`: Nacionalidad del pasajero
- `historial_de_vuelos`: Lista de vuelos realizados

#### 3. **Tripulante** (Hereda de Persona)
Representa al personal de vuelo:
- `rol`: Rol del tripulante (Piloto, Copiloto, Azafata)
- `horas_de_vuelo`: Horas acumuladas de vuelo

#### 4. **Aerolinea**
Representa una compañía aérea:
- `codigo`: Código único identificador (único como una cédula)
- `nombre`: Nombre de la aerolínea
- `pais_origen`: País de origen

#### 5. **Vuelo**
Representa un vuelo turístico:
- `codigo`: Código único del vuelo
- `origen`: País de origen
- `destino`: País de destino
- `duracion`: Duración en horas
- `fecha`: Fecha del vuelo
- `aerolinea`: Aerolínea responsable
- `cantidad_asientos`: Capacidad del avión
- `tipo_vuelo`: "nacional" o "internacional" (se determina automáticamente)
- `estado`: "activo" o "cancelado"
- `tickets`: Lista de tickets vendidos
- `equipajes`: Lista de equipajes en bodega
- `tripulantes`: Lista de tripulantes asignados

#### 6. **Ticket**
Representa un ticket de vuelo:
- `numero`: Número único dentro del vuelo (1 hasta capacidad)
- `pasajero`: Cliente asociado

#### 7. **Equipaje**
Representa el equipaje en bodega:
- `codigo`: Código único (formato: CODIGO_VUELO-NUMERO_TICKET)
- `pasajero`: Pasajero dueño del equipaje
- `vuelo`: Vuelo asociado
- `peso`: Peso en kg
- `precio`: Precio calculado según normativa

## 🎯 Funcionalidades Principales

### 1. Registrar Persona
Permite registrar tanto pasajeros como tripulantes:
- **Pasajero**: Se solicita documento, nombre, apellido, email, teléfono y nacionalidad
- **Tripulante**: Se solicita documento, nombre, apellido, email, teléfono, rol y horas de vuelo acumuladas

### 2. Registrar Compañía Aérea
Registra una nueva aerolínea con:
- País de origen (seleccionado de una lista)
- Nombre de la aerolínea
- El código se genera automáticamente

### 3. Crear Vuelo
Crea un nuevo vuelo con:
- Aerolínea (debe estar registrada)
- Origen y destino (seleccionados de lista de países)
- Duración en horas
- Fecha (formato YYYY-MM-DD)
- Cantidad de asientos
- El tipo de vuelo (nacional/internacional) se determina automáticamente según origen y destino
- El código del vuelo se genera automáticamente

### 4. Crear Ticket
Asigna un pasajero a un vuelo:
- Selecciona un vuelo activo con asientos disponibles
- Selecciona un pasajero registrado
- El número de ticket se asigna automáticamente (1 hasta capacidad)
- Evita duplicaciones (un pasajero no puede tener dos tickets en el mismo vuelo)

### 5. Asignar Personal a Vuelo
Asigna tripulantes a un vuelo:
- Cada vuelo debe tener al menos:
  - 1 Piloto
  - 1 Copiloto
  - 1 Azafata
- Valida que no haya repeticiones

### 6. Registrar Equipaje en Bodega
Registra el equipaje de un pasajero:
- Selecciona vuelo y ticket
- Ingresa peso del equipaje
- El código se genera automáticamente (CODIGO_VUELO-NUMERO_TICKET)
- Calcula el precio según normativa:
  - **Hasta 23 kg**: Sin cargo adicional
  - **24-32 kg**: 
    - Internacional: USD 100
    - Nacional: USD 30
  - **33-45 kg**:
    - Internacional: USD 200
    - Nacional: USD 60
  - **Más de 45 kg**: No se admite

### 7. Visualizar Vuelos
Muestra todos los vuelos con:
- Información del vuelo
- Personal asignado
- Pasajeros registrados
- Estado operativo

### 8. Cancelar Ticket
Cancela un ticket de un pasajero:
- Remueve el ticket del vuelo
- Remueve el equipaje asociado
- El ticket queda en lista de cancelados

### 9. Cancelar Vuelo
Cancela un vuelo completo:
- Solicita causa de cancelación
- Reasigna pasajeros, personal y equipaje a otro vuelo
- Cambia el estado del vuelo a "cancelado"
- Registra la información en historial de vuelos cancelados

### 10. Informes
Submenú con 4 tipos de informes:

#### a. Informe de Pasajeros por Vuelo
Listado con nombre, cédula, nacionalidad y cantidad de equipaje por pasajero.

#### b. Informe de Personal Asignado
Detalle por vuelo del piloto, copiloto y azafatas asignadas.

#### c. Informe de Vuelos por Compañía
Tabla comparativa de vuelos operados por cada compañía aérea (activos, cancelados, total).

#### d. Informe de Vuelos Cancelados
Historial con causa, fecha y cantidad de pasajeros afectados.

## 📊 Normativa de Equipaje

El sistema calcula automáticamente el costo del equipaje según el peso y el tipo de vuelo:

| Peso | Tipo Vuelo | Costo |
|------|------------|-------|
| ≤ 23 kg | Cualquiera | Sin cargo |
| 24-32 kg | Internacional | USD 100 |
| 24-32 kg | Nacional | USD 30 |
| 33-45 kg | Internacional | USD 200 |
| 33-45 kg | Nacional | USD 60 |
| > 45 kg | Cualquiera | No se admite |

**Nota**: Un vuelo es "nacional" cuando origen y destino son el mismo país. Es "internacional" cuando son diferentes.

## 🔒 Validaciones Implementadas

El sistema valida:
- ✅ Documentos duplicados (no puede haber dos personas con el mismo documento)
- ✅ Códigos de aerolínea duplicados
- ✅ Códigos de vuelo duplicados
- ✅ Campos vacíos
- ✅ Tipos de datos incorrectos
- ✅ Disponibilidad de asientos en vuelos
- ✅ Peso máximo de equipaje (45 kg)
- ✅ Tripulación mínima requerida (piloto, copiloto, azafata)
- ✅ Aerolínea debe estar registrada antes de crear vuelo
- ✅ Pasajero debe estar registrado antes de comprar ticket

## 🎨 Interfaz de Usuario

El sistema utiliza una interfaz de consola con:
- Menús numerados para selección de opciones
- Encabezados y separadores visuales para mejor legibilidad
- Mensajes de éxito y error claros
- Validación de entrada con reintentos automáticos

## 📝 Ejemplo de Uso

1. **Registrar una aerolínea**:
   - Selecciona opción 2 del menú principal
   - Elige país de origen
   - Ingresa nombre de la aerolínea

2. **Registrar un pasajero**:
   - Selecciona opción 1 → 1 (Pasajero)
   - Completa los datos solicitados

3. **Crear un vuelo**:
   - Selecciona opción 3
   - Elige la aerolínea
   - Selecciona origen y destino
   - Ingresa duración, fecha y cantidad de asientos

4. **Comprar un ticket**:
   - Selecciona opción 4
   - Elige el vuelo
   - Elige el pasajero

5. **Registrar equipaje**:
   - Selecciona opción 6
   - Elige vuelo y ticket
   - Ingresa peso del equipaje

## 🔧 Consideraciones Técnicas

- **Almacenamiento**: Todos los datos se mantienen en memoria (listas) durante la ejecución
- **Persistencia**: Los datos no se guardan al cerrar el programa (excepto los precargados en `seed.py`)
- **Fechas**: Se usa la librería `datetime` de Python
- **Excepciones**: Se definen excepciones personalizadas en `excepciones/error.py`
- **Herencia**: Se utiliza herencia para `Cliente` y `Tripulante` que heredan de `Persona`

## 📚 Clases y Métodos Importantes

### Clase Sistema
- `menu_principal()`: Muestra el menú principal
- `registrar_persona()`: Registra pasajeros o tripulantes
- `registrar_compania_aerea()`: Registra aerolíneas
- `registrar_vuelo()`: Crea nuevos vuelos
- `crear_ticket()`: Asigna pasajeros a vuelos
- `asignar_personal_vuelo()`: Asigna tripulantes a vuelos
- `registrar_equipaje()`: Registra equipaje en bodega
- `visualizar_vuelos()`: Muestra información de vuelos
- `cancelar_ticket()`: Cancela un ticket
- `cancelar_vuelo()`: Cancela un vuelo completo
- `menu_informes()`: Submenú de informes

## 🐛 Manejo de Errores

El sistema maneja errores mediante excepciones personalizadas:
- `OpcionInvalidaError`: Opción de menú inválida
- `DatoDuplicadoError`: Intento de registrar datos duplicados
- `DatoVacioError`: Campo requerido vacío
- `AerolineaNoRegistradaError`: Aerolínea no existe
- `PesoExcedidoError`: Equipaje excede peso máximo

Todas las excepciones muestran mensajes claros y permiten reintentar la operación.

## 👥 Autores

Este sistema fue desarrollado como parte del obligatorio de Programación 1.

## 📄 Licencia

Este proyecto es parte de un trabajo académico.

---

**Nota**: Para más detalles sobre los requisitos específicos, consultar el documento `Lic_Oblig_P1_2025.pdf`.

