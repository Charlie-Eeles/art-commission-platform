-- Dumped from database version 18.3 (Debian 18.3-1.pgdg13+1)
-- Dumped by pg_dump version 18.3 (Homebrew)

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
-- Name: accounts; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA accounts;


--
-- Name: art; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA art;


--
-- Name: request_status; Type: TYPE; Schema: art; Owner: -
--

CREATE TYPE art.request_status AS ENUM (
    'pending',
    'in_progress',
    'rejected',
    'completed'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: accounts; Owner: -
--

CREATE TABLE accounts.users (
    id uuid DEFAULT uuidv4() NOT NULL,
    email text NOT NULL,
    auth_sub text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: images; Type: TABLE; Schema: art; Owner: -
--

CREATE TABLE art.images (
    id uuid DEFAULT uuidv4() NOT NULL,
    art_name text NOT NULL,
    image_url text NOT NULL,
    upload_id uuid NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: portfolio_settings; Type: TABLE; Schema: art; Owner: -
--

CREATE TABLE art.portfolio_settings (
    id uuid DEFAULT uuidv4() NOT NULL,
    description text,
    is_public boolean NOT NULL,
    commission_slots smallint NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: portfolio_tags; Type: TABLE; Schema: art; Owner: -
--

CREATE TABLE art.portfolio_tags (
    tag_id uuid NOT NULL,
    portfolio_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: requests; Type: TABLE; Schema: art; Owner: -
--

CREATE TABLE art.requests (
    id uuid DEFAULT uuidv4() NOT NULL,
    requester_id uuid NOT NULL,
    portfolio_id uuid NOT NULL,
    status art.request_status DEFAULT 'pending'::art.request_status NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: tags; Type: TABLE; Schema: art; Owner: -
--

CREATE TABLE art.tags (
    id uuid DEFAULT uuidv4() NOT NULL,
    name text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying NOT NULL
);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: accounts; Owner: -
--

ALTER TABLE ONLY accounts.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: portfolio_settings portfolio_settings_pkey; Type: CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.portfolio_settings
    ADD CONSTRAINT portfolio_settings_pkey PRIMARY KEY (id);


--
-- Name: portfolio_settings portfolio_settings_user_id_key; Type: CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.portfolio_settings
    ADD CONSTRAINT portfolio_settings_user_id_key UNIQUE (user_id);


--
-- Name: portfolio_tags portfolio_tags_pkey; Type: CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.portfolio_tags
    ADD CONSTRAINT portfolio_tags_pkey PRIMARY KEY (tag_id, portfolio_id);


--
-- Name: requests requests_pkey; Type: CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: images images_user_id_fkey; Type: FK CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.images
    ADD CONSTRAINT images_user_id_fkey FOREIGN KEY (user_id) REFERENCES accounts.users(id);


--
-- Name: portfolio_settings portfolio_settings_user_id_fkey; Type: FK CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.portfolio_settings
    ADD CONSTRAINT portfolio_settings_user_id_fkey FOREIGN KEY (user_id) REFERENCES accounts.users(id) ON DELETE CASCADE;


--
-- Name: portfolio_tags portfolio_tags_portfolio_id_fkey; Type: FK CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.portfolio_tags
    ADD CONSTRAINT portfolio_tags_portfolio_id_fkey FOREIGN KEY (portfolio_id) REFERENCES art.portfolio_settings(id) ON DELETE CASCADE;


--
-- Name: portfolio_tags portfolio_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.portfolio_tags
    ADD CONSTRAINT portfolio_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES art.tags(id) ON DELETE CASCADE;


--
-- Name: requests requests_portfolio_id_fkey; Type: FK CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.requests
    ADD CONSTRAINT requests_portfolio_id_fkey FOREIGN KEY (portfolio_id) REFERENCES art.portfolio_settings(id) ON DELETE CASCADE;


--
-- Name: requests requests_requester_id_fkey; Type: FK CONSTRAINT; Schema: art; Owner: -
--

ALTER TABLE ONLY art.requests
    ADD CONSTRAINT requests_requester_id_fkey FOREIGN KEY (requester_id) REFERENCES accounts.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20260527194604'),
    ('20260612205313'),
    ('20260801210734'),
    ('20260808200642'),
    ('20260812093936');
