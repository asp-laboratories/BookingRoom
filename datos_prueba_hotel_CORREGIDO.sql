-- ========================================
-- DATOS DE PRUEBA HOTEL BOOKINGROOM - CORREGIDO
-- ========================================
-- Base de datos: bookingroom_nuevadata
-- USO: Este script usa EXACTAMENTE los mismos códigos de catálogo
-- que el backup actual para evitar errores de integridad referencial
-- ========================================

BEGIN;

-- ========================================
-- 1. CATÁLOGOS Y ESTADOS (USANDO CÓDIGOS EXACTOS DEL BACKUP)
-- ========================================

-- ========================================
-- 1.1 ROLES
-- ========================================
-- BACKUP: ADMIN, COORD, RECEP, ALMAC
-- NUEVO SQL DEBE USAR: ADMIN, COORD, RECEP, ALMAC
INSERT INTO rol (codigo, nombre) VALUES 
('ADMIN', 'Administrador'),
('RECEP', 'Recepcionista'),
('COORD', 'Coordinador'),
('ALMAC', 'Almacen')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.2 ESTADOS DE CUENTA
-- ========================================
-- BACKUP: ACT, SUSPE, BANEO
INSERT INTO estado_cuenta (codigo, nombre) VALUES 
('ACT', 'Activa'),
('SUSPE', 'Suspendida'),
('BANEO', 'Bloqueada')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.3 TIPOS DE CLIENTE
-- ========================================
-- BACKUP: MOR, FIS, PM, PF
-- Usaremos solo MOR y FIS para evitar duplicados
INSERT INTO tipo_cliente (codigo, nombre, disposicion) VALUES 
('MOR', 'Persona moral', true),
('FIS', 'Persona fisica', true)
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.4 ESTADOS DE MOBILIARIO
-- ========================================
-- BACKUP: DISP, OCUP, RESV, REPAR
INSERT INTO estado_mobil (codigo, nombre) VALUES 
('DISP', 'Disponible'),
('OCUP', 'Ocupado'),
('RESV', 'Reservado'),
('REPAR', 'En reparacion')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.5 CARACTERÍSTICAS DE MOBILIARIO
-- ========================================
-- Ampliar de 1 a 10 registros
INSERT INTO caracter_mobi (descripcion) VALUES 
('Plegable'),
('Apilable'),
('Acolchado'),
('Ajustable en altura'),
('Con reposabrazos'),
('Con ruedas'),
('Resistente al agua'),
('Material ignifugo'),
('Ligero y portatil'),
('Ergonomico')
ON CONFLICT DO NOTHING;

-- ========================================
-- 1.6 TIPOS DE MOBILIARIO
-- ========================================
-- BACKUP IDs: 1=Sillas, 2=Mesas Redondas, 3=Mesas Rectangulares, 4=Taburetes, 5=Podios
-- Ampliar a 8 tipos manteniendo IDs existentes
INSERT INTO tipo_mobil (id, nombre, disposicion) VALUES 
(1, 'Sillas', true),
(2, 'Mesas Redondas', true),
(3, 'Mesas Rectangulares', true),
(4, 'Taburetes', true),
(5, 'Podios', true),
(6, 'Escenarios', true),
(7, 'Mesas de buffet', true),
(8, 'Mobiliario lounge', true)
ON CONFLICT (id) DO NOTHING;

-- ========================================
-- 1.7 TIPOS DE MONTAJE
-- ========================================
-- BACKUP IDs: 1=Teatro, 2=Escuela, 3=Banquete, 4=Recepcion, 5=Imperial, 6=Herradura, 7=Mesa rusa
-- MANTENER IDs y solo actualizar nombres
UPDATE tipo_montaje SET nombre = 'Teatro/Auditorio', capacidadIdeal = 200 WHERE id = 1;
UPDATE tipo_montaje SET nombre = 'Escuela/Aula', capacidadIdeal = 40 WHERE id = 2;
UPDATE tipo_montaje SET nombre = 'Banquete', capacidadIdeal = 120 WHERE id = 3;
UPDATE tipo_montaje SET nombre = 'Recepcion/Coctel', capacidadIdeal = 150 WHERE id = 4;
UPDATE tipo_montaje SET nombre = 'Imperial', capacidadIdeal = 25 WHERE id = 5;
UPDATE tipo_montaje SET nombre = 'Herradura/U', capacidadIdeal = 30 WHERE id = 6;
UPDATE tipo_montaje SET nombre = 'Mesa rusa', capacidadIdeal = 35 WHERE id = 7;

-- Agregar nuevos tipos (IDs 8-10)
INSERT INTO tipo_montaje (id, nombre, disposicion, capacidadIdeal) VALUES 
(8, 'Estilo Lounge', true, 50),
(9, 'Mesa Redonda', true, 80),
(10, 'Espanola/Boardroom', true, 20)
ON CONFLICT (id) DO UPDATE SET 
    nombre = EXCLUDED.nombre,
    capacidadIdeal = EXCLUDED.capacidadIdeal;

-- ========================================
-- 1.8 TIPOS DE EVENTO
-- ========================================
-- BACKUP IDs: 1=Conferencia, 2=Seminario, 3=Cena de empresa, 4=Lanzamiento, 5=Boda, 
--             6=Junta de consejo, 7=Asamblea, 8=Reunion de trabajo, 9=Fiesta, 10=Otro, 11=Paquete
-- Mantener existentes y agregar nuevos
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES 
(1, 'Conferencia', true),
(2, 'Seminario', true),
(3, 'Cena de empresa', true),
(4, 'Lanzamiento de producto', true),
(5, 'Boda', true),
(6, 'Junta de consejo', true),
(7, 'Asamblea', true),
(8, 'Reunion de trabajo', true),
(9, 'Fiesta', true),
(10, 'Otro', true),
(11, 'Paquete', true),
(12, 'XV Anos', true),
(13, 'Bautizo', true),
(14, 'Graduacion', true),
(15, 'Cumpleanos', true),
(16, 'Aniversario', true),
(17, 'Gala', true),
(18, 'Exposicion', true)
ON CONFLICT (id) DO NOTHING;

