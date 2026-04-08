-- ==========================================
-- DATOS PARA POBLAR LA BASE DE DATOS
-- Proyecto: BookingRoom - Sistema de Reservaciones de Eventos en Salones de Hotel
-- Idempotente: usa ON CONFLICT DO NOTHING para catalogos
-- ==========================================

BEGIN;

-- ==========================================
-- 1. TABLAS DE CATÁLOGO (idempotente)
-- ==========================================

-- Tabla ROL
INSERT INTO rol (codigo, nombre) VALUES 
('ADMIN', 'Administrador'),
('COORD', 'Coordinador'),
('RECEP', 'Recepcionista'),
('ALMAC', 'Almacen')
ON CONFLICT (codigo) DO NOTHING;

-- Tabla ESTADO_CUENTA
INSERT INTO estado_cuenta (codigo, nombre) VALUES 
('ACT', 'Activa'),
('SUSPE', 'Suspendida'),
('BANEO', 'Bloqueada')
ON CONFLICT (codigo) DO NOTHING;

-- Tabla ESTADO_SALON
INSERT INTO estado_salon (codigo, nombre) VALUES 
('DIS', 'Disponible'),
('RESV', 'Reservado'),
('OCUP', 'Ocupado'),
('MANTE', 'En mantenimiento'),
('LIMPI', 'En limpieza')
ON CONFLICT (codigo) DO NOTHING;

-- Tabla ESTADO_MOBIL
INSERT INTO estado_mobil (codigo, nombre) VALUES 
('DISP', 'Disponible'),
('OCUP', 'Ocupado'),
('RESV', 'Reservado'),
('REPAR', 'En reparacion')
ON CONFLICT (codigo) DO NOTHING;

-- Tabla TIPO_MOBIL
INSERT INTO tipo_mobil (nombre, disposicion) VALUES 
('Sillas', TRUE),
('Mesas Redondas', TRUE),
('Mesas Rectangulares', TRUE),
('Taburetes', TRUE),
('Podios', TRUE)
ON CONFLICT DO NOTHING;

-- Tabla ESTADO_EQUIPA
INSERT INTO estado_equipa (codigo, nombre) VALUES 
('DISP', 'Disponible'),
('FUNC', 'Funcional'),
('DANAD', 'Daniado'),
('REPAR', 'En reparacion'),
('RESV', 'Reservado')
ON CONFLICT (codigo) DO NOTHING;

-- Tabla ESTADO_RESERVA
INSERT INTO estado_reserva (codigo, nombre) VALUES 
('SOLIC', 'Solicitada'),
('PEN', 'Pendiente'),
('CONF', 'Confirmada'),
('CON', 'Confirmada'),
('ENPRO', 'En proceso'),
('FIN', 'Finalizada'),
('CAN', 'Cancelada'),
('PAGAD', 'Pagada'),
('PLANT', 'Plantilla')
ON CONFLICT (codigo) DO NOTHING;

-- Tabla TIPO_CLIENTE
INSERT INTO tipo_cliente (codigo, nombre, disposicion) VALUES 
('MOR', 'Persona moral', TRUE),
('FIS', 'Persona fisica', TRUE),
('PM', 'Persona Moral', TRUE),
('PF', 'Persona Fisica', TRUE)
ON CONFLICT (codigo) DO NOTHING;

-- Tabla TIPO_MONTAJE
INSERT INTO tipo_montaje (nombre, disposicion, "capacidadIdeal") VALUES 
('Teatro', TRUE, 100),
('Escuela', TRUE, 60),
('Banquete', TRUE, 80),
('Recepcion', TRUE, 150),
('Imperial', TRUE, 40),
('Herradura', TRUE, 50),
('Mesa rusa', TRUE, 30)
ON CONFLICT DO NOTHING;

-- Tabla TIPO_EVENTO
INSERT INTO tipo_evento (nombre, disposicion) VALUES 
('Conferencia', TRUE),
('Seminario', TRUE),
('Cena de empresa', TRUE),
('Lanzamiento de producto', TRUE),
('Boda', TRUE),
('Junta de consejo', TRUE),
('Asamblea', TRUE),
('Reunion de trabajo', TRUE),
('Fiesta', TRUE),
('Otro', TRUE)
ON CONFLICT DO NOTHING;

