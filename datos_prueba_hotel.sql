-- ========================================
-- DATOS DE PRUEBA HOTEL BOOKINGROOM
-- ========================================
-- Base de datos: bookingroom_nuevadata
-- Objetivo: Datos realistas de un hotel con servicios, 
-- equipamiento, mobiliario, salones y reservaciones coherentes
-- ========================================

-- INSTRUCCIONES DE USO:
-- 1. Crear base de datos: createdb -U postgres bookingroom_nuevadata
-- 2. Aplicar migraciones: python manage.py migrate --database=nueva_data
-- 3. Ejecutar este script: psql -U postgres -d bookingroom_nuevadata -f datos_prueba_hotel.sql
-- ========================================

BEGIN;

-- ========================================
-- 1. CATÁLOGOS Y ESTADOS (Ya existen del backup)
-- ========================================

-- ========================================
-- 1.1 ROLES
-- ========================================
INSERT INTO rol (codigo, nombre) VALUES 
('ADMIN', 'Administrador'),
('RECEP', 'Recepcionista'),
('COORD', 'Coordinador'),
('ALM', 'Almacenista')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.2 ESTADOS DE CUENTA
-- ========================================
INSERT INTO estado_cuenta (codigo, nombre) VALUES 
('ACT', 'Activa'),
('SUSP', 'Suspendida'),
('INACT', 'Inactiva')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.3 TIPOS DE CLIENTE
-- ========================================
INSERT INTO tipo_cliente (codigo, nombre, disposicion) VALUES 
('FIS', 'Persona Física', true),
('MOR', 'Persona Moral', true),
('EXT', 'Extranjero', true),
('GOB', 'Gobierno', true)
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.4 ESTADOS DE MOBILIARIO
-- ========================================
INSERT INTO estado_mobil (codigo, nombre) VALUES 
('DISP', 'Disponible'),
('OCUP', 'Ocupado'),
('DAN', 'Dañado'),
('MAN', 'En Mantenimiento')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.5 CARACTERÍSTICAS DE MOBILIARIO (Ampliar)
-- ========================================
INSERT INTO caracter_mobi (descripcion) VALUES 
('Plegable'),
('Apilable'),
('Acolchado'),
('Ajustable en altura'),
('Con reposabrazos'),
('Con ruedas'),
('Resistente al agua'),
('Material ignífugo'),
('Ligero y portátil'),
('Ergonómico')
ON CONFLICT DO NOTHING;

-- ========================================
-- 1.6 TIPOS DE MOBILIARIO (Ampliar para hotel)
-- ========================================
INSERT INTO tipo_mobil (nombre, disposicion) VALUES 
('Mesas', true),
('Sillas', true),
('Podios y Atriles', true),
('Escenarios', true),
('Mesas de buffet', true),
('Mobiliario lounge', true),
('Mobiliario exterior', true),
('Mobiliario presidencial', true)
ON CONFLICT DO NOTHING;

-- ========================================
-- 1.7 TIPOS DE MONTAJE (Ampliar basado en referencia)
-- ========================================
INSERT INTO tipo_montaje (nombre, disposicion, capacidadIdeal) VALUES 
('Auditorio/Teatro', true, 200),
('Escuela/Aula', true, 40),
('Herradura/U', true, 30),
('Imperial', true, 25),
('Banquete', true, 120),
('Cóctel/Recepción', true, 150),
('Mesa Redonda', true, 80),
('Estilo Lounge', true, 50),
('Mesa Rusa/O', true, 35),
('Española/Boardroom', true, 20)
ON CONFLICT DO NOTHING;

-- ========================================
-- 1.8 TIPOS DE EVENTO
-- ========================================
INSERT INTO tipo_evento (nombre, disposicion) VALUES 
('Boda', true),
('XV Años', true),
('Bautizo', true),
('Graduación', true),
('Corporativo', true),
('Conferencia', true),
('Seminar', true),
('Cumpleaños', true),
('Aniversario', true),
('Gala', true),
('Exposición', true)
ON CONFLICT DO NOTHING;

-- ========================================
-- 1.9 ESTADOS DE RESERVACIÓN
-- ========================================
INSERT INTO estado_reserva (codigo, nombre) VALUES 
('SOLIC', 'Solicitada'),
('PEN', 'Pendiente'),
('CON', 'Confirmada'),
('ENPRO', 'En Proceso'),
('PAGAD', 'Pagada'),
('FIN', 'Finalizada'),
('CAN', 'Cancelada'),
('CANC', 'Cancelada por Cliente'),
('RECH', 'Rechazada')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.10 ESTADOS DE SALÓN
-- ========================================
INSERT INTO estado_salon (codigo, nombre) VALUES 
('DIS', 'Disponible'),
('OCUP', 'Ocupado'),
('RESV', 'Reservado'),
('LIMP', 'En Limpieza'),
('MAN', 'En Mantenimiento')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.11 TIPOS DE EQUIPAMIENTO (Ampliar)
-- ========================================
INSERT INTO tipo_equipa (nombre, disposicion) VALUES 
('Audio', true),
('Video/Proyección', true),
('Iluminación', true),
('Climatización', true),
('Equipos para reuniones', true),
('Equipo empresarial', true),
('Telecomunicaciones', true),
('Accesorios de presentación', true)
ON CONFLICT DO NOTHING;

-- ========================================
-- 1.12 ESTADOS DE EQUIPAMIENTO
-- ========================================
INSERT INTO estado_equipa (codigo, nombre) VALUES 
('DISP', 'Disponible'),
('OCUP', 'Ocupado'),
('DAN', 'Dañado'),
('MAN', 'En Mantenimiento'),
('RESV', 'Reservado')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.13 CONCEPTOS DE PAGO
-- ========================================
INSERT INTO concepto_pago (codigo, nombre) VALUES 
('ABON', 'Abono'),
('LIQ', 'Liquidación'),
('EXT', 'Extra'),
('CANC', 'Cancelación'),
('ADIC', 'Adicional')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.14 MÉTODOS DE PAGO
-- ========================================
INSERT INTO metodo_pago (codigo, nombre) VALUES 
('EFEC', 'Efectivo'),
('TARJ', 'Tarjeta de Crédito'),
('NFC', 'Contactless/NFC'),
('TRANS', 'Transferencia'),
('CHEQ', 'Cheque')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.15 TIPOS DE SERVICIO (Ampliar)
-- ========================================
INSERT INTO tipo_servicio (nombre, descripcion, disposicion) VALUES 
('Servicios para reuniones', 'Servicios orientados a juntas y reuniones de trabajo', true),
('Servicios ejecutivos', 'Servicios premium para clientes VIP', true),
('Internet y Telecom', 'Servicios de conectividad y comunicación', true),
('Catering y Alimentos', 'Servicios de alimentación y bebidas', true),
('Decoración y Ambientación', 'Servicios de diseño y decoración de espacios', true),
('Logística y Coordinación', 'Servicios de organización y coordinación de eventos', true),
('Audiovisuales', 'Servicios técnicos de audio y video', true),
('Limpieza y Mantenimiento', 'Servicios de limpieza durante y después del evento', true),
('Seguridad', 'Servicios de seguridad y control de acceso', true),
('Transporte', 'Servicios de transporte para invitados', true)
ON CONFLICT DO NOTHING;


