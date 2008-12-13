--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: continent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: poab
--

SELECT pg_catalog.setval('continent_id_seq', 7, true);


--
-- Data for Name: continent; Type: TABLE DATA; Schema: public; Owner: poab
--

COPY continent (id, name) FROM stdin;
1	Africa
2	Asia
3	Europa
4	South America
5	North America
6	Antarctica
7	Australia and Oceania
\.


--
-- PostgreSQL database dump complete
--