-- Tabla TIPO_SERVICIO
INSERT INTO tipo_servicio (nombre, descripcion, disposicion) VALUES 
('Catering', 'Servicios de comida y bebida', TRUE),
('Audiovisual', 'Equipos de audio y video', TRUE),
('Decoracion', 'Decoracion de espacios', TRUE),
('Transporte', 'Servicios de transporte', TRUE),
('Fotografia', 'Fotografia y video profesional', TRUE),
('Musica', 'Entretenimiento musical', TRUE),
('Seguridad', 'Seguridad y vigilancia', TRUE),
('Limpieza', 'Servicios de limpieza', TRUE),
('Otro', 'Otros servicios', TRUE),
('Internet', 'Conectividad y tecnologia', TRUE)
ON CONFLICT DO NOTHING;

-- Tabla TIPO_EQUIPA
INSERT INTO tipo_equipa (nombre, disposicion) VALUES 
('Audio', TRUE),
('Video', TRUE),
('Iluminacion', TRUE),
('Computo', TRUE),
('Mobiliario extra', TRUE),
('Otro', TRUE)
ON CONFLICT DO NOTHING;

-- Tabla CONCEPTO_PAGO
INSERT INTO concepto_pago (codigo, nombre) VALUES 
('ANTIC', 'Anticipo'),
('LIQUI', 'Liquidacion'),
('EXTR', 'Extra'),
('ABONO', 'Abono'),
('PENAL', 'Penalizacion')
ON CONFLICT (codigo) DO NOTHING;

-- Tabla METODO_PAGO
INSERT INTO metodo_pago (codigo, nombre) VALUES 
('EFECT', 'Efectivo'),
('TRANS', 'Transferencia'),
('TARJE', 'Tarjeta'),
('NFC', 'NFC'),
('CHEQU', 'Cheque')
ON CONFLICT (codigo) DO NOTHING;

-- ==========================================
-- 2. LIMPIAR TODOS LOS DATOS (Descomenta si necesitas limpiar la BD)
-- ==========================================

-- TRUNCATE salon, montaje, mobiliario, equipamiento, servicio, montaje_mobiliario, 
--        cuenta, trabajador, datos_cliente, reservacion, pago, registr_esta_reserva, 
--        registr_esta_salon, reserva_servicio, reserva_equipa, inventario_mobil, 
--        inventario_equipa, tipo_evento, tipo_montaje, tipo_servicio, tipo_equipa, 
--        tipo_cliente, concepto_pago, metodo_pago, estado_reserva, estado_mobil, 
--        estado_equipa, estado_salon, estado_cuenta, rol, tipo_mobil CASCADE;

-- Limpiar registros existentes (usar con precaución)
-- DELETE FROM reservacion WHERE estado_reserva_id IN ('SOLIC', 'PEN', 'CONF', 'CON', 'ENPRO', 'FIN', 'CAN', 'PAGAD', 'PLANT');
-- DELETE FROM pago WHERE reservacion_id IS NOT NULL;
-- DELETE FROM registr_esta_reserva WHERE reservacion_id IS NOT NULL;
-- DELETE FROM registr_esta_salon WHERE salon_id IS NOT NULL;
-- DELETE FROM reserva_servicio WHERE reservacion_id IS NOT NULL;
-- DELETE FROM reserva_equipa WHERE reservacion_id IS NOT NULL;
-- DELETE FROM inventario_mobil;
-- DELETE FROM inventario_equipa;

-- ==========================================
-- 3. INFRAESTRUCTURA: SALONES
-- ==========================================