-- ========================================
-- 2. CUENTAS Y USUARIOS
-- ========================================

-- ========================================
-- 2.1 CUENTAS
-- ========================================
INSERT INTO cuenta (nombre_usuario, correo_electronico, firebase_uid, estado_cuenta_id) VALUES 
('martha.rivera', 'martha.rivera@email.com', 'firebase_uid_martha', 1),  -- ADMIN
('carlos.mtz', 'carlos.mtz@hotel.com', 'firebase_uid_carlos', 1),         -- RECEP
('luis.garcia', 'luis.garcia@hotel.com', 'firebase_uid_luis', 1),         -- COORD
('ana.perez', 'ana.perez@hotel.com', 'firebase_uid_ana', 1),              -- ALM
('jorge.rodriguez', 'jorge.rodriguez@hotel.com', 'firebase_uid_jorge', 1), -- RECEP
('cliente_corp', 'contacto@corpindustrial.mx', 'firebase_uid_corp', 1),  -- Cliente 1 (3 reservaciones)
('ana.martinez', 'ana.martinez@gmail.com', 'firebase_uid_ana_m', 1),     -- Cliente 2
('roberto.sanchez', 'roberto.sanchez@outlook.com', 'firebase_uid_robert', 1), -- Cliente 3
('events_planner', 'info@eventsplanner.com', 'firebase_uid_events', 1),  -- Cliente 4
('fiestas_deluxe', 'reservaciones@fiestasdeluxe.com', 'firebase_uid_fiestas', 1) -- Cliente 5
ON CONFLICT (correo_electronico) DO NOTHING;

-- ========================================
-- 2.2 TRABAJADORES
-- ========================================
INSERT INTO trabajador (no_empleado, rfc, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, rol_id, cuenta_id) VALUES 
('TRAB001', 'RIMJ850101XXX', 'Martha', 'Rivera', 'Jiménez', '5551234567', 'martha.rivera@email.com', 'ADMIN', 1),
('TRAB002', 'MACL900202XXX', 'Carlos', 'Martínez', 'López', '5552345678', 'carlos.mtz@hotel.com', 'RECEP', 2),
('TRAB003', 'GALJ880303XXX', 'Luis', 'García', 'López', '5553456789', 'luis.garcia@hotel.com', 'COORD', 3),
('TRAB004', 'PEAN920404XXX', 'Ana', 'Pérez', 'Núñez', '5554567890', 'ana.perez@hotel.com', 'ALM', 4),
('TRAB005', 'ROHJ950505XXX', 'Jorge', 'Rodríguez', 'Hernández', '5555678901', 'jorge.rodriguez@hotel.com', 'RECEP', 5)
ON CONFLICT (no_empleado) DO NOTHING;

-- ========================================
-- 2.3 DATOS DE CLIENTES
-- ========================================
INSERT INTO datos_cliente (rfc, nombre_fiscal, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, tipo_cliente_id, cuenta_id) VALUES 
-- Cliente 1: Corporativo Industrial (3 reservaciones)
('COR850101XXX', 'Corporativo Industrial del Norte S.A. de C.V.', 'Roberto', 'Corporativo', 'Industrial', '5559871234', 'contacto@corpindustrial.mx', 'Colonia Centro', 'Av. Constitución', '456', 'MOR', 6),
-- Cliente 2: Ana Martínez
('MANA900515XXX', 'Ana Sofía Martínez', 'Ana Sofía', 'Martínez', 'González', '5558761234', 'ana.martinez@gmail.com', 'Colonia Del Valle', 'Calle Insurgentes Sur', '789', 'FIS', 7),
-- Cliente 3: Roberto Sánchez
('SARL850920XXX', 'Roberto Sánchez', 'Roberto', 'Sánchez', 'Luna', '5557651234', 'roberto.sanchez@outlook.com', 'Colonia Roma Norte', 'Av. Juárez', '321', 'FIS', 8),
-- Cliente 4: Events Planner
('EVP900101XXX', 'Events Planner México S.C.', 'Laura', 'Events', 'Planner', '5556541234', 'info@eventsplanner.com', 'Colonia Polanco', 'Av. Masaryk', '123', 'MOR', 9),
-- Cliente 5: Fiestas Deluxe
('FID850202XXX', 'Fiestas Deluxe Eventos S.A. de C.V.', 'Carmen', 'Fiestas', 'Deluxe', '5555431234', 'reservaciones@fiestasdeluxe.com', 'Colonia Coyoacán', 'Calle Hidalgo', '654', 'MOR', 10)
ON CONFLICT (correo_electronico) DO NOTHING;


-- ========================================
-- 3. SERVICIOS, EQUIPAMIENTO Y MOBILIARIO
-- ========================================

