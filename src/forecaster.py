import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os

sns.set_theme(style="whitegrid")

class FinancialInclusionForecaster:
    def __init__(self, data_path='data/processed/ethiopia_fi_unified_data.csv',
                 impact_path='data/processed/ethiopia_fi_impact_links.csv'):
        self.df_data = pd.read_csv(data_path)
        self.df_impact = pd.read_csv(impact_path)
        self.df_obs = self.df_data[self.df_data['record_type'] == 'observation'].copy()
        self.df_obs['year'] = pd.to_datetime(self.df_obs['observation_date']).dt.year
        
    def fit_trend_regression(self, indicator_code):
        """
        Fits an OLS trend regression on historical Findex years.
        """
        df_ind = self.df_obs[(self.df_obs['indicator_code'] == indicator_code) & 
                            (self.df_obs['gender'] == 'all')].sort_values('year')
        
        X = df_ind['year']
        y = df_ind['value_numeric']
        
        # Add constant
        X_const = sm.add_constant(X)
        model = sm.OLS(y, X_const).fit()
        return model

    def generate_trend_forecast(self, indicator_code, target_years=[2025, 2026, 2027]):
        """
        Generates baseline trend forecasts and confidence intervals using OLS regression.
        """
        model = self.fit_trend_regression(indicator_code)
        
        forecast_df = pd.DataFrame(index=target_years)
        X_pred = sm.add_constant(pd.Series(target_years, name='year'), has_constant='add')
        
        # Get predictions and confidence intervals
        predictions = model.get_prediction(X_pred)
        pred_summary = predictions.summary_frame(alpha=0.05) # 95% CI
        
        forecast_df['trend_forecast'] = pred_summary['mean'].values
        forecast_df['ci_lower'] = pred_summary['mean_ci_lower'].values
        forecast_df['ci_upper'] = pred_summary['mean_ci_upper'].values
        
        # Clip rates to [0, 100]
        for col in forecast_df.columns:
            forecast_df[col] = np.clip(forecast_df[col], 0.0, 100.0)
            
        return forecast_df

    def run_scenarios(self):
        """
        Simulate Base, Optimistic, and Pessimistic scenarios from 2011 to 2027.
        """
        date_range = pd.date_range(start='2011-01-01', end='2027-12-31', freq='ME')
        
        # We focus on the two main targets
        targets = ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT']
        
        # Base organic annual growth
        organic_annual_growth = {
            'ACC_OWNERSHIP': 2.0,      # 2pp organic banking growth
            'USG_DIGITAL_PAYMENT': 0.5 # 0.5pp organic usage growth
        }
        
        baseline_starts = {
            'ACC_OWNERSHIP': 14.0,
            'USG_DIGITAL_PAYMENT': 0.1
        }
        
        # Get baseline organic lines
        df_sim = pd.DataFrame(index=date_range)
        for t in targets:
            df_sim[f'{t}_organic'] = baseline_starts[t]
            
        for i in range(1, len(date_range)):
            curr_date = date_range[i]
            prev_date = date_range[i-1]
            delta_years = (curr_date - prev_date).days / 365.25
            for t in targets:
                df_sim.loc[curr_date, f'{t}_organic'] = (
                    df_sim.loc[prev_date, f'{t}_organic'] + 
                    organic_annual_growth[t] * delta_years
                )
                
        # 1. Base Scenario: Original Shocks from raw impact links
        df_sim = self._simulate_shocks(df_sim, targets, self.df_impact, 'base')
        
        # 2. Optimistic Scenario: Add positive catalysts in 2026
        # Event A: NBE approves mobile money micro-lending/savings (Safaricom M-Kesho or M-Shwari equivalent) in July 2026.
        # Impact: +7.5pp on USG_DIGITAL_PAYMENT and +5.0pp on ACC_OWNERSHIP, lag = 3 months
        # Event B: Fayda Digital ID becomes mandatory for all SIM/DFS registrations in October 2026.
        # Impact: +8.0pp on ACC_OWNERSHIP, lag = 3 months
        opt_impacts = pd.DataFrame([
            {
                'related_indicator': 'USG_DIGITAL_PAYMENT', 'impact_magnitude': 'medium', 'inferred_estimate': 7.5,
                'event_date': '2026-07-01', 'lag_months': 3, 'impact_direction': 'increase'
            },
            {
                'related_indicator': 'ACC_OWNERSHIP', 'impact_magnitude': 'medium', 'inferred_estimate': 5.0,
                'event_date': '2026-07-01', 'lag_months': 3, 'impact_direction': 'increase'
            },
            {
                'related_indicator': 'ACC_OWNERSHIP', 'impact_magnitude': 'medium', 'inferred_estimate': 8.0,
                'event_date': '2026-10-01', 'lag_months': 3, 'impact_direction': 'increase'
            }
        ])
        df_impact_opt = pd.concat([self.df_impact, opt_impacts], ignore_index=True)
        df_sim = self._simulate_shocks(df_sim, targets, df_impact_opt, 'optimistic')
        
        # 3. Pessimistic Scenario: Add negative shocks in 2026
        # Event A: High inflation and currency depreciation lead to further Safaricom/Ethio Telecom price hikes in early 2026.
        # Impact: -5.0pp on USG_DIGITAL_PAYMENT, lag = 2 months
        # Event B: National electricity outages and infrastructure degradation slow down 4G coverage expansion.
        # Impact: -3.0pp on ACC_OWNERSHIP, lag = 6 months
        pess_impacts = pd.DataFrame([
            {
                'related_indicator': 'USG_DIGITAL_PAYMENT', 'impact_magnitude': 'medium', 'inferred_estimate': -5.0,
                'event_date': '2026-01-01', 'lag_months': 2, 'impact_direction': 'decrease'
            },
            {
                'related_indicator': 'ACC_OWNERSHIP', 'impact_magnitude': 'medium', 'inferred_estimate': -3.0,
                'event_date': '2026-06-01', 'lag_months': 6, 'impact_direction': 'decrease'
            }
        ])
        df_impact_pess = pd.concat([self.df_impact, pess_impacts], ignore_index=True)
        df_sim = self._simulate_shocks(df_sim, targets, df_impact_pess, 'pessimistic')
        
        return df_sim

    def _simulate_shocks(self, df_sim, targets, df_links, scenario_name):
        magnitude_build_months = {'high': 24, 'medium': 12, 'low': 6}
        date_range = df_sim.index
        
        # Copy data and map inferred estimates
        df_l = df_links.copy()
        if 'inferred_estimate' not in df_l.columns:
            df_l['inferred_estimate'] = df_l['impact_estimate']
        else:
            df_l['inferred_estimate'] = df_l['inferred_estimate'].fillna(df_l['impact_estimate'])
            
        for idx, row in df_l.iterrows():
            if pd.isna(row['inferred_estimate']):
                direction = 1 if row['impact_direction'] == 'increase' else -1
                mag = row['impact_magnitude']
                val = 0.0
                if mag == 'high':
                    val = 15.0
                elif mag == 'medium':
                    val = 5.0
                elif mag == 'low':
                    val = 1.0
                df_l.at[idx, 'inferred_estimate'] = direction * val
                        
        # Get event dates from df_data
        df_events = self.df_data[self.df_data['record_type'] == 'event'][['record_id', 'observation_date']].rename(
            columns={'observation_date': 'event_date'}
        )
        # Merge to make sure we have event_date
        df_l = df_l.merge(df_events, left_on='parent_id', right_on='record_id', how='left', suffixes=('', '_parent'))
        # If event_date from parent is not null, use it. Otherwise keep the one already in the dataframe (for custom scenario events)
        if 'event_date_parent' in df_l.columns:
            df_l['event_date'] = df_l['event_date'].fillna(df_l['event_date_parent'])
            df_l.drop(columns=['event_date_parent'], inplace=True)
            
        # Initialize simulated column
        for t in targets:
            df_sim[f'{t}_{scenario_name}'] = df_sim[f'{t}_organic']
            
        for i in range(len(date_range)):
            curr_date = date_range[i]
            for idx, link in df_l.iterrows():
                ind = link['related_indicator']
                if ind not in targets:
                    continue
                    
                event_date = pd.to_datetime(link['event_date'])
                lag_months = int(link['lag_months'])
                start_impact_date = event_date + pd.DateOffset(months=lag_months)
                
                # Build duration
                mag = link['impact_magnitude']
                build_w = magnitude_build_months.get(mag, 12)
                end_impact_date = start_impact_date + pd.DateOffset(months=build_w)
                
                impact_val = link['inferred_estimate']
                
                if curr_date < start_impact_date:
                    factor = 0.0
                elif curr_date >= end_impact_date:
                    factor = 1.0
                else:
                    total_days = (end_impact_date - start_impact_date).days
                    elapsed_days = (curr_date - start_impact_date).days
                    factor = elapsed_days / total_days
                    
                df_sim.loc[curr_date, f'{ind}_{scenario_name}'] += impact_val * factor
                
        # Clip rates to [0, 100]
        for t in targets:
            df_sim[f'{t}_{scenario_name}'] = np.clip(df_sim[f'{t}_{scenario_name}'], 0.0, 100.0)
            
        return df_sim