DELETE FROM salon WHERE TRUE;
ALTER SEQUENCE salon_id_seq RESTART WITH 1;
ALTER SEQUENCE montaje_id_seq RESTART WITH 1;
ALTER SEQUENCE tipo_montaje_id_seq RESTART WITH 1;
ALTER SEQUENCE tipo_evento_id_seq RESTART WITH 1;
ALTER SEQUENCE tipo_servicio_id_seq RESTART WITH 1;
ALTER SEQUENCE tipo_equipa_id_seq RESTART WITH 1;
ALTER SEQUENCE mobiliario_id_seq RESTART WITH 1;
ALTER SEQUENCE equipamiento_id_seq RESTART WITH 1;
ALTER SEQUENCE servicio_id_seq RESTART WITH 1;
ALTER SEQUENCE montaje_mobilairio_id_seq RESTART WITH 1;
ALTER SEQUENCE inventario_mobil_id_seq RESTART WITH 1;
ALTER SEQUENCE inventario_equipa_id_seq RESTART WITH 1;
ALTER SEQUENCE cuenta_id_seq RESTART WITH 1;
ALTER SEQUENCE datos_cliente_id_seq RESTART WITH 1;
ALTER SEQUENCE reservacion_id_seq RESTART WITH 1;
ALTER SEQUENCE pago_id_seq RESTART WITH 1;
ALTER SEQUENCE reserva_servicio_id_seq RESTART WITH 1;
ALTER SEQUENCE reserva_equipa_id_seq RESTART WITH 1;
ALTER SEQUENCE registr_esta_reserva_id_seq RESTART WITH 1;
ALTER SEQUENCE registr_esta_salon_id_seq RESTART WITH 1;
ALTER SEQUENCE tipo_mobil_id_seq RESTART WITH 1;
ALTER SEQUENCE caracter_mobi_id_seq RESTART WITH 1;

INSERT INTO salon (nombre, costo, ubicacion, "dimenLargo", "dimenAncho", "dimenAlto", "metrosCuadrados", "maxCapacidad", estado_salon_id) VALUES 
('Salon Diamante', 5000.00, 'Planta baja - Ala norte', 15.0, 10.0, 4.0, 150.0, 150, 'DIS'),
('Salon Esmeralda', 4500.00, 'Planta baja - Ala sur', 12.0, 8.0, 3.5, 96.0, 100, 'DIS'),
('Salon Rubi', 4000.00, 'Piso 1 - Ala este', 10.0, 8.0, 3.0, 80.0, 80, 'DIS'),
('Salon Zafiro', 6000.00, 'Piso 1 - Ala oeste', 14.0, 12.0, 4.0, 168.0, 200, 'DIS'),
('Salon Oro', 8000.00, 'Piso 2 - Centro', 20.0, 15.0, 5.0, 300.0, 350, 'DIS'),
('Salon Platino', 10000.00, 'Piso 2 - Acceso principal', 25.0, 18.0, 6.0, 450.0, 500, 'DIS');

-- ==========================================
-- 4. CONFIGURACIONES DE MONTAJE POR SALON
-- ==========================================

INSERT INTO montaje (salon_id, tipo_montaje_id, costo) VALUES 
(1, 1, 500.00), (1, 2, 400.00), (1, 3, 600.00),
(2, 1, 450.00), (2, 4, 350.00),
(3, 5, 300.00), (3, 6, 350.00),
(4, 1, 600.00), (4, 2, 500.00), (4, 3, 700.00),
(5, 1, 800.00), (5, 2, 700.00), (5, 3, 900.00), (5, 4, 600.00),
(6, 1, 1000.00), (6, 2, 900.00), (6, 3, 1200.00), (6, 4, 800.00), (6, 5, 500.00)
ON CONFLICT DO NOTHING;

-- ==========================================
-- 5. MOBILIARIO
-- ==========================================

INSERT INTO mobiliario (nombre, descripcion, costo, stock, tipo_movil_id) VALUES 
('Silla plegable', 'Silla plegable de plastico resistente', 25.00, 500, 1),
('Silla ejecutiva', 'Silla con descansabrazos y soporte lumbar', 150.00, 100, 1),
('Silla vintage', 'Silla de madera con tapizado de tela', 200.00, 50, 1),
('Mesa redonda 1.5m', 'Mesa redonda para 8 personas', 180.00, 60, 2),
('Mesa redonda 1.8m', 'Mesa redonda para 10 personas', 220.00, 40, 2),
('Mesa rectangular 2m', 'Mesa rectangular para 10 personas', 200.00, 80, 3),
('Mesa rectangular 3m', 'Mesa rectangular para 15 personas', 280.00, 30, 3),
('Taburete alto', 'Taburete para barra de 80cm', 80.00, 50, 4),
('Taburete bajo', 'Taburete para barra de 60cm', 70.00, 50, 4),
('Podio ejecutivo', 'Podio de madera con microphone', 500.00, 10, 5);

-- Inventario de mobiliario por estado (disponible)
INSERT INTO inventario_mobil (mobiliario_id, estado_mobil_id, cantidad) VALUES 
(1, 'DISP', 500),
(2, 'DISP', 100),
(4, 'DISP', 60),
(5, 'DISP', 40),
(6, 'DISP', 80),
(7, 'DISP', 30),
(8, 'DISP', 50),
(9, 'DISP', 50),
(10, 'DISP', 10);

