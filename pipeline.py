# pipeline.py
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def run_ml_pipeline():
    print("⏳ جاري سحب البيانات المعقدة من داتابيز القروض...")
    # 1. سحب البيانات
    conn = sqlite3.connect('database/credit_risk.db')
    df = pd.read_sql("SELECT * FROM loan_requests", conn)
    conn.close()
    
    # 2. فصل المتغيرات (الهدف هو LoanStatus: متعثر 1 أو ملتزم 0)
    X = df.drop(columns=['LoanStatus'])
    if 'id' in X.columns:
        X = X.drop(columns=['id'])
    y = df['LoanStatus']
    
    # 3. تحويل العمود النصي LoanIntent إلى أرقام (One-Hot Encoding)
    X = pd.get_dummies(X, columns=['LoanIntent'], drop_first=False)
    
    # حفظ شكل الأعمدة النهائي عشان الـ Dashboard تمشي عليه بالملي
    os.makedirs('models', exist_ok=True)
    joblib.dump(X.columns.tolist(), 'models/model_features.pkl')
    
    # 4. تقسيم البيانات
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    print("🤖 جاري تدريب موديل تقييم المخاطر الائتمانية...")
    # 5. تدريب الموديل
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 6. التقييم السريع والحفظ
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"🎯 دقة الموديل الحالية في تحديد المخاطر: {acc * 100:.2f}%")
    
    joblib.dump(model, 'models/credit_model.pkl')
    print("💾 تم حفظ الموديل بنجاح في فولدر models/credit_model.pkl\n")

if __name__ == "__main__":
    run_ml_pipeline()