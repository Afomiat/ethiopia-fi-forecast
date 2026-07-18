import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import sys

# Set up page configurations for SEO and design layout
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecast Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling using outfit font, glassmorphic cards, and subtle gradient effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Title styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1f77b4, #9467bd, #e377c2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
        padding-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #666666;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Card design */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.08);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1f77b4;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #555555;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        color: #2ca02c;
        font-weight: 600;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, rgba(31,119,180,0.1), rgba(148,103,189,0.1));
        border-left: 5px solid #1f77b4;
        border-radius: 0 12px 12px 0;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Ensure src/ is in the python path to load the forecaster
sys.path.append('src')
try:
    from forecaster import FinancialInclusionForecaster
except ImportError:
    # Fallback to copy class locally if path configuration fails in streamlit env
    pass

# Load data helper
@st.cache_data
def load_base_data():
    df_data = pd.read_csv('data/processed/ethiopia_fi_unified_data.csv')
    df_impact = pd.read_csv('data/processed/ethiopia_fi_impact_links.csv')
    df_obs = df_data[df_data['record_type'] == 'observation'].copy()
    df_obs['year'] = pd.to_datetime(df_obs['observation_date']).dt.year
    df_events = df_data[df_data['record_type'] == 'event'].copy()
    return df_data, df_impact, df_obs, df_events

df_data, df_impact, df_obs, df_events = load_base_data()

# ----------------- HEADER & META DATA (SEO) -----------------
st.markdown("<h1 class='main-title' id='app-title'>Ethiopia Financial Inclusion Forecast</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Tracking and predicting Ethiopia's digital financial transformation using time series regression and event impact models.</p>", unsafe_allow_html=True)

# ----------------- TABS NAVIGATION -----------------
tab_overview, tab_trends, tab_impacts, tab_forecast = st.tabs([
    "📊 Overview & KPIs", 
    "📈 Historical Trends", 
    "⚡ Event Impact Matrix", 
    "🔮 Forecasting & Scenarios"
])

