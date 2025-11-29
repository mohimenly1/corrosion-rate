# استكشاف الأخطاء - خطأ 500 في Data Screen

## المشكلة
خطأ 500 يظهر في شاشة البيانات بدون رسالة خطأ واضحة.

## الحلول

### 1️⃣ اختبار قاعدة البيانات

قم بتشغيل سكريبت الاختبار:

```bash
cd backend
python test_db_connection.py
```

هذا السكريبت سيفحص:
- ✅ اتصال قاعدة البيانات
- ✅ وجود قاعدة البيانات `corrosion_db`
- ✅ وجود الجداول المطلوبة

### 2️⃣ إنشاء قاعدة البيانات (إذا لم تكن موجودة)

```bash
cd backend
./setup_database.sh
```

أو يدوياً:
```bash
mysql -u root -p < backend/database/schema.sql
```

### 3️⃣ التحقق من ملف .env

تأكد من أن ملف `.env` موجود ويحتوي على:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=corrosion_db
FLASK_ENV=development
FLASK_PORT=5001
```

### 4️⃣ التحقق من أن MySQL يعمل

```bash
# على macOS
brew services list | grep mysql
# أو
sudo /usr/local/mysql/support-files/mysql.server status

# تشغيل MySQL إذا لم يكن يعمل
brew services start mysql
# أو
sudo /usr/local/mysql/support-files/mysql.server start
```

### 5️⃣ فحص سجلات Backend

عند تشغيل Backend، راقب السجلات (logs) في Terminal. ستظهر رسائل خطأ واضحة مثل:

```
ERROR: Error connecting to MySQL: ...
ERROR: Database error in get_samples: ...
```

### 6️⃣ اختبار API مباشرة

```bash
# اختبار health endpoint
curl http://localhost:5001/api/health

# اختبار samples endpoint
curl http://localhost:5001/api/samples
```

إذا ظهر خطأ، ستظهر رسالة الخطأ في JSON.

---

## الأخطاء الشائعة وحلولها

### ❌ "Table 'corrosion_db.corrosion_samples' doesn't exist"

**الحل:**
```bash
cd backend
./setup_database.sh
```

### ❌ "Access denied for user 'root'@'localhost'"

**الحل:**
1. تحقق من كلمة المرور في `.env`
2. أو قم بإنشاء مستخدم جديد:
```sql
CREATE USER 'corrosion_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON corrosion_db.* TO 'corrosion_user'@'localhost';
FLUSH PRIVILEGES;
```

### ❌ "Can't connect to MySQL server"

**الحل:**
1. تأكد من أن MySQL يعمل
2. تحقق من أن `DB_HOST` في `.env` صحيح

### ❌ "Unknown database 'corrosion_db'"

**الحل:**
```bash
cd backend
./setup_database.sh
```

---

## تحسينات تم إضافتها

✅ **معالجة أفضل للأخطاء في Backend:**
- رسائل خطأ واضحة
- فحص وجود الجداول
- سجلات مفصلة

✅ **عرض أفضل للأخطاء في Flutter:**
- رسائل خطأ واضحة
- نصائح للمستخدم
- عرض تفاصيل الخطأ

✅ **سكريبت اختبار قاعدة البيانات:**
- `test_db_connection.py` - لفحص الاتصال والجداول

---

## الخطوات التالية

1. ✅ شغّل `test_db_connection.py` لفحص قاعدة البيانات
2. ✅ إذا كانت قاعدة البيانات غير موجودة، شغّل `setup_database.sh`
3. ✅ أعد تشغيل Backend
4. ✅ أعد تحميل البيانات في Flutter App

---

**إذا استمرت المشكلة، راجع سجلات Backend في Terminal للحصول على تفاصيل الخطأ.**

