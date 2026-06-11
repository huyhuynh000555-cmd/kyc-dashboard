@echo off
echo === KYC Dashboard - Setup ===

cd /d "E:\pi_output\kyc_googlesheet"

:: Copy raw data if not exists
if not exist "storage\data.xlsx" (
    echo Copying raw data...
    copy "E:\bc tất cả data đã kyc (Need 2 clean).xlsx" "storage\data.xlsx"
)

:: Create venv
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate & install
call venv\Scripts\activate
echo Installing packages...
pip install -r requirements.txt

echo.
echo === Done! Run: streamlit run app.py ===
echo.
cmd /k
