-- ========================================
-- EXPORTACIÓN DE USUARIOS
-- Fecha: 2026-04-14 06:56:10
-- ========================================

BEGIN;

-- Insertar con ON CONFLICT para evitar duplicados
--
-- PostgreSQL database dump
--

\restrict U67WsBXEQVwnU4ndMqmBDW9JWmORAEOqUlzRtsEJ0ZTd2NFmN6rgfjHsaxqPJuA

-- Dumped from database version 18.2
-- Dumped by pg_dump version 18.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: estado_cuenta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.estado_cuenta (codigo, nombre) FROM stdin;
ACT	Activa
SUSPE	Suspendida
BANEO	Bloqueada
\.


--
-- Data for Name: cuenta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cuenta (id, nombre_usuario, correo_electronico, estado_cuenta_id, firebase_uid) FROM stdin;
2	Juan	juan.perez@email.com	ACT	\N
3	Maria	maria.lopez@email.com	ACT	\N
4	Carlos	carlos.ramirez@email.com	ACT	\N
5	pepecliente	luisd.gramirez@gmail.com	ACT	P9LmpbBGJEOIDbLrQUASN6BbMIW2
8	gerardo.aguilar	gerardo.aguilar@montecarlo.com	ACT	\N
9	maria.lopez	maria.lopez@montecarlo.com	ACT	\N
10	carlos.mendoza	carlos.mendoza@montecarlo.com	ACT	\N
11	empresa.techsoft	contacto@techsoft.mx	ACT	\N
12	laura.rivas	laura.rivas@gmail.com	ACT	\N
13	eventos.corp	ventas@eventcorp.com	ACT	\N
14	roberto.gomez	roberto.gomez@outlook.com	ACT	\N
15	maria.garcia	maria.garcia@yahoo.com	ACT	\N
16	Davidgr	ldavidgrdrmz@gmail.com	ACT	qOO2959VXKQdlbsZLcGwBJ1wvyB3
1	LuisDgr	luisdagallardo@gmail.com	ACT	7A2duPu23vQuxZMLc0xxp2ZS9VX2
\.


--
-- Data for Name: tipo_cliente; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipo_cliente (codigo, nombre, disposicion) FROM stdin;
MOR	Persona moral	t
FIS	Persona fisica	t
PM	Persona Moral	t
PF	Persona Fisica	t
\.


--
-- Data for Name: datos_cliente; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.datos_cliente (id, rfc, nombre_fiscal, nombre, "apellidoPaterno", "apelidoMaterno", telefono, correo_electronico, dir_colonia, dir_calle, dir_numero, cuenta_id, tipo_cliente_id) FROM stdin;
1	TSO150822TX3	TechSoft de Mexico S.A. de C.V.	TechSoft	Sistemas	\N	6644443322	contacto@techsoft.mx	Zona Rio	Paseo de los Heroes	990	11	MOR
2	RIVL920130F12	Laura Rivas Gonzalez	Laura	Rivas	Gonzalez	6641110099	laura.rivas@gmail.com	Otay	Tecnologico	45	12	FIS
3	ECOR100101ABC	Eventos Corporativos SA	Eventos	Corp	\N	6642228877	ventas@eventcorp.com	Centro	Calle 5ta	88	13	MOR
4	GOMR750615M23	Roberto Gomez Lara	Roberto	Gomez	Lara	6643334455	roberto.gomez@outlook.com	Playas	Paseo Ensenada	312	14	FIS
5	GARC920405J77	Maria Garcia Perez	Maria	Garcia	Perez	6647778899	maria.garcia@yahoo.com	Chapultepec	Circuito	150	15	FIS
6	ABAB1234578	Salvador  Gallardo Ramirez 	Salvador 	Gallardo	Ramirez 	6632021919	luisd.gramirez@gmail.com	Los reyes 	los reyes sur 	20	5	FIS
\.


--
-- Data for Name: rol; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.rol (codigo, nombre) FROM stdin;
ADMIN	Administrador
COORD	Coordinador
RECEP	Recepcionista
ALMAC	Almacen
\.


--
-- Data for Name: trabajador; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trabajador (no_empleado, rfc, nombre, "apellidoPaterno", "apelidoMaterno", telefono, correo_electronico, cuenta_id, rol_id) FROM stdin;
EMP001	GARC850101HDF	Gerardo	Aguilar	Reyes	6641234567	gerardo.aguilar@montecarlo.com	8	ADMIN
EMP002	LOPE900512MDF	Maria	Lopez	Garcia	6649876543	maria.lopez@montecarlo.com	9	COORD
EMP003	MENC880215HDF	Carlos	Mendoza	Ruiz	6645551234	carlos.mendoza@montecarlo.com	10	RECEP
A-12345	ABCABC7891023	Luis David	Gallardo	Ramirez	6632181610	luisdagallardo@gmail.com	1	ADMIN
M-28281	9876543210123	David	Gallardo	Ramirez	6002001919	ldavidgrdrmz@gmail.com	16	ALMAC
\.


--
-- Name: cuenta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cuenta_id_seq', 16, true);


--
-- Name: datos_cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.datos_cliente_id_seq', 6, true);


--
-- PostgreSQL database dump complete
--

\unrestrict U67WsBXEQVwnU4ndMqmBDW9JWmORAEOqUlzRtsEJ0ZTd2NFmN6rgfjHsaxqPJuA


COMMIT;
