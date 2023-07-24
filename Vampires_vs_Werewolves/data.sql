--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-1.pgdg110+1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO "postgres-user";

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO "postgres-user";

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO "postgres-user";

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: common_boots; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.common_boots (
);


ALTER TABLE public.common_boots OWNER TO "postgres-user";

--
-- Name: common_shield; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.common_shield (
);


ALTER TABLE public.common_shield OWNER TO "postgres-user";

--
-- Name: common_sword; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.common_sword (
);


ALTER TABLE public.common_sword OWNER TO "postgres-user";

--
-- Name: common_work; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.common_work (
    id bigint NOT NULL,
    start_time timestamp with time zone NOT NULL,
    hours_worked integer NOT NULL,
    hourly_wage integer NOT NULL,
    user_id bigint NOT NULL,
    end_time timestamp with time zone,
    CONSTRAINT common_work_hourly_wage_check CHECK ((hourly_wage >= 0)),
    CONSTRAINT common_work_hours_worked_check CHECK ((hours_worked >= 0))
);


ALTER TABLE public.common_work OWNER TO "postgres-user";

--
-- Name: common_work_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.common_work ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.common_work_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO "postgres-user";

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO "postgres-user";

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO "postgres-user";

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO "postgres-user";

--
-- Name: profiles_customuser; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.profiles_customuser (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    username character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    hero_type character varying NOT NULL,
    is_active boolean NOT NULL,
    is_staff boolean NOT NULL,
    is_superuser boolean NOT NULL
);


ALTER TABLE public.profiles_customuser OWNER TO "postgres-user";

