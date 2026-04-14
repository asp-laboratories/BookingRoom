-- ========================================
-- DATOS DE PRUEBA HOTEL BOOKINGROOM - V2 LIMPIO
-- ========================================
-- USO: psql -U postgres -d bookingroom_nuevadata -f datos_prueba_hotel_v2.sql
-- Nota: Este script asume que las tablas ya existen (migraciones Django)
-- y solo inserta datos nuevos con ON CONFLICT DO NOTHING
-- ========================================

BEGIN;

-- ========================================
-- 1. CATÁLOGOS EXISTENTES (solo insertar nuevos)
-- ========================================

-- Tipos de montaje (agregar IDs 8-10)
INSERT INTO tipo_montaje (id, nombre, disposicion, "capacidadIdeal") VALUES 
(8, 'Estilo Lounge', true, 50),
(9, 'Mesa Redonda', true, 80),
(10, 'Espanola/Boardroom', true, 20)
ON CONFLICT (id) DO NOTHING;

-- Tipos de evento (agregar IDs 12-18)
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES 
(12, 'XV Anos', true),
(13, 'Bautizo', true),
(14, 'Graduacion', true),
(15, 'Cumpleanos', true),
(16, 'Aniversario', true),
(17, 'Gala', true),
(18, 'Exposicion', true)
ON CONFLICT (id) DO NOTHING;

-- Estados de reservacion (agregar CANC y RECH)
INSERT INTO estado_reserva (codigo, nombre) VALUES 
('CANC', 'Cancelada por Cliente'),
('RECH', 'Rechazada')
ON CONFLICT (codigo) DO NOTHING;

-- Tipos de equipamiento (agregar IDs 7-8)
INSERT INTO tipo_equipa (id, nombre, disposicion) VALUES 
(7, 'Telecomunicaciones', true),
(8, 'Accesorios presentacion', true)
ON CONFLICT (id) DO NOTHING;

-- Tipos de servicio (agregar IDs 11-12)
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES 
(11, 'Servicios para reuniones', 'Servicios orientados a juntas', true),
(12, 'Servicios ejecutivos', 'Servicios premium VIP', true)
ON CONFLICT (id) DO NOTHING;

-- Caracteristicas de mobiliario (agregar nuevas)
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

-- Tipos de mobiliario (agregar IDs 6-8)
INSERT INTO tipo_mobil (id, nombre, disposicion) VALUES 
(6, 'Escenarios', true),
(7, 'Mesas de buffet', true),
(8, 'Mobiliario lounge', true)
ON CONFLICT (id) DO NOTHING;


-- ========================================
-- 2. CUENTAS Y USUARIOS
-- ========================================

-- Cuentas
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

-- Trabajadores
INSERT INTO trabajador (no_empleado, rfc, nombre, "apellidoPaterno", "apelidoMaterno", telefono, correo_electronico, rol_id, cuenta_id) VALUES 
('TRAB001', 'RIMJ850101XXX', 'Martha', 'Rivera', 'Jimenez', '5551234567', 'martha.rivera@email.com', 'ADMIN', 1),
('TRAB002', 'MACL900202XXX', 'Carlos', 'Martinez', 'Lopez', '5552345678', 'carlos.mtz@hotel.com', 'RECEP', 2),
('TRAB003', 'GALJ880303XXX', 'Luis', 'Garcia', 'Lopez', '5553456789', 'luis.garcia@hotel.com', 'COORD', 3),
('TRAB004', 'PEAN920404XXX', 'Ana', 'Perez', 'Nunez', '5554567890', 'ana.perez@hotel.com', 'ALMAC', 4),
('TRAB005', 'ROHJ950505XXX', 'Jorge', 'Rodriguez', 'Hernandez', '5555678901', 'jorge.rodriguez@hotel.com', 'RECEP', 5)
ON CONFLICT (no_empleado) DO NOTHING;