-- ========================================
-- 3.1 SERVICIOS (Basados en tipos de hotel)
-- ========================================
INSERT INTO servicio (nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES 
-- Servicios para reuniones (tipo_servicio_id: 1)
('Servicio de Coffee Break', 'Café, té y botanas durante la reunión', 1500.00, true, 1),
('Servicio de Lunch Box', 'Caja de almuerzo individual para asistentes', 3500.00, true, 1),
('Servicio de Coordinador de Evento', 'Coordinador dedicado durante todo el evento', 2500.00, true, 6),

-- Servicios ejecutivos e internet (tipo_servicio_id: 2, 3)
('WiFi Premium Dedicado', 'Internet de alta velocidad dedicado para el evento', 1200.00, true, 3),
('Videoconferencia HD', 'Sistema de videoconferencia con pantalla 4K', 2800.00, true, 3),
('Servicio de Traducción Simultánea', 'Intérprete profesional para eventos bilingües', 4500.00, true, 2),
('Servicio de Valet Parking', 'Estacionamiento con servicio de valet para invitados', 3000.00, true, 2),

-- Catering y Alimentos (tipo_servicio_id: 4)
('Banquete Premium', 'Banquete de 3 tiempos para eventos sociales', 8500.00, true, 4),
('Cena de Gala', 'Cena formal de 5 tiempos con maridaje', 15000.00, true, 4),
('Buffet Ejecutivo', 'Buffet variado para eventos corporativos', 6000.00, true, 4),
('Barra de Bebidas Premium', 'Barra libre con bebidas premium y coctelería', 7500.00, true, 4),

-- Decoración y Ambientación (tipo_servicio_id: 5)
('Decoración Floral Premium', 'Arreglos florales de alta gama para mesas y escenario', 5000.00, true, 5),
('Iluminación Ambiental LED', 'Iluminación profesional con colores personalizables', 3500.00, true, 5),
('Centro de Mesa Premium', 'Centros de mesa elegantes para eventos sociales', 2500.00, true, 5),

-- Logística y Coordinación (tipo_servicio_id: 6)
('Servicio de Fotografía Profesional', 'Fotógrafo profesional durante todo el evento', 6000.00, true, 6),
('Servicio de Video y Edición', 'Videógrafo profesional con edición post-evento', 8500.00, true, 6),
('DJ y Música Ambiental', 'DJ profesional con equipo de sonido incluido', 4500.00, true, 6),

-- Audiovisuales (tipo_servicio_id: 7)
('Proyector y Pantalla HD', 'Proyector de alta definición con pantalla de 120"', 2000.00, true, 7),
('Sistema de Audio Profesional', 'Consola de audio con micrófonos inalámbricos', 3500.00, true, 7),

-- Limpieza y Seguridad (tipo_servicio_id: 8, 9)
('Servicio de Limpieza Durante Evento', 'Personal de limpieza durante todo el evento', 1800.00, true, 8),
('Seguridad Privada', 'Guardia de seguridad para control de acceso', 2500.00, true, 9)
ON CONFLICT DO NOTHING;

-- ========================================
-- 3.2 EQUIPAMIENTO (Hotel)
-- ========================================
INSERT INTO equipamiento (nombre, descripcion, costo, stock, tipo_equipa_id) VALUES 
-- Audio (tipo_equipa_id: 1)
('Micrófono Inalámbrico Profesional', 'Micrófono de mano con receptor profesional', 1500.00, 8, 1),
('Sistema de Audio Portátil', 'Bocinas portátiles con Bluetooth', 2500.00, 4, 1),
('Consola de Audio Digital', 'Mezclador digital de 16 canales', 3000.00, 2, 1),
('Bocinas de Ambiente', 'Bocinas para distribución de audio ambiental', 1200.00, 6, 1),

-- Video/Proyección (tipo_equipa_id: 2)
('Proyector 4K UHD', 'Proyector de ultra alta definición 5000 lúmenes', 2000.00, 4, 2),
('Pantalla de Proyección 120"', 'Pantalla eléctrica de 120 pulgadas', 800.00, 5, 2),
('Pantalla LED 90"', 'Pantalla LED de alta resolución', 3500.00, 2, 2),
('Cámara de Video Profesional', 'Cámara 4K para grabación de eventos', 1800.00, 3, 2),
('Laptop de Presentación', 'Laptop con software de presentaciones', 1500.00, 4, 2),

-- Iluminación (tipo_equipa_id: 3)
('Kit de Iluminación LED', 'Set de luces LED RGB para ambientación', 2000.00, 5, 3),
('Iluminación de Emergencia', 'Sistema de iluminación de respaldo', 1000.00, 10, 3),
('Controlador de Luces DMX', 'Consola para control de iluminación', 1800.00, 2, 3),

-- Climatización (tipo_equipa_id: 4)
('Ventilador Industrial', 'Ventilador de alta potencia para espacios grandes', 800.00, 6, 4),
('Calefactor Portátil', 'Calefactor eléctrico para espacios cerrados', 1200.00, 4, 4),

-- Equipos para reuniones (tipo_equipa_id: 5)
('Pizarrón Digital Interactivo', 'Pizarrón táctil de 65 pulgadas', 2500.00, 3, 5),
('Rotafolios con Hojas', 'Rotafolio profesional con 50 hojas', 400.00, 8, 5),
('Flip Chart Profesional', 'Flip chart magnético con marcadores', 600.00, 5, 5),

-- Equipo empresarial (tipo_equipa_id: 6)
('Impresora Multifuncional', 'Impresora, scanner y copiadora', 1500.00, 2, 6),
('Scanner de Documentos', 'Scanner de alta velocidad', 800.00, 3, 6),
('Shredder/Trituradora', 'Trituradora de documentos confidenciales', 600.00, 2, 6),
('Máquina de Café Express', 'Máquina de café profesional para eventos', 1800.00, 4, 6)
ON CONFLICT DO NOTHING;

-- ========================================
-- 3.3 MOBILIARIO (Basado en referencia PDF)
-- ========================================
INSERT INTO mobiliario (nombre, descripcion, costo, stock, tipo_movil_id) VALUES 
-- Mesas (tipo_movil_id: 1)
('Mesa Rectangular 2.40m', 'Mesa rectangular plegable de 2.40m x 0.90m', 800.00, 20, 1),
('Mesa Rectangular 1.80m', 'Mesa rectangular plegable de 1.80m x 0.75m', 600.00, 25, 1),
('Mesa Redonda 1.50m', 'Mesa redonda para 8 personas, diámetro 1.50m', 900.00, 15, 1),
('Mesa Redonda 1.80m', 'Mesa redonda para 10-12 personas, diámetro 1.80m', 1100.00, 12, 1),
('Mesa de Buffet', 'Mesa larga para servicio de buffet con mantel', 700.00, 8, 5),

-- Sillas (tipo_movil_id: 2)
('Silla Tiffany', 'Silla elegante estilo Tiffany para eventos formales', 350.00, 80, 2),
('Silla Plegable Estándar', 'Silla plegable resistente y apilable', 200.00, 150, 2),
('Silla con Escritorio (Pala)', 'Silla con superficie de escritura integrada', 250.00, 50, 2),
('Silla Ejecutiva Acolchada', 'Silla ergonómica con reposabrazos', 400.00, 40, 2),

-- Podios y Atriles (tipo_movil_id: 3)
('Podio de Madera Profesional', 'Podio elegante con micrófono integrado', 500.00, 5, 3),
('Atril de Acrílico', 'Atril moderno transparente de acrílico', 450.00, 4, 3),

-- Escenarios (tipo_movil_id: 4)
('Escenario Modular 4x3m', 'Escenario elevado modular de 4x3 metros', 5000.00, 3, 4),
('Escenario Modular 3x2m', 'Escenario elevado modular de 3x2 metros', 3500.00, 4, 4),

-- Mobiliario Lounge (tipo_movil_id: 6)
('Sofá Modular 3 plazas', 'Sofá moderno de 3 plazas para área lounge', 1200.00, 8, 6),
('Puff Individual', 'Puff acolchado individual', 400.00, 15, 6),
('Mesa de Centro Baja', 'Mesa baja de centro para área lounge', 500.00, 10, 6),

-- Mesas Presidenciales (tipo_movil_id: 8)
('Mesa Presidencial 3m', 'Mesa presidencial de 3 metros con mantel premium', 1500.00, 3, 8),
('Taburete Alto', 'Taburete alto para mesas de cóctel', 300.00, 30, 1)
ON CONFLICT DO NOTHING;

-- ========================================
-- 3.4 CARACTERÍSTICAS ASIGNADAS A MOBILIARIO
-- ========================================
-- Mesa Rectangular 2.40m -> Plegable
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (1, 1), (1, 7);
-- Mesa Rectangular 1.80m -> Plegable
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (2, 1), (2, 7);
-- Mesa Redonda 1.50m -> Ligero
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (3, 9);
-- Silla Tiffany -> Apilable, Ergonómico
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (6, 2), (6, 10);
-- Silla Plegable Estándar -> Plegable, Apilable
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (7, 1), (7, 2);
-- Silla Pala -> Plegable
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (8, 1);
-- Silla Ejecutiva -> Acolchado, Con reposabrazos, Ergonómico
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (9, 3), (9, 5), (9, 10);
-- Podium -> Material ignífugo
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (10, 8);
-- Sofá Modular -> Acolchado, Ergonómico
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (16, 3), (16, 10);
-- Puff -> Acolchado, Ligero
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (17, 3), (17, 9);
-- Taburete Alto -> Apilable, Ligero
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (19, 2), (19, 9);


-- ========================================
-- 4. INVENTARIOS
-- ========================================

-- ========================================
-- 4.1 INVENTARIO DE MOBILIARIO
-- ========================================
INSERT INTO inventario_mobil (mobiliario_id, estado_mobil_id, cantidad) VALUES 
(1, 'DISP', 20),   -- Mesa Rectangular 2.40m: 20 disponibles
(2, 'DISP', 25),   -- Mesa Rectangular 1.80m: 25 disponibles
(3, 'DISP', 15),   -- Mesa Redonda 1.50m: 15 disponibles
(4, 'DISP', 12),   -- Mesa Redonda 1.80m: 12 disponibles
(5, 'DISP', 8),    -- Mesa de Buffet: 8 disponibles
(6, 'DISP', 80),   -- Silla Tiffany: 80 disponibles
(7, 'DISP', 150),  -- Silla Plegable: 150 disponibles
(8, 'DISP', 50),   -- Silla Pala: 50 disponibles
(9, 'DISP', 40),   -- Silla Ejecutiva: 40 disponibles
(10, 'DISP', 5),   -- Podio: 5 disponibles
(11, 'DISP', 4),   -- Atril: 4 disponibles
(12, 'DISP', 3),   -- Escenario 4x3m: 3 disponibles
(13, 'DISP', 4),   -- Escenario 3x2m: 4 disponibles
(14, 'DISP', 3),   -- Puff: 3 disponibles
(15, 'DISP', 8),   -- Puff: 8 disponibles
(16, 'DISP', 15),  -- Puff: 15 disponibles
(17, 'DISP', 10),  -- Mesa Centro Baja: 10 disponibles
(18, 'DISP', 3),   -- Mesa Presidencial: 3 disponibles
(19, 'DISP', 30)   -- Taburete Alto: 30 disponibles
ON CONFLICT ON CONSTRAINT estado_mobiliario DO NOTHING;

-- ========================================
-- 4.2 INVENTARIO DE EQUIPAMIENTO
-- ========================================
INSERT INTO inventario_equipa (equipamiento_id, estado_equipa_id, cantidad) VALUES 
(1, 'DISP', 8),    -- Micrófono: 8 disponibles
(2, 'DISP', 4),    -- Sistema Audio Portátil: 4 disponibles
(3, 'DISP', 2),    -- Consola Audio: 2 disponibles
(4, 'DISP', 6),    -- Bocinas Ambiente: 6 disponibles
(5, 'DISP', 4),    -- Proyector 4K: 4 disponibles
(6, 'DISP', 5),    -- Pantalla 120": 5 disponibles
(7, 'DISP', 2),    -- Pantalla LED 90": 2 disponibles
(8, 'DISP', 3),    -- Cámara Video: 3 disponibles
(9, 'DISP', 4),    -- Laptop Presentación: 4 disponibles
(10, 'DISP', 5),   -- Kit Iluminación LED: 5 disponibles
(11, 'DISP', 10),  -- Iluminación Emergencia: 10 disponibles
(12, 'DISP', 2),   -- Controlador Luces: 2 disponibles
(13, 'DISP', 6),   -- Ventilador Industrial: 6 disponibles
(14, 'DISP', 4),   -- Calefactor: 4 disponibles
(15, 'DISP', 3),   -- Pizarrón Digital: 3 disponibles
(16, 'DISP', 8),   -- Rotafolios: 8 disponibles
(17, 'DISP', 5),   -- Flip Chart: 5 disponibles
(18, 'DISP', 2),   -- Impresora: 2 disponibles
(19, 'DISP', 3),   -- Scanner: 3 disponibles
(20, 'DISP', 2),   -- Shredder: 2 disponibles
(21, 'DISP', 4)    -- Máquina Café: 4 disponibles
ON CONFLICT ON CONSTRAINT estado_equipamiento DO NOTHING;


-- ========================================
-- 5. SALONES (Basado en referencia PDF)
-- ========================================
INSERT INTO salon (nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES 
-- Salones para eventos grandes
('Salón Gran Gala', 15000.00, 'Piso 1, Ala Norte', 25.00, 15.00, 4.00, 375.00, 200, 'DIS'),
('Salón Imperial', 12000.00, 'Piso 2, Ala Este', 20.00, 12.00, 3.50, 240.00, 150, 'DIS'),
('Salón Real', 10000.00, 'Piso 1, Ala Sur', 18.00, 10.00, 3.00, 180.00, 120, 'DIS'),
('Salón Plaza', 8000.00, 'Piso 2, Ala Oeste', 15.00, 10.00, 3.00, 150.00, 100, 'DIS'),

-- Salones para eventos medianos
('Salón Ejecutivo', 6000.00, 'Piso 3, Ala Norte', 12.00, 8.00, 2.80, 96.00, 60, 'DIS'),
('Salón Business', 5500.00, 'Piso 3, Ala Sur', 10.00, 8.00, 2.80, 80.00, 50, 'DIS'),
('Salón Konferencia', 5000.00, 'Piso 3, Ala Este', 10.00, 7.00, 2.80, 70.00, 40, 'DIS'),

-- Salones para eventos pequeños
('Salón Boardroom', 4000.00, 'Piso 4, Ala Norte', 8.00, 6.00, 2.60, 48.00, 25, 'DIS'),
('Salón Lounge VIP', 3500.00, 'Piso 4, Ala Sur', 8.00, 5.00, 2.60, 40.00, 20, 'DIS'),

-- Salones exteriores y especiales
('Terraza Mirador', 9000.00, 'Azotea, Nivel 5', 22.00, 12.00, 4.00, 264.00, 150, 'DIS'),
('Jardín Interior', 7500.00, 'Planta Baja, Ala Central', 18.00, 10.00, 6.00, 180.00, 120, 'DIS')
ON CONFLICT DO NOTHING;

-- Registro de estado actual de salones
INSERT INTO registr_esta_salon (salon_id, estado_salon_id, fecha) VALUES 
(1, 'DIS', CURRENT_DATE),
(2, 'DIS', CURRENT_DATE),
(3, 'DIS', CURRENT_DATE),
(4, 'DIS', CURRENT_DATE),
(5, 'DIS', CURRENT_DATE),
(6, 'DIS', CURRENT_DATE),
(7, 'DIS', CURRENT_DATE),
(8, 'DIS', CURRENT_DATE),
(9, 'DIS', CURRENT_DATE),
(10, 'DIS', CURRENT_DATE),
(11, 'DIS', CURRENT_DATE)
ON CONFLICT DO NOTHING;


-- ========================================
-- 6. MONTAJES Y MOBILIARIO ASOCIADO
-- ========================================

-- ========================================
-- 6.1 MONTAJES (Uno por cada salón x tipo)
-- ========================================
INSERT INTO montaje (costo, salon_id, tipo_montaje_id) VALUES 
-- Salón Gran Gala
(2500.00, 1, 1),  -- Auditorio
(3000.00, 1, 5),  -- Banquete
(2800.00, 1, 6),  -- Cóctel

-- Salón Imperial
(2000.00, 2, 1),  -- Auditorio
(2500.00, 2, 5),  -- Banquete
(2200.00, 2, 2),  -- Escuela

-- Salón Real
(1800.00, 3, 5),  -- Banquete
(1500.00, 3, 3),  -- Herradura

-- Salón Business
(1200.00, 6, 2),  -- Escuela
(1400.00, 6, 4),  -- Imperial
(1300.00, 6, 10), -- Boardroom

-- Salón Boardroom
(1000.00, 8, 10), -- Boardroom
(900.00, 8, 4),   -- Imperial
ON CONFLICT DO NOTHING;

-- ========================================
-- 6.2 MOBILIARIO DE CADA MONTAJE
-- ========================================
-- Montaje 1: Gran Gala - Auditorio (ID:1)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(100, false, true, 1, 7),   -- 100 Sillas Plegables
(1, false, true, 1, 10),    -- 1 Podio
(1, false, true, 1, 12);    -- 1 Escenario 4x3m

-- Montaje 2: Gran Gala - Banquete (ID:2)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(12, false, true, 2, 4),    -- 12 Mesas Redondas 1.80m
(120, false, true, 2, 6),   -- 120 Sillas Tiffany
(1, false, true, 2, 18);    -- 1 Mesa Presidencial

-- Montaje 3: Gran Gala - Cóctel (ID:3)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(15, false, true, 3, 5),    -- 15 Mesas de Buffet
(30, false, true, 3, 19),   -- 30 Taburetes Altos
(3, false, true, 3, 16);    -- 3 Sofás Modulares

-- Montaje 4: Imperial - Auditorio (ID:4)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(80, false, true, 4, 7),    -- 80 Sillas Plegables
(1, false, true, 4, 11),    -- 1 Atril
(1, false, true, 4, 13);    -- 1 Escenario 3x2m

-- Montaje 5: Imperial - Banquete (ID:5)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(10, false, true, 5, 4),    -- 10 Mesas Redondas 1.80m
(100, false, true, 5, 6),   -- 100 Sillas Tiffany
(1, false, true, 5, 18);    -- 1 Mesa Presidencial

-- Montaje 6: Imperial - Escuela (ID:6)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(15, false, true, 6, 2),    -- 15 Mesas Rectangulares 1.80m
(40, false, true, 6, 8),    -- 40 Sillas Pala
(1, false, true, 6, 15);    -- 1 Pizarrón Digital

-- Montaje 7: Real - Banquete (ID:7)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(8, false, true, 7, 3),     -- 8 Mesas Redondas 1.50m
(80, false, true, 7, 6),    -- 80 Sillas Tiffany
(2, false, true, 7, 17);    -- 2 Mesas de Centro Baja

-- Montaje 8: Real - Herradura (ID:8)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(10, false, true, 8, 1),    -- 10 Mesas Rectangulares 2.40m
(20, false, true, 8, 9),    -- 20 Sillas Ejecutivas
(1, false, true, 8, 10);    -- 1 Podio

-- Montaje 9: Business - Escuela (ID:9)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(10, false, true, 9, 2),    -- 10 Mesas Rectangulares 1.80m
(25, false, true, 9, 8),    -- 25 Sillas Pala
(2, false, true, 9, 16);    -- 2 Rotafolios

-- Montaje 10: Business - Imperial (ID:10)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(1, false, true, 10, 18),   -- 1 Mesa Presidencial 3m
(15, false, true, 10, 9),   -- 15 Sillas Ejecutivas
(1, false, true, 10, 11);   -- 1 Atril

-- Montaje 11: Business - Boardroom (ID:11)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(1, false, true, 11, 18),   -- 1 Mesa Presidencial
(12, false, true, 11, 9),   -- 12 Sillas Ejecutivas
ON CONFLICT DO NOTHING;


-- ========================================
-- 7. RESERVACIONES (7 total)
-- ========================================

-- ========================================
-- 7.1 RESERVACIONES DEL CLIENTE 1 (Corp. Industrial) - 3 reservaciones
-- ========================================

-- Reservación 1: Conferencia Corporativa
-- Fecha de creación/pago1: 2026-03-10
-- Fecha de evento: 2026-03-25
-- Fecha de pago2: 2026-03-26
INSERT INTO reservacion (
    "nombreEvento", "descripEvento", "estimaAsistentes", 
    "fechaReservacion", "fechaEvento", "horaInicio", "horaFin", 
    subtotal, "IVA", total,
    cliente_id, montaje_id, estado_reserva_id, tipo_evento_id, trabajador_id, 
    es_paquete, nombre_paquete,
    checklist_coordinador, checklist_almacenista, progreso_checklist
) VALUES (
    'Conferencia Anual de Resultados',
    'Presentación de resultados anuales del corporativo con sesión de preguntas y respuestas para accionistas',
    80, 
    '2026-03-10', '2026-03-25', '09:00:00', '17:00:00',
    45000.00, 7200.00, 52200.00,
    1, 9, 'PAGAD', 5, 2,  -- Salón Business, Recepcionista Carlos
    false, '',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": true}',
    100.0
);

-- Reservación 2: Junta Directiva
-- Fecha de creación/pago1: 2026-03-20
-- Fecha de evento: 2026-04-05
-- Fecha de pago2: 2026-04-06
INSERT INTO reservacion (
    "nombreEvento", "descripEvento", "estimaAsistentes", 
    "fechaReservacion", "fechaEvento", "horaInicio", "horaFin", 
    subtotal, "IVA", total,
    cliente_id, montaje_id, estado_reserva_id, tipo_evento_id, trabajador_id, 
    es_paquete, nombre_paquete,
    checklist_coordinador, checklist_almacenista, progreso_checklist
) VALUES (
    'Junta Directiva Trimestral',
    'Reunión de la junta directiva para revisión de estrategia y objetivos del próximo trimestre',
    20, 
    '2026-03-20', '2026-04-05', '10:00:00', '14:00:00',
    18000.00, 2880.00, 20880.00,
    1, 11, 'CON', 5, 2,  -- Salón Boardroom
    false, '',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": true}',
    80.0
);

-- Reservación 3: Seminario de Innovación
-- Fecha de creación/pago1: 2026-04-01
-- Fecha de evento: 2026-04-20
-- Fecha de pago2: pendiente
INSERT INTO reservacion (
    "nombreEvento", "descripEvento", "estimaAsistentes", 
    "fechaReservacion", "fechaEvento", "horaInicio", "horaFin", 
    subtotal, "IVA", total,
    cliente_id, montaje_id, estado_reserva_id, tipo_evento_id, trabajador_id, 
    es_paquete, nombre_paquete,
    checklist_coordinador, checklist_almacenista, progreso_checklist
) VALUES (
    'Seminario de Innovación Tecnológica',
    'Seminario sobre nuevas tecnologías y transformación digital en la industria manufacturera',
    50, 
    '2026-04-01', '2026-04-20', '09:00:00', '18:00:00',
    32000.00, 5120.00, 37120.00,
    1, 6, 'PEN', 7, 2,  -- Salón Imperial - Escuela
    false, '',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": false}',
    '{"mobiliario": true, "equipamiento": false, "inventario": false}',
    60.0
);

-- ========================================
-- 7.2 RESERVACIONES DE OTROS CLIENTES - 4 reservaciones
-- ========================================

-- Reservación 4: Ana Martínez - Boda
-- Fecha de creación/pago1: 2026-03-15
-- Fecha de evento: 2026-04-18
-- Fecha de pago2: 2026-04-19
INSERT INTO reservacion (
    "nombreEvento", "descripEvento", "estimaAsistentes", 
    "fechaReservacion", "fechaEvento", "horaInicio", "horaFin", 
    subtotal, "IVA", total,
    cliente_id, montaje_id, estado_reserva_id, tipo_evento_id, trabajador_id, 
    es_paquete, nombre_paquete,
    checklist_coordinador, checklist_almacenista, progreso_checklist
) VALUES (
    'Boda Ana y Carlos',
    'Celebración de boda con 120 invitados, incluye banquete premium, decoración floral y pista de baile',
    120, 
    '2026-03-15', '2026-04-18', '18:00:00', '02:00:00',
    85000.00, 13600.00, 98600.00,
    2, 2, 'CON', 1, 2,  -- Gran Gala - Banquete
    true, 'Paquete Boda Premium',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true, "decoracion": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": true}',
    85.0
);

-- Reservación 5: Roberto Sánchez - XV Años
-- Fecha de creación/pago1: 2026-04-02
-- Fecha de evento: 2026-04-25
-- Fecha de pago2: pendiente
INSERT INTO reservacion (
    "nombreEvento", "descripEvento", "estimaAsistentes", 
    "fechaReservacion", "fechaEvento", "horaInicio", "horaFin", 
    subtotal, "IVA", total,
    cliente_id, montaje_id, estado_reserva_id, tipo_evento_id, trabajador_id, 
    es_paquete, nombre_paquete,
    checklist_coordinador, checklist_almacenista, progreso_checklist
) VALUES (
    'XV Años de Sofía',
    'Celebración de XV años con tema de princesa, incluye banquete, DJ, iluminación ambiental y fotografía profesional',
    90, 
    '2026-04-02', '2026-04-25', '19:00:00', '01:00:00',
    62000.00, 9920.00, 71920.00,
    3, 7, 'PEN', 2, 2,  -- Salón Real - Banquete
    true, 'Paquete XV Años',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true, "decoracion": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": false}',
    70.0
);

-- Reservación 6: Events Planner - Gala Corporativa
-- Fecha de creación/pago1: 2026-04-05
-- Fecha de evento: 2026-04-28
-- Fecha de pago2: pendiente
INSERT INTO reservacion (
    "nombreEvento", "descripEvento", "estimaAsistentes", 
    "fechaReservacion", "fechaEvento", "horaInicio", "horaFin", 
    subtotal, "IVA", total,
    cliente_id, montaje_id, estado_reserva_id, tipo_evento_id, trabajador_id, 
    es_paquete, nombre_paquete,
    checklist_coordinador, checklist_almacenista, progreso_checklist
) VALUES (
    'Gala de Premios Corporativos 2026',
    'Cena de gala para entrega de premios anuales a empleados destacados, incluye banquetes de 5 tiempos y entretenimiento',
    150, 
    '2026-04-05', '2026-04-28', '20:00:00', '01:00:00',
    125000.00, 20000.00, 145000.00,
    4, 5, 'CON', 10, 2,  -- Imperial - Banquete
    true, 'Paquete Gala Premium',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true, "decoracion": true, "seguridad": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": true}',
    90.0
);

-- Reservación 7: Fiestas Deluxe - Aniversario
-- Fecha de creación/pago1: 2026-04-10
-- Fecha de evento: 2026-05-05
-- Fecha de pago2: pendiente
INSERT INTO reservacion (
    "nombreEvento", "descripEvento", "estimaAsistentes", 
    "fechaReservacion", "fechaEvento", "horaInicio", "horaFin", 
    subtotal, "IVA", total,
    cliente_id, montaje_id, estado_reserva_id, tipo_evento_id, trabajador_id, 
    es_paquete, nombre_paquete,
    checklist_coordinador, checklist_almacenista, progreso_checklist
) VALUES (
    'Aniversario 25 años Empresa',
    'Celebración del 25 aniversario de la empresa con evento social para empleados y sus familias',
    100, 
    '2026-04-10', '2026-05-05', '17:00:00', '23:00:00',
    55000.00, 8800.00, 63800.00,
    5, 3, 'PEN', 9, 5,  -- Gran Gala - Cóctel
    true, 'Paquete Aniversario',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true, "decoracion": true}',
    '{"mobiliario": true, "equipamiento": false, "inventario": false}',
    50.0
);


-- ========================================
-- 8. REGISTRO DE ESTADOS DE RESERVACIÓN
-- ========================================
INSERT INTO registr_esta_reserva (fecha, reservacion_id, estado_reserva_id) VALUES 
-- Reservación 1
('2026-03-10', 1, 'PEN'),  -- Pendiente
('2026-03-25', 1, 'CON'),  -- Confirmada
('2026-03-26', 1, 'PAGAD'), -- Pagada
-- Reservación 2
('2026-03-20', 2, 'PEN'),
('2026-04-05', 2, 'CON'),
-- Reservación 3
('2026-04-01', 3, 'PEN'),
-- Reservación 4
('2026-03-15', 4, 'PEN'),
('2026-04-18', 4, 'CON'),
-- Reservación 5
('2026-04-02', 5, 'PEN'),
-- Reservación 6
('2026-04-05', 6, 'PEN'),
('2026-04-10', 6, 'CON'),
-- Reservación 7
('2026-04-10', 7, 'PEN')
ON CONFLICT DO NOTHING;


-- ========================================
-- 9. SERVICIOS POR RESERVACIÓN
-- ========================================
INSERT INTO reserva_servicio (extra, reservacion_id, servicio_id) VALUES 
-- Reservación 1: Conferencia (80 pax, Business Escuela)
(false, 1, 1),   -- Coffee Break
(false, 1, 3),   -- Coordinador
(false, 1, 4),   -- WiFi Premium
(false, 1, 18),  -- Proyector
(false, 1, 19),  -- Sistema Audio

-- Reservación 2: Junta Directiva (20 pax, Boardroom)
(false, 2, 1),   -- Coffee Break
(false, 2, 6),   -- Videoconferencia
(false, 2, 4),   -- WiFi Premium

-- Reservación 3: Seminario (50 pax, Imperial Escuela)
(false, 3, 1),   -- Coffee Break
(false, 3, 2),   -- Lunch Box
(false, 3, 4),   -- WiFi Premium
(false, 3, 18),  -- Proyector
(false, 3, 19),  -- Sistema Audio
(false, 3, 15),  -- Fotografía

-- Reservación 4: Boda (120 pax, Gran Gala Banquete)
(false, 4, 8),   -- Banquete Premium
(false, 4, 10),  -- Barra de Bebidas
(false, 4, 11),  -- Decoración Floral
(false, 4, 12),  -- Iluminación LED
(false, 4, 13),  -- Centro de Mesa
(false, 4, 16),  -- Video y Edición
(false, 4, 17),  -- DJ

-- Reservación 5: XV Años (90 pax, Real Banquete)
(false, 5, 9),   -- Cena de Gala
(false, 5, 10),  -- Barra de Bebidas
(false, 5, 11),  -- Decoración Floral
(false, 5, 12),  -- Iluminación LED
(false, 5, 17),  -- DJ
(false, 5, 15),  -- Fotografía

-- Reservación 6: Gala (150 pax, Imperial Banquete)
(false, 6, 9),   -- Cena de Gala
(false, 6, 10),  -- Barra de Bebidas
(false, 6, 11),  -- Decoración Floral
(false, 6, 12),  -- Iluminación LED
(false, 6, 13),  -- Centro de Mesa
(false, 6, 15),  -- Fotografía
(false, 6, 16),  -- Video y Edición
(false, 6, 21),  -- Limpieza

-- Reservación 7: Aniversario (100 pax, Gran Gala Cóctel)
(false, 7, 1),   -- Coffee Break
(false, 7, 4),   -- Buffet Ejecutivo
(false, 7, 10),  -- Barra de Bebidas
(false, 7, 17),  -- DJ
(false, 7, 15),  -- Fotografía
ON CONFLICT DO NOTHING;


-- ========================================
-- 10. EQUIPAMIENTO POR RESERVACIÓN
-- ========================================
INSERT INTO reserva_equipa (cantidad, extra, completado, reservacion_id, equipamiento_id) VALUES 
-- Reservación 1: Conferencia
(2, false, true, 1, 5),    -- 2 Proyectores 4K
(2, false, true, 1, 6),    -- 2 Pantallas 120"
(1, false, true, 1, 9),    -- 1 Laptop Presentación

-- Reservación 2: Junta Directiva
(1, false, true, 2, 7),    -- 1 Pantalla LED 90"
(1, false, true, 2, 3),    -- 1 Consola Audio

-- Reservación 3: Seminario
(3, false, true, 3, 5),    -- 3 Proyectores 4K
(3, false, true, 3, 6),    -- 3 Pantallas 120"
(2, false, true, 3, 9),    -- 2 Laptops
(1, false, true, 3, 15),   -- 1 Pizarrón Digital

-- Reservación 4: Boda
(2, false, true, 4, 10),   -- 2 Kits Iluminación LED
(2, false, true, 4, 2),    -- 2 Sistemas Audio Portátil
(1, false, true, 4, 8),    -- 1 Cámara Video

-- Reservación 5: XV Años
(1, false, true, 5, 10),   -- 1 Kit Iluminación LED
(1, false, true, 5, 2),    -- 1 Sistema Audio Portátil
(1, false, true, 5, 1),    -- 1 Micrófono Inalámbrico

-- Reservación 6: Gala
(3, false, true, 6, 10),   -- 3 Kits Iluminación LED
(2, false, true, 6, 3),    -- 2 Consolas Audio
(1, false, true, 6, 8),    -- 1 Cámara Video
(1, false, true, 6, 12),   -- 1 Controlador Luces

-- Reservación 7: Aniversario
(1, false, true, 7, 10),   -- 1 Kit Iluminación LED
(1, false, true, 7, 2),    -- 1 Sistema Audio Portátil
(1, false, true, 7, 21),   -- 1 Máquina de Café
ON CONFLICT DO NOTHING;


-- ========================================
-- 11. PAGOS
-- ========================================

-- ========================================
-- 11.1 PAGOS DE CLIENTE 1 (Corp. Industrial)
-- ========================================

-- Reservación 1: Conferencia - Primer Pago (creación: 2026-03-10)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 26100.00, 26100.00, '2026-03-10', '10:30:00', 1, 1, 'ABON', 'TARJ');

