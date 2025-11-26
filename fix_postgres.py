# fix_postgres.py
import psycopg2
from psycopg2 import sql
import sys

def setup_database():
    print("🔧 Setting up PostgreSQL Database...")
    print("=" * 50)
    
    try:
        # First connect to default 'postgres' database
        print("Step 1: Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host="localhost",
            user="postgres", 
            password="12345678",
            database="postgres",  # Connect to default database first
            client_encoding='UTF8'
        )
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
            conn.commit()
            print("✅ Database 'leaf_disease_db' created successfully!")
        
        # Step 3: Now connect to our actual database
        print("Step 3: Testing connection to 'leaf_disease_db'...")
        cursor.close()
        conn.close()
        
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="12345678", 
            database="leaf_disease_db",
            client_encoding='UTF8'
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
            print("📊 Database is empty (no tables yet)")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 PostgreSQL setup completed successfully!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Possible solutions:")
        print("1. Check if password '12345678' is correct")
        print("2. Try different authentication method")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    if setup_database():
        print("\n🚀 Now run: python manage.py migrate")
    else:
        print("\n❌ Setup failed. Let's try alternative approach...")