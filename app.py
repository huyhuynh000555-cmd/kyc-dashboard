import streamlit as st
from data_layer.repository import load_data
from sidebar.presentation import render_sidebar
from features.overview.presentation import render_overview
from features.center.presentation import render_center

st.set_page_config(
    page_title="KYC Dashboard",
    page_icon="assets/compact_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS: equal height + card style + column gap ──
st.markdown("""
<style>
    /* Equal height columns */
    div[data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
        gap: 9px !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        display: flex;
    }
    div[data-testid="stHorizontalBlock"] > div > div {
        flex: 1;
    }
    /* Card-style chart background */
    .stPlotlyChart {
        background: white;
        border-radius: 10px;
        padding: 9px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    /* Cho phép chart vượt container (hết bị cắt padding) */
    div[data-testid="stElementContainer"] {
        overflow: visible !important;
    }
    div[data-testid="stFullScreenFrame"] {
        overflow: hidden !important;
    }
    /* Tắt scrollbar trong Plotly legend */
    .scrollbar {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

students_df, multi_df = load_data()

centers = sorted(students_df["Primary Center"].unique().tolist())
page, selected_center, course_filter, source_filter, gender_filter, age_filter = render_sidebar(students_df, centers)

# ── Apply filters ──
filtered_students = students_df.copy()
if course_filter != "Tất cả":
    filtered_students = filtered_students[filtered_students["Course Simplified"] == course_filter]
if source_filter != "Tất cả":
    filtered_students = filtered_students[filtered_students["Source Simplified"] == source_filter]
if gender_filter != "Tất cả":
    filtered_students = filtered_students[filtered_students["Gender"] == gender_filter]
if age_filter != "Tất cả":
    filtered_students = filtered_students[filtered_students["Age Group"] == age_filter]

# Filter multi_df theo danh sách Student ID đã lọc
valid_ids = filtered_students["Student ID"].unique()
filtered_multi = multi_df[multi_df["Student ID"].isin(valid_ids)]

if page == "📈 Tổng quan":
    render_overview(filtered_students, filtered_multi)
else:
    render_center(filtered_students, filtered_multi, selected_center)