-- Reservación 1: Segundo Pago (después del evento: 2026-03-26)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Liquidación - 50% restante', 26100.00, 0.00, '2026-03-26', '14:00:00', 2, 1, 'LIQ', 'TARJ');

-- Reservación 2: Junta Directiva - Primer Pago (creación: 2026-03-20)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 10440.00, 10440.00, '2026-03-20', '09:15:00', 1, 2, 'ABON', 'TRANS');

-- Reservación 2: Segundo Pago (después del evento: 2026-04-06)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Liquidación - 50% restante', 10440.00, 0.00, '2026-04-06', '16:30:00', 2, 2, 'LIQ', 'TRANS');

-- Reservación 3: Seminario - Primer Pago (creación: 2026-04-01)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 18560.00, 18560.00, '2026-04-01', '11:00:00', 1, 3, 'ABON', 'TARJ');

-- ========================================
-- 11.2 PAGOS DE OTROS CLIENTES
-- ========================================

-- Reservación 4: Boda - Primer Pago (creación: 2026-03-15)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 49300.00, 49300.00, '2026-03-15', '14:00:00', 1, 4, 'ABON', 'TARJ');

-- Reservación 4: Segundo Pago (después del evento: 2026-04-19)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Liquidación - 50% restante', 49300.00, 0.00, '2026-04-19', '10:00:00', 2, 4, 'LIQ', 'TARJ');