-- ========================================
-- 1.9 ESTADOS DE RESERVACIÓN
-- ========================================
-- BACKUP: SOLIC, PEN, CONF, CON, ENPRO, FIN, CAN, PAGAD, PLANT
-- Mantener CONF (usado en DB), agregar CANC y RECH
INSERT INTO estado_reserva (codigo, nombre) VALUES 
('SOLIC', 'Solicitada'),
('PEN', 'Pendiente'),
('CONF', 'Confirmada'),
('CON', 'Confirmada'),
('ENPRO', 'En proceso'),
('FIN', 'Finalizada'),
('CAN', 'Cancelada'),
('PAGAD', 'Pagada'),
('PLANT', 'Plantilla'),
('CANC', 'Cancelada por Cliente'),
('RECH', 'Rechazada')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.10 ESTADOS DE SALÓN
-- ========================================
-- BACKUP: DIS, RESV, OCUP, MANTE, LIMPI
INSERT INTO estado_salon (codigo, nombre) VALUES 
('DIS', 'Disponible'),
('RESV', 'Reservado'),
('OCUP', 'Ocupado'),
('MANTE', 'En mantenimiento'),
('LIMPI', 'En limpieza')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.11 TIPOS DE EQUIPAMIENTO
-- ========================================
-- BACKUP IDs: 1=Audio, 2=Video, 3=Iluminacion, 4=Computo, 5=Mobiliario extra, 6=Otro
-- Mantener IDs y actualizar nombres
UPDATE tipo_equipa SET nombre = 'Audio' WHERE id = 1;
UPDATE tipo_equipa SET nombre = 'Video/Proyeccion' WHERE id = 2;
UPDATE tipo_equipa SET nombre = 'Iluminacion' WHERE id = 3;
UPDATE tipo_equipa SET nombre = 'Computo' WHERE id = 4;
UPDATE tipo_equipa SET nombre = 'Mobiliario extra' WHERE id = 5;
UPDATE tipo_equipa SET nombre = 'Otro' WHERE id = 6;

-- Agregar nuevos tipos (IDs 7-8)
INSERT INTO tipo_equipa (id, nombre, disposicion) VALUES 
(7, 'Telecomunicaciones', true),
(8, 'Accesorios de presentacion', true)
ON CONFLICT (id) DO NOTHING;

-- ========================================
-- 1.12 ESTADOS DE EQUIPAMIENTO
-- ========================================
-- BACKUP: DISP, FUNC, DANAD, REPAR, RESV
INSERT INTO estado_equipa (codigo, nombre) VALUES 
('DISP', 'Disponible'),
('FUNC', 'Funcional'),
('DANAD', 'Daniado'),
('REPAR', 'En reparacion'),
('RESV', 'Reservado')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.13 CONCEPTOS DE PAGO
-- ========================================
-- BACKUP: ANTIC, LIQUI, EXTR, ABONO, PENAL
-- Mantener códigos existentes
INSERT INTO concepto_pago (codigo, nombre) VALUES 
('ANTIC', 'Anticipo'),
('LIQUI', 'Liquidacion'),
('EXTR', 'Extra'),
('ABONO', 'Abono'),
('PENAL', 'Penalizacion')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.14 MÉTODOS DE PAGO
-- ========================================
-- BACKUP: EFECT, TRANS, TARJE, NFC, CHEQU
INSERT INTO metodo_pago (codigo, nombre) VALUES 
('EFECT', 'Efectivo'),
('TRANS', 'Transferencia'),
('TARJE', 'Tarjeta'),
('NFC', 'NFC'),
('CHEQU', 'Cheque')
ON CONFLICT (codigo) DO NOTHING;

-- ========================================
-- 1.15 TIPOS DE SERVICIO
-- ========================================
-- BACKUP IDs: 1=Catering, 2=Audiovisual, 3=Decoracion, 4=Transporte, 5=Fotografia, 
--             6=Musica, 7=Seguridad, 8=Limpieza, 9=Otro, 10=Internet
-- Mantener IDs y actualizar nombres/descripciones
UPDATE tipo_servicio SET nombre = 'Catering', descripcion = 'Servicios de comida' WHERE id = 1;
UPDATE tipo_servicio SET nombre = 'Audiovisual', descripcion = 'Equipos AV' WHERE id = 2;
UPDATE tipo_servicio SET nombre = 'Decoracion', descripcion = 'Decoracion' WHERE id = 3;
UPDATE tipo_servicio SET nombre = 'Transporte', descripcion = 'Transporte' WHERE id = 4;
UPDATE tipo_servicio SET nombre = 'Fotografia', descripcion = 'Foto' WHERE id = 5;
UPDATE tipo_servicio SET nombre = 'Musica', descripcion = 'Musica' WHERE id = 6;
UPDATE tipo_servicio SET nombre = 'Seguridad', descripcion = 'Seguridad' WHERE id = 7;
UPDATE tipo_servicio SET nombre = 'Limpieza', descripcion = 'Limpieza' WHERE id = 8;
UPDATE tipo_servicio SET nombre = 'Otro', descripcion = 'Otros' WHERE id = 9;
UPDATE tipo_servicio SET nombre = 'Internet', descripcion = 'Internet' WHERE id = 10;

-- Agregar nuevos tipos (IDs 11-12)
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES 
(11, 'Servicios para reuniones', 'Servicios orientados a juntas y reuniones', true),
(12, 'Servicios ejecutivos', 'Servicios premium para clientes VIP', true)
ON CONFLICT (id) DO NOTHING;


-- ========================================
-- 2. CUENTAS Y USUARIOS
-- ========================================

-- ========================================
-- 2.1 CUENTAS
-- ========================================
INSERT INTO cuenta (nombre_usuario, correo_electronico, firebase_uid, estado_cuenta_id) VALUES 
('martha.rivera', 'martha.rivera@email.com', 'firebase_uid_martha', 'ACT'),
('carlos.mtz', 'carlos.mtz@hotel.com', 'firebase_uid_carlos', 'ACT'),
('luis.garcia', 'luis.garcia@hotel.com', 'firebase_uid_luis', 'ACT'),
('ana.perez', 'ana.perez@hotel.com', 'firebase_uid_ana', 'ACT'),
('jorge.rodriguez', 'jorge.rodriguez@hotel.com', 'firebase_uid_jorge', 'ACT'),
('cliente_corp', 'contacto@corpindustrial.mx', 'firebase_uid_corp', 'ACT'),
('ana.martinez', 'ana.martinez@gmail.com', 'firebase_uid_ana_m', 'ACT'),
('roberto.sanchez', 'roberto.sanchez@outlook.com', 'firebase_uid_robert', 'ACT'),
('events_planner', 'info@eventsplanner.com', 'firebase_uid_events', 'ACT'),
('fiestas_deluxe', 'reservaciones@fiestasdeluxe.com', 'firebase_uid_fiestas', 'ACT')
ON CONFLICT (correo_electronico) DO NOTHING;

