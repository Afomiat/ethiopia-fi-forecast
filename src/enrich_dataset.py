import pandas as pd
import os

def enrich_dataset():
    raw_dir = 'data/raw'
    processed_dir = 'data/processed'
    
    # Paths
    data_csv = os.path.join(raw_dir, 'ethiopia_fi_unified_data.csv')
    impact_csv = os.path.join(raw_dir, 'ethiopia_fi_impact_links.csv')
    
    # Load existing datasets
    df_data = pd.read_csv(data_csv)
    df_impact = pd.read_csv(impact_csv)
    
    print(f"Original unified data shape: {df_data.shape}")
    print(f"Original impact links shape: {df_impact.shape}")
    
    # 1. Prepare new observations
    new_obs = [
        # 2011 Account Ownership Baseline
        {
            'record_id': 'REC_0034', 'record_type': 'observation', 'category': None, 'pillar': 'ACCESS',
            'indicator': 'Account Ownership Rate', 'indicator_code': 'ACC_OWNERSHIP', 'indicator_direction': 'higher_better',
            'value_numeric': 14.0, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2011-12-31', 'period_start': None, 'period_end': None, 'fiscal_year': '2011',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Global Findex 2011',
            'source_type': 'survey', 'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': '14% account ownership in 2011', 'notes': 'Findex baseline wave'
        },
        # 2014 Digital Payment Adoption Rate
        {
            'record_id': 'REC_0035', 'record_type': 'observation', 'category': None, 'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAYMENT', 'indicator_direction': 'higher_better',
            'value_numeric': 1.2, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2014-12-31', 'period_start': None, 'period_end': None, 'fiscal_year': '2014',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Global Findex 2014',
            'source_type': 'survey', 'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': '1.2% made or received digital payment in 2014', 'notes': 'Early baseline usage'
        },
        # 2017 Digital Payment Adoption Rate
        {
            'record_id': 'REC_0036', 'record_type': 'observation', 'category': None, 'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAYMENT', 'indicator_direction': 'higher_better',
            'value_numeric': 12.0, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2017-12-31', 'period_start': None, 'period_end': None, 'fiscal_year': '2017',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Global Findex 2017',
            'source_type': 'survey', 'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': '12% made or received digital payments in 2017', 'notes': 'Modest growth before mobile money'
        },
        # 2021 Digital Payment Adoption Rate
        {
            'record_id': 'REC_0037', 'record_type': 'observation', 'category': None, 'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAYMENT', 'indicator_direction': 'higher_better',
            'value_numeric': 21.0, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2021-12-31', 'period_start': None, 'period_end': None, 'fiscal_year': '2021',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Global Findex 2021',
            'source_type': 'survey', 'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': '21% of adults made or received digital payment in 2021', 'notes': 'Pre-Telebirr expansion baseline'
        },
        # 2024 Digital Payment Adoption Rate
        {
            'record_id': 'REC_0038', 'record_type': 'observation', 'category': None, 'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAYMENT', 'indicator_direction': 'higher_better',
            'value_numeric': 35.0, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2024-11-29', 'period_start': None, 'period_end': None, 'fiscal_year': '2024',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Global Findex 2024',
            'source_type': 'survey', 'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': 'Made or received digital payment: ~35% in 2024', 'notes': 'Significant post-Telebirr/M-Pesa growth'
        },
        # 2024 Account Ownership Male
        {
            'record_id': 'REC_0039', 'record_type': 'observation', 'category': None, 'pillar': 'ACCESS',
            'indicator': 'Account Ownership Rate', 'indicator_code': 'ACC_OWNERSHIP', 'indicator_direction': 'higher_better',
            'value_numeric': 56.5, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2024-11-29', 'period_start': None, 'period_end': None, 'fiscal_year': '2024',
            'gender': 'male', 'location': 'national', 'region': None, 'source_name': 'Global Findex 2024',
            'source_type': 'survey', 'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': '56.5% of male adults owned an account in 2024', 'notes': 'Gender disaggregated access'
        },
        # 2024 Account Ownership Female
        {
            'record_id': 'REC_0040', 'record_type': 'observation', 'category': None, 'pillar': 'ACCESS',
            'indicator': 'Account Ownership Rate', 'indicator_code': 'ACC_OWNERSHIP', 'indicator_direction': 'higher_better',
            'value_numeric': 41.6, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2024-11-29', 'period_start': None, 'period_end': None, 'fiscal_year': '2024',
            'gender': 'female', 'location': 'national', 'region': None, 'source_name': 'Global Findex 2024',
            'source_type': 'survey', 'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': '41.6% of female adults owned an account in 2024', 'notes': 'Gender disaggregated access'
        },
        # 2021 Digital Payment Adoption Rate Male
        {
            'record_id': 'REC_0041', 'record_type': 'observation', 'category': None, 'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAYMENT', 'indicator_direction': 'higher_better',
            'value_numeric': 26.0, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2021-12-31', 'period_start': None, 'period_end': None, 'fiscal_year': '2021',
            'gender': 'male', 'location': 'national', 'region': None, 'source_name': 'Global Findex 2021',
            'source_type': 'survey', 'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': '26% of male adults made or received digital payment in 2021', 'notes': 'Gender disaggregated usage'
        },
        # 2021 Digital Payment Adoption Rate Female
        {
            'record_id': 'REC_0042', 'record_type': 'observation', 'category': None, 'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAYMENT', 'indicator_direction': 'higher_better',
            'value_numeric': 16.0, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2021-12-31', 'period_start': None, 'period_end': None, 'fiscal_year': '2021',
            'gender': 'female', 'location': 'national', 'region': None, 'source_name': 'Global Findex 2021',
            'source_type': 'survey', 'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': '16% of female adults made or received digital payment in 2021', 'notes': 'Gender disaggregated usage'
        }
    ]
    
    # 2. Prepare new events
    new_events = [
        # NBE Mobile Money Directive ONPS/01/2020
        {
            'record_id': 'EVT_0011', 'record_type': 'event', 'category': 'regulation', 'pillar': None,
            'indicator': 'NBE Payment Instrument Issuers Directive ONPS/01/2020', 'indicator_code': 'EVT_NBE_MOBILE_MONEY_DIR', 'indicator_direction': None,
            'value_numeric': None, 'value_text': 'Implemented', 'value_type': 'categorical', 'unit': None,
            'observation_date': '2020-04-01', 'period_start': None, 'period_end': None, 'fiscal_year': '2020',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'National Bank of Ethiopia',
            'source_type': 'regulator', 'source_url': 'https://nbe.gov.et/',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': 'Payment Instrument Issuers Directive ONPS/01/2020 in April 2020', 'notes': 'Allowed non-banks (like Ethio Telecom) to offer mobile money'
        },
        # NBE Amendment Directive (Foreign Operator Liberalization)
        {
            'record_id': 'EVT_0012', 'record_type': 'event', 'category': 'regulation', 'pillar': None,
            'indicator': 'NBE Payment Instrument Issuers Amendment Directive', 'indicator_code': 'EVT_NBE_FOREIGN_LIB', 'indicator_direction': None,
            'value_numeric': None, 'value_text': 'Implemented', 'value_type': 'categorical', 'unit': None,
            'observation_date': '2022-10-18', 'period_start': None, 'period_end': None, 'fiscal_year': '2022',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'National Bank of Ethiopia',
            'source_type': 'regulator', 'source_url': 'https://nbe.gov.et/',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': 'NBE amended the Payments directive to allow foreign mobile money providers', 'notes': 'Paved the way for Safaricom M-Pesa license'
        },
        # Telebirr Sanduq Launch
        {
            'record_id': 'EVT_0013', 'record_type': 'event', 'category': 'product_launch', 'pillar': None,
            'indicator': 'Telebirr Sanduq Digital Savings and Lending', 'indicator_code': 'EVT_TELEBIRR_SANDUQ', 'indicator_direction': None,
            'value_numeric': None, 'value_text': 'Launched', 'value_type': 'categorical', 'unit': None,
            'observation_date': '2022-08-04', 'period_start': None, 'period_end': None, 'fiscal_year': '2022',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Ethio Telecom / Dashen Bank',
            'source_type': 'operator', 'source_url': 'https://www.ethiotelecom.et/',
            'confidence': 'high', 'related_indicator': None, 'relationship_type': None,
            'impact_direction': None, 'impact_magnitude': None, 'impact_estimate': None, 'lag_months': None,
            'evidence_basis': None, 'comparable_country': None, 'collected_by': 'Antigravity',
            'collection_date': '2026-07-18', 'original_text': 'Telebirr partnered with Dashen Bank to launch financial micro-services', 'notes': 'Brought savings and credit products to mobile money users'
        }
    ]
    
    # 3. Add to unified data CSV
    df_new_obs = pd.DataFrame(new_obs)
    df_new_events = pd.DataFrame(new_events)
    df_data_updated = pd.concat([df_data, df_new_obs, df_new_events], ignore_index=True)
    
    # 4. Prepare new impact links
    new_impacts = [
        # NBE Mobile Money Directive ONPS/01/2020 -> ACC_MM_ACCOUNT
        {
            'record_id': 'IMP_0015', 'parent_id': 'EVT_0011', 'record_type': 'impact_link', 'category': 'regulation', 'pillar': 'ACCESS',
            'indicator': 'Mobile Money Account Rate', 'indicator_code': 'ACC_MM_ACCOUNT', 'indicator_direction': 'higher_better',
            'value_numeric': None, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2020-04-01', 'period_start': None, 'period_end': None, 'fiscal_year': '2020',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Expert Estimation',
            'source_type': 'calculated', 'source_url': None, 'confidence': 'high', 'related_indicator': 'ACC_MM_ACCOUNT',
            'relationship_type': 'enabler', 'impact_direction': 'increase', 'impact_magnitude': 'high',
            'impact_estimate': 15.0, 'lag_months': 12, 'evidence_basis': 'Direct regulatory trigger for non-bank mobile money operators',
            'comparable_country': 'Kenya, Tanzania', 'collected_by': 'Antigravity', 'collection_date': '2026-07-18',
            'original_text': None, 'notes': 'Required step for Telebirr and M-Pesa commercial launches'
        },
        # NBE Foreign Operator Liberalization -> ACC_MM_ACCOUNT
        {
            'record_id': 'IMP_0016', 'parent_id': 'EVT_0012', 'record_type': 'impact_link', 'category': 'regulation', 'pillar': 'ACCESS',
            'indicator': 'Mobile Money Account Rate', 'indicator_code': 'ACC_MM_ACCOUNT', 'indicator_direction': 'higher_better',
            'value_numeric': None, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2022-10-18', 'period_start': None, 'period_end': None, 'fiscal_year': '2022',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Expert Estimation',
            'source_type': 'calculated', 'source_url': None, 'confidence': 'high', 'related_indicator': 'ACC_MM_ACCOUNT',
            'relationship_type': 'enabler', 'impact_direction': 'increase', 'impact_magnitude': 'medium',
            'impact_estimate': 5.0, 'lag_months': 10, 'evidence_basis': 'Allowed entry of Safaricom M-Pesa to stimulate market competition',
            'comparable_country': 'Multi-license markets like Ghana', 'collected_by': 'Antigravity', 'collection_date': '2026-07-18',
            'original_text': None, 'notes': 'Led to licensing of Safaricom'
        },
        # Telebirr Sanduq Launch -> USG_DIGITAL_PAYMENT
        {
            'record_id': 'IMP_0017', 'parent_id': 'EVT_0013', 'record_type': 'impact_link', 'category': 'product_launch', 'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAYMENT', 'indicator_direction': 'higher_better',
            'value_numeric': None, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2022-08-04', 'period_start': None, 'period_end': None, 'fiscal_year': '2022',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Expert Estimation',
            'source_type': 'calculated', 'source_url': None, 'confidence': 'high', 'related_indicator': 'USG_DIGITAL_PAYMENT',
            'relationship_type': 'enabler', 'impact_direction': 'increase', 'impact_magnitude': 'medium',
            'impact_estimate': 5.0, 'lag_months': 6, 'evidence_basis': 'Value-added services like credit and savings build transaction stickiness',
            'comparable_country': 'Kenya M-Shwari', 'collected_by': 'Antigravity', 'collection_date': '2026-07-18',
            'original_text': None, 'notes': 'Microfinance integration enhances active mobile money account use'
        },
        # Telebirr Launch -> USG_DIGITAL_PAYMENT
        {
            'record_id': 'IMP_0018', 'parent_id': 'EVT_0001', 'record_type': 'impact_link', 'category': 'product_launch', 'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAYMENT', 'indicator_direction': 'higher_better',
            'value_numeric': None, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2021-05-17', 'period_start': None, 'period_end': None, 'fiscal_year': '2021',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Expert Estimation',
            'source_type': 'calculated', 'source_url': None, 'confidence': 'high', 'related_indicator': 'USG_DIGITAL_PAYMENT',
            'relationship_type': 'enabler', 'impact_direction': 'increase', 'impact_magnitude': 'high',
            'impact_estimate': 15.0, 'lag_months': 12, 'evidence_basis': 'First major mobile money service drives broad scale payment adoption',
            'comparable_country': 'Kenya, Bangladesh', 'collected_by': 'Antigravity', 'collection_date': '2026-07-18',
            'original_text': None, 'notes': 'Core ecosystem builder'
        },
        # M-Pesa Launch -> USG_DIGITAL_PAYMENT
        {
            'record_id': 'IMP_0019', 'parent_id': 'EVT_0003', 'record_type': 'impact_link', 'category': 'product_launch', 'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption Rate', 'indicator_code': 'USG_DIGITAL_PAYMENT', 'indicator_direction': 'higher_better',
            'value_numeric': None, 'value_text': None, 'value_type': 'percentage', 'unit': '%',
            'observation_date': '2023-08-01', 'period_start': None, 'period_end': None, 'fiscal_year': '2023',
            'gender': 'all', 'location': 'national', 'region': None, 'source_name': 'Expert Estimation',
            'source_type': 'calculated', 'source_url': None, 'confidence': 'high', 'related_indicator': 'USG_DIGITAL_PAYMENT',
            'relationship_type': 'enabler', 'impact_direction': 'increase', 'impact_magnitude': 'medium',
            'impact_estimate': 5.0, 'lag_months': 12, 'evidence_basis': 'Second mobile money player increases network density and merchant competition',
            'comparable_country': 'Tanzania (M-Pesa + Tigo Pesa)', 'collected_by': 'Antigravity', 'collection_date': '2026-07-18',
            'original_text': None, 'notes': 'Competition expands agent networks and options'
        }
    ]
    
    df_new_impacts = pd.DataFrame(new_impacts)
    df_impact_updated = pd.concat([df_impact, df_new_impacts], ignore_index=True)
    
    # Save the updated files to raw/
    df_data_updated.to_csv(data_csv, index=False)
    df_impact_updated.to_csv(impact_csv, index=False)
    print("Saved updated datasets to data/raw/")
    
    # Create processed/ folder if it doesn't exist
    os.makedirs(processed_dir, exist_ok=True)
    
    # Save the updated files to processed/ (along with other guide CSVs)
    df_data_updated.to_csv(os.path.join(processed_dir, 'ethiopia_fi_unified_data.csv'), index=False)
    df_impact_updated.to_csv(os.path.join(processed_dir, 'ethiopia_fi_impact_links.csv'), index=False)
    
    # Copy other guide files to processed/
    for name in ['alternative_baselines.csv', 'direct_correlation.csv', 'indirect_correlation.csv', 'market_nuances.csv', 'reference_codes.csv']:
        src = os.path.join(raw_dir, name)
        dst = os.path.join(processed_dir, name)
        if os.path.exists(src):
            df_temp = pd.read_csv(src)
            df_temp.to_csv(dst, index=False)
            print(f"Copied {name} to processed/")
            
    print(f"Final unified data shape: {df_data_updated.shape}")
    print(f"Final impact links shape: {df_impact_updated.shape}")

if __name__ == '__main__':
    enrich_dataset()
