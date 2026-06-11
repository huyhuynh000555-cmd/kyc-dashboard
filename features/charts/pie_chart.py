import plotly.express as px
import pandas as pd


def create_pie_chart(df, name_col, value_col, name_display, colors, threshold_pct=2, height=300):
    counts = df.groupby(name_col)[value_col].nunique().reset_index()
    counts.columns = [name_display, value_col]
    total = counts[value_col].sum()
    counts["pct"] = counts[value_col] / total * 100
    counts["legend"] = counts.apply(lambda r: f"{r[value_col]} {r[name_display]}", axis=1)
    texts = [None if p < threshold_pct else f"{p:.1f}%" for p in counts["pct"]]
    fig = px.pie(counts, names="legend", values=value_col,
                 color_discrete_sequence=colors)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), dragmode=False, height=height,
                      legend=dict(orientation="v", y=0.5, x=1.02, font=dict(size=12)),
                      paper_bgcolor="white")
    fig.update_traces(text=texts, textinfo='text', textposition='inside', textfont_size=13)
    return fig


def create_gender_pie(df, colors, height=130):
    gender_counts = df[df["Gender"].isin(["Male", "Female"])]["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Giới tính", "Số lượng"]
    gender_counts["Giới tính"] = gender_counts["Giới tính"].map({"Male": "Nam", "Female": "Nữ"})
    total = gender_counts["Số lượng"].sum()
    gender_counts["pct"] = gender_counts["Số lượng"] / total * 100
    gender_counts["legend"] = gender_counts.apply(lambda r: f"{r['Số lượng']} {r['Giới tính']}", axis=1)
    texts = [None if p < 2 else f"{p:.1f}%" for p in gender_counts["pct"]]
    fig = px.pie(gender_counts, names="legend", values="Số lượng",
                 color_discrete_sequence=colors)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), dragmode=False, height=height,
                      legend=dict(orientation="v", y=0.5, x=1.02, font=dict(size=12)),
                      paper_bgcolor="white")
    fig.update_traces(text=texts, textinfo='text', textposition='inside', textfont_size=13)
    return fig


def create_learning_history_pie(df, colors, height=300):
    counts = df["Learning History Group"].value_counts().reset_index()
    counts.columns = ["Lịch sử", "Học viên"]
    total = counts["Học viên"].sum()
    counts["pct"] = counts["Học viên"] / total * 100
    counts["legend"] = counts.apply(lambda r: f"{r['Học viên']} {r['Lịch sử']}", axis=1)
    texts = [None if p < 2 else f"{p:.1f}%" for p in counts["pct"]]
    fig = px.pie(counts, names="legend", values="Học viên",
                 color_discrete_sequence=colors)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), dragmode=False, height=height,
                      legend=dict(orientation="v", y=0.5, x=1.02, font=dict(size=12)),
                      paper_bgcolor="white")
    fig.update_traces(text=texts, textinfo='text', textposition='inside', textfont_size=13)
    return fig


def create_coverage_pie(df, chart_type, colors, height=250):
    """Create a 2-slice pie chart showing data coverage.
    chart_type: 'parent_job' (PH1 + PH2 aggregated) or 'school'
    """
    if chart_type == "parent_job":
        ph1 = df[["Parent 1 Job"]].rename(columns={"Parent 1 Job": "Job"})
        ph2 = df[["Parent 2 Job"]].rename(columns={"Parent 2 Job": "Job"})
        # Lọc bỏ PH không tồn tại (ko có tên PH)
        if "Parent 1 Name" in df.columns:
            ph1 = ph1[df["Parent 1 Name"].notna()]
        if "Parent 2 Name" in df.columns:
            ph2 = ph2[df["Parent 2 Name"].notna()]
        all_ph = pd.concat([ph1, ph2], ignore_index=True)
        has_info = all_ph["Job"].notna() & (all_ph["Job"] != "Không có thông tin")
        has = has_info.sum()
        no = (~has_info).sum()
        has_label, no_label = "Đã có thông tin", "Không có thông tin"
    else:  # school
        has = df["School Name"].notna().sum()
        no = df["School Name"].isna().sum()
        has_label, no_label = "Đã có tên trường", "Không có thông tin"

    coverage = pd.DataFrame({"Status": [has_label, no_label], "Số lượng": [has, no]})
    coverage["pct"] = coverage["Số lượng"] / coverage["Số lượng"].sum() * 100
    coverage["legend"] = coverage.apply(lambda r: f"{r['Số lượng']} {r['Status']}", axis=1)
    texts = [None if p < 2 else f"{p:.1f}%" for p in coverage["pct"]]
    fig = px.pie(coverage, names="legend", values="Số lượng",
                 color_discrete_sequence=colors)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), dragmode=False, height=height,
                      legend=dict(orientation="v", y=0.5, x=1.02, font=dict(size=11)),
                      paper_bgcolor="white")
    fig.update_traces(text=texts, textinfo='text', textposition='inside', textfont_size=13)
    return fig