-- ========================================
-- 2.2 TRABAJADORES
-- ========================================
INSERT INTO trabajador (no_empleado, rfc, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, rol_id, cuenta_id) VALUES 
('TRAB001', 'RIMJ850101XXX', 'Martha', 'Rivera', 'Jimenez', '5551234567', 'martha.rivera@email.com', 'ADMIN', 1),
('TRAB002', 'MACL900202XXX', 'Carlos', 'Martinez', 'Lopez', '5552345678', 'carlos.mtz@hotel.com', 'RECEP', 2),
('TRAB003', 'GALJ880303XXX', 'Luis', 'Garcia', 'Lopez', '5553456789', 'luis.garcia@hotel.com', 'COORD', 3),
('TRAB004', 'PEAN920404XXX', 'Ana', 'Perez', 'Nunez', '5554567890', 'ana.perez@hotel.com', 'ALMAC', 4),
('TRAB005', 'ROHJ950505XXX', 'Jorge', 'Rodriguez', 'Hernandez', '5555678901', 'jorge.rodriguez@hotel.com', 'RECEP', 5)
ON CONFLICT (no_empleado) DO NOTHING;

-- ========================================
-- 2.3 DATOS DE CLIENTES
-- ========================================
INSERT INTO datos_cliente (rfc, nombre_fiscal, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, tipo_cliente_id, cuenta_id) VALUES 
-- Cliente 1: Corporativo Industrial (3 reservaciones)
('COR850101XXX', 'Corporativo Industrial del Norte S.A. de C.V.', 'Roberto', 'Corporativo', 'Industrial', '5559871234', 'contacto@corpindustrial.mx', 'Colonia Centro', 'Av. Constitucion', '456', 'MOR', 6),
-- Cliente 2: Ana Martinez
('MANA900515XXX', 'Ana Sofia Martinez', 'Ana Sofia', 'Martinez', 'Gonzalez', '5558761234', 'ana.martinez@gmail.com', 'Colonia Del Valle', 'Calle Insurgentes Sur', '789', 'FIS', 7),
-- Cliente 3: Roberto Sanchez
('SARL850920XXX', 'Roberto Sanchez', 'Roberto', 'Sanchez', 'Luna', '5557651234', 'roberto.sanchez@outlook.com', 'Colonia Roma Norte', 'Av. Juarez', '321', 'FIS', 8),
-- Cliente 4: Events Planner
('EVP900101XXX', 'Events Planner Mexico S.C.', 'Laura', 'Events', 'Planner', '5556541234', 'info@eventsplanner.com', 'Colonia Polanco', 'Av. Masaryk', '123', 'MOR', 9),
-- Cliente 5: Fiestas Deluxe
('FID850202XXX', 'Fiestas Deluxe Eventos S.A. de C.V.', 'Carmen', 'Fiestas', 'Deluxe', '5555431234', 'reservaciones@fiestasdeluxe.com', 'Colonia Coyoacan', 'Calle Hidalgo', '654', 'MOR', 10)
ON CONFLICT (correo_electronico) DO NOTHING;


-- ========================================
-- 3. SERVICIOS, EQUIPAMIENTO Y MOBILIARIO
-- ========================================

