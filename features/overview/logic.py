def calculate_overview_stats(df):
    return {
        "total_students": df["Student ID"].nunique(),
        "avg_age": df["Age"].dropna().mean(),
        "study_abroad": df[df["Có Du Học"] == "Có"]["Student ID"].nunique(),
    }
