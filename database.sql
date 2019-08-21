--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;



CREATE TABLE pickups (
    pickup_id integer NOT NULL,
    name character varying(100),
    street_address character varying(100) NOT NULL,
    description character varying(100) NOT NULL,
    zipcode character varying(15) NOT NULL,
    state character varying(2) NOT NULL
);


ALTER TABLE pickups OWNER TO vagrant;

--
-- Name: pickups_pickup_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE pickups_pickup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE pickups_pickup_id_seq OWNER TO vagrant;

--
-- Name: pickups_pickup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE pickups_pickup_id_seq OWNED BY pickups.pickup_id;

--
-- Name: customer_restrictions; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE customer_restrictions (
    cust_restr_id integer NOT NULL,
    customer_id integer NOT NULL,
    diet_id integer NOT NULL
);


ALTER TABLE customer_restrictions OWNER TO vagrant;

--
-- Name: customer_restrictions_cust_restr_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE customer_restrictions_cust_restr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE customer_restrictions_cust_restr_id_seq OWNER TO vagrant;

--
-- Name: customer_restrictions_cust_restr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE customer_restrictions_cust_restr_id_seq OWNED BY customer_restrictions.cust_restr_id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE customers (
    user_id integer NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    email character varying(100) NOT NULL,
    password_hash character varying(500) NOT NULL,
    street_address character varying(100),
    zipcode character varying(15),
    state character varying(2),
    phone character varying(30)
);


ALTER TABLE customers OWNER TO vagrant;

--
-- Name: customers_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE customers_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE customers_user_id_seq OWNER TO vagrant;

--
-- Name: customers_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE customers_user_id_seq OWNED BY customers.user_id;

--
-- Name: product_tags; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE product_tags (
    prod_tag_id integer NOT NULL,
    product_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE product_tags OWNER TO vagrant;

--
-- Name: product_tags_prod_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE product_tags_prod_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_tags_prod_tag_id_seq OWNER TO vagrant;

--
-- Name: product_tags_prod_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE product_tags_prod_tag_id_seq OWNED BY product_tags.prod_tag_id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE products (
    product_id integer NOT NULL,
    name character varying(200) NOT NULL,
    description character varying,
    weight numeric,
    unit character varying(50),
    price numeric NOT NULL,
    price_per numeric,
    per_unit character varying(50),
    aisle character varying(50),
    category character varying(50),
    img character varying(500),
    icon_id integer,
    color character varying(10),
    search_term character varying(50),
    search_strength integer
);


ALTER TABLE products OWNER TO vagrant;

--
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE products_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE products_product_id_seq OWNER TO vagrant;

--
-- Name: products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE products_product_id_seq OWNED BY products.product_id;