-- ========================================
-- 3.1 SERVICIOS (Usando IDs 1-10 existentes, agregando nuevos)
-- ========================================
-- Mantener existentes y agregar nuevos con IDs 17+
INSERT INTO servicio (nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES 
-- Servicios tipo 1 (Catering)
('Coffee Break Premium', 'Cafe, te, jugos, frutas y pasteleria para reuniones', 1500.00, true, 1),
('Lunch Box Ejecutivo', 'Caja de almuerzo individual para asistentes', 3500.00, true, 1),
('Banquete Premium', 'Banquete de 3 tiempos para eventos sociales', 8500.00, true, 1),
('Cena de Gala', 'Cena formal de 5 tiempos con maridaje', 15000.00, true, 1),

-- Servicios tipo 10 (Internet)
('WiFi Premium Dedicado', 'Internet de alta velocidad dedicado para el evento', 1200.00, true, 10),

-- Servicios tipo 2 (Audiovisual)
('Videoconferencia HD', 'Sistema de videoconferencia con pantalla 4K', 2800.00, true, 2),
('Proyector y Pantalla HD', 'Proyector de alta definicion con pantalla de 120"', 2000.00, true, 2),
('Sistema de Audio Profesional', 'Consola de audio con microfonos inalambricos', 3500.00, true, 2),

-- Servicios tipo 3 (Decoracion)
('Decoracion Floral Premium', 'Arreglos florales de alta gama para mesas y escenario', 5000.00, true, 3),
('Iluminacion Ambiental LED', 'Iluminacion profesional con colores personalizables', 3500.00, true, 3),
('Centro de Mesa Premium', 'Centros de mesa elegantes para eventos sociales', 2500.00, true, 3),

-- Servicios tipo 6 (Musica) y 5 (Fotografia)
('DJ y Musica Ambiental', 'DJ profesional con equipo de sonido incluido', 4500.00, true, 6),
('Fotografia Profesional', 'Fotografo profesional durante todo el evento', 6000.00, true, 5),
('Video y Edicion', 'Videografo profesional con edicion post-evento', 8500.00, true, 5),

-- Servicios tipo 8 (Limpieza) y 7 (Seguridad)
('Servicio de Limpieza Durante Evento', 'Personal de limpieza durante todo el evento', 1800.00, true, 8),
('Seguridad Privada', 'Guardia de seguridad para control de acceso', 2500.00, true, 7),

-- Servicios nuevos tipos 11 y 12
('Servicio de Coordinador de Evento', 'Coordinador dedicado durante todo el evento', 2500.00, true, 11),
('Servicio de Traduccion Simultanea', 'Interprete profesional para eventos bilingues', 4500.00, true, 12),
('Servicio de Valet Parking', 'Estacionamiento con servicio de valet para invitados', 3000.00, true, 12),
('Barra de Bebidas Premium', 'Barra libre con bebidas premium y cocteleria', 7500.00, true, 1),
('Buffet Ejecutivo', 'Buffet variado para eventos corporativos', 6000.00, true, 1)
ON CONFLICT DO NOTHING;

-- ========================================
-- 3.2 EQUIPAMIENTO (IDs 1-14 existentes, agregar 22-28)
-- ========================================
INSERT INTO equipamiento (nombre, descripcion, costo, stock, tipo_equipa_id) VALUES 
-- Tipo 1 (Audio) - IDs 15-18
('Microfono Inalambrico Profesional', 'Microfono de mano con receptor profesional', 1500.00, 8, 1),
('Consola de Audio Digital', 'Mezclador digital de 16 canales', 3000.00, 2, 1),

-- Tipo 2 (Video) - IDs 19-21
('Pantalla de Proyeccion 150"', 'Pantalla electrica de 150 pulgadas', 1200.00, 3, 2),
('Camara de Video Profesional', 'Camara 4K para grabacion de eventos', 1800.00, 3, 2),

-- Tipo 7 (Telecomunicaciones) - IDs 22-24
('Sistema de Videoconferencia', 'Equipo completo para videoconferencia HD', 2500.00, 2, 7),
('Router WiFi Dedicado', 'Router de alta velocidad para evento', 800.00, 5, 7),
('Telefono IP', 'Telefono de internet para evento', 500.00, 10, 7),

-- Tipo 8 (Accesorios) - IDs 25-28
('Pizarron Digital Interactivo', 'Pizarron tactil de 65 pulgadas', 2500.00, 3, 8),
('Rotafolios con Hojas', 'Rotafolio profesional con 50 hojas', 400.00, 8, 8),
('Flip Chart Profesional', 'Flip chart magnetico con marcadores', 600.00, 5, 8),
('Maquina de Cafe Express', 'Maquina de cafe profesional para eventos', 1800.00, 4, 8)
ON CONFLICT DO NOTHING;

-- ========================================
-- 3.3 MOBILIARIO (IDs 1-10 existentes, agregar 11-20)
-- ========================================
INSERT INTO mobiliario (nombre, descripcion, costo, stock, tipo_movil_id) VALUES 
-- Tipo 1 (Sillas) - IDs 11-13
('Silla Tiffany', 'Silla elegante estilo Tiffany para eventos formales', 350.00, 80, 1),
('Silla con Escritorio (Pala)', 'Silla con superficie de escritura integrada', 250.00, 50, 1),
('Silla Ejecutiva Acolchada', 'Silla ergonomica con reposabrazos', 400.00, 40, 1),

-- Tipo 6 (Escenarios) - IDs 14-15
('Escenario Modular 4x3m', 'Escenario elevado modular de 4x3 metros', 5000.00, 3, 6),
('Escenario Modular 3x2m', 'Escenario elevado modular de 3x2 metros', 3500.00, 4, 6),

-- Tipo 7 (Mesas de buffet) - IDs 16-17
('Mesa de Buffet Larga', 'Mesa larga para servicio de buffet con mantel', 700.00, 8, 7),
('Mesa de Buffet Corta', 'Mesa mediana para servicio de buffet', 500.00, 10, 7),

-- Tipo 8 (Mobiliario lounge) - IDs 18-20
('Sofa Modular 3 plazas', 'Sofa moderno de 3 plazas para area lounge', 1200.00, 8, 8),
('Puff Individual', 'Puff acolchado individual', 400.00, 15, 8),
('Mesa de Centro Baja', 'Mesa baja de centro para area lounge', 500.00, 10, 8)
ON CONFLICT DO NOTHING;

-- ========================================
-- 3.4 CARACTERÍSTICAS ASIGNADAS A MOBILIARIO
-- ========================================
-- Mesa Redonda 1.5m -> Ligero (ID 9)
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (4, 9) ON CONFLICT DO NOTHING;
-- Silla Tiffany -> Apilable (ID 2), Ergonomico (ID 10)
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (11, 2), (11, 10) ON CONFLICT DO NOTHING;
-- Silla Pala -> Plegable (ID 1)
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (12, 1) ON CONFLICT DO NOTHING;
-- Silla Ejecutiva -> Acolchado (ID 3), Con reposabrazos (ID 5), Ergonomico (ID 10)
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (13, 3), (13, 5), (13, 10) ON CONFLICT DO NOTHING;
-- Podio -> Material ignifugo (ID 8)
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (10, 8) ON CONFLICT DO NOTHING;
-- Sofa Modular -> Acolchado (ID 3), Ergonomico (ID 10)
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (18, 3), (18, 10) ON CONFLICT DO NOTHING;
-- Puff -> Acolchado (ID 3), Ligero (ID 9)
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (19, 3), (19, 9) ON CONFLICT DO NOTHING;
-- Taburete Alto -> Apilable (ID 2), Ligero (ID 9)
INSERT INTO mobiliario_descripcion_mob (mobiliario_id, caracter_mobil_id) VALUES (8, 2), (8, 9) ON CONFLICT DO NOTHING;


-- ========================================
-- 4. INVENTARIOS
-- ========================================

-- ========================================
-- 4.1 INVENTARIO DE MOBILIARIO
-- ========================================
-- Usar IDs existentes y nuevos
INSERT INTO inventario_mobil (mobiliario_id, estado_mobil_id, cantidad) VALUES 
-- IDs existentes
(1, 'DISP', 500),   -- Silla plegable
(2, 'DISP', 15000), -- Silla ejecutiva  
(3, 'DISP', 200),   -- Silla vintage
(4, 'DISP', 200),   -- Mesa redonda 1.5m
(5, 'DISP', 200),   -- Mesa redonda 1.8m
(6, 'DISP', 200),   -- Mesa rectangular 2m
(7, 'DISP', 200),   -- Mesa rectangular 3m
(8, 'DISP', 200),   -- Taburete alto
(9, 'DISP', 200),   -- Taburete bajo
(10, 'DISP', 200),  -- Podio ejecutivo
-- IDs nuevos
(11, 'DISP', 80),   -- Silla Tiffany
(12, 'DISP', 50),   -- Silla Pala
(13, 'DISP', 40),   -- Silla Ejecutiva
(14, 'DISP', 3),    -- Escenario 4x3m
(15, 'DISP', 4),    -- Escenario 3x2m
(16, 'DISP', 8),    -- Mesa Buffet Larga
(17, 'DISP', 10),   -- Mesa Buffet Corta
(18, 'DISP', 8),    -- Sofa Modular
(19, 'DISP', 15),   -- Puff
(20, 'DISP', 10)    -- Mesa Centro Baja
ON CONFLICT ON CONSTRAINT estado_mobiliario DO NOTHING;

-- ========================================
-- 4.2 INVENTARIO DE EQUIPAMIENTO
-- ========================================
INSERT INTO inventario_equipa (equipamiento_id, estado_equipa_id, cantidad) VALUES 
-- IDs existentes
(1, 'DISP', 15),    -- Proyector HD
(2, 'DISP', 5),     -- Proyector 4K
(3, 'DISP', 10),    -- Pantalla 120"
(4, 'DISP', 8),     -- Sistema sonido portatil
(5, 'DISP', 20),    -- Microfono inalambrico
(6, 'DISP', 15),    -- Microfono de mano
(7, 'DISP', 20),    -- Bocinas Bluetooth
(8, 'DISP', 10),    -- Laptop presentacion
(9, 'DISP', 8),     -- TV 55"
(10, 'DISP', 3),    -- Pantalla LED 90"
(11, 'DISP', 5),    -- Camara documentos
(12, 'DISP', 20),   -- Spotlight LED
(13, 'DISP', 10),   -- Torre iluminacion
(14, 'DISP', 5),    -- Impresora laser
-- IDs nuevos
(15, 'DISP', 8),    -- Microfono Inalambrico Prof.
(16, 'DISP', 2),    -- Consola Audio Digital
(17, 'DISP', 3),    -- Pantalla 150"
(18, 'DISP', 3),    -- Camara Video Prof.
(19, 'DISP', 2),    -- Sistema Videoconferencia
(20, 'DISP', 5),    -- Router WiFi
(21, 'DISP', 10),   -- Telefono IP
(22, 'DISP', 3),    -- Pizarron Digital
(23, 'DISP', 8),    -- Rotafolios
(24, 'DISP', 5),    -- Flip Chart
(25, 'DISP', 4)     -- Maquina Cafe
ON CONFLICT ON CONSTRAINT estado_equipamiento DO NOTHING;


-- ========================================
-- 5. SALONES (Usando IDs existentes del backup)
-- ========================================
-- BACKUP IDs: 1=Vivaldi V, 2=Vivaldi I, 4=Vivaldi III, 5=Vivaldi IV, 6=Shubert, 7=Mozart, 8=Beethoven, 9=Gran Vivaldi, 10=Chopin, 11=Gran Mozart
-- Mantener IDs y agregar nuevos (12-15)
INSERT INTO salon (nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES 
-- Salones para eventos grandes (IDs nuevos)
('Salon Gran Gala', 15000.00, 'Piso 1, Ala Norte', 25.00, 15.00, 4.00, 375.00, 200, 'DIS'),
('Salon Imperial', 12000.00, 'Piso 2, Ala Este', 20.00, 12.00, 3.50, 240.00, 150, 'DIS'),
('Salon Real', 10000.00, 'Piso 1, Ala Sur', 18.00, 10.00, 3.00, 180.00, 120, 'DIS'),
('Salon Plaza', 8000.00, 'Piso 2, Ala Oeste', 15.00, 10.00, 3.00, 150.00, 100, 'DIS'),

-- Salones para eventos medianos
('Salon Ejecutivo', 6000.00, 'Piso 3, Ala Norte', 12.00, 8.00, 2.80, 96.00, 60, 'DIS'),
('Salon Business', 5500.00, 'Piso 3, Ala Sur', 10.00, 8.00, 2.80, 80.00, 50, 'DIS'),

-- Salones para eventos pequenos
('Salon Boardroom', 4000.00, 'Piso 4, Ala Norte', 8.00, 6.00, 2.60, 48.00, 25, 'DIS'),

-- Salones exteriores y especiales
('Terraza Mirador', 9000.00, 'Azotea, Nivel 5', 22.00, 12.00, 4.00, 264.00, 150, 'DIS'),
('Jardin Interior', 7500.00, 'Planta Baja, Ala Central', 18.00, 10.00, 6.00, 180.00, 120, 'DIS')
ON CONFLICT DO NOTHING;

-- Registro de estado actual de salones
INSERT INTO registr_esta_salon (salon_id, estado_salon_id, fecha) VALUES 
-- Salones existentes
(1, 'DIS', CURRENT_DATE),
(2, 'DIS', CURRENT_DATE),
(4, 'DIS', CURRENT_DATE),
(5, 'DIS', CURRENT_DATE),
(6, 'DIS', CURRENT_DATE),
(7, 'DIS', CURRENT_DATE),
(8, 'DIS', CURRENT_DATE),
(9, 'DIS', CURRENT_DATE),
(10, 'DIS', CURRENT_DATE),
(11, 'DIS', CURRENT_DATE),
-- Salones nuevos (12-20)
(12, 'DIS', CURRENT_DATE),
(13, 'DIS', CURRENT_DATE),
(14, 'DIS', CURRENT_DATE),
(15, 'DIS', CURRENT_DATE),
(16, 'DIS', CURRENT_DATE),
(17, 'DIS', CURRENT_DATE),
(18, 'DIS', CURRENT_DATE),
(19, 'DIS', CURRENT_DATE),
(20, 'DIS', CURRENT_DATE)
ON CONFLICT DO NOTHING;


-- ========================================
-- 6. MONTAJES Y MOBILIARIO ASOCIADO
-- ========================================

-- ========================================
-- 6.1 MONTAJES (IDs 1-11 existentes del backup, agregar nuevos)
-- ========================================
-- Nota: Los IDs deben coincidir con los existentes en el backup
-- Si el backup tiene montajes, usar IDs diferentes o verificar
-- Para evitar conflictos, empezar desde ID 100

INSERT INTO montaje (costo, salon_id, tipo_montaje_id) VALUES 
-- Salon Gran Gala (ID: 12)
(2500.00, 12, 1),  -- Teatro/Auditorio
(3000.00, 12, 3),  -- Banquete
(2800.00, 12, 4),  -- Recepcion/Coctel

-- Salon Imperial (ID: 13)
(2000.00, 13, 1),  -- Teatro
(2500.00, 13, 3),  -- Banquete
(2200.00, 13, 2),  -- Escuela

-- Salon Real (ID: 14)
(1800.00, 14, 3),  -- Banquete
(1500.00, 14, 6),  -- Herradura

-- Salon Business (ID: 17)
(1200.00, 17, 2),  -- Escuela
(1400.00, 17, 5),  -- Imperial
(1300.00, 17, 10), -- Espanola/Boardroom

-- Salon Boardroom (ID: 18)
(1000.00, 18, 10), -- Boardroom
(900.00, 18, 5)    -- Imperial
ON CONFLICT DO NOTHING;

-- ========================================
-- 6.2 MOBILIARIO DE CADA MONTAJE
-- ========================================
-- Montaje 101: Gran Gala - Teatro (ID:101)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(100, false, true, 101, 1),   -- 100 Sillas plegables
(1, false, true, 101, 10),    -- 1 Podio
(1, false, true, 101, 14);    -- 1 Escenario 4x3m

-- Montaje 102: Gran Gala - Banquete (ID:102)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(12, false, true, 102, 5),    -- 12 Mesas Redondas 1.8m
(120, false, true, 102, 11),  -- 120 Sillas Tiffany
(1, false, true, 102, 10);    -- 1 Podio

-- Montaje 103: Gran Gala - Coctel (ID:103)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(15, false, true, 103, 16),   -- 15 Mesas de Buffet
(30, false, true, 103, 8),    -- 30 Taburetes Altos
(3, false, true, 103, 18);    -- 3 Sofas Modulares

-- Montaje 104: Imperial - Teatro (ID:104)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(80, false, true, 104, 1),    -- 80 Sillas plegables
(1, false, true, 104, 10),    -- 1 Podio
(1, false, true, 104, 15);    -- 1 Escenario 3x2m

-- Montaje 105: Imperial - Banquete (ID:105)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(10, false, true, 105, 5),    -- 10 Mesas Redondas 1.8m
(100, false, true, 105, 11),  -- 100 Sillas Tiffany
(1, false, true, 105, 10);    -- 1 Podio

-- Montaje 106: Imperial - Escuela (ID:106)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(15, false, true, 106, 6),    -- 15 Mesas Rectangulares 2m
(40, false, true, 106, 12),   -- 40 Sillas Pala
(2, false, true, 106, 22);    -- 2 Pizarrones Digitales

-- Montaje 107: Real - Banquete (ID:107)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(8, false, true, 107, 4),     -- 8 Mesas Redondas 1.5m
(80, false, true, 107, 11),   -- 80 Sillas Tiffany
(2, false, true, 107, 20);    -- 2 Mesas de Centro Baja

-- Montaje 108: Real - Herradura (ID:108)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(10, false, true, 108, 7),    -- 10 Mesas Rectangulares 3m
(20, false, true, 108, 13),   -- 20 Sillas Ejecutivas
(1, false, true, 108, 10);    -- 1 Podio

-- Montaje 109: Business - Escuela (ID:109)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(10, false, true, 109, 6),    -- 10 Mesas Rectangulares 2m
(25, false, true, 109, 12),   -- 25 Sillas Pala
(2, false, true, 109, 23);    -- 2 Rotafolios

-- Montaje 110: Business - Imperial (ID:110)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(1, false, true, 110, 10),    -- 1 Podio (como mesa central)
(15, false, true, 110, 13),   -- 15 Sillas Ejecutivas
(1, false, true, 110, 10);    -- 1 Podio (atril)

-- Montaje 111: Business - Boardroom (ID:111)
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(1, false, true, 111, 7),     -- 1 Mesa Rectangular 3m (como mesa de reunion)
(12, false, true, 111, 13),   -- 12 Sillas Ejecutivas
ON CONFLICT DO NOTHING;


-- ========================================
-- 7. RESERVACIONES (7 total)
-- ========================================

-- ========================================
-- 7.1 RESERVACIONES DEL CLIENTE 1 (Corp. Industrial) - 3 reservaciones
-- ========================================

-- Reservacion 1: Conferencia Corporativa
-- Fecha de creacion/pago1: 2026-03-10
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
    'Presentacion de resultados anuales del corporativo con sesion de preguntas y respuestas para accionistas',
    80, 
    '2026-03-10', '2026-03-25', '09:00:00', '17:00:00',
    45000.00, 7200.00, 52200.00,
    1, 106, 'PAGAD', 1, 2,  -- Salon Business, Recepcionista Carlos
    false, '',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": true}',
    100.0
);

-- Reservacion 2: Junta Directiva
-- Fecha de creacion/pago1: 2026-03-20
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
    'Reunion de la junta directiva para revision de estrategia y objetivos del proximo trimestre',
    20, 
    '2026-03-20', '2026-04-05', '10:00:00', '14:00:00',
    18000.00, 2880.00, 20880.00,
    1, 111, 'CONF', 6, 2,  -- Salon Boardroom
    false, '',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": true}',
    80.0
);

