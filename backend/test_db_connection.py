#!/usr/bin/env python3
"""
Script to test database connection and table existence
"""

from database.db_connection import DatabaseConnection
from config import Config
import sys

def test_connection():
    print("=" * 50)
    print("اختبار اتصال قاعدة البيانات")
    print("=" * 50)
    print()
    
    # Test config
    print("📋 إعدادات قاعدة البيانات:")
    db_config = Config.get_db_config()
    print(f"   Host: {db_config['host']}")
    print(f"   Port: {db_config.get('port', 3306)}")
    print(f"   User: {db_config['user']}")
    print(f"   Database: {db_config['database']}")
    print()
    
    # Test connection
    try:
        print("🔌 محاولة الاتصال بقاعدة البيانات...")
        db = DatabaseConnection()
        connection = db.get_connection()
        print("✅ تم الاتصال بنجاح!")
        print()
        
        # Test table existence
        print("📊 التحقق من وجود الجداول...")
        cursor = connection.cursor(dictionary=True)
        
        # Check if database exists
        cursor.execute("SHOW DATABASES LIKE %s", (db_config['database'],))
        if cursor.fetchone():
            print(f"✅ قاعدة البيانات '{db_config['database']}' موجودة")
        else:
            print(f"❌ قاعدة البيانات '{db_config['database']}' غير موجودة!")
            print("   قم بتشغيل: ./setup_database.sh")
            cursor.close()
            return False
        
        # Use the database
        cursor.execute(f"USE {db_config['database']}")
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        required_tables = ['corrosion_samples', 'calculated_corrosion_rates', 'csv_uploads']
        
        print()
        print("📋 الجداول الموجودة:")
        # Extract table names from dictionary results
        existing_tables = []
        for table in tables:
            # SHOW TABLES returns results with key like 'Tables_in_corrosion_db'
            table_name = list(table.values())[0] if table else None
            if table_name:
                existing_tables.append(table_name)
        
        for table in required_tables:
            if table in existing_tables:
                # Count rows
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                result = cursor.fetchone()
                count = result['count'] if result else 0
                print(f"   ✅ {table} ({count} صف)")
            else:
                print(f"   ❌ {table} غير موجود!")
        
        cursor.close()
        print()
        print("=" * 50)
        print("✅ كل شيء يعمل بشكل صحيح!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print()
        print("❌ خطأ في الاتصال:")
        print(f"   {str(e)}")
        print()
        print("💡 الحلول المقترحة:")
        print("   1. تأكد من أن MySQL يعمل")
        print("   2. تحقق من بيانات الاتصال في ملف .env")
        print("   3. قم بتشغيل: ./setup_database.sh")
        print()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