def generate_forecasts():
    forecaster = FinancialInclusionForecaster()
    
    # 1. Generate OLS trend baseline forecasts for 2025-2027
    print("=== PURE OLS TREND FORECASTS ===")
    df_acc_trend = forecaster.generate_trend_forecast('ACC_OWNERSHIP')
    df_pay_trend = forecaster.generate_trend_forecast('USG_DIGITAL_PAYMENT')
    
    print("\nAccount Ownership Rate (Access) OLS Forecasts:")
    print(df_acc_trend)
    print("\nDigital Payment Adoption Rate (Usage) OLS Forecasts:")
    print(df_pay_trend)
    print()
    
    # 2. Run Scenarios
    df_sim = forecaster.run_scenarios()
    
    # Extract values for 2025, 2026, 2027 (taking year-end values)
    print("=== SCENARIO-AUGMENTED FORECASTS ===")
    target_dates = {
        2025: '2025-12-31',
        2026: '2026-12-31',
        2027: '2027-12-31'
    }
    
    for t in ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT']:
        name = 'Account Ownership (Access)' if t == 'ACC_OWNERSHIP' else 'Digital Payment Usage (Usage)'
        print(f"\n{name} Scenarios:")
        for year, dt in target_dates.items():
            closest_idx = df_sim.index.get_indexer([pd.to_datetime(dt)], method='nearest')[0]
            val_base = df_sim[f'{t}_base'].iloc[closest_idx]
            val_opt = df_sim[f'{t}_optimistic'].iloc[closest_idx]
            val_pess = df_sim[f'{t}_pessimistic'].iloc[closest_idx]
            print(f"- {year}: Base = {val_base:.2f}%, Optimistic = {val_opt:.2f}%, Pessimistic = {val_pess:.2f}%")
    print()
    
    # 3. Save Scenario Visualization
    fig, axes = plt.subplots(2, 1, figsize=(12, 12))
    
    # Load actual observations
    df_obs = forecaster.df_obs
    df_obs_acc = df_obs[(df_obs['indicator_code'] == 'ACC_OWNERSHIP') & (df_obs['gender'] == 'all')].sort_values('observation_date')
    df_obs_pay = df_obs[(df_obs['indicator_code'] == 'USG_DIGITAL_PAYMENT') & (df_obs['gender'] == 'all')].sort_values('observation_date')
    
    df_obs_acc['observation_date'] = pd.to_datetime(df_obs_acc['observation_date'])
    df_obs_pay['observation_date'] = pd.to_datetime(df_obs_pay['observation_date'])
    
    # Plot Account Ownership Scenarios
    axes[0].plot(df_sim.index, df_sim['ACC_OWNERSHIP_base'], color='#1f77b4', linewidth=2.5, label='Base Scenario')
    axes[0].plot(df_sim.index, df_sim['ACC_OWNERSHIP_optimistic'], color='#2ca02c', linewidth=2, linestyle='--', label='Optimistic Scenario')
    axes[0].plot(df_sim.index, df_sim['ACC_OWNERSHIP_pessimistic'], color='#d62728', linewidth=2, linestyle='-.', label='Pessimistic Scenario')
    axes[0].scatter(df_obs_acc['observation_date'], df_obs_acc['value_numeric'], color='#000000', s=80, zorder=5, label='Historical Findex')
    
    # Add statsmodels trend line
    years_range = pd.date_range('2011-01-01', '2027-12-31', freq='YE')
    acc_trend_years = [y.year for y in years_range]
    df_acc_full_trend = forecaster.generate_trend_forecast('ACC_OWNERSHIP', target_years=acc_trend_years)
    axes[0].plot(years_range, df_acc_full_trend['trend_forecast'], color='#7f7f7f', linestyle=':', label='OLS Baseline Trend')
    axes[0].fill_between(years_range, df_acc_full_trend['ci_lower'], df_acc_full_trend['ci_upper'], color='#7f7f7f', alpha=0.1, label='95% OLS CI')
    
    axes[0].set_title('Account Ownership Rate (Access) Forecasts (2025-2027)', fontsize=13, fontweight='bold')
    axes[0].set_ylabel('Rate (%)', fontsize=11)
    axes[0].set_xlim(pd.to_datetime('2011-01-01'), pd.to_datetime('2027-12-31'))
    axes[0].set_ylim(0, 80)
    axes[0].legend(loc='upper left', fontsize=10)
    
    # Plot Digital Payment Scenarios
    axes[1].plot(df_sim.index, df_sim['USG_DIGITAL_PAYMENT_base'], color='#ff7f0e', linewidth=2.5, label='Base Scenario')
    axes[1].plot(df_sim.index, df_sim['USG_DIGITAL_PAYMENT_optimistic'], color='#2ca02c', linewidth=2, linestyle='--', label='Optimistic Scenario')
    axes[1].plot(df_sim.index, df_sim['USG_DIGITAL_PAYMENT_pessimistic'], color='#d62728', linewidth=2, linestyle='-.', label='Pessimistic Scenario')
    axes[1].scatter(df_obs_pay['observation_date'], df_obs_pay['value_numeric'], color='#000000', s=80, zorder=5, label='Historical Findex')
    
    pay_trend_years = [y.year for y in years_range if y.year >= 2014]
    df_pay_full_trend = forecaster.generate_trend_forecast('USG_DIGITAL_PAYMENT', target_years=pay_trend_years)
    axes[1].plot(years_range[3:], df_pay_full_trend['trend_forecast'], color='#7f7f7f', linestyle=':', label='OLS Baseline Trend')
    axes[1].fill_between(years_range[3:], df_pay_full_trend['ci_lower'], df_pay_full_trend['ci_upper'], color='#7f7f7f', alpha=0.1, label='95% OLS CI')
    
    axes[1].set_title('Digital Payment Adoption Rate (Usage) Forecasts (2025-2027)', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('Rate (%)', fontsize=11)
    axes[1].set_xlim(pd.to_datetime('2011-01-01'), pd.to_datetime('2027-12-31'))
    axes[1].set_ylim(0, 60)
    axes[1].legend(loc='upper left', fontsize=10)
    
    plt.suptitle("Ethiopia Financial Inclusion: 2025-2027 Forecast Scenarios", fontsize=15, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    plt.savefig('reports/figures/forecasting_scenarios.png', dpi=300)
    plt.close()
    print("Saved forecasting_scenarios.png")

if __name__ == '__main__':
    generate_forecasts()
