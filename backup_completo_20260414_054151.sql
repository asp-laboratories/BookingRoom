-- ========================================
-- BACKUP SELECTIVO BOOKINGROOM
-- Fecha: 2026-04-14 05:41:51
-- ========================================

BEGIN;


-- ========================================
-- Backup de tabla: rol
-- Total registros: 4
-- ========================================

INSERT INTO rol (codigo, nombre) VALUES ('ADMIN', 'Administrador');
INSERT INTO rol (codigo, nombre) VALUES ('COORD', 'Coordinador');
INSERT INTO rol (codigo, nombre) VALUES ('RECEP', 'Recepcionista');
INSERT INTO rol (codigo, nombre) VALUES ('ALMAC', 'Almacen');


-- ========================================
-- Backup de tabla: estado_cuenta
-- Total registros: 3
-- ========================================

INSERT INTO estado_cuenta (codigo, nombre) VALUES ('ACT', 'Activa');
INSERT INTO estado_cuenta (codigo, nombre) VALUES ('SUSPE', 'Suspendida');
INSERT INTO estado_cuenta (codigo, nombre) VALUES ('BANEO', 'Bloqueada');


-- ========================================
-- Backup de tabla: tipo_cliente
-- Total registros: 4
-- ========================================

INSERT INTO tipo_cliente (codigo, nombre, disposicion) VALUES ('MOR', 'Persona moral', TRUE);
INSERT INTO tipo_cliente (codigo, nombre, disposicion) VALUES ('FIS', 'Persona fisica', TRUE);
INSERT INTO tipo_cliente (codigo, nombre, disposicion) VALUES ('PM', 'Persona Moral', TRUE);
INSERT INTO tipo_cliente (codigo, nombre, disposicion) VALUES ('PF', 'Persona Fisica', TRUE);


-- ========================================
-- Backup de tabla: estado_mobil
-- Total registros: 4
-- ========================================

INSERT INTO estado_mobil (codigo, nombre) VALUES ('DISP', 'Disponible');
INSERT INTO estado_mobil (codigo, nombre) VALUES ('OCUP', 'Ocupado');
INSERT INTO estado_mobil (codigo, nombre) VALUES ('RESV', 'Reservado');
INSERT INTO estado_mobil (codigo, nombre) VALUES ('REPAR', 'En reparacion');


-- ========================================
-- Backup de tabla: caracter_mobi
-- Total registros: 1
-- ========================================

INSERT INTO caracter_mobi (id, descripcion) VALUES (1, 'Aaaa');


-- ========================================
-- Backup de tabla: tipo_mobil
-- Total registros: 5
-- ========================================

INSERT INTO tipo_mobil (id, nombre, disposicion) VALUES (1, 'Sillas', TRUE);
INSERT INTO tipo_mobil (id, nombre, disposicion) VALUES (2, 'Mesas Redondas', TRUE);
INSERT INTO tipo_mobil (id, nombre, disposicion) VALUES (3, 'Mesas Rectangulares', TRUE);
INSERT INTO tipo_mobil (id, nombre, disposicion) VALUES (4, 'Taburetes', TRUE);
INSERT INTO tipo_mobil (id, nombre, disposicion) VALUES (5, 'Podios', TRUE);


-- ========================================
-- Backup de tabla: tipo_montaje
-- Total registros: 7
-- ========================================

INSERT INTO tipo_montaje (id, nombre, disposicion, capacidadIdeal) VALUES (1, 'Teatro', TRUE, 100);
INSERT INTO tipo_montaje (id, nombre, disposicion, capacidadIdeal) VALUES (2, 'Escuela', TRUE, 60);
INSERT INTO tipo_montaje (id, nombre, disposicion, capacidadIdeal) VALUES (3, 'Banquete', TRUE, 80);
INSERT INTO tipo_montaje (id, nombre, disposicion, capacidadIdeal) VALUES (4, 'Recepcion', TRUE, 150);
INSERT INTO tipo_montaje (id, nombre, disposicion, capacidadIdeal) VALUES (5, 'Imperial', TRUE, 40);
INSERT INTO tipo_montaje (id, nombre, disposicion, capacidadIdeal) VALUES (6, 'Herradura', TRUE, 50);
INSERT INTO tipo_montaje (id, nombre, disposicion, capacidadIdeal) VALUES (7, 'Mesa rusa', TRUE, 30);


