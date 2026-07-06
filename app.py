# app.py
import streamlit as st
import pandas as pd
import joblib
import sqlite3

st.set_page_config(page_title="Credit Risk Dashboard", layout="wide")
st.title("🏦 نظام تقييم المخاطر الائتمانية والموافقة على القروض")

# سحب البيانات للعرض الإحصائي
@st.cache_data
def load_loan_data():
    conn = sqlite3.connect('database/credit_risk.db')
    df = pd.read_sql("SELECT * FROM loan_requests", conn)
    conn.close()
    return df

df = load_loan_data()

tab1, tab2 = st.tabs(["📊 مؤشرات المحفظة الائتمانية", "🔮 فحص طلبات القروض"])

# --- التبويب الأول: الإحصائيات ---
with tab1:
    st.header("تحليل طلبات القروض الحالية")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("توزيع مبالغ القروض المطلوبة")
        st.line_chart(df['LoanAmount'])
        
    with col2:
        st.subheader("حالة القروض (0 = ملتزم، 1 = متعثر)")
        st.bar_chart(df['LoanStatus'].value_counts())

# --- التبويب الثاني: التوقع وتقييم المخاطر ---
with tab2:
    st.header("🔍 تفاصيل طلب القرض الجديد")
    
    # تحميل الموديل والأعمدة المحفوظة
    model = joblib.load('models/credit_model.pkl')
    model_features = joblib.load('models/model_features.pkl')
    
    col3, col4 = st.columns(2)
    
    with col3:
        age = st.number_input("عمر المتقدم:", min_value=18, max_value=100, value=25)
        income = st.number_input("الدخل السنوي للعميل ($):", min_value=0.0, value=50000.0)
        loan_amount = st.number_input("قيمة القرض المطلوبة ($):", min_value=0.0, value=10000.0)
        
    with col4:
        loan_intent = st.selectbox("الغرض من القرض:", ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE"])
        history_length = st.slider("طول التاريخ الائتماني (بالسنوات):", min_value=0, max_value=30, value=3)
        
    if st.button("تقييم المخاطر الائتمانية ⚖️", type="primary"):
        # 1. تجهيز الداتا الأساسية
        input_data = pd.DataFrame([{
            'PersonAge': age,
            'PersonIncome': income,
            'LoanAmount': loan_amount,
            'CreditHistoryLength': history_length
        }])
        
        # 2. عمل الـ One-Hot Encoding للغرض المختار
        # بنعمل أعمدة صفار لكل الخيارات
        for intent in ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE"]:
            input_data[f'LoanIntent_{intent}'] = 1 if loan_intent == intent else 0
            
        # 3. إعادة ترتيب الأعمدة لتطابق الموديل بالظبط
        input_data = input_data[model_features]
        
        # 4. التوقع
        prediction = model.predict(input_data)[0]
        
        st.markdown("---")
        if prediction == 1:
            st.error("### ❌ تم رفض الطلب: مستوى المخاطرة مرتفع جداً (احتمالية تعثر في السداد)!")
        else:
            st.success("### ✅ تم قبول الطلب: العميل ذو ثقة ائتمانية ومؤهل للحصول على القرض.")