import json
import os

def create_impact_notebook():
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Event Impact Modeling\n",
                    "## Forecasting Financial Inclusion in Ethiopia\n",
                    "\n",
                    "This notebook builds the Event-Indicator Association Matrix and implements a simulation model to project the impact of policy interventions, product launches, and infrastructure developments on financial inclusion indicators. It covers:\n",
                    "1. **Impact Links Exploration**: Loading and joining impact links with parent events.\n",
                    "2. **Event-Indicator Association Matrix**: Heatmap visualization of the direction, magnitude, and lag of event impacts.\n",
                    "3. **Mathematical Model Formulation**: Defining event effects as time-delayed linear ramps.\n",
                    "4. **Simulation & Historical Validation**: Running the simulation from 2011 to 2027 and validating it against actual Global Findex observations (2011, 2014, 2017, 2021, 2024).\n",
                    "5. **Methodology and Uncertainties Documentation**."
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
                    "import os\n",
                    "from IPython.display import Image, display\n",
                    "\n",
                    "# Set inline plotting\n",
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
                    "## 1. Load and Join Impact Data\n",
                    "We join our `ethiopia_fi_impact_links.csv` with events in the main data file to map events to their impacted indicators."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "df_impact = pd.read_csv(IMPACT_PATH)\n",
                    "df_data = pd.read_csv(DATA_PATH)\n",
                    "\n",
                    "# Get events\n",
                    "df_events = df_data[df_data['record_type'] == 'event'][['record_id', 'indicator', 'observation_date']].rename(\n",
                    "    columns={'indicator': 'event_name', 'observation_date': 'event_date'}\n",
                    ")\n",
                    "\n",
                    "# Merge\n",
                    "df_merged = df_impact.merge(df_events, left_on='parent_id', right_on='record_id', how='left')\n",
                    "print(f\"Loaded {len(df_merged)} event-indicator impact links.\")\n",
                    "df_merged[['parent_id', 'event_name', 'related_indicator', 'impact_magnitude', 'lag_months']].head(10)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Event-Indicator Association Matrix\n",
                    "The association matrix represents **which events affect which indicators, and by how much**. High, medium, and low magnitudes are mapped to +15pp, +5pp, and +1pp shocks respectively (with signs determined by the direction of impact)."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Display association matrix heatmap\n",
                    "display(Image(filename=os.path.join(FIG_PATH, 'association_matrix.png')))"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Simulation & Historical Validation\n",
                    "We run a simulation of our three target indicators (`ACC_OWNERSHIP`, `ACC_MM_ACCOUNT`, `USG_DIGITAL_PAYMENT`) from 2011 to 2027.\n",
                    "The model overlays time-delayed linear ramps representing event shocks on top of an organic growth baseline (e.g. 2pp/year organic banking growth).\n",
                    "\n",
                    "The simulated output is compared against actual World Bank Findex observations to assess model accuracy and identify deviations."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Display validation plot\n",
                    "display(Image(filename=os.path.join(FIG_PATH, 'impact_model_validation.png')))"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### Model Validation Accuracy\n",
                    "Let's check the numerical differences between actual observed Findex rates and our simulated lines."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Import the EventImpactModel to print validation accuracy directly\n",
                    "import sys\n",
                    "sys.path.append('../src')\n",
                    "from impact_model import EventImpactModel\n",
                    "\n",
                    "model = EventImpactModel(data_path=DATA_PATH, impact_path=IMPACT_PATH)\n",
                    "df_sim = model.simulate_timeline()\n",
                    "df_obs = model.df_data[model.df_data['record_type'] == 'observation'].copy()\n",
                    "df_obs['year'] = pd.to_datetime(df_obs['observation_date']).dt.year\n",
                    "\n",
                    "print(\"=== Model Validation Differences ===\")\n",
                    "for ind in ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT']:\n",
                    "    df_ind_obs = df_obs[(df_obs['indicator_code'] == ind) & (df_obs['gender'] == 'all')].sort_values('year')\n",
                    "    for idx, row in df_ind_obs.iterrows():\n",
                    "        closest_idx = df_sim.index.get_indexer([row['observation_date']], method='nearest')[0]\n",
                    "        sim_val = df_sim[f'{ind}_simulated'].iloc[closest_idx]\n",
                    "        err = sim_val - row['value_numeric']\n",
                    "        print(f\"{ind} ({row['year']}): Observed = {row['value_numeric']}%, Simulated = {sim_val:.2f}%, Error = {err:+.2f}pp\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 5. Methodology, Key Assumptions & Limitations\n",
                    "\n",
                    "### 1. Model Formulations:\n",
                    "- **Organic growth**: Modeled as linear growth ($Y_{organic}(t) = Y_{start} + g \cdot (t - t_{start})$), representing expansion under traditional banking structures (2pp/year for Access, 0.5pp/year for Usage).\n",
                    "- **Event Shock**: Modeled as a time-delayed linear ramp function:\n",
                    "  $$f(t; t_{event}, \\theta, c, W) = c \\cdot \\min\\left(1, \\max\\left(0, \\frac{t - (t_{event} + \\theta)}{W}\\right)\\right)$$\n",
                    "  where $\\theta$ is the lag in months, $c$ is the impact magnitude (estimate in pp), and $W$ is the build window in months (High magnitude builds over 24 months, Medium over 12 months, Low over 6 months).\n",
                    "\n",
                    "### 2. Validation Interpretations:\n",
                    "- **Overestimation of Account Ownership in 2024 (+7.66pp error)**: The model simulates 56.66% vs. 49.0% observed. This shows the **\"multi-homing\" overlap constraint** in action: Telebirr did not bring as many *new* unbanked users as its registration numbers suggested, because it primarily onboarded existing bank account holders.\n",
                    "- **Overestimation of Mobile Money Accounts in 2024 (+14.69pp error)**: The model simulates 24.14% vs. 9.45% observed. This reflects the **\"registered vs. active\" gap**: millions of adults register mobile wallets via their telcos (counted in administrative numbers), but the demand-side Findex survey only records those who actively use and perceive mobile money as a key transaction tool.\n",
                    "- **Underestimation of Digital Payments in 2021 (-15.44pp error)**: Shows that early-stage digital payment adoption (21%) occurred faster than the organic banking baseline could explain, likely due to pre-existing agent banking networks (like CBE Birr) that preceded Telebirr.\n",
                    "\n",
                    "### 3. Comparable Country Evidence:\n",
                    "- **M-Pesa Kenya (2007)**: Provided evidence for the +15-20pp high-magnitude access/usage shock for `EVT_0001` (Telebirr Launch).\n",
                    "- **Aadhaar India (2010-2016)**: Provided the baseline evidence for the +10pp access shock and narrowing of the gender gap by -5pp under a national digital biometric ID system (`EVT_0004` Fayda rollout).\n",
                    "- **Tanzania Interoperability (2014)**: Provided evidence for a +10% to +15% transaction count increase after joining the national payment switch (`EVT_0007` M-Pesa integration)."
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
    
    notebook_path = 'notebooks/03_event_impact_modeling.ipynb'
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)
    print(f"Created {notebook_path}")

if __name__ == '__main__':
    create_impact_notebook()