-- ========================================
-- Backup de tabla: tipo_evento
-- Total registros: 11
-- ========================================

INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (1, 'Conferencia', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (2, 'Seminario', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (3, 'Cena de empresa', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (4, 'Lanzamiento de producto', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (5, 'Boda', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (6, 'Junta de consejo', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (7, 'Asamblea', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (8, 'Reunion de trabajo', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (9, 'Fiesta', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (10, 'Otro', TRUE);
INSERT INTO tipo_evento (id, nombre, disposicion) VALUES (11, 'Paquete', TRUE);


-- ========================================
-- Backup de tabla: estado_reserva
-- Total registros: 9
-- ========================================

INSERT INTO estado_reserva (codigo, nombre) VALUES ('SOLIC', 'Solicitada');
INSERT INTO estado_reserva (codigo, nombre) VALUES ('PEN', 'Pendiente');
INSERT INTO estado_reserva (codigo, nombre) VALUES ('CONF', 'Confirmada');
INSERT INTO estado_reserva (codigo, nombre) VALUES ('CON', 'Confirmada');
INSERT INTO estado_reserva (codigo, nombre) VALUES ('ENPRO', 'En proceso');
INSERT INTO estado_reserva (codigo, nombre) VALUES ('FIN', 'Finalizada');
INSERT INTO estado_reserva (codigo, nombre) VALUES ('CAN', 'Cancelada');
INSERT INTO estado_reserva (codigo, nombre) VALUES ('PAGAD', 'Pagada');
INSERT INTO estado_reserva (codigo, nombre) VALUES ('PLANT', 'Plantilla');


-- ========================================
-- Backup de tabla: estado_salon
-- Total registros: 5
-- ========================================

INSERT INTO estado_salon (codigo, nombre) VALUES ('DIS', 'Disponible');
INSERT INTO estado_salon (codigo, nombre) VALUES ('RESV', 'Reservado');
INSERT INTO estado_salon (codigo, nombre) VALUES ('OCUP', 'Ocupado');
INSERT INTO estado_salon (codigo, nombre) VALUES ('MANTE', 'En mantenimiento');
INSERT INTO estado_salon (codigo, nombre) VALUES ('LIMPI', 'En limpieza');


-- ========================================
-- Backup de tabla: tipo_equipa
-- Total registros: 6
-- ========================================

INSERT INTO tipo_equipa (id, nombre, disposicion) VALUES (1, 'Audio', TRUE);
INSERT INTO tipo_equipa (id, nombre, disposicion) VALUES (2, 'Video', TRUE);
INSERT INTO tipo_equipa (id, nombre, disposicion) VALUES (3, 'Iluminacion', TRUE);
INSERT INTO tipo_equipa (id, nombre, disposicion) VALUES (4, 'Computo', TRUE);
INSERT INTO tipo_equipa (id, nombre, disposicion) VALUES (5, 'Mobiliario extra', TRUE);
INSERT INTO tipo_equipa (id, nombre, disposicion) VALUES (6, 'Otro', TRUE);


-- ========================================
-- Backup de tabla: estado_equipa
-- Total registros: 5
-- ========================================

INSERT INTO estado_equipa (codigo, nombre) VALUES ('DISP', 'Disponible');
INSERT INTO estado_equipa (codigo, nombre) VALUES ('FUNC', 'Funcional');
INSERT INTO estado_equipa (codigo, nombre) VALUES ('DANAD', 'Daniado');
INSERT INTO estado_equipa (codigo, nombre) VALUES ('REPAR', 'En reparacion');
INSERT INTO estado_equipa (codigo, nombre) VALUES ('RESV', 'Reservado');


-- ========================================
-- Backup de tabla: concepto_pago
-- Total registros: 5
-- ========================================

INSERT INTO concepto_pago (codigo, nombre) VALUES ('ANTIC', 'Anticipo');
INSERT INTO concepto_pago (codigo, nombre) VALUES ('LIQUI', 'Liquidacion');
INSERT INTO concepto_pago (codigo, nombre) VALUES ('EXTR', 'Extra');
INSERT INTO concepto_pago (codigo, nombre) VALUES ('ABONO', 'Abono');
INSERT INTO concepto_pago (codigo, nombre) VALUES ('PENAL', 'Penalizacion');


-- ========================================
-- Backup de tabla: metodo_pago
-- Total registros: 5
-- ========================================

INSERT INTO metodo_pago (codigo, nombre) VALUES ('EFECT', 'Efectivo');
INSERT INTO metodo_pago (codigo, nombre) VALUES ('TRANS', 'Transferencia');
INSERT INTO metodo_pago (codigo, nombre) VALUES ('TARJE', 'Tarjeta');
INSERT INTO metodo_pago (codigo, nombre) VALUES ('NFC', 'NFC');
INSERT INTO metodo_pago (codigo, nombre) VALUES ('CHEQU', 'Cheque');


-- ========================================
-- Backup de tabla: tipo_servicio
-- Total registros: 10
-- ========================================

INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (1, 'Catering', 'Servicios de comida', TRUE);
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (2, 'Audiovisual', 'Equipos AV', TRUE);
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (3, 'Decoracion', 'Decoracion', TRUE);
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (4, 'Transporte', 'Transporte', TRUE);
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (5, 'Fotografia', 'Foto', TRUE);
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (6, 'Musica', 'Musica', TRUE);
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (7, 'Seguridad', 'Seguridad', TRUE);
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (8, 'Limpieza', 'Limpieza', TRUE);
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (9, 'Otro', 'Otros', TRUE);
INSERT INTO tipo_servicio (id, nombre, descripcion, disposicion) VALUES (10, 'Internet', 'Internet', TRUE);


-- ========================================
-- Backup de tabla: cuenta
-- Total registros: 14
-- ========================================

INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (2, 'Juan', 'juan.perez@email.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (3, 'Maria', 'maria.lopez@email.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (4, 'Carlos', 'carlos.ramirez@email.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (5, 'pepecliente', 'luisd.gramirez@gmail.com', 'ACT', 'P9LmpbBGJEOIDbLrQUASN6BbMIW2');
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (8, 'gerardo.aguilar', 'gerardo.aguilar@montecarlo.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (9, 'maria.lopez', 'maria.lopez@montecarlo.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (10, 'carlos.mendoza', 'carlos.mendoza@montecarlo.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (11, 'empresa.techsoft', 'contacto@techsoft.mx', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (12, 'laura.rivas', 'laura.rivas@gmail.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (13, 'eventos.corp', 'ventas@eventcorp.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (14, 'roberto.gomez', 'roberto.gomez@outlook.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (15, 'maria.garcia', 'maria.garcia@yahoo.com', 'ACT', NULL);
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (16, 'Davidgr', 'ldavidgrdrmz@gmail.com', 'ACT', 'qOO2959VXKQdlbsZLcGwBJ1wvyB3');
INSERT INTO cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) VALUES (1, 'LuisDgr', 'luisdagallardo@gmail.com', 'ACT', '7A2duPu23vQuxZMLc0xxp2ZS9VX2');


-- ========================================
-- Backup de tabla: trabajador
-- Total registros: 5
-- ========================================

INSERT INTO trabajador (no_empleado, rfc, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, cuenta_id, rol_id) VALUES ('EMP001', 'GARC850101HDF', 'Gerardo', 'Aguilar', 'Reyes', '6641234567', 'gerardo.aguilar@montecarlo.com', 8, 'ADMIN');
INSERT INTO trabajador (no_empleado, rfc, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, cuenta_id, rol_id) VALUES ('EMP002', 'LOPE900512MDF', 'Maria', 'Lopez', 'Garcia', '6649876543', 'maria.lopez@montecarlo.com', 9, 'COORD');
INSERT INTO trabajador (no_empleado, rfc, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, cuenta_id, rol_id) VALUES ('EMP003', 'MENC880215HDF', 'Carlos', 'Mendoza', 'Ruiz', '6645551234', 'carlos.mendoza@montecarlo.com', 10, 'RECEP');
INSERT INTO trabajador (no_empleado, rfc, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, cuenta_id, rol_id) VALUES ('A-12345', 'ABCABC7891023', 'Luis David', 'Gallardo', 'Ramirez', '6632181610', 'luisdagallardo@gmail.com', 1, 'ADMIN');
INSERT INTO trabajador (no_empleado, rfc, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, cuenta_id, rol_id) VALUES ('M-28281', '9876543210123', 'David', 'Gallardo', 'Ramirez', '6002001919', 'ldavidgrdrmz@gmail.com', 16, 'ALMAC');


-- ========================================
-- Backup de tabla: datos_cliente
-- Total registros: 6
-- ========================================

INSERT INTO datos_cliente (id, rfc, nombre_fiscal, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, cuenta_id, tipo_cliente_id) VALUES (1, 'TSO150822TX3', 'TechSoft de Mexico S.A. de C.V.', 'TechSoft', 'Sistemas', NULL, '6644443322', 'contacto@techsoft.mx', 'Zona Rio', 'Paseo de los Heroes', '990', 11, 'MOR');
INSERT INTO datos_cliente (id, rfc, nombre_fiscal, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, cuenta_id, tipo_cliente_id) VALUES (2, 'RIVL920130F12', 'Laura Rivas Gonzalez', 'Laura', 'Rivas', 'Gonzalez', '6641110099', 'laura.rivas@gmail.com', 'Otay', 'Tecnologico', '45', 12, 'FIS');
INSERT INTO datos_cliente (id, rfc, nombre_fiscal, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, cuenta_id, tipo_cliente_id) VALUES (3, 'ECOR100101ABC', 'Eventos Corporativos SA', 'Eventos', 'Corp', NULL, '6642228877', 'ventas@eventcorp.com', 'Centro', 'Calle 5ta', '88', 13, 'MOR');
INSERT INTO datos_cliente (id, rfc, nombre_fiscal, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, cuenta_id, tipo_cliente_id) VALUES (4, 'GOMR750615M23', 'Roberto Gomez Lara', 'Roberto', 'Gomez', 'Lara', '6643334455', 'roberto.gomez@outlook.com', 'Playas', 'Paseo Ensenada', '312', 14, 'FIS');
INSERT INTO datos_cliente (id, rfc, nombre_fiscal, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, cuenta_id, tipo_cliente_id) VALUES (5, 'GARC920405J77', 'Maria Garcia Perez', 'Maria', 'Garcia', 'Perez', '6647778899', 'maria.garcia@yahoo.com', 'Chapultepec', 'Circuito', '150', 15, 'FIS');
INSERT INTO datos_cliente (id, rfc, nombre_fiscal, nombre, apellidoPaterno, apelidoMaterno, telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, cuenta_id, tipo_cliente_id) VALUES (6, 'ABAB1234578', 'Salvador  Gallardo Ramirez ', 'Salvador ', 'Gallardo', 'Ramirez ', '6632021919', 'luisd.gramirez@gmail.com', 'Los reyes ', 'los reyes sur ', '20', 5, 'FIS');


-- ========================================
-- Backup de tabla: servicio
-- Total registros: 16
-- ========================================

INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (1, 'Coffee break basico', 'Cafe, te, agua y galletas', 120.00, TRUE, 1);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (2, 'Coffee break premium', 'Cafe, te, jugos, frutas y pasteleria', 250.00, TRUE, 1);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (3, 'Comida corrida', 'Menu del dia con entrada, plato fuerte y postre', 350.00, TRUE, 1);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (4, 'Bufete completo', 'Bufete con multiple opciones de comida', 600.00, TRUE, 1);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (5, 'Servicio de limpieza', 'Limpieza del salon durante el evento', 500.00, TRUE, 8);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (6, 'Seguridad privada', 'Guardia de seguridad durante el evento', 800.00, TRUE, 7);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (7, 'Decoracion basica', 'Manteles y centros de mesa', 300.00, TRUE, 3);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (8, 'Decoracion premium', 'Decoracion completa con flores naturales', 1500.00, TRUE, 3);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (9, 'Internet de alta velocidad', 'WiFi de 100 Mbps para el evento', 200.00, TRUE, 10);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (10, 'Impresion de materiales', 'Impresion de invitaciones y programas', 150.00, TRUE, 9);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (11, 'Servicio de valet parking', 'Estacionamiento con valet', 400.00, TRUE, 4);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (12, 'Transporte de invitados', 'Transporte terrestre round trip', 600.00, TRUE, 4);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (13, 'Fotografia profesional', 'Sesion fotografica de 4 horas', 2000.00, TRUE, 5);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (14, 'Video profesional', 'Grabacion en video de 4 horas', 2500.00, TRUE, 5);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (15, 'DJ basico', 'Equipo de musica y DJ por 4 horas', 1500.00, TRUE, 6);
INSERT INTO servicio (id, nombre, descripcion, costo, disposicion, tipo_servicio_id) VALUES (16, 'Banda en vivo', 'Banda de 4 musicos por 3 horas', 5000.00, TRUE, 6);


-- ========================================
-- Backup de tabla: equipamiento
-- Total registros: 14
-- ========================================

INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (1, 'Proyector HD', 'Proyector de alta definicion 1080p', 800.00, 15, 2);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (2, 'Proyector 4K', 'Proyector 4K para presentaciones premium', 1500.00, 5, 2);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (3, 'Pantalla de proyeccion 120"', 'Pantalla retractil de 120 pulgadas', 400.00, 10, 2);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (4, 'Sistema de sonido portatil', 'Bafles portatiles con microfono inalambrico', 1000.00, 8, 1);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (6, 'Microfono de mano', 'Microfono dinamico para escenario', 150.00, 15, 1);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (7, 'Bocinas Bluetooth', 'Bocinas portatiles Bluetooth', 300.00, 20, 1);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (8, 'Laptop de presentacion', 'Laptop con Office preinstalado', 600.00, 10, 4);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (9, 'TV 55"', 'Television 55 pulgadas 4K para exhibicion', 500.00, 8, 2);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (10, 'Pantalla LED 90"', 'Pantalla LED gigante para escenario', 2000.00, 3, 2);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (11, 'Camara de documentos', 'Camara visualizador para presentaciones', 350.00, 5, 2);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (12, 'Spotlight LED', 'Luz de escenario LED 100W', 200.00, 20, 3);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (13, 'Torre de iluminacion', 'Torre de iluminacion portable', 350.00, 10, 3);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (14, 'Impresora laser', 'Impresora laser blanco y negro', 250.00, 5, 4);
INSERT INTO equipamiento (id, nombre, descripcion, costo, stock, tipo_equipa_id) VALUES (5, 'Microfono inalambrico', 'Microfono de solapa inalambrico', 250.00, 20, 1);


-- ========================================
-- Backup de tabla: mobiliario
-- Total registros: 10
-- ========================================

INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (1, 'Silla plegable', 'Silla plegable de plastico resistente', 25.00, 500, 1);
INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (3, 'Silla vintage', 'Silla de madera con tapizado de tela', 200.00, 200, 1);
INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (4, 'Mesa redonda 1.5m', 'Mesa redonda para 8 personas', 180.00, 200, 2);
INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (5, 'Mesa redonda 1.8m', 'Mesa redonda para 10 personas', 220.00, 200, 2);
INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (6, 'Mesa rectangular 2m', 'Mesa rectangular para 10 personas', 200.00, 200, 3);
INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (7, 'Mesa rectangular 3m', 'Mesa rectangular para 15 personas', 280.00, 200, 3);
INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (8, 'Taburete alto', 'Taburete para barra de 80cm', 80.00, 200, 4);
INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (9, 'Taburete bajo', 'Taburete para barra de 60cm', 70.00, 200, 4);
INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (10, 'Podio ejecutivo', 'Podio de madera con microphone', 500.00, 200, 5);
INSERT INTO mobiliario (id, nombre, descripcion, costo, stock, tipo_movil_id) VALUES (2, 'Silla ejecutiva', 'Silla con descansabrazos y soporte lumbar', 150.00, 15000, 1);


-- ========================================
-- Backup de tabla: salon
-- Total registros: 11
-- ========================================

INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (2, 'Vivaldi I', 1800.00, 'Planta Baja - Ala Norte', 9.00, 3.60, 3.60, 32.40, 60, 'DIS');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (4, 'Vivaldi III', 1800.00, 'Planta Baja - Ala Norte', 9.00, 3.60, 3.60, 32.40, 70, 'DIS');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (5, 'Vivaldi IV', 1800.00, 'Planta Baja - Ala Norte', 9.00, 3.60, 3.60, 32.40, 70, 'DIS');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (6, 'Shubert', 4500.00, 'Piso 1 - Centro', 17.00, 9.00, 6.10, 153.00, 180, 'DIS');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (8, 'Beethoven', 5000.00, 'Piso 1 - Este', 17.00, 10.00, 7.90, 170.00, 180, 'DIS');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (9, 'Gran Vivaldi', 6000.00, 'Planta Baja - Gran Salon', 9.00, 24.00, 5.30, 216.00, 60, 'DIS');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (10, 'Chopin', 7500.00, 'Piso 2 - Oeste', 9.00, 25.00, 3.60, 225.00, 250, 'DIS');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (11, 'Gran Mozart', 12000.00, 'Planta Baja - Acceso Principal', 28.00, 17.00, 6.10, 476.00, 700, 'DIS');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (1, 'Vivaldi V', 1500.00, 'Planta Baja - Ala Norte', 9.00, 3.60, 3.60, 32.40, 40, 'LIMPI');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (7, 'Mozart', 4500.00, 'Piso 1 - Centro', 17.00, 9.00, 3.80, 153.00, 180, 'LIMPI');
INSERT INTO salon (id, nombre, costo, ubicacion, dimenLargo, dimenAncho, dimenAlto, metrosCuadrados, maxCapacidad, estado_salon_id) VALUES (3, 'Vivaldi II', 1800.00, 'Planta Baja - Ala Norte', 9.00, 3.60, 3.60, 32.40, 70, 'LIMPI');


-- ========================================
-- Backup de tabla: inventario_mobil
-- Total registros: 22
-- ========================================

INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (16, 1, 'RESV', 1);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (7, 49, 'DISP', 8);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (46, 1, 'OCUP', 8);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (9, 8, 'DISP', 10);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (21, 1, 'RESV', 10);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (15, 2, 'OCUP', 10);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (22, 1, 'RESV', 7);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (4, 0, 'DISP', 5);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (26, 40, 'OCUP', 5);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (2, 0, 'DISP', 2);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (38, 100, 'OCUP', 2);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (8, 21, 'DISP', 9);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (47, 4, 'OCUP', 9);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (1, 394, 'DISP', 1);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (14, 205, 'OCUP', 1);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (3, 54, 'DISP', 4);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (48, 4, 'OCUP', 4);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (5, 72, 'DISP', 6);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (36, 8, 'OCUP', 6);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (6, 25, 'DISP', 7);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (37, 4, 'OCUP', 7);
INSERT INTO inventario_mobil (id, cantidad, estado_mobil_id, mobiliario_id) VALUES (41, 1, 'REPAR', 9);


-- ========================================
-- Backup de tabla: inventario_equipa
-- Total registros: 39
-- ========================================

INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (1, 10, 1, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (2, 5, 1, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (4, 2, 2, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (5, 8, 3, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (6, 2, 3, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (8, 3, 4, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (10, 5, 5, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (12, 5, 6, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (14, 5, 7, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (16, 2, 8, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (20, 1, 10, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (22, 1, 11, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (23, 15, 12, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (24, 5, 12, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (26, 2, 13, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (28, 1, 14, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (11, 9, 6, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (29, 1, 6, 'RESV');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (27, 3, 14, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (31, 1, 14, 'RESV');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (9, 0, 5, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (40, 15, 5, 'RESV');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (13, 12, 7, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (30, 3, 7, 'RESV');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (7, 4, 4, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (3, 2, 2, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (41, 1, 2, 'REPAR');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (18, 2, 9, 'FUNC');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (42, 1, 9, 'REPAR');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (15, 4, 8, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (47, 4, 8, 'RESV');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (25, 7, 13, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (49, 1, 13, 'RESV');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (21, 3, 11, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (52, 1, 11, 'RESV');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (19, 0, 10, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (48, 2, 10, 'RESV');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (17, 0, 9, 'DISP');
INSERT INTO inventario_equipa (id, cantidad, equipamiento_id, estado_equipa_id) VALUES (53, 5, 9, 'RESV');


COMMIT;

-- ========================================
-- BACKUP COMPLETADO
-- Total de registros respaldados: 221
-- Fecha: 2026-04-14 05:41:51
-- ========================================