-- Reservación 5: XV Años - Primer Pago (creación: 2026-04-02)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 35960.00, 35960.00, '2026-04-02', '16:00:00', 1, 5, 'ABON', 'EFEC');

-- Reservación 6: Gala - Primer Pago (creación: 2026-04-05)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 72500.00, 72500.00, '2026-04-05', '11:30:00', 1, 6, 'ABON', 'TARJ');

-- Reservación 6: Segundo Pago (después del evento: 2026-04-29)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Liquidación - 50% restante', 72500.00, 0.00, '2026-04-29', '09:00:00', 2, 6, 'LIQ', 'TRANS');

-- Reservación 7: Aniversario - Primer Pago (creación: 2026-04-10)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 31900.00, 31900.00, '2026-04-10', '15:00:00', 1, 7, 'ABON', 'TRANS');

COMMIT;

-- ========================================
-- RESUMEN DE DATOS INGRESADOS
-- ========================================
-- 
-- CATÁLOGOS Y ESTADOS:
--   ✅ Roles: 4
--   ✅ Estados de cuenta: 3
--   ✅ Tipos de cliente: 4
--   ✅ Estados de mobiliario: 4
--   ✅ Características de mobiliario: 10
--   ✅ Tipos de mobiliario: 8
--   ✅ Tipos de montaje: 10
--   ✅ Tipos de evento: 11
--   ✅ Estados de reservación: 9
--   ✅ Estados de salón: 5
--   ✅ Tipos de equipamiento: 8
--   ✅ Estados de equipamiento: 5
--   ✅ Conceptos de pago: 5
--   ✅ Métodos de pago: 5
--   ✅ Tipos de servicio: 10
--
-- CUENTAS Y USUARIOS:
--   ✅ Cuentas: 10 (5 trabajadores, 5 clientes)
--   ✅ Trabajadores: 5
--   ✅ Datos de clientes: 5
--
-- SERVICIOS Y EQUIPAMIENTO:
--   ✅ Servicios: 21 (cubren todos los tipos)
--   ✅ Equipamiento: 21 (8 categorías)
--   ✅ Mobiliario: 19 (8 tipos)
--
-- INVENTARIOS:
--   ✅ Inventario mobiliario: 19 registros
--   ✅ Inventario equipamiento: 21 registros
--
-- SALONES Y MONTAJES:
--   ✅ Salones: 11 (varios tamaños)
--   ✅ Montajes: 11 (diferentes tipos por salón)
--   ✅ Mobiliario por montaje: ~30 registros
--
-- RESERVACIONES (7 total):
--   ✅ Cliente 1 (Corp. Industrial): 3 reservaciones
--      - Conferencia Anual (PAGADA)
--      - Junta Directiva (CONFIRMADA)
--      - Seminario Innovación (PENDIENTE)
--   ✅ Cliente 2 (Ana Martínez): 1 reservación
--      - Boda (CONFIRMADA)
--   ✅ Cliente 3 (Roberto Sánchez): 1 reservación
--      - XV Años (PENDIENTE)
--   ✅ Cliente 4 (Events Planner): 1 reservación
--      - Gala Corporativa (CONFIRMADA)
--   ✅ Cliente 5 (Fiestas Deluxe): 1 reservación
--      - Aniversario (PENDIENTE)
--
-- PAGOS:
--   ✅ 12 pagos registrados
--   ✅ 5 reservaciones con pago completo
--   ✅ 2 reservaciones pendientes de segundo pago
--
-- SERVICIOS POR RESERVACIÓN: 30 registros
-- EQUIPAMIENTO POR RESERVACIÓN: 21 registros
-- ESTADOS DE RESERVACIÓN: 11 registros
-- ESTADOS DE SALÓN: 11 registros
-- ========================================