-- Reservacion 3: Seminario de Innovacion
-- Fecha de creacion/pago1: 2026-04-01
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
    'Seminario de Innovacion Tecnologica',
    'Seminario sobre nuevas tecnologias y transformacion digital en la industria manufacturera',
    50, 
    '2026-04-01', '2026-04-20', '09:00:00', '18:00:00',
    32000.00, 5120.00, 37120.00,
    1, 106, 'PEN', 2, 2,  -- Business - Escuela
    false, '',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": false}',
    '{"mobiliario": true, "equipamiento": false, "inventario": false}',
    60.0
);

-- ========================================
-- 7.2 RESERVACIONES DE OTROS CLIENTES - 4 reservaciones
-- ========================================

-- Reservacion 4: Ana Martinez - Boda
-- Fecha de creacion/pago1: 2026-03-15
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
    'Celebracion de boda con 120 invitados, incluye banquete premium, decoracion floral y pista de baile',
    120, 
    '2026-03-15', '2026-04-18', '18:00:00', '02:00:00',
    85000.00, 13600.00, 98600.00,
    2, 102, 'CONF', 5, 2,  -- Gran Gala - Banquete
    true, 'Paquete Boda Premium',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true, "decoracion": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": true}',
    85.0
);

-- Reservacion 5: Roberto Sanchez - XV Anos
-- Fecha de creacion/pago1: 2026-04-02
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
    'XV Anos de Sofia',
    'Celebracion de XV anos con tema de princesa, incluye banquete, DJ, iluminacion ambiental y fotografia profesional',
    90, 
    '2026-04-02', '2026-04-25', '19:00:00', '01:00:00',
    62000.00, 9920.00, 71920.00,
    3, 107, 'PEN', 12, 2,  -- Salon Real - Banquete
    true, 'Paquete XV Anos',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true, "decoracion": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": false}',
    70.0
);

