import sys
import os
import pandas as pd
import numpy as np

# Add src/ to python path
sys.path.append('src')
from forecaster import FinancialInclusionForecaster

def test_forecaster_initialization():
    f = FinancialInclusionForecaster()
    assert len(f.df_data) > 0, "Failed to load data"
    assert len(f.df_impact) > 0, "Failed to load impact links"

def test_trend_regression():
    f = FinancialInclusionForecaster()
    model_acc = f.fit_trend_regression('ACC_OWNERSHIP')
    assert model_acc is not None, "Failed to fit OLS regression for Access"
    
    df_acc_trend = f.generate_trend_forecast('ACC_OWNERSHIP', target_years=[2025, 2026, 2027])
    assert len(df_acc_trend) == 3, "OLS forecast should cover 3 years"
    assert 'trend_forecast' in df_acc_trend.columns, "trend_forecast column missing"
    assert not df_acc_trend.isnull().any().any(), "Forecast values should not be NaN"

def test_run_scenarios():
    f = FinancialInclusionForecaster()
    df_sim = f.run_scenarios()
    
    assert len(df_sim) > 0, "Simulation dataframe is empty"
    for col in ['ACC_OWNERSHIP_base', 'ACC_OWNERSHIP_optimistic', 'ACC_OWNERSHIP_pessimistic',
                'USG_DIGITAL_PAYMENT_base', 'USG_DIGITAL_PAYMENT_optimistic', 'USG_DIGITAL_PAYMENT_pessimistic']:
        assert col in df_sim.columns, f"Scenario column {col} is missing"
        assert not df_sim[col].isnull().any(), f"Scenario {col} has NaN values"
        assert (df_sim[col] >= 0.0).all() and (df_sim[col] <= 100.0).all(), f"Scenario {col} values out of rate bounds [0, 100]"
