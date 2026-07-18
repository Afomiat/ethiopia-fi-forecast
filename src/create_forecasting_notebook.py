import json
import os

def create_forecasting_notebook():
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Time Series Forecasting of Access and Usage\n",
                    "## Forecasting Financial Inclusion in Ethiopia\n",
                    "\n",
                    "This notebook implements time series forecasting models for our two core financial inclusion targets in Ethiopia from 2025 to 2027:\n",
                    "1. **Account Ownership Rate (Access)**: % of adults with an account at a financial institution or mobile money provider.\n",
                    "2. **Digital Payment Adoption Rate (Usage)**: % of adults who made or received a digital payment in the past year.\n",
                    "\n",
                    "We implement and compare two forecasting methodologies:\n",
                    "- **Pure Statistical Baseline (OLS Trend)**: Projects historical Findex trends using linear regression with 95% confidence intervals.\n",
                    "- **Scenario-Augmented Simulations**: Integrates time-delayed event shocks under three forward-looking pathways:\n",
                    "  1. *Base Scenario*: Continuation of current scheduled policy and product rollouts.\n",
                    "  2. *Optimistic Scenario*: Additional positive catalysts (e.g. mobile loan approvals, Fayda ID mandates).\n",
                    "  3. *Pessimistic Scenario*: Negative headwinds (e.g. price inflation, infrastructure stagnation)."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "import statsmodels.api as sm\n",
                    "import os\n",
                    "from IPython.display import Image, display\n",
                    "\n",
                    "# Inline plotting\n",
                    "%matplotlib inline\n",
                    "\n",
                    "# Paths\n",
                    "DATA_PATH = '../data/processed/ethiopia_fi_unified_data.csv'\n",
                    "IMPACT_PATH = '../data/processed/ethiopia_fi_impact_links.csv'\n",
                    "FIG_PATH = '../reports/figures/'"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Pure Statistical OLS Trend Forecasting\n",
                    "We fit an ordinary least squares (OLS) linear trend to the historical survey dates (2011, 2014, 2017, 2021, 2024) to project the baseline trend and estimate 95% confidence intervals."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import sys\n",
                    "sys.path.append('../src')\n",
                    "from forecaster import FinancialInclusionForecaster\n",
                    "\n",
                    "forecaster = FinancialInclusionForecaster(data_path=DATA_PATH, impact_path=IMPACT_PATH)\n",
                    "\n",
                    "df_acc_trend = forecaster.generate_trend_forecast('ACC_OWNERSHIP')\n",
                    "df_pay_trend = forecaster.generate_trend_forecast('USG_DIGITAL_PAYMENT')\n",
                    "\n",
                    "print(\"=== OLS Forecast: Account Ownership (Access) ===\")\n",
                    "print(df_acc_trend)\n",
                    "print(\"\\n=== OLS Forecast: Digital Payment Adoption (Usage) ===\")\n",
                    "print(df_pay_trend)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Scenario-Augmented Forecast Simulations (2025-2027)\n",
                    "We run our scenario simulation model (integrating the event shock ramp functions) to project inclusion rates under Base, Optimistic, and Pessimistic scenarios."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "df_sim = forecaster.run_scenarios()\n",
                    "\n",
                    "target_dates = {2025: '2025-12-31', 2026: '2026-12-31', 2027: '2027-12-31'}\n",
                    "for t in ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT']:\n",
                    "    name = 'Account Ownership (Access)' if t == 'ACC_OWNERSHIP' else 'Digital Payment Usage (Usage)'\n",
                    "    print(f\"\\n=== {name} Scenarios ===\")\n",
                    "    for year, dt in target_dates.items():\n",
                    "        closest_idx = df_sim.index.get_indexer([pd.to_datetime(dt)], method='nearest')[0]\n",
                    "        val_base = df_sim[f'{t}_base'].iloc[closest_idx]\n",
                    "        val_opt = df_sim[f'{t}_optimistic'].iloc[closest_idx]\n",
                    "        val_pess = df_sim[f'{t}_pessimistic'].iloc[closest_idx]\n",
                    "        print(f\"- {year}: Base = {val_base:.2f}%, Optimistic = {val_opt:.2f}%, Pessimistic = {val_pess:.2f}%\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualizing Forecasting Scenarios\n",
                    "We render the scenario comparison chart, overlaying the historical survey observations, the OLS statistical trend line (with 95% shaded confidence intervals), and the three scenario simulations."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "display(Image(filename=os.path.join(FIG_PATH, 'forecasting_scenarios.png')))"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 4. Analytical Interpretation and Key Takeaways\n",
                    "\n",
                    "### 1. Access (Account Ownership Rate) Forecasts\n",
                    "- **Statistical Trend**: OLS projects a steady rise to **60.51%** by 2027 (95% CI: 50.69% - 70.32%).\n",
                    "- **Base Simulation**: Projects **72.83%** by 2027. This represents a substantial lift over the statistical baseline, driven by the delayed impact of the Fayda Digital ID program rollout and Telebirr/M-Pesa integration.\n",
                    "- **Optimistic Scenario**: Projects **85.81%** by 2027, assuming a regulatory mandate that links all SIM/wallet activations directly to Fayda ID and approves digital micro-lending licenses in 2026.\n",
                    "- **Pessimistic Scenario**: Projects **69.83%** by 2027. Here, slow network rollout and customer trust/fraud issues choke off account creation, leaving it slightly below the Base scenario.\n",
                    "\n",
                    "### 2. Usage (Digital Payment Adoption Rate) Forecasts\n",
                    "- **Statistical Trend**: OLS projects **43.09%** usage by 2027 (95% CI: 31.16% - 55.03%).\n",
                    "- **Base Simulation**: Projects **33.56%** by 2027. Interestingly, the event-based simulation is *lower* than the statistical trend. This suggests that the rapid rise of digital payments is driven by unmodeled organic factors (such as the widespread integration of mobile banking apps by commercial banks like CBE, or general merchant pricing adjustments) rather than just the specific major launch events.\n",
                    "- **Optimistic Scenario**: Projects **41.06%** by 2027. The introduction of digital savings/lending products on mobile money channels acts as a major catalyst, closing the gap with the statistical trend.\n",
                    "- **Pessimistic Scenario**: Projects **28.56%** by 2027. Price hikes and digital transaction service charges depress customer usage, leading to stagnation.\n",
                    "\n",
                    "### 3. Key Uncertainties and Forecasting Limitations:\n",
                    "1. **Survey Frequency**: Because Findex data is only collected every 3-4 years, the statistical trend regression is highly sensitive to the small sample size (5 data points).\n",
                    "2. **Multi-Homing Behavior**: If future events merely cause existing bank customers to open additional mobile wallets, the actual Findex Account Ownership Rate (which is binary: yes/no) will stagnate, while administrative operator account numbers will surge. The Optimistic scenario assumes we successfully onboard *new* unbanked populations."
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    notebook_path = 'notebooks/04_forecasting.ipynb'
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)
    print(f"Created {notebook_path}")

if __name__ == '__main__':
    create_forecasting_notebook()
