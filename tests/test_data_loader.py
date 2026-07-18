import pandas as pd
import os

def test_load_unified_data():
    path = 'data/processed/ethiopia_fi_unified_data.csv'
    assert os.path.exists(path), f"File {path} does not exist"
    df = pd.read_csv(path)
    assert len(df) > 0, "Dataset is empty"
    assert 'record_type' in df.columns, "Column 'record_type' is missing"
    assert 'record_id' in df.columns, "Column 'record_id' is missing"
    print(f"Successfully loaded {path} with {len(df)} records")

def test_load_impact_links():
    path = 'data/processed/ethiopia_fi_impact_links.csv'
    assert os.path.exists(path), f"File {path} does not exist"
    df = pd.read_csv(path)
    assert len(df) > 0, "Dataset is empty"
    assert 'parent_id' in df.columns, "Column 'parent_id' is missing"
    assert 'related_indicator' in df.columns, "Column 'related_indicator' is missing"
    print(f"Successfully loaded {path} with {len(df)} records")

def test_load_reference_codes():
    path = 'data/processed/reference_codes.csv'
    assert os.path.exists(path), f"File {path} does not exist"
    df = pd.read_csv(path)
    assert len(df) > 0, "Dataset is empty"
    assert 'code' in df.columns, "Column 'code' is missing"
    print(f"Successfully loaded {path} with {len(df)} records")
