CREATE DATABASE api;
CREATE DATABASE airflow;
CREATE DATABASE ecommerce;

-- Se quiser garantir privilégios:
GRANT ALL PRIVILEGES ON DATABASE api TO postgres;
GRANT ALL PRIVILEGES ON DATABASE airflow TO postgres;
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO postgres;
