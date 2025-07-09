from kafka import KafkaConsumer
import psycopg2
import json
from datetime import datetime

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "weed",
    "user": "postgres",
    "password": "1234",
    "table": "detections"
}

# Reusable function to connect to the database
def get_db_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )

# Ensure the detections table exists
def ensure_table_exists():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {DB_CONFIG['table']} (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        num_detections INTEGER NOT NULL
                    )
                """)
        print(f"Ensured table '{DB_CONFIG['table']}' exists.")
    except Exception as e:
        print("Error ensuring table exists:", e)

# Insert detection count into the database
def insert_into_postgres(count):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    INSERT INTO {DB_CONFIG['table']} (timestamp, num_detections)
                    VALUES (%s, %s)
                    """,
                    (datetime.now(), count)
                )
        print("Inserted")
    except Exception as e:
        print("Insert Error:", e)

# Kafka consumer loop
def consume_messages():
    consumer = KafkaConsumer(
        'weed',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id='my-group',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    print("Listening for messages...")

    for message in consumer:
        try:
            data = json.loads(message.value)
            count = sum(1 for obj in data.get('objects', []) if 'weed' in obj)
            insert_into_postgres(count)
        except Exception as e:
            print("Message processing error:", e)

if __name__ == "__main__":
    ensure_table_exists()
    consume_messages()