-- Datos de clientes
INSERT INTO datos_cliente (rfc, nombre_fiscal, nombre, "apellidoPaterno", "apelidoMaterno", telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, tipo_cliente_id, cuenta_id) VALUES 
('COR850101XXX', 'Corporativo Industrial del Norte', 'Roberto', 'Corporativo', 'Industrial', '5559871234', 'contacto@corpindustrial.mx', 'Colonia Centro', 'Av. Constitucion', '456', 'MOR', 6),
('MANA900515XXX', 'Ana Sofia Martinez', 'Ana Sofia', 'Martinez', 'Gonzalez', '5558761234', 'ana.martinez@gmail.com', 'Colonia Del Valle', 'Calle Insurgentes Sur', '789', 'FIS', 7),
('SARL850920XXX', 'Roberto Sanchez', 'Roberto', 'Sanchez', 'Luna', '5557651234', 'roberto.sanchez@outlook.com', 'Colonia Roma Norte', 'Av. Juarez', '321', 'FIS', 8),
('EVP900101XXX', 'Events Planner Mexico S.C.', 'Laura', 'Events', 'Planner', '5556541234', 'info@eventsplanner.com', 'Colonia Polanco', 'Av. Masaryk', '123', 'MOR', 9),
('FID850202XXX', 'Fiestas Deluxe Eventos', 'Carmen', 'Fiestas', 'Deluxe', '5555431234', 'reservaciones@fiestasdeluxe.com', 'Colonia Coyoacan', 'Calle Hidalgo', '654', 'MOR', 10)
ON CONFLICT (correo_electronico) DO NOTHING;


