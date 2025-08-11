# 📈 Stock Alerts API

نظام API لإدارة تنبيهات الأسهم مع إرسال إشعارات بريدية عند تحقق الشروط.

---

## 🛠️ المتطلبات

- Python 3.8+  
- Django 4+  
- Django REST Framework  
- مكتبة `apscheduler` للمهام المجدولة  
- إعدادات بريد SMTP (مثل Gmail)

---

## 🚀 تشغيل المشروع

1. تثبيت الحزم المطلوبة:

pip install -r requirements.txt



2. إنشاء الهجرات وترحيل قاعدة البيانات:

python manage.py makemigrations
python manage.py migrate



3. بدء الخادم:

python manage.py runserver



---

## 🔑 نقاط نهاية الـ API (API Endpoints)

| الطريقة  | المسار                    | الوصف                      | الحماية             |
|----------|---------------------------|----------------------------|---------------------|
| POST     | `/api/register/`           | تسجيل مستخدم جديد           | مفتوح (AllowAny)     |
| POST     | `/api/token/`              | الحصول على توكن JWT         | مفتوح               |
| POST     | `/api/token/refresh/`      | تحديث توكن JWT              | مفتوح               |
| GET، POST، PUT، DELETE | `/api/alerts/`          | إدارة التنبيهات             | محمي (مستخدم مسجل)  |
| GET      | `/api/triggered-alerts/`   | عرض التنبيهات التي تم تفعيلها| محمي (مستخدم مسجل)  |

---

## 🛡️ طريقة التسجيل وتسجيل الدخول

- تسجيل مستخدم جديد بPOST إلى `/api/register/` مع بيانات:

{
"username": "yourusername",
"email": "youremail@example.com",
"password": "yourpassword"
}



- تسجيل الدخول بPOST إلى `/api/token/` مع:

{
"username": "yourusername",
"password": "yourpassword"
}

سيرجع لك Access Token و Refresh Token:

{
"access": "<access_token>",
"refresh": "<refresh_token>"
}

---

## 🧩 كيفية استخدام التوكن

أضف الهيدر التالي في كل طلب API محمي:

Authorization: Bearer <access_token>

---

## 🔄 جدولة المهام

- يتم استخدام مكتبة `apscheduler` لفحص أسعار الأسهم وتنفيذ تنبيهات كل دقيقة تلقائيًا.
- يمكن تعديل إعدادات الجدولة في ملف `scheduler.py`.

---

## ✉️ إعداد البريد الإلكتروني في `settings.py`

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # مثال Gmail SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-email-password' # استخدم App Password لأمان أكثر


---

## ⚙️ استخدام API التنبيهات

1. أنشئ تنبيه جديد بPOST إلى `/api/alerts/`:

{
"stock_symbol": "AAPL",
"alert_type": "threshold",
"threshold_value": 150,
"condition": "gt",
"duration_hours": 0,
"is_active": true
}



2. استعرض التنبيهات بGET على `/api/alerts/`.

3. استعرض التنبيهات المشغلة بGET على `/api/triggered-alerts/`.

---

## 📋 تطوير مستقبلي

- إضافة اختبارات (tests)  
- إرسال البريد بشكل غير متزامن (مثلاً Celery)  
- واجهة مستخدم Frontend  
- توثيق API تلقائيًا باستخدام Swagger أو Redoc

---

## دعم ومساعدة

إذا احتجت شرحًا أو مساعدة أخرى في تشغيل أو تطوير المشروع، أنا جاهز لدعمك.

---