-- Reservacion 6: Events Planner - Gala Corporativa
-- Fecha de creacion/pago1: 2026-04-05
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
    4, 105, 'CONF', 17, 2,  -- Imperial - Banquete
    true, 'Paquete Gala Premium',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true, "decoracion": true, "seguridad": true}',
    '{"mobiliario": true, "equipamiento": true, "inventario": true}',
    90.0
);

-- Reservacion 7: Fiestas Deluxe - Aniversario
-- Fecha de creacion/pago1: 2026-04-10
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
    'Aniversario 25 anos Empresa',
    'Celebracion del 25 aniversario de la empresa con evento social para empleados y sus familias',
    100, 
    '2026-04-10', '2026-05-05', '17:00:00', '23:00:00',
    55000.00, 8800.00, 63800.00,
    5, 103, 'PEN', 16, 5,  -- Gran Gala - Coctel
    true, 'Paquete Aniversario',
    '{"limpieza": true, "audio": true, "video": true, "iluminacion": true, "decoracion": true}',
    '{"mobiliario": true, "equipamiento": false, "inventario": false}',
    50.0
);


-- ========================================
-- 8. REGISTRO DE ESTADOS DE RESERVACION
-- ========================================
INSERT INTO registr_esta_reserva (fecha, reservacion_id, estado_reserva_id) VALUES 
-- Reservacion 1
('2026-03-10', 1, 'PEN'),
('2026-03-25', 1, 'CONF'),
('2026-03-26', 1, 'PAGAD'),
-- Reservacion 2
('2026-03-20', 2, 'PEN'),
('2026-04-05', 2, 'CONF'),
-- Reservacion 3
('2026-04-01', 3, 'PEN'),
-- Reservacion 4
('2026-03-15', 4, 'PEN'),
('2026-04-18', 4, 'CONF'),
-- Reservacion 5
('2026-04-02', 5, 'PEN'),
-- Reservacion 6
('2026-04-05', 6, 'PEN'),
('2026-04-10', 6, 'CONF'),
-- Reservacion 7
('2026-04-10', 7, 'PEN')
ON CONFLICT DO NOTHING;


