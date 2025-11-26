# fix_postgres_v2.py
import psycopg2
from psycopg2 import sql

def setup_database():
    print("🔧 Setting up PostgreSQL Database (Fixed Version)...")
    print("=" * 50)
    
    try:
        # Step 1: Connect to default 'postgres' database with autocommit
        print("Step 1: Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host="localhost",
            user="postgres", 
            password="12345678",
            database="postgres"
        )
        conn.autocommit = True  # This is the key - no transaction block!
        print("✅ Connected to PostgreSQL server!")
        
        cursor = conn.cursor()
        
        # Step 2: Check if our database exists
        print("Step 2: Checking if 'leaf_disease_db' exists...")
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'leaf_disease_db'")
        db_exists = cursor.fetchone()
        
        if db_exists:
            print("✅ Database 'leaf_disease_db' already exists!")
        else:
            print("❌ Database 'leaf_disease_db' doesn't exist. Creating it...")
            cursor.execute("CREATE DATABASE leaf_disease_db;")
            print("✅ Database 'leaf_disease_db' created successfully!")
        
        cursor.close()
        conn.close()
        
        # Step 3: Test connection to the new database
        print("Step 3: Testing connection to 'leaf_disease_db'...")
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="12345678", 
            database="leaf_disease_db"
        )
        print("✅ Successfully connected to 'leaf_disease_db'!")
        
        # Step 4: List any existing tables
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            print("📊 Existing tables in leaf_disease_db:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("📊 Database is empty (no tables yet) - Ready for Django migrations!")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 PostgreSQL setup completed successfully!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    if setup_database():
        print("\n🚀 Now run these commands:")
        print("1. python manage.py migrate")
        print("2. python manage.py createsuperuser") 
        print("3. python manage.py runserver")
    else:
        print("\n❌ Setup failed.")