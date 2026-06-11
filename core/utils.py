import streamlit as st
from core.constants import COLOR_PRIMARY, COLOR_HEADER


def fmt_num(n):
    if n >= 1000: return f"{n:,}"
    return str(n)


def metric_card(col, label, value, suffix=""):
    col.markdown(
        f"""
        <div style="background:white;border-radius:10px;padding:16px 12px;text-align:center;
                    box-shadow:0 1px 3px rgba(0,0,0,0.06);height:148px;
                    box-sizing:border-box;
                    display:flex;flex-direction:column;justify-content:center;">
            <div style="font-size:12px;color:#888;text-transform:uppercase;letter-spacing:0.5px;">{label}</div>
            <div style="font-size:28px;font-weight:700;color:{COLOR_PRIMARY};margin-top:4px;">{value}</div>
            {f'<div style="font-size:12px;color:#666;">{suffix}</div>' if suffix else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def styled_header(title, subtitle=""):
    st.markdown(
        f"""
        <div style="background:{COLOR_HEADER};padding:24px 24px 18px 24px;margin:0 -16px 16px -16px;border-radius:10px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="color:white;font-size:18px;font-weight:600;">{title}</div>
                {f'<div style="color:rgba(255,255,255,0.85);font-size:13px;">{subtitle}</div>' if subtitle else ''}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(text):
    st.markdown(
        f"<h3 style='font-size:14px;font-weight:600;color:#555;margin:16px 0 8px;text-transform:uppercase;letter-spacing:0.3px;'>{text}</h3>",
        unsafe_allow_html=True,
    )
