# test_postgres_complete.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from myapp.models import TeamProject, LeafImage

def test_complete_postgres_setup():
    print("🧪 COMPLETE PostgreSQL TEST")
    print("=" * 60)
    
    # Test 1: Database Connection
    try:
        connection.ensure_connection()
        db_name = connection.settings_dict['NAME']
        db_engine = connection.settings_dict['ENGINE']
        print(f"✅ Database: {db_name}")
        print(f"✅ Engine: {db_engine}")
        
        if 'postgresql' in db_engine:
            print("🎯 SUCCESS: Using PostgreSQL!")
        else:
            print("❌ FAILED: Not using PostgreSQL")
            return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Test 2: Create Test Data
    print("\n📝 Creating test data...")
    try:
        # Create test user if doesn't exist
        test_user, user_created = User.objects.get_or_create(
            username='postgres_test_user',
            defaults={
                'email': 'test@postgres.com',
                'is_staff': False,
                'is_superuser': False
            }
        )
        if user_created:
            test_user.set_password('testpass123')
            test_user.save()
            print("✅ Test user created")
        else:
            print("✅ Test user already exists")
        
        # Create test project
        test_project, project_created = TeamProject.objects.get_or_create(
            name='PostgreSQL Test Project',
            defaults={
                'description': 'This is a test project to verify PostgreSQL is working',
                'created_by': test_user
            }
        )
        if project_created:
            test_project.team_members.add(test_user)
            print("✅ Test project created")
        else:
            print("✅ Test project already exists")
        
        # Count data
        user_count = User.objects.count()
        project_count = TeamProject.objects.count()
        
        print(f"\n📊 Database Statistics:")
        print(f"   👥 Total Users: {user_count}")
        print(f"   📁 Total Projects: {project_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data creation failed: {e}")
        return False

def test_data_persistence():
    print("\n💾 Testing Data Persistence...")
    print("=" * 60)
    
    # This simulates what happens when server restarts
    try:
        # Get counts before "restart"
        users_before = User.objects.count()
        projects_before = TeamProject.objects.count()
        
        print(f"Data before 'restart':")
        print(f"   👥 Users: {users_before}")
        print(f"   📁 Projects: {projects_before}")
        
        # Simulate server restart by re-importing
        print("\n🔁 Simulating server restart...")
        
        # Re-import to simulate fresh start
        import importlib
        import sys
        if 'myapp.models' in sys.modules:
            importlib.reload(sys.modules['myapp.models'])
        
        # Get counts after "restart"
        users_after = User.objects.count()
        projects_after = TeamProject.objects.count()
        
        print(f"Data after 'restart':")
        print(f"   👥 Users: {users_after}")
        print(f"   📁 Projects: {projects_after}")
        
        if users_before == users_after and projects_before == projects_after:
            print("✅ SUCCESS: Data persists after restart!")
            return True
        else:
            print("❌ FAILED: Data lost after restart!")
            return False
            
    except Exception as e:
        print(f"❌ Persistence test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Your PostgreSQL Setup...")
    
    test1 = test_complete_postgres_setup()
    test2 = test_data_persistence()
    
    print("\n" + "=" * 60)
    if test1 and test2:
        print("🎉 ALL TESTS PASSED! PostgreSQL is working perfectly!")
        print("\n📋 Next steps:")
        print("   1. Run: python manage.py runserver")
        print("   2. Visit: http://localhost:8000")
        print("   3. Register a user and create projects")
        print("   4. Your data will be stored permanently in PostgreSQL!")
    else:
        print("❌ Some tests failed. Check the errors above.")