-- Montaje de mobiliario por configuracion de salon
-- Salon Diamante - Teatro (id_montaje=1)
INSERT INTO montaje_mobiliario (cantidad, montaje_id, mobiliario_id) VALUES 
(150, 1, 1),
(15, 1, 4);

-- Salon Diamante - Escuela (id_montaje=2)
INSERT INTO montaje_mobiliario (cantidad, montaje_id, mobiliario_id) VALUES 
(60, 2, 1),
(10, 2, 6);

-- Salon Diamante - Banquete (id_montaje=3)
INSERT INTO montaje_mobiliario (cantidad, montaje_id, mobiliario_id) VALUES 
(80, 3, 4),
(10, 3, 5);

-- Salon Zafiro - Teatro (id_montaje=6)
INSERT INTO montaje_mobiliario (cantidad, montaje_id, mobiliario_id) VALUES 
(200, 6, 2),
(25, 6, 7);

-- Salon Zafiro - Banquete (id_montaje=8)
INSERT INTO montaje_mobiliario (cantidad, montaje_id, mobiliario_id) VALUES 
(200, 8, 2),
(25, 8, 5);

-- Salon Platino - Teatro (id_montaje=11)
INSERT INTO montaje_mobiliario (cantidad, montaje_id, mobiliario_id) VALUES 
(500, 11, 2),
(50, 11, 7);

-- Salon Platino - Banquete (id_montaje=13)
INSERT INTO montaje_mobiliario (cantidad, montaje_id, mobiliario_id) VALUES 
(500, 13, 2),
(60, 13, 5);

-- ==========================================
-- 6. EQUIPAMIENTO
-- ==========================================

INSERT INTO equipamiento (nombre, descripcion, costo, stock, tipo_equipa_id) VALUES 
('Proyector HD', 'Proyector de alta definicion 1080p', 800.00, 15, 2),
('Proyector 4K', 'Proyector 4K para presentaciones premium', 1500.00, 5, 2),
('Pantalla de proyeccion 120"', 'Pantalla retractil de 120 pulgadas', 400.00, 10, 2),
('Sistema de sonido portatil', 'Bafles portatiles con microfono inalambrico', 1000.00, 8, 1),
('Microfono inalambrico', 'Microfono de solapa inalambrico', 250.00, 20, 1),
('Microfono de mano', 'Microfono dinamico para escenario', 150.00, 15, 1),
('Bocinas Bluetooth', 'Bocinas portatiles Bluetooth', 300.00, 20, 1),
('Laptop de presentacion', 'Laptop con Office preinstalado', 600.00, 10, 4),
('TV 55"', 'Television 55 pulgadas 4K para exhibicion', 500.00, 8, 2),
('Pantalla LED 90"', 'Pantalla LED gigante para escenario', 2000.00, 3, 2),
('Camara de documentos', 'Camara visualizador para presentaciones', 350.00, 5, 2),
('Spotlight LED', 'Luz de escenario LED 100W', 200.00, 20, 3),
('Torre de iluminacion', 'Torre de iluminacion portable', 350.00, 10, 3),
('Impresora laser', 'Impresora laser blanco y negro', 250.00, 5, 4);

-- Inventario de equipamiento por estado
INSERT INTO inventario_equipa (equipamiento_id, estado_equipa_id, cantidad) VALUES 
(1, 'DISP', 10),
(1, 'FUNC', 5),
(2, 'DISP', 3),
(2, 'FUNC', 2),
(3, 'DISP', 8),
(3, 'FUNC', 2),
(4, 'DISP', 5),
(4, 'FUNC', 3),
(5, 'DISP', 15),
(5, 'FUNC', 5),
(6, 'DISP', 10),
(6, 'FUNC', 5),
(7, 'DISP', 15),
(7, 'FUNC', 5),
(8, 'DISP', 8),
(8, 'FUNC', 2),
(9, 'DISP', 5),
(9, 'FUNC', 3),
(10, 'DISP', 2),
(10, 'FUNC', 1),
(11, 'DISP', 4),
(11, 'FUNC', 1),
(12, 'DISP', 15),
(12, 'FUNC', 5),
(13, 'DISP', 8),
(13, 'FUNC', 2),
(14, 'DISP', 4),
(14, 'FUNC', 1);

