# database/db_handler.py
import sqlite3
import pandas as pd
import os

def init_db():
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect('database/credit_risk.db')
    cursor = conn.cursor()
    
    # إنشاء جدول تقييم مخاطر القروض
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loan_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            PersonAge INTEGER,
            PersonIncome REAL,
            LoanAmount REAL,
            LoanIntent TEXT,
            CreditHistoryLength INTEGER,
            LoanStatus INTEGER
        )
    ''''')
    conn.commit()
    conn.close()
    print("✅ تم إنشاء قاعدة بيانات المخاطر الائتمانية بنجاح!")

def load_csv_to_db():
    df = pd.read_csv('data/credit_risk.csv')
    conn = sqlite3.connect('database/credit_risk.db')
    
    # رفع البيانات للجدول
    df.to_sql('loan_requests', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
    print(f"✅ تم رفع {len(df)} طلب قرض إلى الداتابيز بنجاح!")

if __name__ == "__main__":
    init_db()
    load_csv_to_db()