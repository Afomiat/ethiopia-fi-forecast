import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class EventImpactModel:
    def __init__(self, data_path='data/processed/ethiopia_fi_unified_data.csv', 
                 impact_path='data/processed/ethiopia_fi_impact_links.csv'):
        self.df_data = pd.read_csv(data_path)
        self.df_impact = pd.read_csv(impact_path)
        self.df_events = self.df_data[self.df_data['record_type'] == 'event'].copy()
        self.df_events['observation_date'] = pd.to_datetime(self.df_events['observation_date'])
        
    def build_association_matrix(self):
        """
        Builds the Event-Indicator Association Matrix.
        Rows: Events
        Columns: Key Indicators
        Values: Impact Estimates (percentage points or relative changes)
        """
        events_info = self.df_events[['record_id', 'indicator', 'observation_date']].rename(
            columns={'indicator': 'event_name', 'observation_date': 'event_date'}
        )
        df_merged = self.df_impact.merge(events_info, left_on='parent_id', right_on='record_id', how='left')
        
        # Create pivot table
        # We fill values with impact_estimate. If estimate is missing, we infer it from magnitude
        df_merged['inferred_estimate'] = df_merged['impact_estimate']
        
        # Inference logic
        for idx, row in df_merged.iterrows():
            if pd.isna(row['inferred_estimate']):
                direction = 1 if row['impact_direction'] == 'increase' else -1
                mag = row['impact_magnitude']
                if mag == 'high':
                    df_merged.at[idx, 'inferred_estimate'] = direction * 15.0
                elif mag == 'medium':
                    df_merged.at[idx, 'inferred_estimate'] = direction * 5.0
                elif mag == 'low':
                    df_merged.at[idx, 'inferred_estimate'] = direction * 1.0
                    
        pivot_matrix = df_merged.pivot_table(
            index='event_name', 
            columns='related_indicator', 
            values='inferred_estimate', 
            aggfunc='first'
        ).fillna(0)
        
        return pivot_matrix, df_merged

    def simulate_timeline(self, start_date='2011-01-01', end_date='2027-12-31', step='ME'):
        """
        Simulate the indicators monthly or yearly, incorporating linear ramps for event impacts.
        """
        date_range = pd.date_range(start=start_date, end=end_date, freq=step)
        df_sim = pd.DataFrame(index=date_range)
        
        # Define target indicators to simulate
        indicators = ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT']
        
        # Base trends (derived from pre-event or baseline rates)
        # We assume a linear organic growth rate per year without digital/mobile money shocks
        # Access (Account Ownership): organic growth of ~2.5pp per year (from 2011 to 2021 historical trend was 32pp over 10 years ~ 3.2pp, but let's separate organic bank growth vs telco shocks)
        organic_annual_growth = {
            'ACC_OWNERSHIP': 2.0,      # 2pp organic banking growth per year
            'ACC_MM_ACCOUNT': 0.0,     # 0pp organic MM growth (starts at 0 without regulations/launches)
            'USG_DIGITAL_PAYMENT': 0.5 # 0.5pp organic digital payment growth
        }
        
        # Baseline starting values in Jan 2011
        baseline_starts = {
            'ACC_OWNERSHIP': 14.0,
            'ACC_MM_ACCOUNT': 0.0,
            'USG_DIGITAL_PAYMENT': 0.1
        }
        
        # Build-up duration for events (in months) based on impact magnitude
        # High magnitude builds over 24 months, Medium over 12 months, Low over 6 months
        magnitude_build_months = {
            'high': 24,
            'medium': 12,
            'low': 6
        }
        
        # Get all impact links
        _, df_links = self.build_association_matrix()
        
        # Initialize simulation columns
        for ind in indicators:
            df_sim[f'{ind}_organic'] = baseline_starts[ind]
            df_sim[f'{ind}_simulated'] = baseline_starts[ind]
            
        # Run monthly step simulation
        # 1. Update organic values for all dates
        for i in range(1, len(date_range)):
            curr_date = date_range[i]
            prev_date = date_range[i-1]
            delta_years = (curr_date - prev_date).days / 365.25
            for ind in indicators:
                df_sim.loc[curr_date, f'{ind}_organic'] = (
                    df_sim.loc[prev_date, f'{ind}_organic'] + 
                    organic_annual_growth[ind] * delta_years
                )
                
        # 2. Run simulation by adding shocks on top of the organic value for each date
        for i in range(len(date_range)):
            curr_date = date_range[i]
            for ind in indicators:
                df_sim.loc[curr_date, f'{ind}_simulated'] = df_sim.loc[curr_date, f'{ind}_organic']
                
            # For each impact link, add its contribution
            for idx, link in df_links.iterrows():
                ind = link['related_indicator']
                if ind not in indicators:
                    continue
                    
                event_date = pd.to_datetime(link['event_date'])
                lag_months = int(link['lag_months'])
                start_impact_date = event_date + pd.DateOffset(months=lag_months)
                
                # Build duration
                mag = link['impact_magnitude']
                build_w = magnitude_build_months.get(mag, 12)
                end_impact_date = start_impact_date + pd.DateOffset(months=build_w)
                
                impact_val = link['inferred_estimate']
                
                # Check where current date falls relative to impact start and end
                if curr_date < start_impact_date:
                    factor = 0.0
                elif curr_date >= end_impact_date:
                    factor = 1.0
                else:
                    # Gradual linear build-up
                    total_days = (end_impact_date - start_impact_date).days
                    elapsed_days = (curr_date - start_impact_date).days
                    factor = elapsed_days / total_days
                    
                # Add the shock to the simulated value on this specific date
                df_sim.loc[curr_date, f'{ind}_simulated'] += impact_val * factor
                
        return df_sim

