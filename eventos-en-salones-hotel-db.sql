-- 
-- ==========================================
-- 1. TABLAS DE CATÁLOGO (Nivel Independiente)
-- ==========================================

CREATE TABLE ROL (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE ESTADO_CUENTA (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE ESTADO_MOBIL (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE CARACTER_MOBI (
    numero SERIAL PRIMARY KEY,
    descripcion TEXT
);

CREATE TABLE TIPO_MOBIL (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    disposicion BOOLEAN
);

CREATE TABLE TIPO_MONTAJE (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    disposicion BOOLEAN
);

CREATE TABLE TIPO_EVENTO (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
    disposicion BOOLEAN
);

CREATE TABLE ESTADO_RESERVA (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE TIPO_CLIENTE (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE ESTADO_SALON (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE TIPO_SERVICIO (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    disposicion BOOLEAN
);

CREATE TABLE TIPO_EQUIPA (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    disposicion BOOLEAN
);

CREATE TABLE ESTADO_EQUIPA (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE CONCEPTO_PAGO (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE METODO_PAGO (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100)
);

-- ==========================================
-- 2. TABLAS DE ENTIDADES Y RELACIONES
-- ==========================================

CREATE TABLE CUENTA (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    contrasena VARCHAR(255),
    estado_cuenta VARCHAR(5) REFERENCES ESTADO_CUENTA(codigo)
);

CREATE TABLE TRABAJADOR (
    no_empleado VARCHAR(10) PRIMARY KEY,
    RFC VARCHAR(15),
    nombrePila VARCHAR(100),
    nombrePriApellido VARCHAR(100),
    nombreSegApellido VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(150),
    cuenta INTEGER REFERENCES CUENTA(numero),
    rol VARCHAR(5) REFERENCES ROL(codigo)
);

CREATE TABLE CLIENTE (
    numero SERIAL PRIMARY KEY,
    RFC VARCHAR(15),
    nombre_fiscal VARCHAR(200),
    nombrePila VARCHAR(100),
    nombrePriApellido VARCHAR(100),
    nombreSegApellido VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(150),
    dirColonia VARCHAR(100),
    dirCalle VARCHAR(100),
    dirNumero VARCHAR(20),
    tipo_cliente VARCHAR(5) REFERENCES TIPO_CLIENTE(codigo),
    cuenta INTEGER REFERENCES CUENTA(numero)
);

CREATE TABLE MOBILIARIO (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    costo REAL,
    stock INTEGER,
    tipo_mobil INTEGER REFERENCES TIPO_MOBIL(numero)
);

CREATE TABLE INVENTARIO_MOB (
    estado_mobil VARCHAR(5) REFERENCES ESTADO_MOBIL(codigo),
    mobiliario INTEGER REFERENCES MOBILIARIO(numero),
    cantidad INTEGER,
    PRIMARY KEY (estado_mobil, mobiliario)
);

CREATE TABLE DESCRIPCION_MOB (
    caracter_mobil INTEGER REFERENCES CARACTER_MOBI(numero),
    mobiliario INTEGER REFERENCES MOBILIARIO(numero),
    PRIMARY KEY (caracter_mobil, mobiliario)
);

CREATE TABLE SALON (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    costo REAL,
    ubicacion TEXT,
    dimenLargo REAL,
    dimenAncho REAL,
    dimenAlto REAL,
    metrosCuadrados REAL,
    maxCapacidad INTEGER,
    estado_salon VARCHAR(5) REFERENCES ESTADO_SALON(codigo)
);

CREATE TABLE REGISTR_ESTAD_SAL (
    salon INTEGER REFERENCES SALON(numero),
    estado_salon VARCHAR(5) REFERENCES ESTADO_SALON(codigo),
    fecha TIMESTAMP,
    PRIMARY KEY (salon, estado_salon)
);

CREATE TABLE MONTAJE (
    numero SERIAL PRIMARY KEY,
    costo REAL,
    salon INTEGER REFERENCES SALON(numero),
    tipo_montaje INTEGER REFERENCES TIPO_MONTAJE(numero)
);

CREATE TABLE MONTAJE_MOBILIARIO (
    numero SERIAL PRIMARY KEY,
    cantidad INTEGER,
    completado BOOLEAN,
    montaje INTEGER REFERENCES MONTAJE(numero),
    mobiliario INTEGER REFERENCES MOBILIARIO(numero)
);

CREATE TABLE RESERVACION (
    numero SERIAL PRIMARY KEY,
    descripEvento TEXT,
    estimaAsistentes INTEGER,
    fechaReservacion DATE,
    fechaEvento DATE,
    horaInicio TIME,
    horaFin TIME,
    subtotal REAL,
    IVA REAL,
    total REAL,
    cliente INTEGER REFERENCES CLIENTE(numero),
    montaje INTEGER REFERENCES MONTAJE(numero),
    estado_reserva VARCHAR(5) REFERENCES ESTADO_RESERVA(codigo),
    tipo_evento INTEGER REFERENCES TIPO_EVENTO(numero)
);

CREATE TABLE TRABAJA_RESERVA (
    reservacion INTEGER REFERENCES RESERVACION(numero),
    trabajador VARCHAR(10) REFERENCES TRABAJADOR(no_empleado),
    PRIMARY KEY (reservacion, trabajador)
);

CREATE TABLE ENCUESTA (
    numero SERIAL PRIMARY KEY,
    personal INTEGER,
    equipamientos INTEGER,
    servicios INTEGER,
    salon INTEGER,
    mobiliarios INTEGER,
    reservacion INTEGER REFERENCES RESERVACION(numero)
);

CREATE TABLE REGISTR_ESTAD_RESERVA (
    reservacion INTEGER REFERENCES RESERVACION(numero),
    estado_reserva VARCHAR(5) REFERENCES ESTADO_RESERVA(codigo),
    fecha TIMESTAMP,
    PRIMARY KEY (reservacion, estado_reserva)
);

CREATE TABLE EQUIPAMIENTO (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    costo REAL,
    stock INTEGER,
    tipo_equipa INTEGER REFERENCES TIPO_EQUIPA(numero)
);

CREATE TABLE INVENTARIO_EQUIPA (
    equipamiento INTEGER REFERENCES EQUIPAMIENTO(numero),
    estado_equipa VARCHAR(5) REFERENCES ESTADO_EQUIPA(codigo),
    cantidad INTEGER,
    PRIMARY KEY (equipamiento, estado_equipa)
);

CREATE TABLE RESERVA_EQUIPA (
    numero SERIAL PRIMARY KEY,
    cantidad INTEGER,
    reservacion INTEGER REFERENCES RESERVACION(numero),
    equipamiento INTEGER REFERENCES EQUIPAMIENTO(numero)
);

CREATE TABLE SERVICIO (
    numero SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    costo REAL,
    disposicion BOOLEAN,
    tipo_servicio INTEGER REFERENCES TIPO_SERVICIO(numero)
);

CREATE TABLE RESERVA_SERVICIO (
    reservacion INTEGER REFERENCES RESERVACION(numero),
    servicio INTEGER REFERENCES SERVICIO(numero),
    PRIMARY KEY (reservacion, servicio)
);

CREATE TABLE PAGO (
    numero SERIAL PRIMARY KEY,
    nota TEXT,
    monto REAL,
    fecha DATE,
    hora TIME,
    no_pago INTEGER,
    reservacion INTEGER REFERENCES RESERVACION(numero),
    concepto_pago VARCHAR(5) REFERENCES CONCEPTO_PAGO(codigo),
    metodo_pago VARCHAR(5) REFERENCES METODO_PAGO(codigo)
);
