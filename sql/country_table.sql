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
-- Name: country_iso_numcode_seq; Type: SEQUENCE SET; Schema: public; Owner: poab
--

SELECT pg_catalog.setval('country_iso_numcode_seq', 2, true);


--
-- Data for Name: country; Type: TABLE DATA; Schema: public; Owner: poab
--

COPY country (iso_numcode, continent_id, iso_countryname, iso3_nationalcode, flickr_countryname) FROM stdin;
548	7	Vanuatu	VUT	Vanuatu
638	1	Réunion	REU	\N
238	4	Falkland Islands (Malvinas)	FLK	Falkland Islands
634	5	Qatar	QAT	Qatar
642	3	Romania	ROU	Romania
608	5	Philippines	PHL	Philippines
630	4	Puerto Rico	PRI	Puerto Rico
600	4	Paraguay	PRY	Paraguay
585	5	Palau	PLW	Palau
604	4	Peru	PER	Peru
484	5	Mexico	MEX	Mexico
533	5	Aruba	ABW	Aruba
254	4	French Guyana	GUF	French Guyana
512	5	Oman	OMN	Oman
586	5	Pakistan	PAK	Pakistan
558	4	Nicaragua	NIC	Nicaragua
547	7	Norfolk Islands	NFK	\N
414	5	Kuwait	KWT	Kuwait
562	1	Niger	NER	Niger
316	2	Guam	GUM	Guam
540	7	New Caledonia	NCL	New Caledonia
520	7	Nauru	NRU	Nauru
554	7	New Zealand	NZL	New Zealand
598	7	Papua New Guinea	PNG	Papua New Guinea
744	5	Svalbard and Jan Mayen	SJM	Svalbard and Jan Mayen
508	1	Mozambique	MOZ	Mozambique
516	1	Namibia	NAM	Namibia
175	1	Mayotte	MYT	Mayotte
524	5	Nepal	NPL	Nepal
498	3	Moldova	MDA	Moldova
492	3	Monaco	MCO	Monaco
496	5	Mongolia	MNG	Mongolia
466	1	Mali	MLI	Mali
584	5	Marshall Islands	MHL	Marshall Islands
480	1	Mauritius	MUS	Mauritius
500	5	Montserrat	MSR	Montserrat
583	7	Micronesia	FSM	Federated States of Micronesia
434	1	Libya	LBY	Libya
454	1	Malawi	MWI	Malawi
458	5	Malaysia	MYS	Malaysia
462	5	Maldives	MDV	Maldives
446	5	Macao	MAC	Macao
417	5	Kyrgyzstan	KGZ	Kyrgyzstan
422	5	Lebanon	LBN	Lebanon
426	1	Lesotho	LSO	Lesotho
430	1	Liberia	LBR	Liberia
398	3	Kazakhstan	KAZ	Kazakhstan
404	1	Kenya	KEN	Kenya
408	5	North Korea	PRK	North Korea
410	5	South Korea	KOR	South Korea
570	7	Niue	NIU	Niue
364	2	Iran	IRN	Iran
292	3	Gibraltar	GIB	Gibraltar
368	2	Iraq	IRQ	Iraq
376	2	Israel	ISR	Israel
388	5	Jamaica	JAM	Jamaica
392	2	Japan	JPN	Japan
344	2	Hong Kong	HKG	Hongkong
474	5	Martinique	MTQ	Martinique
50	2	Bangladesh	BGD	Bangladesh
320	5	Guatemala	GTM	Guatemala
324	1	Guinea	GIN	Guinea
332	5	Haiti	HTI	Haiti
340	5	Honduras	HND	Honduras
356	2	India	IND	India
270	1	Gambia	GMB	Gambia
226	1	Equatorial Guinea	GNQ	Equatorial Guinea
268	3	Georgia	GEO	Georgia
288	1	Ghana	GHA	Ghana
304	5	Greenland	GRL	Greenland
308	3	Grenada	GRD	Grenada
232	1	Eritrea	ERI	Eritrea
231	1	Ethiopia	ETH	Ethiopia
242	5	Fiji	FJI	Fiji
12	1	Algeria	DZA	Algeria
72	1	Botswana	BWA	Botswana
24	1	Angola	AGO	Angola
266	1	Gabon	GAB	Gabon
312	5	Guadeloupe	GLP	Guadeloupe
32	4	Argentina	ARG	Argentina
51	3	Armenia	ARM	Armenia
170	4	Colombia	COL	Colombia
36	7	Australia	AUS	Australia
52	5	Barbados	BRB	Barbados
86	2	British Indian Ocean Territory	IOT	British Indian Ocean Territory
31	3	Azerbaijan	AZE	Azerbaijan
112	3	Belarus	BLR	Belarus
84	5	Belize	BLZ	Belize
204	1	Benin	BEN	Benin
136	5	Cayman Islands	CYM	Cayman Islands
178	1	Congo	COG	Congo
60	5	Bermuda	BMU	Bermuda
140	1	Central African Republic	CAF	Central African Republic
100	3	Bulgaria	BGR	Bulgaria
148	1	Chad	TCD	Chad
108	1	Burundi	BDI	Burundi
116	2	Cambodia	KHM	Cambodia
64	2	Bhutan	BTN	Bhutan
120	1	Cameroon	CMR	Cameroon
192	5	Cuba	CUB	Cuba
152	4	Chile	CHL	Chile
262	1	Djibouti	DJI	Djibouti
156	2	China	CHN	China
174	1	Comoros	COM	Comoros
124	5	Canada	CAN	Canada
68	4	Bolivia	BOL	Bolivia
214	5	Dominican Republic	DOM	Dominican Republic
218	4	Ecuador	ECU	Ecuador
222	5	El Salvador	SLV	El Salvador
44	5	Bahamas	BHS	Bahamas
92	5	British Virgin Islands	VGB	British Virgin Islands
10	6	Antarctica	ATA	Antarctic
840	5	USA	USA	United States
180	1	The democratic Republic of the Congo	COD	Democratic Republic of Congo
384	1	Côte d'Ivoire	CIV	Ivory Coast
212	5	Dominica	DMA	Marquesas Islands, French Polynesia
624	1	Guinea Bissau	GNB	Guinea-Bissau
528	3	Netherlands	NLD	Netherlands
882	7	Western Samoa	WSM	Samoa
688	3	Serbia	SRB	Serbia
772	7	Tokelau	TKL	Tokelau
887	5	Yemen	YEM	Yemen
876	7	Wallis & Futuna	WLF	Wallis and Futuna
784	5	United Arab Emirates	ARE	United Arab Emirates
20	3	Andorra	AND	Andorra
352	3	Iceland	ISL	Iceland
894	1	Zambia	ZMB	Zambia
258	5	French Polynesia	PYF	French Polynesia
862	4	Venezuela	VEN	Venezuela
831	3	Guernsey	GGY	United Kingdom
360	2	Indonesia	IDN	Indonesia
470	3	Malta	MLT	Malta
780	5	Trinidad & Tobago	TTO	Trinidad and Tobago
768	1	Togo	TGO	Togo
662	5	St. Lucia	LCA	St. Lucia
616	3	Poland	POL	Poland
8	3	Albania	ALB	Albania
440	3	Lithuania	LTU	Lithuania
16	7	American Samoa	ASM	American Samoa
724	3	Spain	ESP	Spain
850	5	Virgin Islands  USA	VIR	\N
660	5	Anguilla	AIA	Anguilla
858	4	Uruguay	URY	Uruguay
184	7	Cook Islands	COK	Cook Islands
196	3	Cyprus	CYP	Cyprus
40	3	Austria	AUT	Austria
276	3	Germany	DEU	Germany
208	3	Denmark	DNK	Denmark
860	2	Uzbekistan	UZB	Uzbekistan
300	3	Greece	GRC	Greece
826	3	United Kingdom	GBR	United Kingdom
166	7	Cocos (Keeling) Islands	CCK	Cocos (Keeling) Islands
328	4	Guyana	GUY	Guyana
372	3	Ireland	IRL	Ireland
250	3	France	FRA	France
732	1	Western Sahara	ESH	Western Sahara
442	3	Luxembourg	LUX	Luxembourg
670	5	St. Vincents	VCT	\N
400	5	Jordan	JOR	Jordan
296	7	Kiribati	KIR	Kiribati
795	5	Turkmenistan	TKM	Turkmenistan
716	1	Zimbabwe	ZWE	Zimbabwe
428	3	Latvia	LVA	Latvia
798	7	Tuvalu	TUV	Tuvalu
666	1	St. Pierre	SPM	\N
800	1	Uganda	UGA	Uganda
796	5	Turks & Caicos Island	TCA	Turks And Caicos Islands
706	1	Somalia	SOM	Somalia
690	1	Seychelles	SYC	Seychelles
620	3	Portugal	PRT	Portugal
646	1	Rwanda	RWA	Rwanda
807	3	Macedonia	MKD	Macedonia
380	3	Italy	ITA	Italy
566	1	Nigeria	NGA	Nigeria
578	3	Norway	NOR	Norway
710	1	South Africa	ZAF	South Africa
804	3	Ukraine	UKR	Ukraine
4	2	Afghanistan	AFG	Afghanistan
450	1	Madagascar	MDG	Madagascar
752	3	Sweden	SWE	Sweden
776	7	Tonga	TON	Tonga
788	1	Tunisia	TUN	Tunisia
158	2	Taiwan	TWN	Taiwan
834	1	Tanzania	TZA	Tanzania
764	5	Thailand	THA	Thailand
792	3	Turkey	TUR	Turkey
736	1	Sudan	SDN	Sudan
740	4	Suriname	SUR	Suriname
748	1	Swaziland	SWZ	Swaziland
694	1	Sierra Leone	SLE	Sierra Leone
686	1	Senegal	SEN	Senegal
478	1	Mauritania	MRT	Mauritania
818	1	Egypt	EGY	Egypt
233	3	Estonia	EST	Estonia
234	3	Faroe Islands	FRO	Faroe Islands
756	3	Switzerland	CHE	Switzerland
703	3	Slovakia	SVK	Slovakia
705	3	Slovenia	SVN	Slovenia
891	3	Serbia Montenegro	SCG	Serbia
591	4	Panama	PAN	Panama
504	1	Morocco	MAR	Morocco
348	3	Hungary	HUN	Hungary
246	3	Finland	FIN	Finland
682	2	Saudi Arabia	SAU	Saudi Arabia
56	3	Belgium	BEL	Belgium
76	4	Brazil	BRA	Brazil
854	1	Burkina Faso	BFA	Burkina Faso
104	2	Myanmar	MMR	Myanmar
96	2	Brunei Darussalam	BRN	Brunei
626	5	Timor-Leste	TLS	East Timor
418	5	Lao People's Democratic Republic	LAO	Laos
643	3	Russian Federation	RUS	Russia
499	3	Montenegro	MNE	Montenegro
239	4	South Georgia and the South Sandwich Islands	SGS	South Georgia and South Sandwich Islands
760	5	Syria	SYR	Syria
678	1	Sao Tome & Principe	STP	Sao Tome and Principe
762	5	Tajikistan	TJK	Tajikistan
275	2	Palestinian Occupied Territories	PSE	Palestinian Occupied Territories
28	5	Antigua and Barbuda	ATG	Antigua and Barbuda
48	2	Bahrain	BHR	Bahrain
162	2	Christmas Island	CXR	Christmas Island
336	3	Holy See (Vatican City State)	VAT	Vatican
438	3	Liechtenstein	LIE	Liechtenstein
70	3	Bosnia and Herzegovina	BIH	Bosnia and Herzegovina
132	1	Cape Verde	CVP	Cape Verde
188	5	Costa Rica	CRI	Costa Rica
191	3	Croatia	HRV	Croatia
203	3	Czech Republic	CZE	Czech Republic
674	3	San Marino	SMR	San Marino
530	5	Netherlands Antilles	ANT	Netherlands Antilles
90	7	Solomon Islands	SLB	Solomon Islands
144	2	Sri Lanka	LKA	Sri Lanka
702	2	Singapore	SGP	Singapore
659	5	St. Kitts & Nevis	KNA	Saint Kitts and Nevis
654	1	St. Helena	SHN	Saint Helena and Dependencies
704	5	Viet Nam	VNM	Vietnam
248	3	Åland Islands	ALA	Aland+Islands
580	5	Northern Marianas	MNP	\N
334	6	Heard Island and McDonald Islands	HDH	\N
260	6	French Southern Territories	ATF	\N
74	6	Bouvet Island	BVT	\N
\.


--
-- PostgreSQL database dump complete
--