def plot_and_validate():
    model = EventImpactModel()
    pivot_matrix, _ = model.build_association_matrix()
    
    # Save Heatmap of Association Matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_matrix, annot=True, cmap="PiYG", center=0, fmt=".1f", cbar_kws={'label': 'Impact Estimate (pp)'})
    plt.title("Event-Indicator Association Matrix", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('reports/figures/association_matrix.png', dpi=300)
    plt.close()
    print("Saved association_matrix.png")
    
    # Run Simulation
    df_sim = model.simulate_timeline()
    
    # Load actual observations for validation
    df_obs = model.df_data[model.df_data['record_type'] == 'observation'].copy()
    df_obs['year'] = pd.to_datetime(df_obs['observation_date']).dt.year
    
    # Create comparison plots
    fig, axes = plt.subplots(3, 1, figsize=(12, 15))
    indicators = ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT']
    titles = ['Account Ownership (Access)', 'Mobile Money Account Rate', 'Digital Payment Adoption (Usage)']
    
    for i, ind in enumerate(indicators):
        ax = axes[i]
        # Get simulated and organic lines
        ax.plot(df_sim.index, df_sim[f'{ind}_simulated'], label='Model with Event Shocks', color='#1f77b4', linewidth=2.5)
        ax.plot(df_sim.index, df_sim[f'{ind}_organic'], label='Baseline (Organic Growth Only)', color='#7f7f7f', linestyle='--', linewidth=1.5)
        
        # Plot actual observations
        df_ind_obs = df_obs[(df_obs['indicator_code'] == ind) & (df_obs['gender'] == 'all')].sort_values('observation_date')
        df_ind_obs['observation_date'] = pd.to_datetime(df_ind_obs['observation_date'])
        ax.scatter(df_ind_obs['observation_date'], df_ind_obs['value_numeric'], color='#d62728', s=100, zorder=5, label='Actual Observations')
        for idx, row in df_ind_obs.iterrows():
            ax.annotate(f"{row['value_numeric']}%", (row['observation_date'], row['value_numeric']), 
                        textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold', color='#d62728')
            
        ax.set_title(titles[i], fontsize=12, fontweight='bold')
        ax.set_ylabel('Rate (%)', fontsize=10)
        ax.set_xlim(pd.to_datetime('2011-01-01'), pd.to_datetime('2027-12-31'))
        ax.legend(loc='upper left')
        
    plt.suptitle("Validation of Event-Indicator Impact Model: Simulated vs. Actual", fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    plt.savefig('reports/figures/impact_model_validation.png', dpi=300)
    plt.close()
    print("Saved impact_model_validation.png")
    
    # Print validation errors for 2021 and 2024
    print("\n=== MODEL VALIDATION ACCURACY ===")
    for ind in ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT']:
        df_ind_obs = df_obs[(df_obs['indicator_code'] == ind) & (df_obs['gender'] == 'all')].sort_values('year')
        for idx, row in df_ind_obs.iterrows():
            obs_year = row['year']
            obs_val = row['value_numeric']
            # Find closest date in simulation
            closest_idx = df_sim.index.get_indexer([row['observation_date']], method='nearest')[0]
            sim_val = df_sim[f'{ind}_simulated'].iloc[closest_idx]
            err = sim_val - obs_val
            print(f"- {ind} ({obs_year}): Observed = {obs_val}%, Simulated = {sim_val:.2f}%, Error = {err:+.2f}pp")
            
if __name__ == '__main__':
    # Clean up check_impacts scratch script
    scratch_check = 'scratch/check_impacts.py'
    if os.path.exists(scratch_check):
        os.remove(scratch_check)
        print("Removed temporary check_impacts script")
        
    plot_and_validate()
