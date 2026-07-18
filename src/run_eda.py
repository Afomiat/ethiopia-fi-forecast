import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for graphics
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def run_eda():
    raw_dir = 'data/processed'
    fig_dir = 'reports/figures'
    os.makedirs(fig_dir, exist_ok=True)
    
    # Load files
    data_path = os.path.join(raw_dir, 'ethiopia_fi_unified_data.csv')
    impact_path = os.path.join(raw_dir, 'ethiopia_fi_impact_links.csv')
    
    df_data = pd.read_csv(data_path)
    df_impact = pd.read_csv(impact_path)
    
    # 1. Separate observations
    df_obs = df_data[df_data['record_type'] == 'observation'].copy()
    # Convert dates and extract year
    df_obs['observation_date'] = pd.to_datetime(df_obs['observation_date'])
    df_obs['year'] = df_obs['observation_date'].dt.year
    
    print("=== DATASET OVERVIEW ===")
    print(df_data['record_type'].value_counts())
    print()
    print("=== OBSERVATIONS BY PILLAR ===")
    print(df_obs['pillar'].value_counts())
    print()
    print("=== CONFIDENCE DISTRIBUTION ===")
    print(df_obs['confidence'].value_counts())
    print()
    
    # 2. Temporal Coverage Visualization
    pivot_coverage = df_obs.pivot_table(index='indicator_code', columns='year', values='value_numeric', aggfunc='count').fillna(0)
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_coverage > 0, cmap="Blues", cbar=False, linewidths=0.5, yticklabels=True)
    plt.title("Temporal Data Coverage by Indicator and Year", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Indicator Code", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'temporal_coverage.png'), dpi=300)
    plt.close()
    print("Saved temporal_coverage.png")
    
    # 3. Access Analysis: Account Ownership Trajectory (2011-2024)
    # Get national account ownership
    df_acc_nat = df_obs[(df_obs['indicator_code'] == 'ACC_OWNERSHIP') & (df_obs['gender'] == 'all')].sort_values('year')
    # Get gender disaggregated account ownership
    df_acc_male = df_obs[(df_obs['indicator_code'] == 'ACC_OWNERSHIP') & (df_obs['gender'] == 'male')].sort_values('year')
    df_acc_female = df_obs[(df_obs['indicator_code'] == 'ACC_OWNERSHIP') & (df_obs['gender'] == 'female')].sort_values('year')
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_acc_nat['year'], df_acc_nat['value_numeric'], marker='o', linewidth=3, color='#1f77b4', label='National Average')
    plt.plot(df_acc_male['year'], df_acc_male['value_numeric'], marker='s', linestyle='--', linewidth=2, color='#2ca02c', label='Male Adults')
    plt.plot(df_acc_female['year'], df_acc_female['value_numeric'], marker='^', linestyle='--', linewidth=2, color='#d62728', label='Female Adults')
    
    # Annotate values
    for x, y in zip(df_acc_nat['year'], df_acc_nat['value_numeric']):
        plt.annotate(f"{y}%", (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold', color='#1f77b4')
    for x, y in zip(df_acc_male['year'], df_acc_male['value_numeric']):
        plt.annotate(f"{y}%", (x, y), textcoords="offset points", xytext=(0,10), ha='center', color='#2ca02c')
    for x, y in zip(df_acc_female['year'], df_acc_female['value_numeric']):
        plt.annotate(f"{y}%", (x, y), textcoords="offset points", xytext=(0,-15), ha='center', color='#d62728')
        
    plt.title("Account Ownership Rate Trajectory in Ethiopia (2011-2024)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Account Ownership (%)", fontsize=12)
    plt.xlim(2010, 2025)
    plt.ylim(0, 70)
    plt.legend(loc='upper left', fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'account_ownership_trajectory.png'), dpi=300)
    plt.close()
    print("Saved account_ownership_trajectory.png")
    
    # Calculate Growth Rates
    df_acc_nat = df_acc_nat.copy()
    df_acc_nat['growth_pp'] = df_acc_nat['value_numeric'].diff()
    df_acc_nat['growth_rate'] = df_acc_nat['value_numeric'].pct_change() * 100
    print("\n=== ACCOUNT OWNERSHIP GROWTH RATES ===")
    print(df_acc_nat[['year', 'value_numeric', 'growth_pp', 'growth_rate']])
    print()
    
    # 4. Usage (Digital Payments) vs Mobile Money Accounts
    # Get digital payment adoption
    df_pay_nat = df_obs[(df_obs['indicator_code'] == 'USG_DIGITAL_PAYMENT') & (df_obs['gender'] == 'all')].sort_values('year')
    # Get mobile money accounts
    df_mm_nat = df_obs[(df_obs['indicator_code'] == 'ACC_MM_ACCOUNT') & (df_obs['gender'] == 'all')].sort_values('year')
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_acc_nat['year'], df_acc_nat['value_numeric'], marker='o', linewidth=2, color='#1f77b4', label='Account Ownership Rate (Access)')
    plt.plot(df_pay_nat['year'], df_pay_nat['value_numeric'], marker='s', linewidth=2.5, color='#ff7f0e', label='Digital Payment Adoption Rate (Usage)')
    plt.plot(df_mm_nat['year'], df_mm_nat['value_numeric'], marker='d', linestyle='-.', linewidth=2, color='#9467bd', label='Mobile Money Account Rate')
    
    for x, y in zip(df_pay_nat['year'], df_pay_nat['value_numeric']):
        plt.annotate(f"{y}%", (x, y), textcoords="offset points", xytext=(0,10), ha='center', color='#ff7f0e', fontweight='bold')
    for x, y in zip(df_mm_nat['year'], df_mm_nat['value_numeric']):
        plt.annotate(f"{y}%", (x, y), textcoords="offset points", xytext=(0,-15), ha='center', color='#9467bd')
        
    plt.title("Access vs. Usage: Financial Inclusion Trajectory (2011-2024)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Percentage of Adults (%)", fontsize=12)
    plt.xlim(2010, 2025)
    plt.ylim(0, 70)
    plt.legend(loc='upper left', fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'digital_payments_vs_mobile_money.png'), dpi=300)
    plt.close()
    print("Saved digital_payments_vs_mobile_money.png")
    
    # 5. Infrastructure and Enablers (4G Coverage, Mobile Penetration, Fayda ID)
    df_4g = df_obs[df_obs['indicator_code'] == 'ACC_4G_COV'].sort_values('year')
    df_mobile = df_obs[df_obs['indicator_code'] == 'ACC_MOBILE_PEN'].sort_values('year')
    df_fayda = df_obs[df_obs['indicator_code'] == 'ACC_FAYDA'].sort_values('year')
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = '#2ca02c'
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Coverage & Subscription Penetration (%)', color=color, fontsize=12)
    p1, = ax1.plot(df_4g['year'], df_4g['value_numeric'], marker='o', color=color, linewidth=2, label='4G Population Coverage')
    p2, = ax1.plot(df_mobile['year'], df_mobile['value_numeric'], marker='x', linestyle='--', color='#8c564b', linewidth=2, label='Mobile Penetration')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 100)
    
    ax2 = ax1.twinx()  
    color = '#d62728'
    ax2.set_ylabel('Fayda Digital ID Enrollment (Millions)', color=color, fontsize=12)
    # Convert Fayda values to millions
    fayda_mil = df_fayda['value_numeric'] / 1e6
    p3, = ax2.plot(df_fayda['year'], fayda_mil, marker='^', linestyle='-.', color=color, linewidth=2.5, label='Fayda Registrations (Right)')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 20)
    
    # Legend
    lines = [p1, p2, p3]
    ax1.legend(lines, [l.get_label() for l in lines], loc='upper left', fontsize=11)
    
    plt.title("Infrastructure and Enablers Growth in Ethiopia (2023-2025)", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'infrastructure_enablers.png'), dpi=300)
    plt.close()
    print("Saved infrastructure_enablers.png")
    
    # 6. Event Timeline and Overlay
    # Let's plot Account Ownership & Digital Payments, and overlay vertical lines for events
    df_evt = df_data[df_data['record_type'] == 'event'].copy()
    df_evt['observation_date'] = pd.to_datetime(df_evt['observation_date'])
    df_evt['year_frac'] = df_evt['observation_date'].dt.year + (df_evt['observation_date'].dt.month - 1) / 12.0
    
    plt.figure(figsize=(12, 7))
    plt.plot(df_acc_nat['year'], df_acc_nat['value_numeric'], marker='o', linewidth=2.5, color='#1f77b4', label='Account Ownership (Access)')
    plt.plot(df_pay_nat['year'], df_pay_nat['value_numeric'], marker='s', linewidth=2.5, color='#ff7f0e', label='Digital Payment Adoption (Usage)')
    
    # Mark Events
    colors = plt.cm.tab10(np.linspace(0, 1, len(df_evt)))
    for idx, (i, row) in enumerate(df_evt.sort_values('observation_date').iterrows()):
        x_val = row['year_frac']
        plt.axvline(x=x_val, color=colors[idx], linestyle=':', alpha=0.8)
        # Label the event near the top of the chart with rotation
        plt.text(x_val, 50 - (idx % 4) * 8, row['indicator'].split(' Launch')[0].split(' Program')[0], 
                 rotation=90, verticalalignment='bottom', fontsize=9, fontweight='bold', color=colors[idx])
                 
    plt.title("Ecosystem Milestones Overlaid on Financial Inclusion Trends", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Rate (%)", fontsize=12)
    plt.xlim(2010, 2026.5)
    plt.ylim(0, 75)
    plt.legend(loc='upper left', fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'event_timeline_overlay.png'), dpi=300)
    plt.close()
    print("Saved event_timeline_overlay.png")
    
    # 7. Correlation Analysis
    # Let's create an aligned DataFrame by year for years 2011 to 2025
    years_range = list(range(2011, 2026))
    df_aligned = pd.DataFrame(index=years_range)
    
    # Fill values by indicator
    for ind in ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT', 'ACC_4G_COV', 'ACC_MOBILE_PEN', 'ACC_FAYDA', 'USG_P2P_COUNT']:
        ind_data = df_obs[(df_obs['indicator_code'] == ind) & (df_obs['gender'] == 'all')]
        if len(ind_data) > 0:
            s = ind_data.groupby('year')['value_numeric'].mean()
            # Reindex to all years
            s = s.reindex(years_range)
            # Interpolate linearly for correlation analysis (since years are sparse)
            df_aligned[ind] = s.interpolate(method='linear', limit_direction='both')
            
    corr_matrix = df_aligned.corr()
    print("\n=== CORRELATION MATRIX (INTERPOLATED YEARLY ALIGNED) ===")
    print(corr_matrix)
    print()
    
    plt.figure(figsize=(8, 7))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1, square=True)
    plt.title("Correlation Matrix between Inclusion & Enabler Indicators", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, 'correlation_matrix.png'), dpi=300)
    plt.close()
    print("Saved correlation_matrix.png")
    
    print("\n=== DATA QUALITY ASSESSMENT ===")
    print(f"Total Observation rows: {len(df_obs)}")
    print(f"Total Event rows: {len(df_evt)}")
    print(f"Average Confidence of Observations: {df_obs['confidence'].value_counts()}")
    print("Sparse indicators:")
    for col in df_aligned.columns:
        actual_count = df_obs[(df_obs['indicator_code'] == col) & (df_obs['gender'] == 'all')]['value_numeric'].count()
        print(f"- {col}: {actual_count} actual observations over 15 years")

if __name__ == '__main__':
    run_eda()
