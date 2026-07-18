# Forecasting Financial Inclusion in Ethiopia

This project tracks, models, and forecasts Ethiopia's digital financial transformation using time series regression and event impact simulation. Built as a pair-programming project for a consortium of stakeholders—including development finance institutions, mobile money operators, and the National Bank of Ethiopia (NBE)—this system analyzes progress on two core targets defined by the World Bank's Global Findex:
1. **Access** — Account Ownership Rate (`ACC_OWNERSHIP`)
2. **Usage** — Digital Payment Adoption Rate (`USG_DIGITAL_PAYMENT`)

---

## 📁 Repository Structure

```
ethiopia-fi-forecast/
├── .github/workflows/
│   └── unittests.yml          # GitHub Actions CI unit test runner
├── data/
│   ├── raw/                  # Raw Excel books and exported baseline CSVs
│   │   ├── ethiopia_fi_unified_data.xlsx
│   │   ├── Additional Data Points Guide.xlsx
│   │   ├── reference_codes.xlsx
│   │   ├── ethiopia_fi_unified_data.csv
│   │   ├── ethiopia_fi_impact_links.csv
│   │   └── reference_codes.csv
│   └── processed/            # Enriched and clean datasets ready for modeling
│       ├── ethiopia_fi_unified_data.csv
│       ├── ethiopia_fi_impact_links.csv
│       └── reference_codes.csv
├── notebooks/                # Jupyter Notebook deliverables for each task
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_event_impact_modeling.ipynb
│   └── 04_forecasting.ipynb
├── src/                      # Core modules and scripts
│   ├── extract_sheets.py     # Parses raw Excel workbooks and outputs CSVs
│   ├── enrich_dataset.py     # Appends observations, events, and impact links
│   ├── run_eda.py            # Runs exploratory data analysis and exports figures
│   ├── impact_model.py       # Simulates event shocks using mathematical ramp functions
│   └── forecaster.py         # Performs OLS trend regressions and scenario simulations
├── dashboard/
│   └── app.py                # High-fidelity interactive Streamlit dashboard
├── tests/                    # Automation test suite
│   ├── test_data_loader.py   # Verifies data-loading integrity
│   └── test_forecaster.py    # Verifies regression and simulation model math
├── reports/
│   ├── interim_report.md     # Task 1 & 2 Interim Submission Report
│   └── figures/              # Generated visualizations
│       ├── temporal_coverage.png
│       ├── account_ownership_trajectory.png
│       ├── digital_payments_vs_mobile_money.png
│       ├── infrastructure_enablers.png
│       ├── association_matrix.png
│       ├── impact_model_validation.png
│       └── forecasting_scenarios.png
├── data_enrichment_log.md    # Source metadata for Task 1 additions
├── requirements.txt          # Python packages list
├── README.md                 # Project README documentation
└── .gitignore                # Configured to ignore venv, python artifacts, etc.
```

---

## 🛠️ Environment Setup & Installation (Windows Terminal)

This project is built using Python 3.11, `virtualenv` (`venv`), and standard data science libraries (Pandas, Statsmodels, Plotly, Streamlit).

### 1. Initialize and Activate Virtual Environment
Open your Windows Terminal (PowerShell) in the project directory:
```powershell
# Create the virtual environment
python -m venv venv

# Set PowerShell execution policy for this terminal session (if restricted)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate the virtual environment
.\venv\Scripts\Activate.ps1
```
Once activated, your terminal prompt will be prefixed with `(venv)`.

### 2. Install Project Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run Automated Tests
Verify that your installation and data models are correct:
```powershell
pytest tests/
```
*(You should see all tests pass successfully).*

---

## 🚀 How to Run the Project Pipeline

### Step 1: Extract Excel Workbooks
Extract the sheets from the raw Excel workbooks into CSV files:
```powershell
python src/extract_sheets.py
```

### Step 2: Enrich the Datasets
Append new observations, regulatory events, and impact links to form the processed datasets:
```powershell
python src/enrich_dataset.py
```

### Step 3: Run Exploratory Analysis & Generate Visuals
Execute the EDA module to save the charts to `reports/figures/`:
```powershell
python src/run_eda.py
```

### Step 4: Run Scenario Projections
Execute the forecasting simulation script to compile numerical projections:
```powershell
python src/forecaster.py
```

### Step 5: Launch the Streamlit Dashboard
Launch the high-fidelity interactive dashboard:
```powershell
streamlit run dashboard/app.py
```

---

## 📊 Summary of Modeling Findings (Projections to 2027)

Our OLS Trend regressions and Scenario-Augmented simulation models project the following trajectories:

### 1. Account Ownership Rate (Access)
*   **OLS Baseline Trend (No Shocks):** Projects **60.5%** by 2027 (95% CI: 50.7% - 70.3%).
*   **Base Scenario (Scheduled Events):** Projects **72.8%** by 2027, driven by the delayed impact of the Fayda National ID rollout and Telebirr/M-Pesa wallet expansions.
*   **Optimistic Scenario (Positive Catalysts):** Projects **85.8%** by 2027, assuming a strict regulatory mandate linking SIM cards to Fayda ID and positive micro-lending licensing shocks.
*   **Pessimistic Scenario (Headwinds):** Projects **69.8%** by 2027.

### 2. Digital Payment Adoption Rate (Usage)
*   **OLS Baseline Trend:** Projects **43.1%** by 2027 (95% CI: 31.2% - 55.0%).
*   **Base Scenario:** Projects **33.6%** by 2027. 
*   **Optimistic Scenario:** Projects **41.1%** by 2027, driven by mobile savings/lending rollouts.
*   **Pessimistic Scenario:** Projects **28.6%** by 2027.

*Note: The OLS baseline usage trend (43.1%) is higher than the Base event simulation (33.6%). This indicates that the rapid growth in digital transactions in Ethiopia is heavily supported by unmodeled organic enablers (such as commercial bank mobile app adoption and merchant cash-free preferences) rather than just major mobile money product launches.*

---

## ⚡ Core Methodology

1.  **Event Shock Ramp Models:** Major events (like mobile money launches) are modeled using time-delayed linear ramp functions:
    $$f(t; t_{event}, \theta, c, W) = c \cdot \min\left(1, \max\left(0, \frac{t - (t_{event} + \theta)}{W}\right)\right)$$
    where $\theta$ is the lag in months, $c$ is the impact magnitude (estimate in percentage points), and $W$ is the build window in months (6, 12, or 24 months based on magnitude).
2.  **Scenario Analysis:** Shocks are applied non-recursively on top of a linear organic growth baseline (2pp/year organic banking access growth).
3.  **Historical Validation:** The model is validated by comparing simulated outputs with actual Global Findex surveys. The overestimation of 2024 Account Ownership (+7.6pp error) validates the presence of the **"multi-homing" constraint** (mobile wallets onboarding existing bank account holders rather than new unbanked individuals).
