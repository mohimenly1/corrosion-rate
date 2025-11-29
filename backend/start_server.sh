#!/bin/bash

# Script to start the Flask backend server

echo "=========================================="
echo "تشغيل خادم Corrosion Rate Backend"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 إنشاء بيئة افتراضية..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 تفعيل البيئة الافتراضية..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.deps_installed" ]; then
    echo "📥 تثبيت المكتبات المطلوبة..."
    pip install -r requirements.txt
    touch venv/.deps_installed
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  ملف .env غير موجود. يتم إنشاء ملف افتراضي..."
    cp .env.example .env 2>/dev/null || cat > .env << EOF
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=corrosion_db
FLASK_ENV=development
FLASK_PORT=5000
EOF
    echo "✅ تم إنشاء ملف .env"
    echo "💡 يرجى تعديل ملف .env وإدخال بيانات قاعدة البيانات"
    echo ""
fi

# Get local IP address for Android emulator
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")
if [ "$LOCAL_IP" != "localhost" ]; then
    echo "🌐 عنوان IP المحلي: $LOCAL_IP"
    echo "💡 استخدم هذا العنوان في Flutter app للاتصال من الـ emulator"
    echo ""
fi

# Get port from .env or use default
PORT=$(grep FLASK_PORT .env 2>/dev/null | cut -d '=' -f2 || echo "5001")

echo "🚀 بدء تشغيل الخادم..."
echo "📍 الخادم سيعمل على: http://localhost:$PORT"
echo "📍 للوصول من الـ emulator: http://$LOCAL_IP:$PORT"
echo ""
echo "⏹️  اضغط Ctrl+C لإيقاف الخادم"
echo ""

# Run the server
python app.py

