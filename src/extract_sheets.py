import pandas as pd
import os

def extract_excel_sheets():
    raw_dir = 'data/raw'
    
    # 1. Extract ethiopia_fi_unified_data.xlsx
    fi_file = os.path.join(raw_dir, 'ethiopia_fi_unified_data.xlsx')
    if os.path.exists(fi_file):
        print(f"Extracting sheets from {fi_file}...")
        df_data = pd.read_excel(fi_file, sheet_name='ethiopia_fi_unified_data')
        df_impact = pd.read_excel(fi_file, sheet_name='Impact_sheet')
        
        # Save to CSV
        df_data.to_csv(os.path.join(raw_dir, 'ethiopia_fi_unified_data.csv'), index=False)
        df_impact.to_csv(os.path.join(raw_dir, 'ethiopia_fi_impact_links.csv'), index=False)
        print("Saved ethiopia_fi_unified_data.csv and ethiopia_fi_impact_links.csv")

    # 2. Extract Additional Data Points Guide.xlsx
    guide_file = os.path.join(raw_dir, 'Additional Data Points Guide.xlsx')
    if os.path.exists(guide_file):
        print(f"Extracting sheets from {guide_file}...")
        sheets = {
            'A. Alternative Baselines': 'alternative_baselines.csv',
            'B. Direct Corrln': 'direct_correlation.csv',
            'C. Indirect Corrln': 'indirect_correlation.csv',
            'D. Market Naunces': 'market_nuances.csv'
        }
        for sheet_name, csv_name in sheets.items():
            df = pd.read_excel(guide_file, sheet_name=sheet_name)
            df.to_csv(os.path.join(raw_dir, csv_name), index=False)
            print(f"Saved {csv_name} from sheet '{sheet_name}'")

    # 3. Extract reference_codes.xlsx
    ref_file = os.path.join(raw_dir, 'reference_codes.xlsx')
    if os.path.exists(ref_file):
        print(f"Extracting sheets from {ref_file}...")
        df_ref = pd.read_excel(ref_file, sheet_name='reference_codes')
        df_ref.to_csv(os.path.join(raw_dir, 'reference_codes.csv'), index=False)
        print("Saved reference_codes.csv")

if __name__ == '__main__':
    extract_excel_sheets()
