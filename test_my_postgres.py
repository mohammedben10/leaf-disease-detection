# test_my_postgres.py
import psycopg2

def test_my_database():
    print("🔍 Testing YOUR PostgreSQL Database...")
    print("=" * 50)
    
    try:
        # Connect using YOUR credentials
        connection = psycopg2.connect(
            host="localhost",
            database="leaf_disease_db",
            user="postgres", 
            password="12345678"  # Your password
        )
        print("✅ Connected to leaf_disease_db successfully!")
        
        # Check what's in the database
        cursor = connection.cursor()
        
        # List all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        print("📊 Current tables in your database:")
        if tables:
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("   (No tables yet - database is empty)")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Make sure:")
        print("   - PostgreSQL is running")
        print("   - Database 'leaf_disease_db' exists") 
        print("   - Username: postgres, Password: 12345678 is correct")
        return False

if __name__ == "__main__":
    test_my_database()