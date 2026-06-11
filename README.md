# KYC Dashboard — Streamlit App

Dashboard hiển thị dữ liệu KYC (đã unpivot) với 1 trang tổng quan + 10 trang center.

## Cách chạy local

```bash
pip install -r requirements.txt
cd streamlit_kyc
streamlit run app.py
```

## Cách deploy lên Streamlit Cloud

1. Push code lên GitHub
2. Vào https://streamlit.io/cloud → Sign in với GitHub
3. Chọn repo → Deploy
4. Xong! Nhận link public

## Cấu trúc thư mục

```
streamlit_kyc/
├── app.py              # Ứng dụng chính
├── requirements.txt    # Thư viện cần cài
├── data/
│   └── bc_kyc_long_format.xlsx   # Dữ liệu
└── .streamlit/
    └── config.toml     # Theme màu sắc
```
