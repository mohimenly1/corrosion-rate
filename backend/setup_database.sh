#!/bin/bash

# Script to setup MySQL database for Corrosion Rate Application

echo "=========================================="
echo "إعداد قاعدة بيانات Corrosion Rate"
echo "=========================================="
echo ""

# Check if MySQL is running
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL غير مثبت. يرجى تثبيت MySQL أولاً."
    exit 1
fi

echo "📝 يرجى إدخال كلمة مرور MySQL (root):"
read -s MYSQL_PASSWORD

# Get port from .env or use default 3308
DB_PORT=$(grep DB_PORT .env 2>/dev/null | cut -d '=' -f2 || echo "3308")

if [ -z "$MYSQL_PASSWORD" ]; then
    MYSQL_CMD="mysql -u root -P $DB_PORT"
else
    MYSQL_CMD="mysql -u root -p$MYSQL_PASSWORD -P $DB_PORT"
fi

echo ""
echo "🔧 جاري إنشاء قاعدة البيانات والجداول..."

# Run schema file
if $MYSQL_CMD < database/schema.sql; then
    echo "✅ تم إنشاء قاعدة البيانات بنجاح!"
    echo ""
    echo "📊 قاعدة البيانات: corrosion_db"
    echo "📋 الجداول المنشأة:"
    echo "   - corrosion_samples"
    echo "   - calculated_corrosion_rates"
    echo "   - csv_uploads"
    echo ""
    echo "✨ جاهز للاستخدام!"
else
    echo "❌ حدث خطأ في إنشاء قاعدة البيانات."
    echo "💡 تأكد من:"
    echo "   1. MySQL يعمل"
    echo "   2. كلمة المرور صحيحة"
    echo "   3. لديك صلاحيات إنشاء قواعد البيانات"
    exit 1
fi

