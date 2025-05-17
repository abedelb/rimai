import boto3
import json
import psycopg2
import os
import argparse
from botocore.client import Config


from dotenv import dotenv_values


env_config = dotenv_values(".env.local")
# create tables into the database
def create_tables(conn):
    SCHEMA_FILE = "./schema.json"
    cursor = conn.cursor()
    with open(SCHEMA_FILE, 'r') as f:
        schema = json.load(f)


    # --- Create tables ---
    for table, definition in schema.items():
        columns_def = ', '.join([f"{col} {type}" for col, type in definition['columns'].items()])
        create_stmt = f"CREATE TABLE IF NOT EXISTS {table} ({columns_def});"
        print(f"🧱 Creating table {table}...")
        cursor.execute(create_stmt)
        print(f"✅ table {table} created")
    conn.commit()
    cursor.close() # close the cursor

def inject_data(table_name, conn, s3):

    cursor = conn.cursor()
    print(f"✅ Start injecting data for {table_name}")
    # List all .json files in bucket
    file_obj = s3.get_object(Bucket=env_config.get('BUCKET_NAME'), Key=table_name + '.json')
    content = file_obj["Body"].read().decode("utf-8")
    rows = json.loads(content)
    for row in rows:
        columns = ', '.join(row.keys())
        placeholders = ', '.join(['%s'] * len(row))
        values = list(row.values())
        insert_stmt = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            cursor.execute(insert_stmt, values)
        except Exception as e:
            print(f"❌ Failed inserting into {table_name}: {e}")
            conn.rollback()
        else:
            conn.commit()

    print(f"✅ All data injected for table {table_name}")
    cursor.close() # close the cursor

def reset_database(tables, conn):
    cursor = conn.cursor()
    print("🧹 Resetting database...")
    for table in tables:
        print(f"🧹 Droping table {table}...")
        cursor.execute(f"DROP TABLE IF EXISTS {table};")

    conn.commit()
    cursor.close() # close the cursor

def run_injector(tables, conn, s3):

    # STEP 1 Create tables
    create_tables(conn)
    for table in tables:
        inject_data(table, conn, s3)

    ## close database connection
if __name__=='__main__':
    
    # create a database connection 
    conn = psycopg2.connect(
        host=env_config.get('PG_HOST'),
        port=env_config.get('PG_PORT'),
        dbname=env_config.get('PG_DATABASE'),
        user=env_config.get('PG_USER'),
        password=env_config.get('PG_PASSWORD')
    )
   
    s3 = boto3.client(
        "s3",
        endpoint_url=env_config.get('MINIO_ENDPOINT'),
        aws_access_key_id=env_config.get('MINIO_ACCESS_KEY'),
        aws_secret_access_key=env_config.get('MINIO_SECRET_KEY'),
        config=Config(signature_version='s3v4'),
        region_name="us-east-1"
    )

    parser = argparse.ArgumentParser(
                    prog='Data injector',
                    description='Injects data from s3 to postgresql database')

    parser.add_argument(
        "command",
        choices=["run", "reset"],
        help="Choose 'run' to launch injector or 'reset' to clear the database."
    )

    tables = ['products', 'users', 'reviews', 'orders']

    args = parser.parse_args()

    if args.command == "run":
        run_injector(tables, conn, s3)
    elif args.command == "reset":
        reset_database(tables, conn)
    