# ================= TAB 1: OVERVIEW & KPIS =================
with tab_overview:
    st.markdown("## Ecosystem Summary & KPIs", help="Current state of financial inclusion in Ethiopia based on Global Findex and operator data.")
    
    # KPI Grid using 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class='glass-card' style='border-top: 4px solid #1f77b4;'>
                <div class='metric-label'>Account Ownership Rate (Access)</div>
                <div class='metric-value'>49.0%</div>
                <div class='metric-delta'>+3.0pp since 2021 | Target: 60%</div>
            </div>
            """, unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            """
            <div class='glass-card' style='border-top: 4px solid #ff7f0e;'>
                <div class='metric-label'>Digital Payment Adoption (Usage)</div>
                <div class='metric-value'>35.0%</div>
                <div class='metric-delta'>+14.0pp since 2021 | Target: 45%</div>
            </div>
            """, unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            """
            <div class='glass-card' style='border-top: 4px solid #2ca02c;'>
                <div class='metric-label'>Active Mobile Money Rate</div>
                <div class='metric-value'>9.45%</div>
                <div class='metric-delta'>+4.75pp since 2021 | 65M+ Registrations</div>
            </div>
            """, unsafe_allow_html=True
        )

    # Highlight Crossover Block
    st.markdown(
        """
        <div class='highlight-box'>
            <h3>📈 P2P Digital Crossover Achieved</h3>
            In the fiscal year 2024/25, the number of peer-to-peer (P2P) mobile money transfers in Ethiopia officially 
            surpassed the total number of cash ATM withdrawals. This represents a historic structural shift from cash dependency 
            to digital circulation.
        </div>
        """, unsafe_allow_html=True
    )
    
    # Crossover Chart & metrics
    c_col1, c_col2 = st.columns([2, 3])
    with c_col1:
        st.markdown("### Transaction Crossover Metrics (FY2024/25)")
        # Display key metrics in table format
        cross_data = {
            "Metric": [
                "P2P Transaction Count", 
                "ATM Transaction Count", 
                "P2P/ATM Crossover Ratio", 
                "P2P Transaction Value", 
                "ATM Transaction Value",
                "Value Multiplier"
            ],
            "Value": [
                "128.3 Million", 
                "119.3 Million", 
                "1.08", 
                "ETB 577.7 Billion", 
                "ETB 156.1 Billion",
                "3.7x Higher"
            ]
        }
        st.table(pd.DataFrame(cross_data))
        
    with c_col2:
        # Plotly chart comparing counts and values
        crossover_categories = ['ATM Withdrawals', 'P2P Transactions']
        counts = [119.3, 128.3] # In millions
        values = [156.1, 577.7] # In Billions ETB
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=crossover_categories, y=counts, 
            name='Transaction Count (Millions)',
            marker_color='#1f77b4',
            text=[f"{c}M" for c in counts],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=crossover_categories, y=values, 
            name='Transaction Value (Billion ETB)',
            marker_color='#9467bd',
            text=[f"ETB {v}B" for v in values],
            textposition='auto'
        ))
        fig.update_layout(
            title_text='Transaction Counts vs. Values (FY24/25)',
            bgroupmode='group',
            xaxis_title='Channel Type',
            legend_title='Metric Type',
            height=380,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig, use_container_width=True, key="crossover_chart")

# ================= TAB 2: HISTORICAL TRENDS =================
with tab_trends:
    st.markdown("## Historical Trajectory Analysis")
    
    t_col1, t_col2 = st.columns(2)
    
    with t_col1:
        st.markdown("### Account Ownership Trajectory (2011-2024)")
        
        # Gender breakdown filter
        gender_sel = st.multiselect(
            "Select Gender Cohorts to Compare:",
            options=["all", "male", "female"],
            default=["all", "male", "female"],
            key="gender_cohort_select"
        )
        
        # Filter and plot
        df_acc = df_obs[(df_obs['indicator_code'] == 'ACC_OWNERSHIP') & (df_obs['gender'].isin(gender_sel))].sort_values('year')
        
        fig_acc = px.line(
            df_acc, x='year', y='value_numeric', color='gender', markers=True,
            labels={'value_numeric': 'Account Ownership Rate (%)', 'year': 'Year'},
            color_discrete_map={'all': '#1f77b4', 'male': '#2ca02c', 'female': '#d62728'}
        )
        fig_acc.update_layout(height=400, yaxis_range=[0, 70])
        st.plotly_chart(fig_acc, use_container_width=True, key="acc_history_chart")
        
        st.markdown(
            "**Key Note:** The gender gap stood at **20pp** in 2021 (56% male, 36% female) and closed slightly to **15pp** in 2024 "
            "(56.5% male, 41.6% female). However, female account ownership remains significantly below the national average."
        )

    with t_col2:
        st.markdown("### Digital Payment Adoption vs. Mobile Money Accounts")
        
        # Filter national average data for MM accounts and Digital Payments
        df_trends = df_obs[
            (df_obs['indicator_code'].isin(['USG_DIGITAL_PAYMENT', 'ACC_MM_ACCOUNT'])) & 
            (df_obs['gender'] == 'all')
        ].sort_values('year')
        
        fig_trends = px.line(
            df_trends, x='year', y='value_numeric', color='indicator', markers=True,
            labels={'value_numeric': 'Rate (%)', 'year': 'Year'},
            color_discrete_map={'Digital Payment Adoption Rate': '#ff7f0e', 'Mobile Money Account Rate': '#9467bd'}
        )
        fig_trends.update_layout(height=400, yaxis_range=[0, 50])
        st.plotly_chart(fig_trends, use_container_width=True, key="usage_trends_chart")
        
        st.markdown(
            "**The Registration vs. Usage Gap:** While registered mobile wallets exceed 65 million (representing over 90% of adults), "
            "actual active Mobile Money Account possession stands at only **9.45%** and general Digital Payment Usage is **35%**. "
            "Most mobile money wallets are used passively for bank cash-outs, rather than primary circulation accounts."
        )

    # Infrastructure comparison
    st.markdown("---")
    st.markdown("### Supply-Side Enablers (2023-2025)")
    infra_col1, infra_col2 = st.columns(2)
    
    with infra_col1:
        # Show Fayda Enrollment and 4G coverage values
        df_infra = df_obs[df_obs['indicator_code'].isin(['ACC_4G_COV', 'ACC_MOBILE_PEN']) & (df_obs['gender'] == 'all')].sort_values('year')
        fig_infra = px.bar(
            df_infra, x='year', y='value_numeric', color='indicator', bgroupmode='group',
            labels={'value_numeric': 'Percentage (%)', 'year': 'Year'},
            color_discrete_sequence=['#2ca02c', '#8c564b']
        )
        fig_infra.update_layout(height=350, yaxis_range=[0, 100])
        st.plotly_chart(fig_infra, use_container_width=True, key="infra_chart")
        
    with infra_col2:
        df_fayda = df_obs[df_obs['indicator_code'] == 'ACC_FAYDA'].sort_values('observation_date')
        df_fayda['observation_date'] = pd.to_datetime(df_fayda['observation_date'])
        
        fig_fayda = px.line(
            df_fayda, x='observation_date', y='value_numeric', markers=True,
            title='Fayda Digital ID Registrations (2024-2025)',
            labels={'value_numeric': 'Enrollment Count', 'observation_date': 'Date'}
        )
        fig_fayda.update_traces(line_color='#d62728', line_width=3)
        fig_fayda.update_layout(height=320)
        st.plotly_chart(fig_fayda, use_container_width=True, key="fayda_chart")

# ================= TAB 3: EVENT IMPACT MATRIX =================
with tab_impacts:
    st.markdown("## Event Impact Modeling Framework")
    
    # Description
    st.markdown(
        "Events (policies, product launches, infrastructure investments) leave their `pillar` blank, and instead connect to "
        "target indicators through `impact_link` entities. This maps how a single event triggers multi-dimensional shifts "
        "across Access, Usage, and Affordability."
    )
    
    # Pivot matrix calculations
    events_info = df_events[['record_id', 'indicator', 'observation_date']].rename(
        columns={'indicator': 'event_name', 'observation_date': 'event_date'}
    )
    df_merged_links = df_impact.merge(events_info, left_on='parent_id', right_on='record_id', how='left')
    
    # Map estimates
    df_merged_links['inferred_estimate'] = df_merged_links['impact_estimate']
    for idx, row in df_merged_links.iterrows():
        if pd.isna(row['inferred_estimate']):
            direction = 1 if row['impact_direction'] == 'increase' else -1
            mag = row['impact_magnitude']
            val = 15.0 if mag == 'high' else (5.0 if mag == 'medium' else 1.0)
            df_merged_links.at[idx, 'inferred_estimate'] = direction * val
            
    pivot_matrix = df_merged_links.pivot_table(
        index='event_name', columns='related_indicator', values='inferred_estimate', aggfunc='first'
    ).fillna(0)
    
    # Heatmap Plotly
    fig_heat = px.imshow(
        pivot_matrix, text_auto=".1f",
        labels=dict(x="Impacted Indicator", y="Triggering Event", color="Estimate (pp)"),
        color_continuous_scale="PiYG", color_continuous_midpoint=0
    )
    fig_heat.update_layout(height=500, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_heat, use_container_width=True, key="heatmap_plotly_chart")
    
    # Comparable Country Evidence Expandable list
    st.markdown("### Comparable Country Evidence Case Studies")
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        with st.expander("🇰🇪 Kenya M-Pesa (2007)"):
            st.markdown(
                "**Evidence Basis for:** `EVT_0001` (Telebirr Launch)\n\n"
                "**Context:** Following the 2007 Safaricom M-Pesa rollout, Kenya saw account ownership expand "
                "from ~27% to over 75% in a decade. A major +15pp access shock (`IMP_0001`) with a 12-month lag "
                "is aligned with M-Pesa's historical expansion rates."
            )
            
    with col_c2:
        with st.expander("🇮🇳 India Aadhaar ID (2010-2016)"):
            st.markdown(
                "**Evidence Basis for:** `EVT_0004` (Fayda Digital ID Rollout)\n\n"
                "**Context:** Under the Aadhaar biometric system, account ownership in India rose by +15-20pp. "
                "Importantly, it closed the gender ownership gap by -5pp (`IMP_0009`) since women disproportionately "
                "lacked traditional papers (such as birth certificates or utility bills) required for e-KYC compliance."
            )
            
    with col_c3:
        with st.expander("🇹🇿 Tanzania Interoperability (2014)"):
            st.markdown(
                "**Evidence Basis for:** `EVT_0007` (M-Pesa EthSwitch Integration)\n\n"
                "**Context:** Interoperability across Tigo, Airtel, and Vodacom in Tanzania in 2014 resulted in a "
                "+10-15% increase in transaction count (`IMP_0012`) and a +15% active user bump within 3 months, "
                "by facilitating cross-platform commerce."
            )

# ================= TAB 4: FORECASTING & SCENARIOS =================
with tab_forecast:
    st.markdown("## Interactive Forecasting Simulator (2025-2027)")
    
    # Split sidebar-like control area inside tab
    set_col1, set_col2 = st.columns([1, 3])
    
    with set_col1:
        st.markdown("### Model Configurations")
        
        # Target Selector
        target_ind = st.selectbox(
            "Select Target Indicator:",
            options=["ACC_OWNERSHIP", "USG_DIGITAL_PAYMENT"],
            format_func=lambda x: "Account Ownership Rate (Access)" if x == "ACC_OWNERSHIP" else "Digital Payment Adoption Rate (Usage)",
            key="target_indicator_select"
        )
        
        # Scenario Toggles
        show_base = st.checkbox("Show Base Scenario (Scheduled events)", value=True, key="show_base_toggle")
        show_opt = st.checkbox("Show Optimistic Scenario (Catalysts)", value=True, key="show_opt_toggle")
        show_pess = st.checkbox("Show Pessimistic Scenario (Headwinds)", value=True, key="show_pess_toggle")
        show_ols = st.checkbox("Show OLS Trend Baseline (+95% CI)", value=True, key="show_ols_toggle")
        
        st.markdown("### Interactive Event Shocks")
        st.markdown("Toggle future events below to see the simulated projections adjust in real time:")
        
        # Dynamic Shocks Toggles
        toggle_switch = st.checkbox("Interoperability (Oct 2025)", value=True, key="toggle_interop")
        toggle_ethiopay = st.checkbox("EthioPay IPS Launch (Dec 2025)", value=True, key="toggle_ethiopay")
        
        # Custom Future Events Toggles
        toggle_loans = st.checkbox("Mobile Lending Licenses (July 2026)", value=True, key="toggle_loans")
        toggle_fayda_mandate = st.checkbox("Fayda Wallet Mandate (Oct 2026)", value=True, key="toggle_fayda")
        
        toggle_inflation = st.checkbox("FX Price Headwinds (Jan 2026)", value=False, key="toggle_inflation")

    with set_col2:
        # Load forecaster instance
        forecaster_inst = FinancialInclusionForecaster()
        
        # Dynamically modify df_impact based on checkbox configurations
        df_impact_dyn = df_impact.copy()
        
        # 1. Check Interoperability toggles (Oct 2025)
        if not toggle_switch:
            # Set integration impact links to 0
            df_impact_dyn.loc[df_impact_dyn['parent_id'] == 'EVT_0007', 'impact_estimate'] = 0.0
            
        # 2. Check EthioPay toggle
        if not toggle_ethiopay:
            df_impact_dyn.loc[df_impact_dyn['parent_id'] == 'EVT_0008', 'impact_estimate'] = 0.0
            
        # 3. Handle base scenario sim
        df_sim_dyn = pd.DataFrame(index=pd.date_range(start='2011-01-01', end='2027-12-31', freq='ME'))
        df_sim_dyn['ACC_OWNERSHIP_organic'] = 14.0
        df_sim_dyn['USG_DIGITAL_PAYMENT_organic'] = 0.1
        
        # Apply organic linear trend updates
        organic_annual_growth = {'ACC_OWNERSHIP': 2.0, 'USG_DIGITAL_PAYMENT': 0.5}
        for i in range(1, len(df_sim_dyn.index)):
            curr_d = df_sim_dyn.index[i]
            prev_d = df_sim_dyn.index[i-1]
            delta_y = (curr_d - prev_d).days / 365.25
            for t in ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT']:
                df_sim_dyn.loc[curr_d, f'{t}_organic'] = (
                    df_sim_dyn.loc[prev_d, f'{t}_organic'] + 
                    organic_annual_growth[t] * delta_y
                )
                
        # Simulate base
        df_sim_dyn = forecaster_inst._simulate_shocks(df_sim_dyn, ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT'], df_impact_dyn, 'base')
        
        # Simulate optimistic with toggled loans/fayda
        opt_list = []
        if toggle_loans:
            opt_list.append({
                'related_indicator': 'USG_DIGITAL_PAYMENT', 'impact_magnitude': 'medium', 'inferred_estimate': 7.5,
                'event_date': '2026-07-01', 'lag_months': 3, 'impact_direction': 'increase'
            })
            opt_list.append({
                'related_indicator': 'ACC_OWNERSHIP', 'impact_magnitude': 'medium', 'inferred_estimate': 5.0,
                'event_date': '2026-07-01', 'lag_months': 3, 'impact_direction': 'increase'
            })
        if toggle_fayda_mandate:
            opt_list.append({
                'related_indicator': 'ACC_OWNERSHIP', 'impact_magnitude': 'medium', 'inferred_estimate': 8.0,
                'event_date': '2026-10-01', 'lag_months': 3, 'impact_direction': 'increase'
            })
            
        if opt_list:
            df_impact_opt_dyn = pd.concat([df_impact_dyn, pd.DataFrame(opt_list)], ignore_index=True)
        else:
            df_impact_opt_dyn = df_impact_dyn
            
        df_sim_dyn = forecaster_inst._simulate_shocks(df_sim_dyn, ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT'], df_impact_opt_dyn, 'optimistic')
        
        # Simulate pessimistic with toggled inflation
        pess_list = []
        if toggle_inflation:
            pess_list.append({
                'related_indicator': 'USG_DIGITAL_PAYMENT', 'impact_magnitude': 'medium', 'inferred_estimate': -5.0,
                'event_date': '2026-01-01', 'lag_months': 2, 'impact_direction': 'decrease'
            })
            pess_list.append({
                'related_indicator': 'ACC_OWNERSHIP', 'impact_magnitude': 'medium', 'inferred_estimate': -3.0,
                'event_date': '2026-06-01', 'lag_months': 6, 'impact_direction': 'decrease'
            })
            
        if pess_list:
            df_impact_pess_dyn = pd.concat([df_impact_dyn, pd.DataFrame(pess_list)], ignore_index=True)
        else:
            df_impact_pess_dyn = df_impact_dyn
            
        df_sim_dyn = forecaster_inst._simulate_shocks(df_sim_dyn, ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT'], df_impact_pess_dyn, 'pessimistic')
        
        # 4. Fit OLS and generate OLS line
        years_range = pd.date_range('2011-01-01', '2027-12-31', freq='YE')
        trend_years = [y.year for y in years_range if (target_ind == 'ACC_OWNERSHIP' or y.year >= 2014)]
        df_trend_val = forecaster_inst.generate_trend_forecast(target_ind, target_years=trend_years)
        
        # Get historical Findex observations for plot
        df_hist = df_obs[(df_obs['indicator_code'] == target_ind) & (df_obs['gender'] == 'all')].sort_values('observation_date')
        df_hist['observation_date'] = pd.to_datetime(df_hist['observation_date'])
        
        # Build Plotly Chart
        fig_fore = go.Figure()
        
        # Historical points
        fig_fore.add_trace(go.Scatter(
            x=df_hist['observation_date'], y=df_hist['value_numeric'],
            mode='markers+text', name='Historical Findex',
            marker=dict(color='#000000', size=12),
            text=[f"{v}%" for v in df_hist['value_numeric']],
            textposition='top center',
            textfont=dict(weight='bold', color='#000000')
        ))
        
        # OLS Baseline
        if show_ols:
            trend_dates = pd.to_datetime([f"{y}-12-31" for y in trend_years])
            fig_fore.add_trace(go.Scatter(
                x=trend_dates, y=df_trend_val['trend_forecast'],
                mode='lines', name='OLS Baseline Trend',
                line=dict(color='#7f7f7f', width=2, dash='dot')
            ))
            fig_fore.add_trace(go.Scatter(
                x=list(trend_dates) + list(trend_dates)[::-1],
                y=list(df_trend_val['ci_upper']) + list(df_trend_val['ci_lower'])[::-1],
                fill='toself', fillcolor='rgba(127,127,127,0.1)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo='skip', showlegend=True, name='95% OLS CI'
            ))
            
        # Base Scenario
        if show_base:
            fig_fore.add_trace(go.Scatter(
                x=df_sim_dyn.index, y=df_sim_dyn[f'{target_ind}_base'],
                mode='lines', name='Base Scenario',
                line=dict(color='#1f77b4', width=3)
            ))
            
        # Optimistic Scenario
        if show_opt:
            fig_fore.add_trace(go.Scatter(
                x=df_sim_dyn.index, y=df_sim_dyn[f'{target_ind}_optimistic'],
                mode='lines', name='Optimistic Scenario',
                line=dict(color='#2ca02c', width=2.5, dash='dash')
            ))
            
        # Pessimistic Scenario
        if show_pess:
            fig_fore.add_trace(go.Scatter(
                x=df_sim_dyn.index, y=df_sim_dyn[f'{target_ind}_pessimistic'],
                mode='lines', name='Pessimistic Scenario',
                line=dict(color='#d62728', width=2.5, dash='dashdot')
            ))
            
        name_str = "Account Ownership Rate (Access)" if target_ind == "ACC_OWNERSHIP" else "Digital Payment Adoption Rate (Usage)"
        fig_fore.update_layout(
            title_text=f"Projections for {name_str} (2011-2027)",
            xaxis_title='Year',
            yaxis_title='Rate (%)',
            height=500,
            yaxis_range=[0, 95] if target_ind == 'ACC_OWNERSHIP' else [0, 65],
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_fore, use_container_width=True, key="dynamic_forecast_chart")
        
        # Display scenario output values at year-end 2027
        idx_2027 = df_sim_dyn.index.get_indexer([pd.to_datetime('2027-12-31')], method='nearest')[0]
        
        st.markdown("#### Projected Target Values (Year-End 2027):")
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        
        f_col1.metric("OLS Baseline", f"{df_trend_val['trend_forecast'].iloc[-1]:.1f}%")
        f_col2.metric("Base Simulation", f"{df_sim_dyn[f'{target_ind}_base'].iloc[idx_2027]:.1f}%")
        f_col3.metric("Optimistic", f"{df_sim_dyn[f'{target_ind}_optimistic'].iloc[idx_2027]:.1f}%")
        f_col4.metric("Pessimistic", f"{df_sim_dyn[f'{target_ind}_pessimistic'].iloc[idx_2027]:.1f}%")
        
        # Recommendations box
        st.markdown("---")
        st.markdown(
            """
            <div class='glass-card'>
                <h4>🏦 Policy & Strategic Recommendations</h4>
                <ol>
                    <li><b>Promote Active Wallet Circulation:</b> Shift focus from raw registration numbers to transaction depth. Incentivize digital micro-savings (Sanduq) and micro-credit licenses to turn dormant wallets into active digital bank accounts.</li>
                    <li><b>Fayda ID Mandate Integration:</b> Support the National ID Program (NIDP) to accelerate Fayda ID registrations. Linking digital IDs to SIM card activations simplifies remote e-KYC compliance and can boost Access rates by <b>+8pp</b>.</li>
                    <li><b>Mitigate the Gender Gap:</b> Target female phone ownership and digital literacy. Since women hold only 14% of mobile money wallets, expanding female-led agent networks can disproportionately pull unbanked women into the financial system.</li>
                </ol>
            </div>
            """, unsafe_allow_html=True
        )