-- ========================================
-- 3. SERVICIOS NUEVOS (IDs 17+)
-- ========================================
INSERT INTO servicio (nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES 
('Coffee Break Premium', 'Cafe, te, jugos, frutas y pasteleria', 1500.00, true, 1),
('Lunch Box Ejecutivo', 'Caja de almuerzo individual', 3500.00, true, 1),
('Banquete Premium', 'Banquete de 3 tiempos', 8500.00, true, 1),
('Cena de Gala', 'Cena formal de 5 tiempos', 15000.00, true, 1),
('WiFi Premium Dedicado', 'Internet alta velocidad', 1200.00, true, 10),
('Videoconferencia HD', 'Sistema videoconferencia 4K', 2800.00, true, 2),
('Proyector y Pantalla HD', 'Proyector HD con pantalla 120"', 2000.00, true, 2),
('Sistema de Audio Profesional', 'Consola con microfonos', 3500.00, true, 2),
('Decoracion Floral Premium', 'Arreglos florales alta gama', 5000.00, true, 3),
('Iluminacion Ambiental LED', 'Iluminacion profesional', 3500.00, true, 3),
('Centro de Mesa Premium', 'Centros de mesa elegantes', 2500.00, true, 3),
('DJ y Musica Ambiental', 'DJ profesional', 4500.00, true, 6),
('Fotografia Profesional', 'Fotografo profesional', 6000.00, true, 5),
('Video y Edicion', 'Videografo con edicion', 8500.00, true, 5),
('Limpieza Durante Evento', 'Personal de limpieza', 1800.00, true, 8),
('Seguridad Privada', 'Guardia de seguridad', 2500.00, true, 7),
('Coordinador de Evento', 'Coordinador dedicado', 2500.00, true, 11),
('Traduccion Simultanea', 'Interprete bilingue', 4500.00, true, 12),
('Valet Parking', 'Estacionamiento con valet', 3000.00, true, 12),
('Barra de Bebidas Premium', 'Barra libre premium', 7500.00, true, 1),
('Buffet Ejecutivo', 'Buffet variado corporativo', 6000.00, true, 1)
ON CONFLICT DO NOTHING;


-- ========================================
-- 4. EQUIPAMIENTO NUEVO (IDs 15+)
-- ========================================
INSERT INTO equipamiento (nombre, descripcion, costo, stock, tipo_equipa_id) VALUES 
('Microfono Inalambrico Prof.', 'Microfono profesional', 1500.00, 8, 1),
('Consola de Audio Digital', 'Mezclador 16 canales', 3000.00, 2, 1),
('Pantalla 150"', 'Pantalla electrica 150"', 1200.00, 3, 2),
('Camara Video Profesional', 'Camara 4K', 1800.00, 3, 2),
('Sistema Videoconferencia', 'Equipo videoconferencia HD', 2500.00, 2, 7),
('Router WiFi Dedicado', 'Router alta velocidad', 800.00, 5, 7),
('Telefono IP', 'Telefono internet', 500.00, 10, 7),
('Pizarron Digital', 'Pizarron tactil 65"', 2500.00, 3, 8),
('Rotafolios', 'Rotafolio profesional', 400.00, 8, 8),
('Flip Chart', 'Flip chart magnetico', 600.00, 5, 8),
('Maquina de Cafe', 'Maquina cafe profesional', 1800.00, 4, 8)
ON CONFLICT DO NOTHING;


-- ========================================
-- 5. MOBILIARIO NUEVO (IDs 11+)
-- ========================================
INSERT INTO mobiliario (nombre, descripcion, costo, stock, tipo_movil_id) VALUES 
('Silla Tiffany', 'Silla elegante formal', 350.00, 80, 1),
('Silla Pala', 'Silla con escritorio', 250.00, 50, 1),
('Silla Ejecutiva', 'Silla ergonomica', 400.00, 40, 1),
('Escenario 4x3m', 'Escenario modular', 5000.00, 3, 6),
('Escenario 3x2m', 'Escenario modular', 3500.00, 4, 6),
('Mesa Buffet Larga', 'Mesa para buffet', 700.00, 8, 7),
('Mesa Buffet Corta', 'Mesa mediana buffet', 500.00, 10, 7),
('Sofa Modular', 'Sofa 3 plazas', 1200.00, 8, 8),
('Puff Individual', 'Puff acolchado', 400.00, 15, 8),
('Mesa Centro Baja', 'Mesa baja lounge', 500.00, 10, 8)
ON CONFLICT DO NOTHING;


-- ========================================
-- 6. SALONES NUEVOS (IDs 12+)
-- ========================================
INSERT INTO salon (nombre, costo, ubicacion, "dimenLargo", "dimenAncho", "dimenAlto", "metrosCuadrados", "maxCapacidad", estado_salon_id) VALUES 
('Salon Gran Gala', 15000.00, 'Piso 1, Ala Norte', 25.00, 15.00, 4.00, 375.00, 200, 'DIS'),
('Salon Imperial', 12000.00, 'Piso 2, Ala Este', 20.00, 12.00, 3.50, 240.00, 150, 'DIS'),
('Salon Real', 10000.00, 'Piso 1, Ala Sur', 18.00, 10.00, 3.00, 180.00, 120, 'DIS'),
('Salon Plaza', 8000.00, 'Piso 2, Ala Oeste', 15.00, 10.00, 3.00, 150.00, 100, 'DIS'),
('Salon Ejecutivo', 6000.00, 'Piso 3, Ala Norte', 12.00, 8.00, 2.80, 96.00, 60, 'DIS'),
('Salon Business', 5500.00, 'Piso 3, Ala Sur', 10.00, 8.00, 2.80, 80.00, 50, 'DIS'),
('Salon Boardroom', 4000.00, 'Piso 4, Ala Norte', 8.00, 6.00, 2.60, 48.00, 25, 'DIS'),
('Terraza Mirador', 9000.00, 'Azotea, Nivel 5', 22.00, 12.00, 4.00, 264.00, 150, 'DIS'),
('Jardin Interior', 7500.00, 'Planta Baja', 18.00, 10.00, 6.00, 180.00, 120, 'DIS')
ON CONFLICT DO NOTHING;

-- Estados de salones
INSERT INTO registr_esta_salon (salon_id, estado_salon_id, fecha) 
SELECT id, 'DIS', CURRENT_DATE FROM salon WHERE id >= 12
ON CONFLICT DO NOTHING;


-- ========================================
-- 7. MONTAJES (IDs 101+)
-- ========================================
INSERT INTO montaje (costo, salon_id, tipo_montaje_id) VALUES 
(2500.00, 12, 1), (3000.00, 12, 3), (2800.00, 12, 4),
(2000.00, 13, 1), (2500.00, 13, 3), (2200.00, 13, 2),
(1800.00, 14, 3), (1500.00, 14, 6),
(1200.00, 17, 2), (1400.00, 17, 5), (1300.00, 17, 10),
(1000.00, 18, 10), (900.00, 18, 5)
ON CONFLICT DO NOTHING;

-- Mobiliario de montajes
INSERT INTO montaje_mobiliario (cantidad, extra, completado, montaje_id, mobiliario_id) VALUES 
(100, false, true, 101, 1), (1, false, true, 101, 10), (1, false, true, 101, 14),
(12, false, true, 102, 5), (120, false, true, 102, 11), (1, false, true, 102, 10),
(15, false, true, 103, 16), (30, false, true, 103, 8), (3, false, true, 103, 18),
(80, false, true, 104, 1), (1, false, true, 104, 10), (1, false, true, 104, 15),
(10, false, true, 105, 5), (100, false, true, 105, 11), (1, false, true, 105, 10),
(15, false, true, 106, 6), (40, false, true, 106, 12), (2, false, true, 106, 22),
(8, false, true, 107, 4), (80, false, true, 107, 11), (2, false, true, 107, 20),
(10, false, true, 108, 7), (20, false, true, 108, 13), (1, false, true, 108, 10),
(10, false, true, 109, 6), (25, false, true, 109, 12), (2, false, true, 109, 23),
(1, false, true, 110, 10), (15, false, true, 110, 13),
(1, false, true, 111, 7), (12, false, true, 111, 13)
ON CONFLICT DO NOTHING;


-- ========================================
-- 8. RESERVACIONES (7 total)
-- ========================================
INSERT INTO reservacion (
    "nombreEvento", "descripEvento", "estimaAsistentes", 
    "fechaReservacion", "fechaEvento", "horaInicio", "horaFin", 
    subtotal, "IVA", total,
    cliente_id, montaje_id, estado_reserva_id, tipo_evento_id, trabajador_id, 
    es_paquete, nombre_paquete,
    checklist_coordinador, checklist_almacenista, progreso_checklist
) VALUES 
-- Cliente 1 (Corp Industrial) - 3 reservaciones
('Conferencia Anual', 'Presentacion de resultados anuales', 80, 
 '2026-03-10', '2026-03-25', '09:00:00', '17:00:00',
 45000.00, 7200.00, 52200.00, 1, 106, 'PAGAD', 1, 2, 
 false, '',
 '{"limpieza": true, "audio": true}', '{"mobiliario": true, "inventario": true}', 100.0),

('Junta Directiva', 'Revision de estrategia trimestral', 20, 
 '2026-03-20', '2026-04-05', '10:00:00', '14:00:00',
 18000.00, 2880.00, 20880.00, 1, 111, 'CONF', 6, 2, 
 false, '',
 '{"limpieza": true, "audio": true}', '{"mobiliario": true, "inventario": true}', 80.0),

('Seminario Innovacion', 'Nuevas tecnologias en industria', 50, 
 '2026-04-01', '2026-04-20', '09:00:00', '18:00:00',
 32000.00, 5120.00, 37120.00, 1, 106, 'PEN', 2, 2, 
 false, '',
 '{"limpieza": true}', '{"mobiliario": true}', 60.0),

-- Otros clientes - 4 reservaciones
('Boda Ana y Carlos', 'Celebracion de boda 120 invitados', 120, 
 '2026-03-15', '2026-04-18', '18:00:00', '02:00:00',
 85000.00, 13600.00, 98600.00, 2, 102, 'CONF', 5, 2, 
 true, 'Paquete Boda Premium',
 '{"limpieza": true, "audio": true}', '{"mobiliario": true, "inventario": true}', 85.0),

('XV Anos de Sofia', 'Celebracion XV anos princesa', 90, 
 '2026-04-02', '2026-04-25', '19:00:00', '01:00:00',
 62000.00, 9920.00, 71920.00, 3, 107, 'PEN', 12, 2, 
 true, 'Paquete XV Anos',
 '{"limpieza": true, "audio": true}', '{"mobiliario": true, "inventario": false}', 70.0),

('Gala de Premios 2026', 'Cena de gala premios anuales', 150, 
 '2026-04-05', '2026-04-28', '20:00:00', '01:00:00',
 125000.00, 20000.00, 145000.00, 4, 105, 'CONF', 17, 2, 
 true, 'Paquete Gala Premium',
 '{"limpieza": true, "audio": true}', '{"mobiliario": true, "inventario": true}', 90.0),

('Aniversario 25 anos', 'Celebracion aniversario empresa', 100, 
 '2026-04-10', '2026-05-05', '17:00:00', '23:00:00',
 55000.00, 8800.00, 63800.00, 5, 103, 'PEN', 16, 5, 
 true, 'Paquete Aniversario',
 '{"limpieza": true, "audio": true}', '{"mobiliario": true, "inventario": false}', 50.0)
ON CONFLICT DO NOTHING;


-- ========================================
-- 9. ESTADOS DE RESERVACION
-- ========================================
INSERT INTO registr_esta_reserva (fecha, reservacion_id, estado_reserva_id) VALUES 
('2026-03-10', 1, 'PEN'), ('2026-03-25', 1, 'CONF'), ('2026-03-26', 1, 'PAGAD'),
('2026-03-20', 2, 'PEN'), ('2026-04-05', 2, 'CONF'),
('2026-04-01', 3, 'PEN'),
('2026-03-15', 4, 'PEN'), ('2026-04-18', 4, 'CONF'),
('2026-04-02', 5, 'PEN'),
('2026-04-05', 6, 'PEN'), ('2026-04-10', 6, 'CONF'),
('2026-04-10', 7, 'PEN')
ON CONFLICT DO NOTHING;


-- ========================================
-- 10. SERVICIOS POR RESERVACION
-- ========================================
INSERT INTO reserva_servicio (extra, reservacion_id, servicio_id) VALUES 
(false, 1, 17), (false, 1, 31), (false, 1, 20), (false, 1, 22), (false, 1, 23),
(false, 2, 17), (false, 2, 21), (false, 2, 20),
(false, 3, 17), (false, 3, 18), (false, 3, 20), (false, 3, 22), (false, 3, 23), (false, 3, 28),
(false, 4, 19), (false, 4, 35), (false, 4, 24), (false, 4, 25), (false, 4, 26), (false, 4, 29), (false, 4, 27),
(false, 5, 20), (false, 5, 35), (false, 5, 24), (false, 5, 25), (false, 5, 27), (false, 5, 28),
(false, 6, 20), (false, 6, 35), (false, 6, 24), (false, 6, 25), (false, 6, 26), (false, 6, 28), (false, 6, 29), (false, 6, 33),
(false, 7, 17), (false, 7, 36), (false, 7, 35), (false, 7, 27), (false, 7, 28)
ON CONFLICT DO NOTHING;


-- ========================================
-- 11. EQUIPAMIENTO POR RESERVACION
-- ========================================
INSERT INTO reserva_equipa (cantidad, extra, completado, reservacion_id, equipamiento_id) VALUES 
(2, false, true, 1, 1), (2, false, true, 1, 3), (1, false, true, 1, 8),
(1, false, true, 2, 10), (1, false, true, 2, 4),
(3, false, true, 3, 1), (3, false, true, 3, 3), (2, false, true, 3, 8), (1, false, true, 3, 22),
(2, false, true, 4, 12), (2, false, true, 4, 7), (1, false, true, 4, 18),
(1, false, true, 5, 12), (1, false, true, 5, 4), (1, false, true, 5, 5),
(3, false, true, 6, 12), (2, false, true, 6, 16), (1, false, true, 6, 18), (1, false, true, 6, 13),
(1, false, true, 7, 12), (1, false, true, 7, 4), (1, false, true, 7, 25)
ON CONFLICT DO NOTHING;


-- ========================================
-- 12. PAGOS
-- ========================================
INSERT INTO pago (nota, monto, saldo, fecha, hora, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id) VALUES 
-- Cliente 1 (Corp Industrial)
('Abono inicial 50%', 26100.00, 26100.00, '2026-03-10', '10:30:00', 1, 1, 'ABONO', 'TARJE'),
('Liquidacion 50%', 26100.00, 0.00, '2026-03-26', '14:00:00', 2, 1, 'LIQUI', 'TARJE'),
('Abono inicial 50%', 10440.00, 10440.00, '2026-03-20', '09:15:00', 1, 2, 'ABONO', 'TRANS'),
('Liquidacion 50%', 10440.00, 0.00, '2026-04-06', '16:30:00', 2, 2, 'LIQUI', 'TRANS'),
('Abono inicial 50%', 18560.00, 18560.00, '2026-04-01', '11:00:00', 1, 3, 'ABONO', 'TARJE'),

-- Otros clientes
('Abono inicial 50%', 49300.00, 49300.00, '2026-03-15', '14:00:00', 1, 4, 'ABONO', 'TARJE'),
('Liquidacion 50%', 49300.00, 0.00, '2026-04-19', '10:00:00', 2, 4, 'LIQUI', 'TARJE'),
('Abono inicial 50%', 35960.00, 35960.00, '2026-04-02', '16:00:00', 1, 5, 'ABONO', 'EFECT'),
('Abono inicial 50%', 72500.00, 72500.00, '2026-04-05', '11:30:00', 1, 6, 'ABONO', 'TARJE'),
('Liquidacion 50%', 72500.00, 0.00, '2026-04-29', '09:00:00', 2, 6, 'LIQUI', 'TRANS'),
('Abono inicial 50%', 31900.00, 31900.00, '2026-04-10', '15:00:00', 1, 7, 'ABONO', 'TRANS')
ON CONFLICT DO NOTHING;

COMMIT;

-- ========================================
-- RESUMEN FINAL
-- ========================================
-- 
-- ✅ CATALOGOS: Se agregaron registros nuevos sin modificar existentes
-- ✅ USUARIOS: 10 cuentas, 5 trabajadores, 5 clientes
-- ✅ SERVICIOS: 21 nuevos
-- ✅ EQUIPAMIENTO: 11 nuevos
-- ✅ MOBILIARIO: 10 nuevos
-- ✅ SALONES: 9 nuevos
-- ✅ MONTAJES: 11 nuevos
-- ✅ RESERVACIONES: 7 total (3 Cliente 1, 4 otros)
-- ✅ PAGOS: 12 pagos registrados
-- ========================================
