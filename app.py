import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="RF Cable Expert", layout="wide")

st.title("📡 RF Cable Engineering Wizard")
st.markdown("---")

# חלוקת המסך לעמודות
col_in, col_out = st.columns([1, 2])

with col_in:
    st.header("📋 דרישות ונתונים")
    pn = st.text_input("מק\"ט כבל", "PLTS 240")
    freq = st.number_input("תדר עבודה (GHz)", value=5.0, step=0.1)
    length = st.number_input("אורך כבל (מטרים)", value=1.0, step=0.1)
    
    st.subheader("סביבת עבודה")
    t_min = st.number_input("טמפ' מינימום (C)", value=-50)
    t_max = st.number_input("טמפ' מקסימום (C)", value=85)
    
    st.subheader("נתוני יצרן (מה-Datasheet)")
    loss_per_m = st.number_input("ניחות למטר (dB/m)", value=0.58)
    ppm_val = st.number_input("מקדם פאזה תרמי (PPM)", value=100)

# חישובים הנדסיים
delta_t = t_max - t_min
total_loss = (length * loss_per_m) + 0.3 # 0.3dB estimate for connectors
v_p = 0.83
phase_shift_mm = length * delta_t * ppm_val * 1e-3
wavelength_mm = (300 / freq) * v_p
phase_deg = (phase_shift_mm / wavelength_mm) * 360

with col_out:
    st.header("📊 ניתוח תוצאות")
    
    # תצוגת Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("ניחות כולל", f"{total_loss:.2f} dB")
    m2.metric("סטיית פאזה תרמית", f"{phase_deg:.1f}°")
    m3.metric("שינוי אורך חשמלי", f"{phase_shift_mm:.2f} mm")
    
    # טבלת סיכום
    st.subheader("סיכום מפרט טכני")
    res_df = pd.DataFrame({
        "Parameter": ["Cable P/N", "Frequency", "Length", "Total Loss", "Phase Stability (Temp)"],
        "Value": [pn, f"{freq} GHz", f"{length} m", f"{total_loss:.2f} dB", f"{phase_deg:.1f} degrees"]
    })
    st.table(res_df)

    # כפתור הורדה
    csv = res_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 הורד דוח RF (CSV)", csv, f"Report_{pn}.csv", "text/csv")
