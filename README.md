# 🏦 Credit Risk Assessment & Loan Approval Pipeline

مشروع متكامل (End-to-End Pipeline) لتقييم المخاطر الائتمانية وتوقع احتمالية تعثر العملاء في سداد القروض (Credit History & Default Risk) باستخدام خوارزميات تعلم الآلة وواجهة تفاعلية ذكية.

مميزات المشروع (Features)
* **هندسة البيانات (Data Engineering):** بناء وإدارة قاعدة بيانات محلية باستخدام **SQLite** لتخزين طلبات القروض ومعالجتها.
* **معالجة البيانات (Data Preprocessing):** تطبيق تقنية **One-Hot Encoding** للتعامل مع المتغيرات النصية (مثل غرض القرض) لتهيئتها للموديل.
* **تعلم الآلة (Machine Learning):** تدريب موديل **Random Forest Classifier** لتصنيف جدارة العملاء الائتمانية وتوقع نسبة المخاطرة بدقة.
* **لوحة تحكم تفاعلية (Dashboard):** واجهة مستخدم متطورة بـ **Streamlit** تعرض مؤشرات المحفظة الائتمانية للبنك، مع نظام فحص فوري لطلبات القروض الجديدة.

تقسيم المشروع (Project Structure)
```text
├── data/               # ملف البيانات المالية الحساسة (CSV)
├── database/           # كود إنشاء وإدارة قاعدة بيانات القروض SQLite
├── models/             # الموديل المدرب وملفات تحويل الأعمدة المحفوظة
├── app.py              # كود واجهة لوحة التحكم وفحص القروض (Streamlit)
├── pipeline.py         # كود سحب البيانات، المعالجة، تدريب الموديل وتقييمه
└── README.md           # توثيق المشروع الشامل
(How to Run)
تثبيت المكتبات الأساسية:
pip install pandas scikit-learn streamlit joblib

تهيئة قاعدة البيانات ورفع طلبات القروض:
python database/db_handler.py

تشغيل الـ Pipeline وتدريب موديل المخاطر:
python pipeline.py

إطلاق لوحة التحكم (Dashboard):
streamlit run app.py