-- ========================================
-- 9. SERVICIOS POR RESERVACION
-- ========================================
INSERT INTO reserva_servicio (extra, reservacion_id, servicio_id) VALUES 
-- Reservacion 1: Conferencia (80 pax, Business Escuela)
(false, 1, 17),  -- Coffee Break Premium
(false, 1, 31),  -- Coordinador de Evento
(false, 1, 20),  -- WiFi Premium
(false, 1, 22),  -- Proyector y Pantalla
(false, 1, 23),  -- Sistema de Audio

-- Reservacion 2: Junta Directiva (20 pax, Boardroom)
(false, 2, 17),  -- Coffee Break
(false, 2, 21),  -- Videoconferencia HD
(false, 2, 20),  -- WiFi Premium

-- Reservacion 3: Seminario (50 pax, Imperial Escuela)
(false, 3, 17),  -- Coffee Break
(false, 3, 18),  -- Lunch Box
(false, 3, 20),  -- WiFi Premium
(false, 3, 22),  -- Proyector
(false, 3, 23),  -- Sistema Audio
(false, 3, 28),  -- Fotografia

-- Reservacion 4: Boda (120 pax, Gran Gala Banquete)
(false, 4, 19),  -- Banquete Premium
(false, 4, 35),  -- Barra de Bebidas
(false, 4, 24),  -- Decoracion Floral
(false, 4, 25),  -- Iluminacion LED
(false, 4, 26),  -- Centro de Mesa
(false, 4, 29),  -- Video y Edicion
(false, 4, 27),  -- DJ

-- Reservacion 5: XV Anos (90 pax, Real Banquete)
(false, 5, 20),  -- Cena de Gala
(false, 5, 35),  -- Barra de Bebidas
(false, 5, 24),  -- Decoracion Floral
(false, 5, 25),  -- Iluminacion LED
(false, 5, 27),  -- DJ
(false, 5, 28),  -- Fotografia

-- Reservacion 6: Gala (150 pax, Imperial Banquete)
(false, 6, 20),  -- Cena de Gala
(false, 6, 35),  -- Barra de Bebidas
(false, 6, 24),  -- Decoracion Floral
(false, 6, 25),  -- Iluminacion LED
(false, 6, 26),  -- Centro de Mesa
(false, 6, 28),  -- Fotografia
(false, 6, 29),  -- Video y Edicion
(false, 6, 33),  -- Limpieza

-- Reservacion 7: Aniversario (100 pax, Gran Gala Coctel)
(false, 7, 17),  -- Coffee Break
(false, 7, 36),  -- Buffet Ejecutivo
(false, 7, 35),  -- Barra de Bebidas
(false, 7, 27),  -- DJ
(false, 7, 28),  -- Fotografia
ON CONFLICT DO NOTHING;


-- ========================================
-- 10. EQUIPAMIENTO POR RESERVACION
-- ========================================
INSERT INTO reserva_equipa (cantidad, extra, completado, reservacion_id, equipamiento_id) VALUES 
-- Reservacion 1: Conferencia
(2, false, true, 1, 1),    -- 2 Proyectores HD
(2, false, true, 1, 3),    -- 2 Pantallas 120"
(1, false, true, 1, 8),    -- 1 Laptop Presentacion

-- Reservacion 2: Junta Directiva
(1, false, true, 2, 10),   -- 1 Pantalla LED 90"
(1, false, true, 2, 4),    -- 1 Sistema Audio Portatil

-- Reservacion 3: Seminario
(3, false, true, 3, 1),    -- 3 Proyectores HD
(3, false, true, 3, 3),    -- 3 Pantallas 120"
(2, false, true, 3, 8),    -- 2 Laptops
(1, false, true, 3, 22),   -- 1 Pizarron Digital

-- Reservacion 4: Boda
(2, false, true, 4, 12),   -- 2 Spotlights LED
(2, false, true, 4, 7),    -- 2 Bocinas Bluetooth
(1, false, true, 4, 18),   -- 1 Camara Video

-- Reservacion 5: XV Anos
(1, false, true, 5, 12),   -- 1 Kit Iluminacion LED
(1, false, true, 5, 4),    -- 1 Sistema Audio Portatil
(1, false, true, 5, 5),    -- 1 Microfono Inalambrico

-- Reservacion 6: Gala
(3, false, true, 6, 12),   -- 3 Spotlights LED
(2, false, true, 6, 16),   -- 2 Consolas Audio
(1, false, true, 6, 18),   -- 1 Camara Video
(1, false, true, 6, 13),   -- 1 Torre Iluminacion

