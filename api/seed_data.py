import os
import random
import psycopg2
from faker import Faker
from datetime import datetime, timedelta
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json  # Adicione esta importação

fake = Faker("pt_BR")

def get_connection():
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "api")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "postgres")
    db_port = os.getenv("DB_PORT", "5432")

    conn = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_pass,
        port=db_port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def create_tables():
    """
    Cria as tabelas: products, customers, logistics, sales.
    Obs: Caso queira recriar do zero, use DROP TABLE IF EXISTS antes.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(100),
            price NUMERIC(10,2),
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(20),
            address TEXT,
            city VARCHAR(100),
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS logistics (
            id SERIAL PRIMARY KEY,
            company_name VARCHAR(255),
            service_type VARCHAR(100),
            contact_phone VARCHAR(20),
            origin_warehouse VARCHAR(255),
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES customers(id),
            logistic_id INT REFERENCES logistics(id),
            sale_date TIMESTAMP,
            status VARCHAR(50),
            total_amount NUMERIC(10,2),
            items JSONB,
            shipping_info JSONB,
            payment_info JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.close()
    conn.close()

def drop_tables():
    """
    Limpa os dados das tabelas, mantendo a estrutura.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS sales;")
    cur.execute("DROP TABLE IF EXISTS customers;")
    cur.execute("DROP TABLE IF EXISTS products;")
    cur.execute("DROP TABLE IF EXISTS logistics;")

    conn.commit()
    cur.close()
    conn.close()

def seed_products(num_records=200):
    """
    Gera produtos falsos com nome, categoria e preço.
    """
    conn = get_connection()
    cur = conn.cursor()

    categories = ["Eletrônicos", "Roupas", "Cozinha", "Jogos", "Livros", "Escritório", "Casa & Decoração"]
    for _ in range(num_records):
        name = fake.sentence(nb_words=3) 
        category = random.choice(categories)
        price = round(random.uniform(10.0, 3000.0), 2)

        cur.execute("""
            INSERT INTO products (name, category, price)
            VALUES (%s, %s, %s)
        """, (name, category, price))

    conn.commit()
    cur.close()
    conn.close()

def seed_customers(num_records=200):
    """
    Gera clientes falsos com nome, email, telefone e endereço.
    """
    conn = get_connection()
    cur = conn.cursor()

    for _ in range(num_records):
        full_name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        address = fake.street_address()
        city = fake.city()

        cur.execute("""
            INSERT INTO customers (full_name, email, phone, address, city)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, email, phone, address, city))

    conn.commit()
    cur.close()
    conn.close()

def seed_logistics(num_records=10):
    """
    Gera transportadoras/empresas de logística.
    """
    conn = get_connection()
    cur = conn.cursor()

    service_types = ["Expresso", "Normal", "Internacional", "Same-Day", "Overnight"]
    for _ in range(num_records):
        company_name = fake.company()
        service_type = random.choice(service_types)
        contact_phone = fake.phone_number()
        origin_warehouse = fake.city() 

        cur.execute("""
            INSERT INTO logistics (company_name, service_type, contact_phone, origin_warehouse)
            VALUES (%s, %s, %s, %s)
        """, (company_name, service_type, contact_phone, origin_warehouse))

    conn.commit()
    cur.close()
    conn.close()

def seed_sales(num_records=1000):
    """
    Gera vendas (sales) com dados altamente aninhados em JSON:
      - items: array de produtos (nome, qty, unit_price, total, desconto, etc.)
      - shipping_info: carrier, tracking, histórico de atualização, etc.
      - payment_info: método de pagamento, parcelas, etc.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM customers")
    customer_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id, name, price FROM products")
    product_rows = cur.fetchall()

    cur.execute("SELECT id, company_name FROM logistics")
    logistic_rows = cur.fetchall()

    statuses = ["PENDING", "APPROVED", "SHIPPED", "DELIVERED", "CANCELLED"]

    payment_methods = ["credit_card", "boleto", "pix", "paypal"]

    for _ in range(num_records):
        customer_id = random.choice(customer_ids)
        logistic = random.choice(logistic_rows)
        logistic_id = logistic[0]
        logistic_company_name = logistic[1]

        sale_date = fake.date_time_between(start_date="-2y", end_date="now")
        status = random.choice(statuses)

        num_items = random.randint(1, 5)
        items_list = []
        total_amount = 0.0
        for _i in range(num_items):
            product_id, product_name, product_price = random.choice(product_rows)
            qty = random.randint(1, 5)
            discount = round(random.uniform(0, 0.3), 2)  # até 30%
            unit_price = float(product_price)
            price_after_discount = unit_price * (1 - discount)
            line_total = round(price_after_discount * qty, 2)

            item_data = {
                "product_id": product_id,
                "product_name": product_name,
                "quantity": qty,
                "unit_price": unit_price,
                "discount": discount,
                "line_total": line_total
            }
            items_list.append(item_data)
            total_amount += line_total

        total_amount = round(total_amount, 2)

        shipping_info = {
            "carrier": logistic_company_name,
            "tracking_number": f"TRK-{random.randint(100000, 999999)}",
            "tracking_history": []
        }

        tracking_steps = random.randint(1, 3)
        current_status = "label_created"
        current_date = sale_date
        for _ts in range(tracking_steps):
            current_date += timedelta(days=random.randint(1, 5))
            current_status = random.choice(["label_created", "in_transit", "out_for_delivery", "delivered"])
            shipping_info["tracking_history"].append({
                "status": current_status,
                "updated_at": current_date.isoformat()
            })

        pay_method = random.choice(payment_methods)
        payment_info = {
            "method": pay_method,
        }
        if pay_method == "credit_card":
            payment_info["installments"] = random.choice([1,2,3,4,5,6,10,12])
            payment_info["card_last4"] = str(random.randint(1000,9999))
        elif pay_method == "boleto":
            payment_info["boleto_number"] = f"BOL-{fake.bothify(text='####-####-####')}"
        elif pay_method == "pix":
            payment_info["pix_key"] = fake.uuid4()
        elif pay_method == "paypal":
            payment_info["paypal_id"] = fake.email()

        items_json = json.dumps(items_list)
        shipping_info_json = json.dumps(shipping_info)
        payment_info_json = json.dumps(payment_info)

        cur.execute("""
            INSERT INTO sales (
                customer_id,
                logistic_id,
                sale_date,
                status,
                total_amount,
                items,
                shipping_info,
                payment_info
            )
            VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s::jsonb)
        """, (
            customer_id,
            logistic_id,
            sale_date,
            status,
            total_amount,
            items_json,         
            shipping_info_json,
            payment_info_json
        ))

    conn.commit()
    cur.close()
    conn.close()

def main():
    print("Limpando tabelas...")
    drop_tables()

    print("Criando tabelas...")
    create_tables()

    print("Inserindo products...")
    seed_products(num_records=654)

    print("Inserindo customers...")
    seed_customers(num_records=1565)

    print("Inserindo logistics...")
    seed_logistics(num_records=9)

    print("Inserindo sales...")
    seed_sales(num_records=9862)

    print("Concluído!")

if __name__ == "__main__":
    main()
