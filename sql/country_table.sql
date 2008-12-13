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

SELECT pg_catalog.setval('country_iso_numcode_seq', 1, false);


--
-- Data for Name: country; Type: TABLE DATA; Schema: public; Owner: poab
--

COPY country (iso_numcode, continent_id, iso_countryname, iso3_nationalcode, flickr_countryname) FROM stdin;
12	1	Algeria	DZA	\N
20	3	Andorra	AND	\N
24	1	Angola	AGO	\N
44	5	Bahamas	BHS	\N
32	4	Argentina	ARG	\N
31	3	Azerbaijan	AZE	\N
36	7	Australia	AUS	\N
48	2	Bahrain	BHR	\N
50	2	Bangladesh	BGD	\N
51	3	Armenia	ARM	\N
52	5	Barbados	BRB	\N
60	5	Bermuda	BMU	\N
64	2	Bhutan	BTN	\N
68	4	Bolivia	BOL	\N
72	1	Botswana	BWA	\N
84	5	Belize	BLZ	\N
86	2	British Indian Ocean Territory	IOT	\N
90	7	Solomon Islands	SLB	\N
96	2	Brunei	BRN	\N
100	3	Bulgaria	BGR	\N
108	1	Burundi	BDI	\N
112	3	Belarus	BLR	\N
116	2	Cambodia	KHM	\N
120	1	Cameroon	CMR	\N
124	5	Canada	CAN	\N
136	5	Cayman Islands	CYM	\N
140	1	Central African Rep.	CAF	\N
144	2	Sri Lanka	LKA	\N
148	1	Chad	TCD	\N
152	4	Chile	CHL	\N
156	2	China	CHN	\N
166	5	Cocos Island	CCK	\N
170	4	Colombia	COL	\N
174	1	Comoros	COM	\N
175	1	Mayotte	MYT	\N
178	1	Congo	COG	\N
180	1	Zaire	COD	\N
188	5	Costa Rica	CRI	\N
192	5	Cuba	CUB	\N
204	1	Benin	BEN	\N
214	5	Dominican Republic	DOM	\N
222	5	El Salvador	SLV	\N
218	4	Ecuador	ECU	\N
226	1	Equatorial Guinea	GNQ	\N
231	1	Ethiopia	ETH	\N
232	1	Eritrea	ERI	\N
238	4	Falkland Islands	FLK	\N
242	5	Fiji	FJI	\N
254	4	French Guiana	GUF	\N
260	6	French Southern Territories	ATF	\N
262	1	Djibouti	DJI	\N
266	1	Gabon	GAB	\N
268	3	Georgia	GEO	\N
270	1	Gambia	GMB	\N
288	1	Ghana	GHA	\N
292	3	Gibraltar	GIB	\N
308	3	Grenada	GRD	\N
304	5	Greenland	GRL	\N
312	5	Guadeloupe	GLP	\N
316	2	Guam	GUM	\N
320	5	Guatemala	GTM	\N
324	1	Guinea	GIN	\N
332	5	Haiti	HTI	\N
340	5	Honduras	HND	\N
344	2	Hong Kong	HKG	\N
356	2	India	IND	\N
364	2	Iran	IRN	\N
368	2	Iraq	IRQ	\N
376	2	Israel	ISR	\N
388	5	Jamaica	JAM	\N
392	2	Japan	JPN	\N
398	3	Kazakhstan	KAZ	\N
404	1	Kenya	KEN	\N
408	5	Korea North	PRK	\N
410	5	Korea South	KOR	\N
414	5	Kuwait	KWT	\N
417	5	Kyrgyzstan	KGZ	\N
422	5	Lebanon	LBN	\N
426	1	Lesotho	LSO	\N
430	1	Liberia	LBR	\N
434	1	Libya	LBY	\N
446	5	Macao	MAC	\N
454	1	Malawi	MWI	\N
458	5	Malaysia	MYS	\N
462	5	Maldives	MDV	\N
466	1	Mali	MLI	\N
474	5	Martinique	MTQ	\N
480	1	Mauritius	MUS	\N
484	5	Mexico	MEX	\N
492	3	Monaco	MCO	\N
496	5	Mongolia	MNG	\N
498	3	Moldova	MDA	\N
500	5	Montserrat	MSR	\N
508	1	Mozambique	MOZ	\N
512	5	Oman	OMN	\N
516	1	Namibia	NAM	\N
520	7	Nauru	NRU	\N
524	5	Nepal	NPL	\N
533	5	Aruba	ABW	\N
540	7	New Caledonia	NCL	\N
547	7	Norfolk Islands	NFK	\N
548	7	Vanuatu	VUT	\N
554	7	New Zealand	NZL	\N
558	4	Nicaragua	NIC	\N
562	1	Niger	NER	\N
570	7	Niue	NIU	\N
583	7	Micronesia	FSM	\N
584	5	Marshall Islands	MHL	\N
585	5	Palau	PLW	\N
586	5	Pakistan	PAK	\N
598	7	Papua New Guinea	PNG	\N
600	4	Paraguay	PRY	\N
604	4	Peru	PER	\N
608	5	Philippines	PHL	\N
630	4	Puerto Rico	PRI	\N
634	5	Qatar	QAT	\N
638	1	Reunion	REU	\N
642	3	Romania	ROU	\N
4	2	Afghanistan	AFG	\N
8	3	Albania	ALB	\N
10	6	Antarctic Territories	ATA	\N
16	7	American Samoa	ASM	\N
40	3	Austria	AUT	\N
28	5	Antigua & Barbuda	ATG	\N
56	3	Belgium	BEL	\N
70	3	Bosnia & Herz.	BIH	\N
76	4	Brazil	BRA	\N
92	5	British Virgin Islands	VGB	\N
104	2	Myanmar	MMR	\N
132	1	Cape Verde Island	CVP	\N
158	2	Taiwan	TWN	\N
162	2	Christmas Island	CXR	\N
184	7	Cook Islands	COK	\N
191	3	Croatia	HRV	\N
196	3	Cyprus South	CYP	\N
203	3	Czech Republic	CZE	\N
208	3	Denmark	DNK	\N
212	5	Dominica	DMA	\N
233	3	Estonia	EST	\N
234	3	Faeroe Islands	FRO	\N
246	3	Finland	FIN	\N
250	3	France	FRA	\N
258	5	French Polynesia	PYF	\N
752	3	Sweden	SWE	\N
275	2	Palestine	PSE	\N
276	3	Germany	DEU	\N
296	7	Kiribati	KIR	\N
300	3	Greece	GRC	\N
328	4	Guyana	GUY	\N
336	3	Italy Vatican City	VAT	\N
348	3	Hungary	HUN	\N
352	3	Iceland	ISL	\N
360	2	Indonesia	IDN	\N
372	3	Ireland	IRL	\N
380	3	Italy	ITA	\N
384	1	Ivory Coast	CIV	\N
400	5	Jordan	JOR	\N
418	5	Laos	LAO	\N
756	3	Switzerland	CHE	\N
428	3	Latvia	LVA	\N
438	3	Liechtenstein	LIE	\N
440	3	Lithuania	LTU	\N
442	3	Luxembourg	LUX	\N
450	1	Madagascar	MDG	\N
470	3	Malta	MLT	\N
478	1	Mauritania	MRT	\N
504	1	Morocco	MAR	\N
528	3	Netherlands	NLD	\N
530	5	Netherlands Antilles	ANT	\N
566	1	Nigeria	NGA	\N
578	3	Norway	NOR	\N
580	5	Northern Marianas	MNP	\N
591	4	Panama	PAN	\N
616	3	Poland	POL	\N
620	3	Portugal	PRT	\N
624	1	Guinea Bissau	GNB	\N
626	5	East Timor	TLS	\N
643	3	Russia	RUS	\N
646	1	Rwanda	RWA	\N
654	1	St. Helena	SHN	\N
760	5	Syrian	SYR	\N
666	1	St. Pierre	SPM	\N
674	3	San Marino	SMR	\N
678	1	Sao Tome & Principe	STP	\N
686	1	Senegal	SEN	\N
690	1	Seychelles	SYC	\N
694	1	Sierra Leone	SLE	\N
762	5	Tajikstan	TJK	\N
703	3	Slovakia	SVK	\N
704	5	Vietnam	VNM	\N
705	3	Slovenia	SVN	\N
706	1	Somalia	SOM	\N
710	1	South Africa	ZAF	\N
716	1	Zimbabwe	ZWE	\N
724	3	Spain	ESP	\N
736	1	Sudan	SDN	\N
740	4	Suriname	SUR	\N
748	1	Swaziland	SWZ	\N
764	5	Thailand	THA	\N
768	1	Togo	TGO	\N
772	7	Tokelau	TKL	\N
776	7	Tonga	TON	\N
780	5	Trinidad & Tobago	TTO	\N
659	5	St. Kitts & Nevis	KNA	\N
660	5	Anguilla	AIA	\N
662	5	St. Lucia	LCA	\N
670	5	St. Vincents	VCT	\N
682	2	Saudi Arabia	SAU	\N
702	2	Singapore	SGP	\N
784	5	United Arab Emirates	ARE	\N
788	1	Tunisia	TUN	\N
792	3	Turkey	TUR	\N
795	5	Turkmenistan	TKM	\N
796	5	Turks & Caicos Island	TCA	\N
798	7	Tuvalu	TUV	\N
800	1	Uganda	UGA	\N
804	3	Ukraine	UKR	\N
807	3	Macedonia	MKD	\N
818	1	Egypt	EGY	\N
826	3	UK	GBR	\N
831	3	Guernsey	GGY	\N
834	1	Tanzania	TZA	\N
840	5	USA	USA	\N
850	5	Virgin Islands  USA	VIR	\N
854	1	Burkina Faso	BFA	\N
858	4	Uruguay	URY	\N
860	2	Uzbekistan	UZB	\N
862	4	Venezuela	VEN	\N
876	7	Wallis & Futuna	WLF	\N
882	7	Western Samoa	WSM	\N
887	5	Yemen	YEM	\N
891	3	Serbia Montenegro	SCG	\N
894	1	Zambia	ZMB	\N
\.


--
-- PostgreSQL database dump complete
--

