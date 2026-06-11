import pandas as pd
from pathlib import Path
import streamlit as st


# ── Constants ──
CENTER_MAP = {
    "Tran Van Xa": "Nguyễn Khuyến", "Le Duan": "Lê Duẩn",
    "Vo Thi Sau": "Võ Thị Sáu", "Pham Van Thuan": "Phạm Văn Thuận",
    "Nguyen Trai": "Nguyễn Trãi", "Hung Vuong": "Hùng Vương",
    "Phuoc Tan": "Phước Tân", "Tran Phu": "Trần Phú",
    "Binh Phuoc": "Bình Phước",
}
MULTI_SELECT_COLS = ["Interest", "Problem", "Goal", "Target Destination"]


def load_data():
    """Đọc raw wide format → trả về (students_df, multi_df)"""
    raw = _read_raw_wide()

    # ── 1. students_df: single-value columns ──
    single_cols = [c for c in raw.columns if c not in MULTI_SELECT_COLS]
    students = raw[single_cols].copy()

    # Clean center names
    students["Primary Center"] = students["Primary Center"].map(CENTER_MAP).fillna(students["Primary Center"])
    students["Age"] = pd.to_numeric(students["Age"], errors="coerce")

    # Clean "0" → "Không có thông tin"
    for col in ["Parent 1 Job", "Parent 2 Job"]:
        if col in students.columns:
            students[col] = students[col].replace("0", "Không có thông tin")
            students[col] = students[col].replace(0, "Không có thông tin")

    # Rule: có tên PH + ko có job → "Không có thông tin"; ko có tên PH + ko job → bỏ qua
    for pname, pjob in [("Parent 1 Name", "Parent 1 Job"), ("Parent 2 Name", "Parent 2 Job")]:
        if pname in students.columns:
            mask = students[pname].notna() & (students[pjob].isna() | (students[pjob] == "Không có thông tin"))
            students.loc[mask, pjob] = "Không có thông tin"

    # Clean "Trường ." → NaN
    dirty = students["School Name"].astype(str).str.strip().str.lower().str.match(r'^trường\s*\.{1,}$')
    students.loc[dirty, "School Name"] = pd.NA

    # Age Group
    bins, labels = [0, 5, 8, 12, 15, 200], ["3-5", "6-8", "9-12", "13-15", "16+"]
    students["Age Group"] = pd.cut(students["Age"], bins=bins, labels=labels, right=True).astype(str)

    # Study Abroad Flag
    def study_flag(cost):
        if pd.isna(cost): return "Không"
        c = str(cost).strip().lower()
        return "Không" if c in ("-none-", "no information yet", "") else "Có"
    students["Có Du Học"] = students["Study Abroad Cost"].apply(study_flag)

    # Course Simplified
    def course_simple(c):
        if pd.isna(c): return None
        orig = str(c).strip()
        uc = orig.upper()
        if "EGENIUS" in uc.replace("-", ""): return "B2C-EGENIUS"
        if "IELTS" in uc: return "B2C-IELTSNEXTGEN"
        if "EPIONEER" in uc: return "B2C-EPIONEER"
        return orig
    students["Course Simplified"] = students["Course Category"].apply(course_simple)

    # Source Simplified
    def source_simple(s):
        if pd.isna(s): return "Khác"
        s = str(s).strip()
        return s if s in ("Walk in", "Local Data", "EC Referral", "Digital Marketing", "Trade Show") else "Khác"
    students["Source Simplified"] = students["Source"].apply(source_simple)

    # Learning History Group
    def history_group(h):
        if pd.isna(h) or str(h).strip().lower() in ("-none-", "chưa có", ""):
            return "Không có"
        h_lower = str(h).strip().lower()
        if "đang" in h_lower and ("vmg" in h_lower or "vmc" in h_lower): return "Đang học tại VMG"
        if "cũ" in h_lower and ("vmg" in h_lower or "vmc" in h_lower): return "Từng học VMG"
        if "từng" in h_lower and ("vmg" in h_lower or "vmc" in h_lower): return "Từng học VMG"
        if ("kiểm tra" in h_lower or "test" in h_lower) and ("vmg" in h_lower or "vmc" in h_lower): return "Đã test đầu vào VMG"
        if "trường" in h_lower or "chỉ học" in h_lower or "học ở" in h_lower: return "Chỉ học ở trường"
        if "trung tâm" in h_lower or "hvg" in h_lower: return "Từng học TT khác"
        if "chưa" in h_lower: return "Chưa học TA"
        return "Khác"
    students["Learning History Group"] = students["Learning History"].apply(history_group)

    # ── 2. multi_df: unpivot multi-select columns ──
    multi_rows = []
    for _, row in raw.iterrows():
        sid = row["Student ID"]
        for col in MULTI_SELECT_COLS:
            val = row.get(col)
            if pd.isna(val):
                continue
            for item in str(val).split(","):
                item = item.strip()
                if item and item.lower() != "-none-":
                    multi_rows.append({"Student ID": sid, "Dimension": col, "Value": item})

    multi = pd.DataFrame(multi_rows)

    # Add "Không có dữ liệu" for students with zero multi-select data
    students_with_multi = set(multi["Student ID"].unique()) if not multi.empty else set()
    no_data_students = [s for s in students["Student ID"] if s not in students_with_multi]
    if no_data_students:
        no_data_rows = [{"Student ID": s, "Dimension": "Không có dữ liệu", "Value": "–"} for s in no_data_students]
        multi = pd.concat([multi, pd.DataFrame(no_data_rows)], ignore_index=True)

    return students, multi


def _read_raw_wide():
    """Đọc raw wide format từ Google Sheets hoặc fallback Excel"""
    # ── Try Google Sheets ──
    try:
        if "sheets_id" in st.secrets:
            import gspread
            from google.oauth2.service_account import Credentials

            scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
            creds = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes=scope
            )
            client = gspread.authorize(creds)
            sheet = client.open_by_key(st.secrets["sheets_id"])
            ws = sheet.sheet1
            rows = ws.get_all_records()
            df = pd.DataFrame(rows)
            if not df.empty:
                df.columns = [c.replace("\xa0", "").strip() for c in df.columns]
                return df
    except Exception:
        pass  # No Google Sheets config — use local Excel

    # ── Fallback: raw Excel file ──
    paths = [
        "storage/data.xlsx",
        "../bc tất cả data đã kyc (Need 2 clean).xlsx",
        "E:/bc tất cả data đã kyc (Need 2 clean).xlsx",
        "/mnt/e/bc tất cả data đã kyc (Need 2 clean).xlsx",
    ]
    for p in paths:
        if Path(p).exists():
            df = pd.read_excel(p, engine="openpyxl")
            df.columns = [c.replace("\xa0", "").strip() for c in df.columns]
            return df

    st.error(
        "Không tìm thấy dữ liệu! "
        "Cần file raw Excel: 'bc tất cả data đã kyc (Need 2 clean).xlsx' "
        "tại thư mục storage/ hoặc thư mục gốc của app. "
        "Hoặc config Google Sheets trong secrets.toml."
    )
    st.stop()