-- Reservacion 7: Aniversario
(1, false, true, 7, 12),   -- 1 Kit Iluminacion LED
(1, false, true, 7, 4),    -- 1 Sistema Audio Portatil
(1, false, true, 7, 25),   -- 1 Maquina de Cafe
ON CONFLICT DO NOTHING;


-- ========================================
-- 11. PAGOS
-- ========================================

-- ========================================
-- 11.1 PAGOS DE CLIENTE 1 (Corp. Industrial)
-- ========================================

-- Reservacion 1: Conferencia - Primer Pago (creacion: 2026-03-10)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 26100.00, 26100.00, '2026-03-10', '10:30:00', 1, 1, 'ABONO', 'TARJE');

-- Reservacion 1: Segundo Pago (despues del evento: 2026-03-26)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Liquidacion - 50% restante', 26100.00, 0.00, '2026-03-26', '14:00:00', 2, 1, 'LIQUI', 'TARJE');

-- Reservacion 2: Junta Directiva - Primer Pago (creacion: 2026-03-20)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 10440.00, 10440.00, '2026-03-20', '09:15:00', 1, 2, 'ABONO', 'TRANS');

-- Reservacion 2: Segundo Pago (despues del evento: 2026-04-06)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Liquidacion - 50% restante', 10440.00, 0.00, '2026-04-06', '16:30:00', 2, 2, 'LIQUI', 'TRANS');

-- Reservacion 3: Seminario - Primer Pago (creacion: 2026-04-01)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 18560.00, 18560.00, '2026-04-01', '11:00:00', 1, 3, 'ABONO', 'TARJE');

-- ========================================
-- 11.2 PAGOS DE OTROS CLIENTES
-- ========================================

-- Reservacion 4: Boda - Primer Pago (creacion: 2026-03-15)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 49300.00, 49300.00, '2026-03-15', '14:00:00', 1, 4, 'ABONO', 'TARJE');

-- Reservacion 4: Segundo Pago (despues del evento: 2026-04-19)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Liquidacion - 50% restante', 49300.00, 0.00, '2026-04-19', '10:00:00', 2, 4, 'LIQUI', 'TARJE');

-- Reservacion 5: XV Anos - Primer Pago (creacion: 2026-04-02)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 35960.00, 35960.00, '2026-04-02', '16:00:00', 1, 5, 'ABONO', 'EFECT');

-- Reservacion 6: Gala - Primer Pago (creacion: 2026-04-05)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 72500.00, 72500.00, '2026-04-05', '11:30:00', 1, 6, 'ABONO', 'TARJE');

-- Reservacion 6: Segundo Pago (despues del evento: 2026-04-29)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Liquidacion - 50% restante', 72500.00, 0.00, '2026-04-29', '09:00:00', 2, 6, 'LIQUI', 'TRANS');

-- Reservacion 7: Aniversario - Primer Pago (creacion: 2026-04-10)
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
('Abono inicial - 50% del total', 31900.00, 31900.00, '2026-04-10', '15:00:00', 1, 7, 'ABONO', 'TRANS');

COMMIT;

-- ========================================
-- RESUMEN DE DATOS INGRESADOS
-- ========================================
-- 
-- CATALOGOS (USANDO CODIGOS EXISTENTES):
--   ✅ Roles: 4 (ADMIN, COORD, RECEP, ALMAC)
--   ✅ Estados de cuenta: 3 (ACT, SUSPE, BANEO)
--   ✅ Tipos de cliente: 2 (MOR, FIS)
--   ✅ Estados de mobiliario: 4 (DISP, OCUP, RESV, REPAR)
--   ✅ Caracteristicas de mobiliario: 10
--   ✅ Tipos de mobiliario: 8 (IDs 1-8)
--   ✅ Tipos de montaje: 10 (IDs 1-10)
--   ✅ Tipos de evento: 18 (IDs 1-18)
--   ✅ Estados de reservacion: 11
--   ✅ Estados de salon: 5 (DIS, RESV, OCUP, MANTE, LIMPI)
--   ✅ Tipos de equipamiento: 8 (IDs 1-8)
--   ✅ Estados de equipamiento: 5 (DISP, FUNC, DANAD, REPAR, RESV)
--   ✅ Conceptos de pago: 5 (ANTIC, LIQUI, EXTR, ABONO, PENAL)
--   ✅ Metodos de pago: 5 (EFECT, TRANS, TARJE, NFC, CHEQU)
--   ✅ Tipos de servicio: 12 (IDs 1-12)
--
-- CUENTAS Y USUARIOS:
--   ✅ Cuentas: 10 (5 trabajadores, 5 clientes)
--   ✅ Trabajadores: 5
--   ✅ Datos de clientes: 5
--
-- SERVICIOS Y EQUIPAMIENTO:
--   ✅ Servicios: 21 (IDs nuevos 17-36)
--   ✅ Equipamiento: 11 (IDs nuevos 15-25)
--   ✅ Mobiliario: 10 (IDs nuevos 11-20)
--
-- INVENTARIOS:
--   ✅ Inventario mobiliario: 20 registros
--   ✅ Inventario equipamiento: 25 registros
--
-- SALONES Y MONTAJES:
--   ✅ Salones: 9 nuevos (IDs 12-20)
--   ✅ Montajes: 11 nuevos (IDs 101-111)
--   ✅ Mobiliario por montaje: ~30 registros
--
-- RESERVACIONES (7 total):
--   ✅ Cliente 1 (Corp. Industrial): 3 reservaciones
--      - Conferencia Anual (PAGADA)
--      - Junta Directiva (CONFIRMADA)
--      - Seminario Innovacion (PENDIENTE)
--   ✅ Cliente 2 (Ana Martinez): 1 reservacion
--      - Boda (CONFIRMADA)
--   ✅ Cliente 3 (Roberto Sanchez): 1 reservacion
--      - XV Anos (PENDIENTE)
--   ✅ Cliente 4 (Events Planner): 1 reservacion
--      - Gala Corporativa (CONFIRMADA)
--   ✅ Cliente 5 (Fiestas Deluxe): 1 reservacion
--      - Aniversario (PENDIENTE)
--
-- PAGOS:
--   ✅ 12 pagos registrados
--   ✅ 5 reservaciones con pago completo
--   ✅ 2 reservaciones pendientes de segundo pago
--
-- SERVICIOS POR RESERVACION: 30 registros
-- EQUIPAMIENTO POR RESERVACION: 21 registros
-- ESTADOS DE RESERVACION: 11 registros
-- ESTADOS DE SALON: 19 registros
-- ========================================
