# Forecasting Financial Inclusion in Ethiopia

This project aims to build a forecasting system that tracks Ethiopia's digital financial transformation using time series methods. The system focuses on predicting Ethiopia's progress on two core dimensions of financial inclusion:
1. **Access** — Account Ownership Rate
2. **Usage** — Digital Payment Adoption Rate

## Project Structure

```
ethiopia-fi-forecast/
├── .github/workflows/
│   └── unittests.yml
├── data/
│   ├── raw/                      # Starter dataset
│   │   ├── ethiopia_fi_unified_data.csv (to be added)
│   │   └── reference_codes.csv (to be added)
│   └── processed/                # Analysis-ready data
├── notebooks/
│   └── README.md
├── src/
│   ├── __init__.py
├── dashboard/
│   └── app.py
├── tests/
│   └── __init__.py
├── models/
├── reports/
│   └── figures/
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Set Up the Environment (Windows Terminal)

### 1. Set Up Python Virtual Environment
Open Windows Terminal in this repository directory and run:
```powershell
# Create virtual environment
python -m venv venv
```

### 2. Activate the Environment
Depending on your shell, run:
- **PowerShell (Recommended)**:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  .\venv\Scripts\Activate.ps1
  ```
- **Command Prompt (CMD)**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```

Once activated, your terminal prompt should display `(venv)`.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Running the Dashboard
After installing the requirements, run:
```bash
streamlit run dashboard/app.py
```