-- ==========================================
-- 7. SERVICIOS
-- ==========================================

INSERT INTO servicio (nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES 
('Coffee break basico', 'Cafe, te, agua y galletas', 120.00, TRUE, 1),
('Coffee break premium', 'Cafe, te, jugos, frutas y pasteleria', 250.00, TRUE, 1),
('Comida corrida', 'Menu del dia con entrada, plato fuerte y postre', 350.00, TRUE, 1),
('Bufete completo', 'Bufete con multiple opciones de comida', 600.00, TRUE, 1),
('Servicio de limpieza', 'Limpieza del salon durante el evento', 500.00, TRUE, 8),
('Seguridad privada', 'Guardia de seguridad durante el evento', 800.00, TRUE, 7),
('Decoracion basica', 'Manteles y centros de mesa', 300.00, TRUE, 3),
('Decoracion premium', 'Decoracion completa con flores naturales', 1500.00, TRUE, 3),
('Internet de alta velocidad', 'WiFi de 100 Mbps para el evento', 200.00, TRUE, 10),
('Impresion de materiales', 'Impresion de invitaciones y programas', 150.00, TRUE, 9),
('Servicio de valet parking', 'Estacionamiento con valet', 400.00, TRUE, 4),
('Transporte de invitados', 'Transporte terrestre round trip', 600.00, TRUE, 4),
('Fotografia profesional', 'Sesion fotografica de 4 horas', 2000.00, TRUE, 5),
('Video profesional', 'Grabacion en video de 4 horas', 2500.00, TRUE, 5),
('DJ basico', 'Equipo de musica y DJ por 4 horas', 1500.00, TRUE, 6),
('Banda en vivo', 'Banda de 4 musicos por 3 horas', 5000.00, TRUE, 6);

-- ==========================================
-- 8. TRABAJADORES Y CUENTAS
-- ==========================================

-- Cuentas originales de Firebase (si no existen)
INSERT INTO cuenta (nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES 
('LuisD', 'luisdagallardo@gmail.com', 'ACT', '7A2duPu23vQuxZMLc0xxp2ZS9VX2'),
('Juan', 'juan.perez@email.com', 'ACT', NULL),
('Maria', 'maria.lopez@email.com', 'ACT', NULL),
('Carlos', 'carlos.ramirez@email.com', 'ACT', NULL),
('pepecliente', 'luisd.gramirez@gmail.com', 'ACT', 'P9LmpbBGJEOIDbLrQUASN6BbMIW2'),
('zuanper', 'zuanpergaming@gmail.com', 'ACT', '4xtaJc6nSpPEC4SbphIeoFya6Nk1'),
('Mr pepe', 'zuanperg@gmail.com', 'ACT', 'oYOBceIdXQPVibT4N0N56C68y1L2')
ON CONFLICT (correo_electronico) DO NOTHING;

-- Cuentas de trabajadores (si no existen)
INSERT INTO cuenta (nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES 
('gerardo.aguilar', 'gerardo.aguilar@montecarlo.com', 'ACT', NULL),
('maria.lopez', 'maria.lopez@montecarlo.com', 'ACT', NULL),
('carlos.mendoza', 'carlos.mendoza@montecarlo.com', 'ACT', NULL)
ON CONFLICT (correo_electronico) DO NOTHING;

-- Trabajadores (si no existen)
INSERT INTO trabajador (no_empleado, rfc, nombre, "apellidoPaterno", "apelidoMaterno", telefono, correo_electronico, cuenta_id, rol_id) VALUES 
('EMP001', 'GARC850101HDF', 'Gerardo', 'Aguilar', 'Reyes', '6641234567', 'gerardo.aguilar@montecarlo.com', 8, 'ADMIN'),
('EMP002', 'LOPE900512MDF', 'Maria', 'Lopez', 'Garcia', '6649876543', 'maria.lopez@montecarlo.com', 9, 'COORD'),
('EMP003', 'MENC880215HDF', 'Carlos', 'Mendoza', 'Ruiz', '6645551234', 'carlos.mendoza@montecarlo.com', 10, 'RECEP')
ON CONFLICT (no_empleado) DO NOTHING;

-- ==========================================
-- 9. CLIENTES
-- ==========================================

-- Cuentas de clientes (si no existen)
INSERT INTO cuenta (nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES 
('empresa.techsoft', 'contacto@techsoft.mx', 'ACT', NULL),
('laura.rivas', 'laura.rivas@gmail.com', 'ACT', NULL),
('eventos.corp', 'ventas@eventcorp.com', 'ACT', NULL),
('roberto.gomez', 'roberto.gomez@outlook.com', 'ACT', NULL),
('maria.garcia', 'maria.garcia@yahoo.com', 'ACT', NULL)
ON CONFLICT (correo_electronico) DO NOTHING;

-- Datos de clientes (si no existen)
INSERT INTO datos_cliente (rfc, "nombre_fiscal", nombre, "apellidoPaterno", "apelidoMaterno", telefono, correo_electronico, "dir_colonia", "dir_calle", "dir_numero", tipo_cliente_id, cuenta_id) VALUES 
('TSO150822TX3', 'TechSoft de Mexico S.A. de C.V.', 'TechSoft', 'Sistemas', NULL, '6644443322', 'contacto@techsoft.mx', 'Zona Rio', 'Paseo de los Heroes', '990', 'MOR', 11),
('RIVL920130F12', 'Laura Rivas Gonzalez', 'Laura', 'Rivas', 'Gonzalez', '6641110099', 'laura.rivas@gmail.com', 'Otay', 'Tecnologico', '45', 'FIS', 12),
('ECOR100101ABC', 'Eventos Corporativos SA', 'Eventos', 'Corp', NULL, '6642228877', 'ventas@eventcorp.com', 'Centro', 'Calle 5ta', '88', 'MOR', 13),
('GOMR750615M23', 'Roberto Gomez Lara', 'Roberto', 'Gomez', 'Lara', '6643334455', 'roberto.gomez@outlook.com', 'Playas', 'Paseo Ensenada', '312', 'FIS', 14),
('GARC920405J77', 'Maria Garcia Perez', 'Maria', 'Garcia', 'Perez', '6647778899', 'maria.garcia@yahoo.com', 'Chapultepec', 'Circuito', '150', 'FIS', 15)
ON CONFLICT (correo_electronico) DO NOTHING;

-- ==========================================
-- 10. RESERVACIONES DE EJEMPLO
-- ==========================================

INSERT INTO reservacion ("nombreEvento", "descripEvento", "estimaAsistentes", "fechaReservacion", "fechaEvento", "horaInicio", "horaFin", subtotal, "IVA", total, cliente_id, montaje_id, estado_reserva_id, tipo_evento_id, trabajador_id, "es_paquete", "nombre_paquete") VALUES 
('Conferencia Anual TechSoft 2026', 'Primera conferencia anual de la empresa con keynote y presentaciones tecnicas', 80, '2026-04-01', '2026-04-15', '09:00:00', '18:00:00', 8500.00, 1360.00, 9860.00, 1, 4, 'CONF', 1, 'EMP001', FALSE, ''),

('Cena de Navidad TechSoft', 'Cena de navidad para empleados y familias', 120, '2026-04-01', '2026-04-20', '19:00:00', '23:00:00', 12000.00, 1920.00, 13920.00, 1, 5, 'CONF', 3, 'EMP002', FALSE, ''),

('Junta de Consejo Directivo', 'Reunion trimestral del consejo administrativo', 15, '2026-04-01', '2026-04-18', '10:00:00', '14:00:00', 3500.00, 560.00, 4060.00, 2, 3, 'CONF', 6, 'EMP001', FALSE, ''),

('Lanzamiento de Producto XYZ', 'Evento de lanzamiento de nuevo producto con medios de comunicacion', 200, '2026-04-01', '2026-04-25', '11:00:00', '20:00:00', 25000.00, 4000.00, 29000.00, 3, 6, 'CONF', 4, 'EMP001', FALSE, ''),

('Reunion de trabajo mensual', 'Sesion de planeacion estrategica del equipo', 25, '2026-04-01', '2026-04-22', '09:00:00', '13:00:00', 4000.00, 640.00, 4640.00, 4, 1, 'CONF', 8, 'EMP003', FALSE, ''),

('Seminario de Capacitacion', 'Seminario de capacitacion para personal nuevo', 50, '2026-04-01', '2026-05-10', '08:00:00', '17:00:00', 6000.00, 960.00, 6960.00, 5, 2, 'SOLIC', 2, 'EMP002', FALSE, '');

-- ==========================================
-- 11. HISTORIAL DE ESTADOS DE RESERVACIONES
-- ==========================================

INSERT INTO registr_esta_reserva (reservacion_id, estado_reserva_id, fecha) VALUES 
(1, 'SOLIC', '2026-04-01'),
(1, 'CONF', '2026-04-03'),
(2, 'SOLIC', '2026-04-05'),
(2, 'CONF', '2026-04-07'),
(3, 'SOLIC', '2026-04-08'),
(3, 'CONF', '2026-04-10'),
(4, 'SOLIC', '2026-04-12'),
(4, 'CONF', '2026-04-14'),
(5, 'SOLIC', '2026-04-15'),
(5, 'CONF', '2026-04-17'),
(6, 'SOLIC', '2026-04-18');

-- ==========================================
-- 12. PAGOS
-- ==========================================

INSERT INTO pago (nota, monto, saldo, no_pago, reservacion_id, concepto_pago_id, metodo_pago_id, fecha, hora) VALUES 
('Anticipo 50% - Conferencia TechSoft', 4930.00, 0.00, 1, 1, 'ANTIC', 'TARJE', '2026-04-03', '10:00:00'),
('Liquidacion - Conferencia TechSoft', 4930.00, 0.00, 2, 1, 'LIQUI', 'TRANS', '2026-04-10', '14:00:00'),
('Anticipo 50% - Cena Navidad', 6960.00, 0.00, 1, 2, 'ANTIC', 'TRANS', '2026-04-07', '11:00:00'),
('Liquidacion - Cena Navidad', 6960.00, 0.00, 2, 2, 'LIQUI', 'TRANS', '2026-04-15', '16:00:00'),
('Pago unico - Junta Laura', 4060.00, 0.00, 1, 3, 'LIQUI', 'EFECT', '2026-04-10', '09:00:00'),
('Anticipo 50% - Lanzamiento', 14500.00, 0.00, 1, 4, 'ANTIC', 'TARJE', '2026-04-14', '12:00:00'),
('Liquidacion - Lanzamiento', 14500.00, 0.00, 2, 4, 'LIQUI', 'TRANS', '2026-04-20', '10:00:00'),
('Pago unico - Reunion Roberto', 4640.00, 0.00, 1, 5, 'LIQUI', 'NFC', '2026-04-17', '08:00:00');

-- ==========================================
-- 13. SERVICIOS POR RESERVACION
-- ==========================================

INSERT INTO reserva_servicio (extra, reservacion_id, servicio_id) VALUES 
(FALSE, 1, 1),
(FALSE, 1, 9),
(FALSE, 1, 6),
(FALSE, 2, 2),
(FALSE, 2, 4),
(FALSE, 2, 7),
(FALSE, 3, 1),
(FALSE, 4, 2),
(FALSE, 4, 8),
(FALSE, 4, 13),
(FALSE, 4, 15),
(FALSE, 5, 1),
(FALSE, 6, 1);

-- ==========================================
-- 14. EQUIPAMIENTO POR RESERVACION
-- ==========================================

INSERT INTO reserva_equipa (cantidad, extra, completado, reservacion_id, equipamiento_id) VALUES 
(2, FALSE, FALSE, 1, 1),
(1, FALSE, FALSE, 1, 4),
(1, FALSE, FALSE, 1, 5),
(1, FALSE, FALSE, 2, 3),
(2, FALSE, FALSE, 2, 7),
(1, FALSE, FALSE, 3, 1),
(1, FALSE, FALSE, 4, 2),
(1, FALSE, FALSE, 4, 9),
(2, FALSE, FALSE, 4, 4),
(1, FALSE, FALSE, 4, 5),
(1, FALSE, FALSE, 5, 1),
(1, FALSE, FALSE, 6, 1);

-- ==========================================
-- 15. REGISTROS DE ESTADO DE SALONES
-- ==========================================

INSERT INTO registr_esta_salon (salon_id, estado_salon_id, fecha) VALUES 
(1, 'DIS', '2026-04-01'),
(2, 'DIS', '2026-04-01'),
(3, 'DIS', '2026-04-01'),
(4, 'DIS', '2026-04-01'),
(5, 'DIS', '2026-04-01'),
(6, 'DIS', '2026-04-01');

COMMIT;