--
-- Name: profiles_customuser_groups; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.profiles_customuser_groups (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.profiles_customuser_groups OWNER TO "postgres-user";

--
-- Name: profiles_customuser_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.profiles_customuser_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.profiles_customuser_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: profiles_customuser_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.profiles_customuser ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.profiles_customuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: profiles_customuser_user_permissions; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.profiles_customuser_user_permissions (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.profiles_customuser_user_permissions OWNER TO "postgres-user";

--
-- Name: profiles_customuser_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.profiles_customuser_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.profiles_customuser_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: profiles_userprofile; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.profiles_userprofile (
    id bigint NOT NULL,
    health integer NOT NULL,
    xp integer NOT NULL,
    level integer NOT NULL,
    gold integer NOT NULL,
    user_id bigint NOT NULL,
    gender character varying(10) NOT NULL,
    defence integer NOT NULL,
    power integer NOT NULL,
    speed integer NOT NULL,
    losses integer NOT NULL,
    wins integer NOT NULL,
    hourly_wage integer NOT NULL,
    is_working boolean NOT NULL,
    CONSTRAINT profiles_userprofile_defence_342a722c_check CHECK ((defence >= 0)),
    CONSTRAINT profiles_userprofile_hourly_wage_check CHECK ((hourly_wage >= 0)),
    CONSTRAINT profiles_userprofile_losses_check CHECK ((losses >= 0)),
    CONSTRAINT profiles_userprofile_power_check CHECK ((power >= 0)),
    CONSTRAINT profiles_userprofile_speed_check CHECK ((speed >= 0)),
    CONSTRAINT profiles_userprofile_wins_check CHECK ((wins >= 0))
);


ALTER TABLE public.profiles_userprofile OWNER TO "postgres-user";

--
-- Name: profiles_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.profiles_userprofile ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.profiles_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: user_messages_custommessage; Type: TABLE; Schema: public; Owner: postgres-user
--

CREATE TABLE public.user_messages_custommessage (
    id bigint NOT NULL,
    content text NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    read boolean NOT NULL,
    recipient_id bigint NOT NULL,
    sender_id bigint NOT NULL
);


ALTER TABLE public.user_messages_custommessage OWNER TO "postgres-user";

--
-- Name: user_messages_custommessage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres-user
--

ALTER TABLE public.user_messages_custommessage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.user_messages_custommessage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add custom user	6	add_customuser
22	Can change custom user	6	change_customuser
23	Can delete custom user	6	delete_customuser
24	Can view custom user	6	view_customuser
25	Can add user profile	7	add_userprofile
26	Can change user profile	7	change_userprofile
27	Can delete user profile	7	delete_userprofile
28	Can view user profile	7	view_userprofile
29	Can add custom message	8	add_custommessage
30	Can change custom message	8	change_custommessage
31	Can delete custom message	8	delete_custommessage
32	Can view custom message	8	view_custommessage
33	Can add custom message	9	add_custommessage
34	Can change custom message	9	change_custommessage
35	Can delete custom message	9	delete_custommessage
36	Can view custom message	9	view_custommessage
37	Can add boots	10	add_boots
38	Can change boots	10	change_boots
39	Can delete boots	10	delete_boots
40	Can view boots	10	view_boots
41	Can add shield	11	add_shield
42	Can change shield	11	change_shield
43	Can delete shield	11	delete_shield
44	Can view shield	11	view_shield
45	Can add sword	12	add_sword
46	Can change sword	12	change_sword
47	Can delete sword	12	delete_sword
48	Can view sword	12	view_sword
49	Can add work	13	add_work
50	Can change work	13	change_work
51	Can delete work	13	delete_work
52	Can view work	13	view_work
\.


--
-- Data for Name: common_boots; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.common_boots  FROM stdin;
\.


--
-- Data for Name: common_shield; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.common_shield  FROM stdin;
\.


--
-- Data for Name: common_sword; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.common_sword  FROM stdin;
\.


--
-- Data for Name: common_work; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.common_work (id, start_time, hours_worked, hourly_wage, user_id, end_time) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2023-07-22 10:06:09.099034+00	1	Speed	1	[{"added": {}}]	10	1
2	2023-07-22 10:06:33.088522+00	1	Shield	1	[{"added": {}}]	11	1
3	2023-07-22 10:07:00.999851+00	1	Sword	1	[{"added": {}}]	12	1
4	2023-07-22 16:35:44.909712+00	1	Speed	3		10	1
5	2023-07-22 16:36:08.709013+00	2	Boots	1	[{"added": {}}]	10	1
6	2023-07-22 16:58:45.604896+00	3	Boots	1	[{"added": {}}]	10	1
7	2023-07-23 09:04:43.787428+00	1	Sword	2	[{"changed": {"fields": ["Image"]}}]	12	1
8	2023-07-23 09:05:08.154069+00	1	Shield	2	[{"changed": {"fields": ["Image"]}}]	11	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	profiles	customuser
7	profiles	userprofile
8	custom_messages	custommessage
9	user_messages	custommessage
10	common	boots
11	common	shield
12	common	sword
13	common	work
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2023-07-16 15:09:07.155379+00
2	contenttypes	0002_remove_content_type_name	2023-07-16 15:09:07.173322+00
3	auth	0001_initial	2023-07-16 15:09:07.264904+00
4	auth	0002_alter_permission_name_max_length	2023-07-16 15:09:07.279809+00
5	auth	0003_alter_user_email_max_length	2023-07-16 15:09:07.300519+00
6	auth	0004_alter_user_username_opts	2023-07-16 15:09:07.316757+00
7	auth	0005_alter_user_last_login_null	2023-07-16 15:09:07.332255+00
8	auth	0006_require_contenttypes_0002	2023-07-16 15:09:07.342062+00
9	auth	0007_alter_validators_add_error_messages	2023-07-16 15:09:07.354546+00
10	auth	0008_alter_user_username_max_length	2023-07-16 15:09:07.367856+00
11	auth	0009_alter_user_last_name_max_length	2023-07-16 15:09:07.3827+00
12	auth	0010_alter_group_name_max_length	2023-07-16 15:09:07.399002+00
13	auth	0011_update_proxy_permissions	2023-07-16 15:09:07.41156+00
14	auth	0012_alter_user_first_name_max_length	2023-07-16 15:09:07.42429+00
15	profiles	0001_initial	2023-07-16 15:09:07.573809+00
16	admin	0001_initial	2023-07-16 15:09:07.629093+00
17	admin	0002_logentry_remove_auto_add	2023-07-16 15:09:07.648834+00
18	admin	0003_logentry_add_action_flag_choices	2023-07-16 15:09:07.670893+00
19	profiles	0002_userprofile_gender	2023-07-16 15:09:07.708656+00
20	sessions	0001_initial	2023-07-16 15:09:07.747671+00
21	profiles	0003_alter_userprofile_name	2023-07-16 15:14:26.490563+00
22	profiles	0004_remove_userprofile_name	2023-07-16 15:18:15.152631+00
23	profiles	0005_userprofile_defence_userprofile_power_and_more	2023-07-17 08:07:16.552586+00
24	profiles	0006_rename_defence_userprofile_defense	2023-07-17 09:04:16.646814+00
25	profiles	0007_rename_defense_userprofile_defence	2023-07-17 09:06:25.671371+00
26	profiles	0008_rename_hp_userprofile_health_and_more	2023-07-18 07:20:47.720499+00
27	profiles	0009_userprofile_last_health_update	2023-07-18 07:35:22.642535+00
28	profiles	0010_remove_userprofile_last_health_update	2023-07-18 07:58:28.119512+00
29	custom_messages	0001_initial	2023-07-19 10:41:46.909038+00
30	custom_messages	0002_custommessage_read	2023-07-19 16:04:52.914924+00
31	user_messages	0001_initial	2023-07-19 16:42:33.696093+00
32	profiles	0011_userprofile_last_healed_at_userprofile_losses_and_more	2023-07-21 16:16:09.765032+00
33	profiles	0012_remove_userprofile_last_healed_at	2023-07-21 16:18:59.861336+00
44	common	0001_initial	2023-07-24 09:30:30.253707+00
45	common	0002_boots_image_boots_required_level_shield_image_and_more	2023-07-24 09:30:30.267075+00
46	common	0003_boots_price_shield_price_sword_price	2023-07-24 09:30:30.275931+00
47	common	0004_work	2023-07-24 09:30:30.28277+00
48	common	005_work_end_time	2023-07-24 09:30:30.289878+00
49	common	0006_boots_sell_price_shield_sell_price_sword_sell_price	2023-07-24 09:30:30.301246+00
50	profiles	0013_userprofile_boots_userprofile_shield_and_more	2023-07-24 09:30:30.307416+00
51	profiles	0014_userprofile_hourly_wage	2023-07-24 09:30:30.31543+00
52	profiles	0015_remove_userprofile_hourly_wage	2023-07-24 09:30:30.323161+00
53	profiles	0016_userprofile_hourly_wage	2023-07-24 09:30:30.329539+00
54	profiles	0017_userprofile_is_working	2023-07-24 09:30:30.340356+00
55	profiles	0018_remove_userprofile_boots_remove_userprofile_shield_and_more	2023-07-24 09:30:30.347712+00
56	profiles	0019_userprofile_test	2023-07-24 09:36:41.558611+00
57	profiles	0020_remove_userprofile_test	2023-07-24 09:37:11.058678+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
830hi9yflsp1j2j1cl3e93rkf0ycb89v	.eJxVjMsOwiAUBf-FtSG8oS7d9xvI5XGlaiAp7cr479KkC92emTlv4mHfit97Xv2SyJVwcvndAsRnrgdID6j3RmOr27oEeij0pJ3OLeXX7XT_Dgr0MmqBwlhwzGEyaQJpuGUCeEhSRaOkDYjC6YDMZa3iwCpHrR1mB8OeOPl8AdjIN60:1qNZUV:DdEvFvNitv0VXHItFXJt5adIpbAurRpHHgLXSWVwB7g	2023-08-06 13:51:19.227026+00
\.


--
-- Data for Name: profiles_customuser; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.profiles_customuser (id, password, last_login, username, email, hero_type, is_active, is_staff, is_superuser) FROM stdin;
7	pbkdf2_sha256$600000$hkgukgQUuqXlTTRj9aYQ31$d/al4NLkp8atBK9aZkzOuojmpaIb9SnPrPO+5Wq7N7k=	2023-07-22 09:26:25.611242+00	mitko	some1@email.com	Vampire	t	f	f
6	pbkdf2_sha256$600000$yu1HPShV22LYH4z1Iznqh0$4eaMHv2CSRGrk8prrtRBEKFDqUBXzmcn4055QK036cs=	2023-07-17 15:54:15.041764+00	mitkoo	some@email.com	Werewolf	t	f	f
1	pbkdf2_sha256$600000$MvoInBVYNYkCQRpTj2P6qD$evIx7MmVwk0yLbmj1JOnrDdanMOeku7aZH+rKdfnZU0=	2023-07-23 13:51:19.21905+00	galka	galka@abv.bg	Vampire	t	t	t
8	pbkdf2_sha256$600000$4Z3rb1fp3xWBc21GU2tdAw$NSKixBGF4fGeOaPIjoSWOJLLNOZxA6/KTQlzyW5oUB0=	2023-07-19 08:58:51.587978+00	mitkoooo	mail@mail.com	Werewolf	t	f	f
5	pbkdf2_sha256$600000$dQPTq5EFo0gljFkVcLWtiT$QRleMc/x7LSrXPTLqE647p19onOjMhU133973cP6E30=	2023-07-20 18:52:33.209286+00	galkaaa	galkaaa@abv.bg	Werewolf	t	f	f
\.


--
-- Data for Name: profiles_customuser_groups; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.profiles_customuser_groups (id, customuser_id, group_id) FROM stdin;
\.


--
-- Data for Name: profiles_customuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.profiles_customuser_user_permissions (id, customuser_id, permission_id) FROM stdin;
\.


--
-- Data for Name: profiles_userprofile; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.profiles_userprofile (id, health, xp, level, gold, user_id, gender, defence, power, speed, losses, wins, hourly_wage, is_working) FROM stdin;
7	0	100	1	10	7	Male	13	18	11	3	0	10	f
5	100	100	1	70	5	Female	10	10	10	2	0	10	f
1	89	736	3	6234	1	Female	35	73	36	0	9	30	f
8	100	100	1	35	8		10	10	10	3	0	10	f
\.


--
-- Data for Name: user_messages_custommessage; Type: TABLE DATA; Schema: public; Owner: postgres-user
--

COPY public.user_messages_custommessage (id, content, "timestamp", read, recipient_id, sender_id) FROM stdin;
1	Hello, galkaaa	2023-07-19 17:29:31.615068+00	f	5	1
2	Hello, galkaaa	2023-07-19 17:30:16.375192+00	f	5	1
3	Hello	2023-07-19 17:31:14.889408+00	f	5	1
4	Hello	2023-07-19 17:31:37.136826+00	f	5	1
5	hello	2023-07-19 17:32:51.305593+00	f	5	1
6	hello	2023-07-19 17:36:11.227855+00	f	5	1
7	hello	2023-07-19 17:36:40.567402+00	f	5	1
8	hello	2023-07-19 17:37:10.473947+00	f	5	1
9	hello	2023-07-19 17:37:17.109416+00	f	5	1
10	hello	2023-07-19 17:41:12.51001+00	f	5	1
11	hello	2023-07-19 17:41:41.352441+00	f	5	1
12	test	2023-07-20 10:55:02.108656+00	f	8	1
13	hiiiii	2023-07-20 11:03:12.902688+00	f	5	1
14	hi again	2023-07-20 11:05:35.18999+00	f	5	1
15	new test	2023-07-20 18:44:09.181862+00	f	7	1
16	Love you!!! :* <3	2023-07-20 18:53:44.130345+00	f	1	7
17	I love you so much <3 :* :*	2023-07-21 09:35:05.159999+00	f	7	1
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 52, true);


--
-- Name: common_work_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.common_work_id_seq', 12, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 8, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 57, true);


--
-- Name: profiles_customuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.profiles_customuser_groups_id_seq', 1, false);


--
-- Name: profiles_customuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.profiles_customuser_id_seq', 8, true);


--
-- Name: profiles_customuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.profiles_customuser_user_permissions_id_seq', 1, false);


--
-- Name: profiles_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.profiles_userprofile_id_seq', 8, true);


--
-- Name: user_messages_custommessage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres-user
--

SELECT pg_catalog.setval('public.user_messages_custommessage_id_seq', 17, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: common_work common_work_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.common_work
    ADD CONSTRAINT common_work_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: profiles_customuser profiles_customuser_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser
    ADD CONSTRAINT profiles_customuser_email_key UNIQUE (email);


--
-- Name: profiles_customuser_groups profiles_customuser_groups_customuser_id_group_id_220744dc_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser_groups
    ADD CONSTRAINT profiles_customuser_groups_customuser_id_group_id_220744dc_uniq UNIQUE (customuser_id, group_id);


--
-- Name: profiles_customuser_groups profiles_customuser_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser_groups
    ADD CONSTRAINT profiles_customuser_groups_pkey PRIMARY KEY (id);


--
-- Name: profiles_customuser profiles_customuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser
    ADD CONSTRAINT profiles_customuser_pkey PRIMARY KEY (id);


--
-- Name: profiles_customuser_user_permissions profiles_customuser_user_customuser_id_permission_8b97c241_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser_user_permissions
    ADD CONSTRAINT profiles_customuser_user_customuser_id_permission_8b97c241_uniq UNIQUE (customuser_id, permission_id);


--
-- Name: profiles_customuser_user_permissions profiles_customuser_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser_user_permissions
    ADD CONSTRAINT profiles_customuser_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: profiles_customuser profiles_customuser_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser
    ADD CONSTRAINT profiles_customuser_username_key UNIQUE (username);


--
-- Name: profiles_userprofile profiles_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_userprofile
    ADD CONSTRAINT profiles_userprofile_pkey PRIMARY KEY (id);


--
-- Name: profiles_userprofile profiles_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_userprofile
    ADD CONSTRAINT profiles_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: user_messages_custommessage user_messages_custommessage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.user_messages_custommessage
    ADD CONSTRAINT user_messages_custommessage_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: common_work_user_id_4e121b58; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX common_work_user_id_4e121b58 ON public.common_work USING btree (user_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: profiles_customuser_email_5086907d_like; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX profiles_customuser_email_5086907d_like ON public.profiles_customuser USING btree (email varchar_pattern_ops);


--
-- Name: profiles_customuser_groups_customuser_id_2d6c62c5; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX profiles_customuser_groups_customuser_id_2d6c62c5 ON public.profiles_customuser_groups USING btree (customuser_id);


--
-- Name: profiles_customuser_groups_group_id_cc13aa3b; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX profiles_customuser_groups_group_id_cc13aa3b ON public.profiles_customuser_groups USING btree (group_id);


--
-- Name: profiles_customuser_user_permissions_customuser_id_190c9e96; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX profiles_customuser_user_permissions_customuser_id_190c9e96 ON public.profiles_customuser_user_permissions USING btree (customuser_id);


--
-- Name: profiles_customuser_user_permissions_permission_id_f7140861; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX profiles_customuser_user_permissions_permission_id_f7140861 ON public.profiles_customuser_user_permissions USING btree (permission_id);


--
-- Name: profiles_customuser_username_955d4cf1_like; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX profiles_customuser_username_955d4cf1_like ON public.profiles_customuser USING btree (username varchar_pattern_ops);


--
-- Name: user_messages_custommessage_recipient_id_5df37f6b; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX user_messages_custommessage_recipient_id_5df37f6b ON public.user_messages_custommessage USING btree (recipient_id);


--
-- Name: user_messages_custommessage_sender_id_86534dc7; Type: INDEX; Schema: public; Owner: postgres-user
--

CREATE INDEX user_messages_custommessage_sender_id_86534dc7 ON public.user_messages_custommessage USING btree (sender_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_work common_work_user_id_4e121b58_fk_profiles_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.common_work
    ADD CONSTRAINT common_work_user_id_4e121b58_fk_profiles_customuser_id FOREIGN KEY (user_id) REFERENCES public.profiles_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_profiles_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_profiles_customuser_id FOREIGN KEY (user_id) REFERENCES public.profiles_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: profiles_customuser_user_permissions profiles_customuser__customuser_id_190c9e96_fk_profiles_; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser_user_permissions
    ADD CONSTRAINT profiles_customuser__customuser_id_190c9e96_fk_profiles_ FOREIGN KEY (customuser_id) REFERENCES public.profiles_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: profiles_customuser_groups profiles_customuser__customuser_id_2d6c62c5_fk_profiles_; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser_groups
    ADD CONSTRAINT profiles_customuser__customuser_id_2d6c62c5_fk_profiles_ FOREIGN KEY (customuser_id) REFERENCES public.profiles_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: profiles_customuser_user_permissions profiles_customuser__permission_id_f7140861_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser_user_permissions
    ADD CONSTRAINT profiles_customuser__permission_id_f7140861_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: profiles_customuser_groups profiles_customuser_groups_group_id_cc13aa3b_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_customuser_groups
    ADD CONSTRAINT profiles_customuser_groups_group_id_cc13aa3b_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: profiles_userprofile profiles_userprofile_user_id_616bed88_fk_profiles_customuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.profiles_userprofile
    ADD CONSTRAINT profiles_userprofile_user_id_616bed88_fk_profiles_customuser_id FOREIGN KEY (user_id) REFERENCES public.profiles_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_messages_custommessage user_messages_custom_recipient_id_5df37f6b_fk_profiles_; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.user_messages_custommessage
    ADD CONSTRAINT user_messages_custom_recipient_id_5df37f6b_fk_profiles_ FOREIGN KEY (recipient_id) REFERENCES public.profiles_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_messages_custommessage user_messages_custom_sender_id_86534dc7_fk_profiles_; Type: FK CONSTRAINT; Schema: public; Owner: postgres-user
--

ALTER TABLE ONLY public.user_messages_custommessage
    ADD CONSTRAINT user_messages_custom_sender_id_86534dc7_fk_profiles_ FOREIGN KEY (sender_id) REFERENCES public.profiles_customuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--
